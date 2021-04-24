from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, MapCompose, TakeFirst
from urllib.parse import urljoin


def join_text(items):
    return ' '.join(items)

def clear_text(items):
    items = items.strip()
    return items if len(items) else None


def make_dict(items):
    return {items[i]: items[i+1] for i in range(0, len(items), 2)}


def avito_seller_url(seller):
    return urljoin("https://avito.ru/", seller)

def replace_n(items):
    return items.replace('\n', '')


class AvitoLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_out = TakeFirst()
    address_in = MapCompose(replace_n)
    address_out = TakeFirst()
    description_in = MapCompose(clear_text)
    description_out = make_dict
    seller_in = MapCompose(avito_seller_url)
    seller_out = TakeFirst()
    name_in = MapCompose(replace_n)
    name_out = TakeFirst()
    phone_out = TakeFirst()
