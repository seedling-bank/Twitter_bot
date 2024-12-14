import http.client
import json
import ssl
import traceback

import loguru
import requests

import con.config


class ApiDanceService:

    def __init__(self):
        self.api_key = con.config.settings.APIDANCE_API_KEY
        self.twitter_auth_token = con.config.settings.TWITTER_AUTH_TOKEN

    def get_search_data(self, search):
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

    def get_twitter_details(self, tweet_id):
        for attempt in range(1, con.config.settings.MAX_RETRIES + 1):
            url = f"https://api.apidance.pro/sapi/TweetDetail?tweet_id={tweet_id}&cursor"

            payload = {}
            headers = {
                'apikey': self.api_key
            }

            response = requests.request("GET", url, headers=headers, data=payload)
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


api_dance_service = ApiDanceService()
