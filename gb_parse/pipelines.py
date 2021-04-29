# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class GbParsePipeline:
    def __init__(self, friend_path):
        self.friend_path = friend_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            friend_path=crawler.settings.get('friend_path'),
        )

    def process_item(self, item, spider):
        if item['type'] == 'user_profile':
            return spider.get_friends(self.friend_path.set_user_profile(item), tag=item['tag'])

