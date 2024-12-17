import asyncio
import json
import traceback

import loguru

from base import BaseJob
from services.apidance_service import api_dance_service
from services.gpt_analyze_services import gpt_analyze_service
from services.twitter_service import twitter_service
from utils.content_generation import twitter_content_generation
from utils.search_term import get_search_term


class AutomaticallyTweet(BaseJob):

    def init(self):
        loguru.logger.info("Initializing AutomaticallyTweet")

    def get_scheduler(self):
        return {
            "trigger": "cron",
            "second": "0",  # 指定秒数为0
            "minute": "0",
            "hour": "*/1",  # 任意小时
            # "hour": "*",  # 任意小时
            "day": "*",  # 任意日期
            "month": "*",  # 任意月份
            "day_of_week": "*",  # 任意星期
            "timezone": "UTC",
            "misfire_grace_time": 600,
        }

    async def twitter_bot(self):
        try:
            search_list = ['btc', 'eth', 'web3', 'ai', 'agent']
            search = get_search_term(search_list)
            loguru.logger.info(f"Searching for {search}")
            while True:
                search_results = api_dance_service.get_search_data(search=search)
                if search_results != "local_rate_limited":
                    if 'Rate limit exceeded.' not in search_results:
                        break
                loguru.logger.info(f"search_results for {search_results}")
            user_info = twitter_service.get_twitter_username(json.loads(search_results))
            loguru.logger.info(f"user_info for {user_info}")
            initial_content = await gpt_analyze_service.twitter_name_analyzer(user_info.get("user_username"))
            loguru.logger.info(f"initial_content for {initial_content}")
            twitter_content = await twitter_content_generation(analyze_content=initial_content, user_info=user_info)
            loguru.logger.info(f"twitter_content for {twitter_content}")
            api_dance_service.send_on_twitter(twitter_content=twitter_content)

        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    async def do_job(self):
        loguru.logger.info("---->{TradingToken} start")
        await self.twitter_bot()


automatically_tweet = AutomaticallyTweet()


async def main():
    try:
        automatically_tweet = AutomaticallyTweet()
        await automatically_tweet.twitter_bot()
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


if __name__ == '__main__':
    asyncio.run(main())
