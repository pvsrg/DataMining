# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class GbParseSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


#str_cookie = 'u=2oo0iulx.1d1kigv.1uyjll80fxt00; v=1619198397; __cfduid=de877f8fca944106f6ff8ae75c40cfb431619198398; buyer_location_id=633540; luri=krasnodar; sx=H4sIAAAAAAACAwXBQQqAIBAF0LvMusUoU329TWQIuRCacELx7r03KK0tuf34OrPCsrJBuSoqxUGNIr0eIST05y7VkEu2UxmmYiKiTAtdFN3mgoeAZc4fF1WvUVQAAAA=; so=1619198404; dfp_group=43; SEARCH_HISTORY_IDS=1; no-ssr=1'
#str_cookie = 'u=2oo0iulx.1d1kigv.1uyjll80fxt00; v=1619198397; __cfduid=de877f8fca944106f6ff8ae75c40cfb431619198398; buyer_location_id=633540; luri=krasnodar; sx=H4sIAAAAAAACAwXBQQqAIBAF0LvMusUoU329TWQIuRCacELx7r03KK0tuf34OrPCsrJBuSoqxUGNIr0eIST05y7VkEu2UxmmYiKiTAtdFN3mgoeAZc4fF1WvUVQAAAA=; so=1619198404; dfp_group=43; SEARCH_HISTORY_IDS=1; no-ssr=1; _ym_uid=1619198407301912797; _ym_d=1619198407; _gcl_au=1.1.829851381.1619198411; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRTVkQUs5enJOeWhpRjNUOU9iNk5tM25jQnJCVUFHd1VNQ3NobzlOWGsyUFhEOHFQa3BqZzJmdkVzUFdQZ1dKMlljRHNjcFFtSnM0K2laQlpZV2lnOFJyUnYwbTZzb1ltNVdwbE8rZ2k1M1F0WkxZYmEyYjB0UTZJRnhnSzBRc09DaEU5WFJjUFRXWTR2bVlsUk1kL3c1eWxaQmFjUjVRdGdQVkM3djF2WWF3dmM3aitmMi9rYjFWQVd1a05iS1lERWh4aEMxcThaaFRqTmdTT0tBa25rZTd2bWtLSGRqUUZFQTRZODFUL1BLMHNBU2tNeHlESlBjTWRoY29ndWs2QVkiLCJpYXQiOjE2MTkxOTg0MDYsImV4cCI6MTYyMDQwODAwNn0.lJR4Tvfms3l_f-ATr-63lF3BgzaNfcU-AQE9TrHOhPs; _ym_visorc=b; _ym_isad=2; _ga=GA1.2.1095849036.1619198412; _gid=GA1.2.449756516.1619198412; _dc_gtm_UA-2546784-1=1; _fbp=fb.1.1619198412058.1762888091; ST-TEST=TEST; f=5.075fb8b9995e92ff36b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9e2bfa4611aac769efa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa51b1fde863bf5c12f8ee35c29834d631c9ba923b7b327da7be2fce6256b648cdde01905e00c6523f2985db2d99140e2d0ee226f11256b780315536c94b3e90e338f0f5e6e0d2832e148af97ce8307cffa606506660fbbb5346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f2113b5d1bc97c513e12da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088; ft="z08A/65VdkNAZFR7wI1/WdxsOHNZpif94bi/q5j2HKN8DRxVWnZYI0dxFhlgRGijTFmS+j2McUp7kuN7cuW6LCOgLALrgmfUW3vnGaGSOxLj0fHe4TiGE1X3TcWMpvs8O3f2fM+1ZgEVFwh35D/3cb0EXEzRiBUIcxCRBK3TKB27BcLbkTaYwgEJhOnzBmDq"'
str_cookie = 'u=2oo0ix2n.1d1kigv.zx9uplguvu0; v=1619200311; buyer_location_id=633540; luri=krasnodar; sx=H4sIAAAAAAACAw3KwQqAIAwA0H/ZucMWpsu/CRMJgxELF4n/Xu/8OuxL2ylsz4uobEXRWFGUBWKHBhFun6/TLB1Z2RVJlcX0LyzCriaYIEMkT+vMPhCN8QGSHCdKVAAAAA==; so=1619200312; dfp_group=29; __cfduid=dc6a8fdfa17e1a1e8c3b90e00dc4e94061619200313; SEARCH_HISTORY_IDS=1; no-ssr=1; _ym_uid=161920031886322508; _ym_d=1619200318; _gcl_au=1.1.38617457.1619200318; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRTVkQUs5enJOeWhpRjNUOU9iNk5tM2hEcTBGMXJ1dy9XUG9VVityZDNnanVDUmpUclhMRUNSQjBISHoxQmdWSk8xUU1SUHlBYTU5NTZjaVovMXNTTWFQVGxkYnI5cHBqRUVmOUdoQW9pY010T1lCQ2VTNFZNOXZieEpTSjZIbVRlZzRTYzhwcVk2NytaQmVJNHczTTl1c2lndUlReXlPbTh4eGdDeXhidUVKc3RzTnIyTVRhK3NyUWd5TDNNQWtCQUJCR2dTK2M2ZGVaS2FVMFVCQWYwTWtheHFuaGwyREF3WXhiZGx4T01HUldNcWNhMWNNdXZQcHNsNXRCTkZmczQiLCJpYXQiOjE2MTkyMDAzMTcsImV4cCI6MTYyMDQwOTkxN30.BeYkmNrsVa368AGj8O3WI721EpIgdWRTfSwvMW3sjzI; _ym_visorc=b; _ym_isad=2; _ga=GA1.2.705960988.1619200319; _gid=GA1.2.706530569.1619200319; _dc_gtm_UA-2546784-1=1; _fbp=fb.1.1619200319624.1369433928; ST-TEST=TEST; f=5.075fb8b9995e92ff36b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9e2bfa4611aac769efa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa51b1fde863bf5c12f8ee35c29834d631c9ba923b7b327da7be2fce6256b648cdde01905e00c6523f2985db2d99140e2d0ee226f11256b780315536c94b3e90e338f0f5e6e0d2832e148af97ce8307cffa606506660fbbb5346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21954a20ae70152a612da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088; ft="z08A/65VdkNAZFR7wI1/WdxsOHNZpif94bi/q5j2HKN8DRxVWnZYI0dxFhlgRGijTFmS+j2McUp7kuN7cuW6LCOgLALrgmfUW3vnGaGSOxLj0fHe4TiGE1X3TcWMpvs8O3f2fM+1ZgEVFwh35D/3cZ8sE+9N4Z2dKh2zSFH5adaQZR3MEy0d1THSsm4f/Qhp"'
#str_cookie = 'u=2oo0ix2n.1d1kigv.zx9uplguvu0; v=1619200311; buyer_location_id=633540; luri=krasnodar; dfp_group=29; __cfduid=dc6a8fdfa17e1a1e8c3b90e00dc4e94061619200313; SEARCH_HISTORY_IDS=1; no-ssr=1; _ym_uid=161920031886322508; _ym_d=1619200318; _gcl_au=1.1.38617457.1619200318; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRTVkQUs5enJOeWhpRjNUOU9iNk5tM2hEcTBGMXJ1dy9XUG9VVityZDNnanVDUmpUclhMRUNSQjBISHoxQmdWSk8xUU1SUHlBYTU5NTZjaVovMXNTTWFQVGxkYnI5cHBqRUVmOUdoQW9pY010T1lCQ2VTNFZNOXZieEpTSjZIbVRlZzRTYzhwcVk2NytaQmVJNHczTTl1c2lndUlReXlPbTh4eGdDeXhidUVKc3RzTnIyTVRhK3NyUWd5TDNNQWtCQUJCR2dTK2M2ZGVaS2FVMFVCQWYwTWtheHFuaGwyREF3WXhiZGx4T01HUldNcWNhMWNNdXZQcHNsNXRCTkZmczQiLCJpYXQiOjE2MTkyMDAzMTcsImV4cCI6MTYyMDQwOTkxN30.BeYkmNrsVa368AGj8O3WI721EpIgdWRTfSwvMW3sjzI; _ym_visorc=b; _ym_isad=2; _ga=GA1.2.705960988.1619200319; _gid=GA1.2.706530569.1619200319; _fbp=fb.1.1619200319624.1369433928; f=5.075fb8b9995e92ff36b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9e2bfa4611aac769efa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa51b1fde863bf5c12f8ee35c29834d631c9ba923b7b327da7be2fce6256b648cdde01905e00c6523f2985db2d99140e2d0ee226f11256b780315536c94b3e90e338f0f5e6e0d2832e148af97ce8307cffa606506660fbbb5346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21954a20ae70152a612da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088; ft="z08A/65VdkNAZFR7wI1/WdxsOHNZpif94bi/q5j2HKN8DRxVWnZYI0dxFhlgRGijTFmS+j2McUp7kuN7cuW6LCOgLALrgmfUW3vnGaGSOxLj0fHe4TiGE1X3TcWMpvs8O3f2fM+1ZgEVFwh35D/3cZ8sE+9N4Z2dKh2zSFH5adaQZR3MEy0d1THSsm4f/Qhp"; sx=H4sIAAAAAAACAw3LMQrAIAwAwL9k7mDE2uhvREWoQ4YUIxX/3t5+C8o5Cl5pvsYIaROjJIaFGOKCARFutempo/PMrNKaE1anPQv9ozMcUCGix2DJE4a9Pw02W8JUAAAA; so=1619200420; _dc_gtm_UA-2546784-1=1'
#str_cookie = 'u=2oo0ix2n.1d1kigv.zx9uplguvu0; v=1619200311; buyer_location_id=633540; luri=krasnodar; __cfduid=dc6a8fdfa17e1a1e8c3b90e00dc4e94061619200313; SEARCH_HISTORY_IDS=1; no-ssr=1; _ym_uid=161920031886322508; _ym_d=1619200318; _gcl_au=1.1.38617457.1619200318; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRTVkQUs5enJOeWhpRjNUOU9iNk5tM2hEcTBGMXJ1dy9XUG9VVityZDNnanVDUmpUclhMRUNSQjBISHoxQmdWSk8xUU1SUHlBYTU5NTZjaVovMXNTTWFQVGxkYnI5cHBqRUVmOUdoQW9pY010T1lCQ2VTNFZNOXZieEpTSjZIbVRlZzRTYzhwcVk2NytaQmVJNHczTTl1c2lndUlReXlPbTh4eGdDeXhidUVKc3RzTnIyTVRhK3NyUWd5TDNNQWtCQUJCR2dTK2M2ZGVaS2FVMFVCQWYwTWtheHFuaGwyREF3WXhiZGx4T01HUldNcWNhMWNNdXZQcHNsNXRCTkZmczQiLCJpYXQiOjE2MTkyMDAzMTcsImV4cCI6MTYyMDQwOTkxN30.BeYkmNrsVa368AGj8O3WI721EpIgdWRTfSwvMW3sjzI; _ym_visorc=b; _ym_isad=2; _ga=GA1.2.705960988.1619200319; _gid=GA1.2.706530569.1619200319; _fbp=fb.1.1619200319624.1369433928; f=5.075fb8b9995e92ff36b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9e2bfa4611aac769efa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa51b1fde863bf5c12f8ee35c29834d631c9ba923b7b327da7be2fce6256b648cdde01905e00c6523f2985db2d99140e2d0ee226f11256b780315536c94b3e90e338f0f5e6e0d2832e148af97ce8307cffa606506660fbbb5346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21954a20ae70152a612da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088; ft="z08A/65VdkNAZFR7wI1/WdxsOHNZpif94bi/q5j2HKN8DRxVWnZYI0dxFhlgRGijTFmS+j2McUp7kuN7cuW6LCOgLALrgmfUW3vnGaGSOxLj0fHe4TiGE1X3TcWMpvs8O3f2fM+1ZgEVFwh35D/3cZ8sE+9N4Z2dKh2zSFH5adaQZR3MEy0d1THSsm4f/Qhp"; sx=H4sIAAAAAAACAw3GOw6AIAwA0Lt0diiGT+U2CoYBTRMbqUq8u77pdciuZRPm60EU0iKoJMhCDLFDgwjH5qQuvN+nJEsqNtU/FVULMSUYYIVovJlGCj7Q+36FTieEVAAAAA==; so=1619201278; dfp_group=29; _dc_gtm_UA-2546784-1=1'

class GbParseDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        cookies = {key_val.split('=')[0]: key_val.split('=')[1] for key_val in str_cookie.split('; ')}
        request.cookies = cookies
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
