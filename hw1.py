from pathlib import Path
import time
import json
import requests


class Parse5ka:
    headers = {
        "User-Agent": "Phillip Kirkorov"
    }

    def __init__(self, start_url: str, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        while True:
            response = requests.get(url, *args, **kwargs, headers=self.headers)
            if response.status_code in (200, 301, 304):
                return response
            time.sleep(1)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data.get('next')
            for product in data.get('results', []):
                yield product

    def _save(self, data, file_path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


class CategoriesParcer(Parse5ka):
    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self):
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category['products'] = []
            params = f"?categories={category['parent_group_code']}"
            url = f"{self.start_url}{params}"

            category['products'].extend(list(self._parse(url)))
            file_name = f"{category['parent_group_code']}.json"
            cat_path = self.save_path.joinpath(file_name)
            self._save(category, cat_path)


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == '__main__':
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    save_path_categories = get_save_path("categories")
    #save_path_products = get_save_path("products")
    #parser = Parse5ka(url, save_path_products )
    #parser.run()
    cat_parser = CategoriesParcer(cat_url, url, save_path_categories)
    cat_parser.run()
