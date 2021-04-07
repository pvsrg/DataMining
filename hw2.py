import requests
import time
from urllib.parse import urljoin
import bs4
import datetime
import pymongo


MONTHS = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'мая': 5, 'июн': 6,
          'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12}


class MagnitParse:

    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client["gb_data_mining"]
        self.collection = db["magnit"]

    def _get_response(self, url, *args, **kwargs):
        while True:
            response = requests.get(url, *args, **kwargs)
            if response.status_code in (200, 301, 304):
                return response
            time.sleep(1)

    def _get_soup(self, url, *args, **kwargs):
        return bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, "lxml")

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    @property
    def _template(self):
        return {
            "product_name": lambda tag: tag.find("div", attrs={"class": "card-sale__title"}).text,
            "url": lambda tag: urljoin(self.start_url, tag.attrs.get("href", "")),
            "promo_name": lambda tag: tag.find("div", attrs={"class": "card-sale__name"}).text,
            "image_url": lambda tag: urljoin(self.start_url, tag.find("img").attrs.get("data-src", "")),
            "old_price": lambda tag: float(
                ".".join(
                    [itm for itm in tag.find('div', attrs={'class': 'label__price_old'}).text.split()]
                )),
            "new_price": lambda tag: float(
                ".".join(
                    [itm for itm in tag.find('div', attrs={'class': 'label__price_new'}).text.split()]
                )),
            "date_from": lambda tag: self._date_convert(
                tag.find('div', attrs={'class': 'card-sale__date'}).text)[0],
            "date_to": lambda tag: self._date_convert(
                tag.find('div', attrs={'class': 'card-sale__date'}).text)[1],
        }

    def _date_convert(self, date_str):
        date_list = date_str.replace("с ", "", 1).replace("\n", "").split("до")
        result = []
        for date in date_list:
            temp_date = date.split()
            result.append(
                datetime.datetime(
                    year=datetime.datetime.now().year,
                    day=int(temp_date[0]),
                    month=MONTHS[temp_date[1][:3]],
                )
            )
        if result[0] > result[1]:
            result[1].replace(year=result[1].year + 1)
        return result

    def _parse(self, url):
        soup = self._get_soup(url)
        catalog_main = soup.find("div", attrs={"class": "сatalogue__main"})
        product_tags = catalog_main.find_all('a', recursive=False)
        for product_tag in product_tags:
            product = {}
            for key, funk in self._template.items():
                try:
                    product[key] = funk(product_tag)
                except (AttributeError, ValueError):
                    if key in ("image_url", "old_price", "date_from", "date_to"):
                        continue
                    else:
                        break
            else:
                yield product

    def _save(self, data):
        self.collection.insert_one(data)


if __name__ == '__main__':
    url = "https://magnit.ru/promo/?geo=moskva"
    db_client = pymongo.MongoClient("mongodb+srv://myUser:myPassword@cluster0.armiz.mongodb.net/myDatabase?retryWrites=true&w=majority")
    parser = MagnitParse(url, db_client)
    parser.run()

