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


class AutomaticallyReply(BaseJob):

    def init(self):
        loguru.logger.info("Initializing AutomaticallyTweet")

    def get_scheduler(self):
        return {
            "trigger": "cron",
            "second": "5",  # 指定秒数为0
            "minute": "*",
            "hour": "*",  # 任意小时
            "day": "*",  # 任意日期
            "month": "*",  # 任意月份
            "day_of_week": "*",  # 任意星期
            "timezone": "UTC",
            "misfire_grace_time": 600,
        }

    async def twitter_bot(self):
        try:
            twitter_ids = ['1867412735946109218']
            for twitter_id in twitter_ids:
                try:
                    result = api_dance_service.get_twitter_details(twitter_id)
                except Exception as e:
                    pass
                print(result)
                # break

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
