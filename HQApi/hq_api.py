import base64
import json

import requests

from HQApi.exceptions import ApiResponseError, BannedIPError


class BaseHQApi:
    def __init__(self, authtoken, region="1", headers="1"):
        self.authtoken = authtoken
        self.region = region
        if headers == 1:
            self.version = requests.get("https://www.apkmirror.com/apk/intermedia-labs/hq-trivia/").text.split(
                '-release/">HQ Trivia ')[1].split('</a>')[0]  # Fetch lastest version
            self.headers = {
                "x-hq-stk": base64.b64encode(str(self.region).encode()).decode(),
                "x-hq-client": "Android/" + self.version,
                "Authorization": "Bearer " + self.authtoken}
        elif headers == 2:
            self.version = \
                requests.get("https://itunes.apple.com/us/app/hq-live-trivia-game-show/id1232278996/").text.split(
                    '<p class="l-column small-6 medium-12 whats-new__latest__version">Version ')[1].split('</p>')[
                    0]  # Fetch lastest version
            self.headers = {
                "x-hq-stk": base64.b64encode(str(self.region).encode()).decode(),
                'x-hq-device': 'iPhone9,4',
                'x-hq-client': 'iOS/{} b110'.format(self.version),
                'User-Agent': 'HQ-iOS/120 CFNetwork/974.2.1 Darwin/18.0.0'}

    def api(self):
        return self

    def fetch(self, method="GET", func="", data=None):
        if data is None:
            data = {}
        return method, func, data, self.headers

    def get_users_me(self):
        return self.fetch("GET", "users/me")

    def get_user(self, id):
        return self.fetch("GET", "users/{}".format(str(id)))

    def search(self, name):
        return self.fetch("GET", 'users?q={}'.format(name))

    def get_payouts_me(self):
        return self.fetch("GET", "users/me/payouts")

    def get_show(self):
        return self.fetch("GET", "shows/now")

    def easter_egg(self):
        return self.fetch("POST", "easter-eggs/makeItRain")

    def make_payout(self, email):
        return self.fetch("POST", "users/me/payouts", {"email": email})

    def send_code(self, phone, method):
        return self.fetch("POST", "verifications", {"phone": phone, "method": method})

    def confirm_code(self, verificationid, code):
        return self.fetch("POST", "verifications/{}".format(verificationid), {"code": code})

    def register(self, verificationid, name, refferal):
        return self.fetch("POST", "users", {
            "country": base64.b64encode(str(self.region).encode()).decode(), "language": "eu",
            "referringUsername": refferal,
            "username": name,
            "verificationId": verificationid})

    def aws_credentials(self):
        return self.fetch("GET", "credentials/s3")

    def delete_avatar(self):
        return self.fetch("DELETE", "users/me/avatarUrl")

    def add_friend(self, id):
        return self.fetch("POST", "friends/{}/requests".format(str(id)))

    def friend_status(self, id):
        return self.fetch("GET", "friends/{}/status".format(str(id)))

    def remove_friend(self, id):
        return self.fetch("DELETE", "friends/{}".format(str(id)))

    def accept_friend(self, id):
        return self.fetch("PUT", "friends/{}/status".format(str(id)), {"status": "ACCEPTED"})

    def check_username(self, name):
        return self.fetch("POST", "usernames/available", {"username": name})

    def custom(self, method, func, data):
        return self.fetch(method, func, data)


class HQApi(BaseHQApi):
    def __init__(self, authtoken, region="1", headers=None):
        super().__init__(authtoken, region=region)
        if headers is None:
            headers = {}
        self.authToken = authtoken
        self.region = region
        self.session = requests.Session()
        self.session.headers.update(headers)

    def fetch(self, method="GET", func="", data=None):
        if data is None:
            data = {}
        try:
            if method == "GET":
                content = self.session.get("https://api-quiz.hype.space/{}".format(func), data=data).json()
            elif method == "POST":
                content = self.session.post("https://api-quiz.hype.space/{}".format(func), data=data).json()
            elif method == "PATCH":
                content = self.session.patch("https://api-quiz.hype.space/{}".format(func), data=data).json()
            elif method == "DELETE":
                content = self.session.delete("https://api-quiz.hype.space/{}".format(func), data=data).json()
            else:
                content = self.session.get("https://api-quiz.hype.space/{}".format(func), data=data).json()
            error = content.get("error")
            if error:
                raise ApiResponseError(json.dumps(content))
            return content
        except json.decoder.JSONDecodeError:
            raise BannedIPError("Your IP is banned")


class AsyncHQApi(BaseHQApi):
    def __init__(self, authtoken, connector, region="1"):
        super().__init__(authtoken, region=region)
        self.authtoken = authtoken
        self.region = region
        self.connector = connector

    async def fetch(self, method="GET", func="", data=None):
        if data is None:
            data = {}
        if method == "GET":
            async with self.connector.session.get("https://api-quiz.hype.space/{}".format(func),
                                                  data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
        elif method == "POST":
            async with self.connector.session.post("https://api-quiz.hype.space/{}".format(func),
                                                   data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
        elif method == "PATCH":
            async with self.connector.session.patch("https://api-quiz.hype.space/{}".format(func),
                                                    data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
        elif method == "DELETE":
            async with self.connector.session.delete("https://api-quiz.hype.space/{}".format(func),
                                                     data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
        else:
            async with self.connector.session.get("https://api-quiz.hype.space/{}".format(func),
                                                  data=data) as response:
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(json.dumps(content))
                return content
