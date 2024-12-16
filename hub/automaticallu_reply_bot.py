import asyncio
import json
import re
import traceback

import loguru

import con.config
from base import BaseJob
from services.apidance_service import api_dance_service
from services.gpt_analyze_services import gpt_analyze_service
from services.twitter_service import twitter_service
from utils.content_generation import twitter_content_generation
from utils.language_detection import language_detection
from utils.search_term import get_search_term


class AutomaticallyReply(BaseJob):

    def __init__(self):
        self.reply_to_twitter = []
        self.replied_id_list = []

    def init(self):
        loguru.logger.info("Initializing AutomaticallyTweet")

    def get_scheduler(self):
        return {
            "trigger": "cron",
            "second": "0",  # 指定秒数为0
            "minute": "*/1",
            "hour": "*",  # 任意小时
            "day": "*",  # 任意日期
            "month": "*",  # 任意月份
            "day_of_week": "*",  # 任意星期
            "timezone": "UTC",
            "misfire_grace_time": 600,
        }

    async def twitter_bot(self):

        try:
            while True:
                user_twitter_data = api_dance_service.get_user_twitter_data(user_id=con.config.settings.TWITTER_ID)
                if user_twitter_data != "local_rate_limited":
                    break
                elif 'errors' not in user_twitter_data:
                    break

            twitter_list = twitter_service.user_data_processing(user_twitter_data)

            if twitter_list:
                for twitter_id in twitter_list:
                    if twitter_id in self.replied_id_list:
                        continue
                    while True:
                        try:
                            result = api_dance_service.get_twitter_details(twitter_id)
                            print(result)
                            if result != "local_rate_limited":  # 检查条件
                                if 'Rate limit exceeded.' not in result:
                                    print(1)
                                    twitter_info = twitter_service.remove_current_user(json.loads(result))
                                    self.reply_to_twitter.extend(twitter_info)
                                    break
                        except Exception as e:
                            pass
            if self.reply_to_twitter:
                for twitter_reply in self.reply_to_twitter:
                    twitter_text = twitter_reply.get('text', None)
                    if twitter_text:
                        twitter_reply['text'] = re.sub(r'@\w+', "", twitter_text).strip()
                        language_result = await language_detection(twitter_reply['text'])
                        twitter_reply['language'] = language_result.name
                        result = await gpt_analyze_service.twitter_name_analyzer(twitter_reply['text'])
                        data = await gpt_analyze_service.get_gpt_translation(result, twitter_reply['language'])
                        twitter_return = api_dance_service.send_reply_to_twitter(twitter_content=data,
                                                                                 twitter_id=twitter_reply['tweet_id'])
                        twitter_return_id = twitter_service.get_reply_id(twitter_return)
                        self.replied_id_list.append(twitter_return_id)
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    async def do_job(self):
        loguru.logger.info("---->{TradingToken} start")
        await self.twitter_bot()


automatically_reply = AutomaticallyReply()


async def main():
    try:
        automatically_reply = AutomaticallyReply()
        await automatically_reply.twitter_bot()
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


if __name__ == '__main__':
    asyncio.run(main())
