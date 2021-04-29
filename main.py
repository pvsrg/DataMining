import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gb_parse.spiders.instagram import InstagramSpider
from fpath import FriendPath

if __name__ == "__main__":

    from_path = FriendPath("from_path")
    to_path = FriendPath("to_path")
    to_path.set_towards_path(from_path)
    from_path.set_towards_path(to_path)

    dotenv.load_dotenv(".env")
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crawler_settings["friend_path"] = from_path
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    users = {"nike": "from", "nbg.nike": "to"}
    crawler_proc.crawl(
        InstagramSpider,
        login=os.getenv("INSTGRM_USERNAME"),
        password=os.getenv("INSTGRM_PASSWORD"),
        from_user="nike",
        to_user="nbg.nike",
        from_path=from_path,
        to_path=to_path,
        nmb_friend=24,
    )
    crawler_proc.start()
