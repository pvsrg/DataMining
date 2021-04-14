import scrapy
import urllib
import re
import base64


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    _css_selectors = {
        "brands": "div.ColumnItemList_container__5gTrc a.blackLink",
        "pagination": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "car": "#serp article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu",
    }

    def _get_follow(self, response, selector_css, callback, **kwargs):
        for link_selector in response.css(selector_css):
            yield response.follow(link_selector.attrib.get("href"), callback=callback)

    def parse(self, response, **kwargs):
        yield from self._get_follow(response, self._css_selectors["brands"], self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_follow(response, self._css_selectors["pagination"], self.brand_parse)
        yield from self._get_follow(response, self._css_selectors["car"], self.car_parse)


    @staticmethod
    def car_parse_script(resp, data):
        data_script = {
            "photos": [r'"type","photo","big","(https:[^"]+jpg)",',
                       lambda res: res],
            "author": [r'"youlaId","([^"]+)","avatar"',
                       lambda res: resp.urljoin(f"/user/{res[0]}").replace("auto.", "", 1)],
            "company": [r'"url","([^"]+)/#info","youlaId"',
                       lambda res: res[0]],
            "phone": [r'"phone","([^"]+)",',
                      lambda res: base64.b64decode(base64.b64decode(res[0].encode("ASCII"))).decode("UTF-8")]
        }

        marker = "window.transitState = decodeURIComponent"
        for script in resp.css("script"):
            try:
                if marker in script.css("::text").extract_first():
                    text_block = urllib.parse.unquote(script.css("::text").extract_first())
                    for key, val in data_script.items():
                        try:
                            pattern, func = val[0], val[1]
                            re_pattern = re.compile(pattern)
                            result = re.findall(re_pattern, text_block)
                            data[key] = func(result)
                        except IndexError:
                            continue
                        except (ValueError, AttributeError):
                            continue
                    return
            except TypeError:
                continue

    data_query = {
        "title": lambda resp: resp.css(".AdvertCard_advertTitle__1S1Ak::text").get(),
        "url": lambda resp: resp.url,
        "price": lambda resp: float(
            resp.css("div.AdvertCard_price__3dDCr::text").get().replace("\u2009", "")
        ),
        "characteristics": lambda resp: [
            {
                "name":  itm.css(".AdvertSpecs_label__2JHnS::text").extract_first(),
                "value": itm.css(".AdvertSpecs_data__xK2Qx::text").extract_first()
                or itm.css(".AdvertSpecs_data__xK2Qx a::text").extract_first(),
            }
            for itm in resp.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")
        ],
        "description": lambda resp: resp.css(
            ".AdvertCard_descriptionInner__KnuRi::text").extract_first(),
    }

    def car_parse(self, response):
        data = {}
        for key, selector in self.data_query.items():
            try:
                data[key] = selector(response)
            except (ValueError, AttributeError):
                continue

        AutoyoulaSpider.car_parse_script(response, data)
        yield data