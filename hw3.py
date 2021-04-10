import requests
import bs4
from urllib.parse import urljoin
import datetime
from datetime import datetime
from database.database import Database


class GbBlogParse:
    default_headers = {"User_agent": "Phillip Kirkorov"}

    def __init__(self, start_url, database: Database):
        self.db = database
        self.start_url = start_url
        self.done_urls = set()
        self.tasks = []
        self._append_task(self.start_url, self.parse_feed)

    def get_task(self, url, callback):
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        return task

    def _append_task(self, url, callback):
        if url not in self.done_urls:
            self.tasks.append(self.get_task(url, callback))
            self.done_urls.add(url)

    def _get_response(self, url, **kwargs):
        headers = self.default_headers.copy()
        headers.update(kwargs)
        response = requests.get(url, headers=headers)
        return response

    def _get_soup(self, url):
        soup = bs4.BeautifulSoup(self._get_response(url).text, "lxml")
        return soup

    def parse_post(self, url, soup):
        print(soup.find("h1", attrs={"class": "blogpost-title"}).text)
        author_tag = soup.find("div", attrs={"itemprop": "author"})
        data = {
            "post_data": {
                "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
                "url": url,
                "id": soup.find("comments").attrs.get("commentable-id"),
                "post_img": soup.find("div", attrs={"class": "content_text"}).img.attrs.get("src")
                            if soup.find("div", attrs={"class": "content_text"}).img
                            else None,
                "post_date": datetime.strptime(
                    (soup.find("div", attrs={"class":"blogpost-date-views"}).time.attrs.get("datetime"))[:19],
                    "%Y-%m-%dT%H:%M:%S"),
            },
            "author_data": {
                "url": urljoin(url, author_tag.parent.attrs.get("href")),
                "name": author_tag.text,
            },
            "tags_data": [
                {"name": tag.text, "url": urljoin(url, tag.attrs.get("href"))}
                for tag in soup.find_all("a", attrs={"class": "small"})
            ],
            "comments_data": self._get_comments(soup.find("comments").attrs.get("commentable-id")),
        }
        return data

    def _get_comments(self, post_id):
        api_path = f"/api/v2/comments?commentable_type=Post&commentable_id={post_id}&order=desc"
        data = []
        while True:
            response_headers = {"range": f"{len(data)}-{len(data) + 10}"}
            response = self._get_response(urljoin(self.start_url, api_path), **response_headers)
            data.extend(response.json())
            if len(data) >= int(response.headers.get('Content-Count')):
                break
        return data

    def parse_feed(self, url, soup):
        ul = soup.find("ul", attrs={"class": "gb__pagination"})
        pag_urls = set(
            urljoin(url, href.attrs.get("href"))
            for href in ul.find_all("a")
            if href.attrs.get("href")
        )
        for pag_url in pag_urls:
            self._append_task(pag_url, self.parse_feed)

        post_items = soup.find("div", attrs={"class": "post-items-wrapper"})
        posts_urls = set(
            urljoin(url, href.attrs.get("href"))
            for href in post_items.find_all("a", attrs={"class": "post-item__title"})
            if href.attrs.get("href")
        )

        for post_url in posts_urls:
            self._append_task(post_url, self.parse_post)

    def run(self):
        for task in self.tasks:
            task_result = task()
            if task_result:
                self.save(task_result)

    def save(self, data):
        self.db.create_post(data)


if __name__ == "__main__":
    database = Database("sqlite:///gb_blog.db")
    parser = GbBlogParse("https://gb.ru/posts", database)
    parser.run()
