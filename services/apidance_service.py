import asyncio
import http.client
import json
import ssl
import traceback
import urllib.parse
from typing import Optional

import loguru
import requests

import con.config
from services.twitter_service import twitter_service


class ApiDanceService:

    def __init__(self):
        self.api_key = con.config.settings.APIDANCE_API_KEY
        self.twitter_auth_token = con.config.settings.TWITTER_AUTH_TOKEN

    def get_search_data(self, search):
        """
        获取第一页搜索结果
        :param search:
        :return:
        """
        for attempt in range(1, con.config.settings.MAX_RETRIES + 1):
            base_url = f'api.apidance.pro'

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            conn = http.client.HTTPSConnection(base_url, context=context)
            payload = ''
            headers = {
                'apikey': self.api_key
            }
            conn.request('GET', f"/sapi/Search?q={search}", payload, headers)
            response = conn.getresponse()
            data = response.read()
            return data.decode('utf-8')

    def get_next_search_data(self, search, next_cursor_str):
        """
        获取下一页的搜索结果
        :param search:
        :param next_cursor_str:
        :return:
        """
        for attempt in range(1, con.config.settings.MAX_RETRIES + 1):
            base_url = f'api.apidance.pro'

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            conn = http.client.HTTPSConnection(base_url, context=context)
            payload = ''
            headers = {
                'apikey': self.api_key
            }
            conn.request('GET', f"/sapi/Search?q={search}&cursor={next_cursor_str}", payload, headers)
            response = conn.getresponse()
            data = response.read()
            return data.decode('utf-8')

    def get_twitter_details(self, tweet_id):
        for attempt in range(1, con.config.settings.MAX_RETRIES + 1):
            url = f"https://api.apidance.pro/sapi/TweetDetail?tweet_id={tweet_id}&cursor"

            payload = {}
            headers = {
                'apikey': self.api_key
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            return response.text

    def get_user_twitter_data(self, user_id):
        if user_id:
            base_url = "https://api.apidance.pro/graphql/UserTweets?variables="
            payload = {}
            headers = {
                'apikey': self.api_key
            }

            variables = {
                "userId": user_id,
                "count": 20,
                "includePromotedContent": False,
                "withQuickPromoteEligibilityTweetFields": True,
                "withVoice": True,
                "withV2Timeline": True,
            }
            url = base_url + json.dumps(variables)
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                return response.text

    def get_user_tweets_and_replies(self, user_id):
        """
        获取用户twitter和回复
        :param user_id:
        :return:
        """
        if user_id:
            base_url = "https://api.apidance.pro/graphql/UserTweetsAndReplies?variables="
            headers = {
                'apikey': self.api_key
            }
            params = {
                "userId": user_id,  # 用户 ID
                "count": 20,  # 返回的推文数量
                "includePromotedContent": False,  # 布尔值，是否包含推广内容
                "withCommunity": True,  # 布尔值，是否包含社区相关内容
                "withVoice": True,  # 布尔值，是否包含语音推文
                "withV2Timeline": True  # 布尔值，是否使用 v2 时间线
            }
            url = base_url + json.dumps(params)
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                return response.text

    def send_on_twitter(self, twitter_content):
        url = "https://api.apidance.pro/graphql/CreateTweet"

        payload = json.dumps({
            "variables": {
                "tweet_text": f"{twitter_content}",
                "dark_request": False,
                "media": {
                    "media_entities": [],
                    "possibly_sensitive": False
                },
                "semantic_annotation_ids": [],
                "includePromotedContent": False
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key,
            'AuthToken': self.twitter_auth_token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def send_reply_to_twitter(self, twitter_content, twitter_id):
        url = "https://api.apidance.pro/graphql/CreateTweet"
        payload = json.dumps({
            "variables": {
                "tweet_text": f"{twitter_content}",
                "reply": {
                    "in_reply_to_tweet_id": f"{twitter_id}",
                    "exclude_reply_user_ids": []
                },
                "dark_request": False,
                "media": {
                    "media_entities": [],
                    "possibly_sensitive": False
                },
                "semantic_annotation_ids": [],
                "includePromotedContent": False
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key,
            'AuthToken': self.twitter_auth_token
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    async def get_user_twitter_article(self, user_id: str):
        try:
            loguru.logger.error(user_id)
            while True:
                result = await self.get_user_twitter_data_by_apidance(user_id=user_id)
                if result != "local_rate_limited":
                    if 'Rate limit exceeded.' not in result:
                        break
            data = twitter_service.user_twitter_processing(json.loads(result))
            return data
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())
            return False

    async def get_user_twitter_data_by_apidance(self, user_id: str):
        if user_id:
            base_url = "https://api.apidance.pro/graphql/UserTweets?variables="
            payload = {}
            headers = {
                'apikey': self.api_key
            }

            variables = {
                "userId": user_id,
                "count": 20,
                "includePromotedContent": False,
                "withQuickPromoteEligibilityTweetFields": True,
                "withVoice": True,
                "withV2Timeline": True,
            }
            url = base_url + json.dumps(variables)
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                return response.text

    def get_user_following(self, user_info):
        base_url = "https://api.apidance.pro/graphql/Following?variables="
        params = {
            "userId": user_info["user_id"],
            "count": 20,
            "includePromotedContent": False
        }
        headers = {
            'apikey': self.api_key
        }
        url = base_url + json.dumps(params)

        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return response.text


api_dance_service = ApiDanceService()


async def main():
    result = api_dance_service.get_search_data("MBTAI_")
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
