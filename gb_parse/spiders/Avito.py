import scrapy
from urllib.parse import urljoin

from gb_parse.loaders import AvitoLoader
from gb_parse.spiders.xpaths import AVITO_PAGE_XPATH, AVITO_APARTMENT_XPATH, \
                                    AVITO_SELLER_ID, AVITO_START_XPATH
from gb_parse.spiders.phone import define_phone


class AvitoSpider(scrapy.Spider):
    name = "kvartiry"
    allowed_domains = ["avito.ru"]
    start_urls = [
        "https://www.avito.ru/krasnodar/kvartiry/"
    ]

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            try:
                yield response.follow(url, callback=callback)
            except (ValueError, AttributeError):
                continue

    def parse(self, response):
        yield from self._get_follow_xpath(response, AVITO_START_XPATH, self.parse_page)

    def parse_page(self, response):
        callbacks = {
            "pagination": self.parse_page,
            "apartment": self.apartment_parse,
        }
        for key, xpath in AVITO_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def apartment_parse(self, response):
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in AVITO_APARTMENT_XPATH.items():
            try:
                loader.add_xpath(key, xpath)
            except (ValueError, AttributeError):
                continue
        return response.follow(urljoin('http://www.avito.ru/web/1/items/phone/',
                               response.xpath(AVITO_SELLER_ID).re(r'&iid=([^"]+)')[0]),
                               callback=self.seller_parse,
                               cb_kwargs=dict(loader=loader))

    def seller_parse(self, response, loader):
        try:
            loader.add_value("phone", define_phone(response.json().get('image64')[22:]))
        except (ValueError, AttributeError):
            print('Not define Phone')
        return loader.load_item()
