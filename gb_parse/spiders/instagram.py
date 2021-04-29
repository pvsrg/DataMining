import json
from urllib.parse import urlencode
import scrapy
from scrapy import Request


class InstagramSpider(scrapy.Spider):
    name = 'instagram_spider'
    allowed_domains = ["www.instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    _login_url = "https://www.instagram.com/accounts/login/ajax/"
    api_url = "/graphql/query/"

    def __init__(self, login, password, from_user, to_user, from_path, to_path, nmb_friend, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.from_user = from_user
        self.from_path = from_path
        self.to_user = to_user
        self.to_path = to_path
        self.nmb_friend = nmb_friend

    def parse(self, response):
        js_data = self.js_data_extract(response)
        yield scrapy.FormRequest(
                    self._login_url,
                    method="POST",
                    callback=self.parse_login,
                    formdata={"username": self.login, "enc_password": self.password,},
                    headers={"X-CSRFToken": js_data["config"]["csrf_token"]},
                    )

    def parse_login(self, response):
        if response.json()["authenticated"]:
            yield self.request_user(self.from_user, self.from_path)
            yield self.request_user(self.to_user, self.to_path)

    def request_user(self, user, path):
        return Request(url=f"{self.start_urls[0]}{user}/",
                       callback=self.parse_users,
                       cb_kwargs=dict(path=path)
                       )

    def parse_users(self, response, path):
        js_data = self.js_data_extract(response)
        user_id = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]
        user_name = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["username"]
        path.start({user_id: [user_name, None]})
        yield from self.run_parse_users(response, path)

    def run_parse_users(self, response, path):
        for user_id in path.get_user():
            url = f"{self.api_url}?{urlencode(self.friends_params(user_id, after=''))}"
            yield response.follow(url=url,
                                  callback=self.parse_friends,
                                  cb_kwargs=dict(user_id=user_id, friends={}, path=path)
                                  )

    def parse_friends(self, response, user_id, friends, path):
        js_data = response.json()
        for friend in js_data['data']['user']['edge_follow']['edges']:
            friends.update({friend['node']['id']: friend['node']['username']})
        if js_data['data']['user']['edge_follow']['page_info']['has_next_page']:
            after = js_data['data']['user']['edge_follow']['page_info']['end_cursor']
            url = f"{self.api_url}?{urlencode(self.friends_params(user_id, after=after))}"
            yield response.follow(
                                url=url,
                                callback=self.parse_friends,
                                cb_kwargs=dict(user_id=user_id, friends=friends, path=path)
            )
        else:
            path.put_friends(user_id=user_id, friends=friends)
            yield from self.run_parse_users(response, path)

    def js_data_extract(self, response):
        script = response.xpath(
            "//script[contains(text(), 'window._sharedData = ')]/text()"
        ).extract_first()
        return json.loads(script.replace("window._sharedData = ", "")[:-1])

    def friends_params(self, users_id, after):
        query_hash = "3dec7e2c57367ef3da3d987d89f9dbc8"
        variables = {
            "id": users_id,
            "include_reel": True,
            "fetch_mutual": False,
            "first": self.nmb_friend,
        }
        if len(after):
            variables["after"] = after

        query_params = {"query_hash": query_hash, "variables": json.dumps(variables)}
        return query_params

