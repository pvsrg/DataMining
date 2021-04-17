from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def flat_text(items):
    return '\n'.join(items)


def join_text(items):
    return ' '.join(items)


def split_text(items):
    return items.split(',')


def lower_text(items):
    return items.lower()


def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)


class HHLoader(ItemLoader):
    default_item_class = dict
    collection_out = TakeFirst()
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = join_text
    description_out = flat_text
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()


class HCLoader(ItemLoader):
    default_item_class = dict
    collection_out = TakeFirst()
    url_out = TakeFirst()
    title_out = join_text
    site_out = TakeFirst()
    activities_in = MapCompose(lower_text)
    activities_out = MapCompose(split_text)
    description_out = TakeFirst()
