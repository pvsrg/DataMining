# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import pymongo
import os



class GbImageDownloadPipeline(ImagesPipeline):
    img_fields = ['profile_pic_url', 'display_url']

    def get_media_requests(self, item, info):
        fields = ItemAdapter(item).asdict()
        for field in self.img_fields:
            if fields['data'].get(field):
                yield Request(fields['data'].get(field))

    def item_completed(self, results, item, info):
        item["photos"] = [itm[1] for itm in results]
        return item


class GbParsePipeline:
    def __init__(self, mongo_db):
        self.mongo_uri = os.getenv('MONGODB_URI')
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = item['collection']
        item.pop('collection')
        self.db[collection].insert_one(ItemAdapter(item).asdict())
        return item


