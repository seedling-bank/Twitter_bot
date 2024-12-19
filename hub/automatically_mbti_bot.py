import asyncio
import json
import re
import time
import traceback
from asyncio import Lock

import loguru
import redis
from redis.asyncio import from_url

import con.config
from base import BaseJob
from services.apidance_service import api_dance_service
from services.gpt_analyze_services import gpt_analyze_service
from services.mbti_service import mbti_service
from services.twitter_service import twitter_service
from utils.content_generation import twitter_content_generation
from utils.language_detection import language_detection
from utils.search_term import get_search_term

redis_client = from_url(con.config.settings.REDIS_URL, decode_responses=True, max_connections=100000)


class AutomaticallyMbti(BaseJob):

    def __init__(self, redis_key='replied_id_set'):
        self.redis_client = None
        self.redis_key = redis_key
        self.lock = Lock()

    async def initialize_redis(self):

        # 初始化 Redis 客户端
        self.redis_client = from_url(con.config.settings.REDIS_URL, decode_responses=True, max_connections=100000)

    async def add_to_replied_set(self, reply_id):
        """添加ID到集合中，并同步到Redis"""
        await self.redis_client.sadd(self.redis_key, reply_id)

    async def remove_from_replied_set(self, reply_id):
        """从集合中移除ID，并同步到Redis"""
        await self.redis_client.srem(self.redis_key, reply_id)

    async def is_in_replied_set(self, reply_id):
        """检查是否在集合中"""
        return self.redis_client.sismember(self.redis_key, reply_id)

    async def get_all_replied_ids(self):
        """获取 Redis 集合中的所有 ID"""
        raw_ids = await self.redis_client.smembers(self.redis_key)
        # 数据已经是字符串类型，直接返回
        return set(raw_ids)

    def init(self):
        loguru.logger.info("Initializing AutomaticallyMbti")

    def get_scheduler(self):
        return {
            "trigger": "cron",
            "second": "*/10",  # 指定秒数为0
            "minute": "*",
            "hour": "*",  # 任意小时
            "day": "*",  # 任意日期
            "month": "*",  # 任意月份
            "day_of_week": "*",  # 任意星期
            "timezone": "UTC",
            "misfire_grace_time": 600,
        }

    async def twitter_bot(self):
        await self.initialize_redis()
        search_result_list = []
        try:
            # 获取搜索第一页
            while True:
                search_results = api_dance_service.get_search_data(search=con.config.settings.TWITTER_NAME)
                if search_results != "local_rate_limited":
                    if 'Rate limit exceeded.' not in search_results:
                        break
            if search_results:
                tweets = json.loads(search_results).get('tweets')
                search_result_list.extend(tweets)

            response_list_required = twitter_service.get_search_resul_analysis(search_result_list)
            loguru.logger.error(f"response_list_required----------------_{response_list_required}")
            if response_list_required:
                ids = await self.get_all_replied_ids()
                for twitter_info in response_list_required:
                    if (twitter_info['tweet_id'] not in ids and
                            "@lyricpaxsrks MBTI" in twitter_info['tweet_content']):
                        language_result = await language_detection(twitter_info['tweet_content'])
                        twitter_info['language'] = language_result.name
                        await asyncio.create_task(self.user_mbti_analyzer(twitter_info))
                        await self.add_to_replied_set(str(twitter_info['tweet_id']))
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    async def user_mbti_analyzer(self, twitter_info):
        if twitter_info:
            user_twitter_id = twitter_info['id_str']
            user_twitter_data = await api_dance_service.get_user_twitter_article(user_twitter_id)
            print(user_twitter_data)
            user_mbti = await mbti_service.get_user_mbti_analyze(data=user_twitter_data,
                                                                 user_name=twitter_info['id_str'])
            api_dance_service.send_reply_to_twitter(twitter_content=user_mbti, twitter_id=twitter_info['tweet_id'])

    async def do_job(self):
        loguru.logger.info("---->{AutomaticallyMbti} start")
        await self.twitter_bot()


automatically_mbti = AutomaticallyMbti()


async def main():
    try:
        automatically_mbti = AutomaticallyMbti()
        await automatically_mbti.twitter_bot()
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


if __name__ == '__main__':
    asyncio.run(main())
