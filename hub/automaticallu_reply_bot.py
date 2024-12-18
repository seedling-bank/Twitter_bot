import asyncio
import json
import re
import time
import traceback
from asyncio import Lock

import loguru
import redis

import con.config
from base import BaseJob
from services.apidance_service import api_dance_service
from services.gpt_analyze_services import gpt_analyze_service
from services.mbti_service import mbti_service
from services.twitter_service import twitter_service
from utils.content_generation import twitter_content_generation
from utils.language_detection import language_detection
from utils.search_term import get_search_term

pool = redis.ConnectionPool.from_url(con.config.settings.REDIS_URL, max_connections=100000)
redis_client = redis.Redis(connection_pool=pool)


class AutomaticallyReply(BaseJob):

    def __init__(self, redis_key='replied_id_set'):
        self.redis_client = redis_client
        self.redis_key = redis_key
        self.lock = Lock()

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
        raw_ids = self.redis_client.smembers(self.redis_key)
        return {id.decode() for id in raw_ids}

    def init(self):
        loguru.logger.info("Initializing AutomaticallyReply")

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
            loguru.logger.error(f"self.replied_id_set----------------_{await self.get_all_replied_ids()}")
            if response_list_required:
                for twitter_info in response_list_required:
                    if (twitter_info['tweet_id'] not in await self.get_all_replied_ids() and
                            "@lyricpaxsrks MBTI" in twitter_info['tweet_content']):
                        language_result = await language_detection(twitter_info['tweet_content'])
                        twitter_info['language'] = language_result.name
                        await asyncio.create_task(self.user_mbti_analyzer(twitter_info))
                        await self.add_to_replied_set(str(twitter_info['tweet_id']))
                await self.process_all_twitter_info(response_list_required, gpt_analyze_service, api_dance_service)
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    async def process_twitter_info(self, twitter_info, gpt_analyze_service, api_dance_service, semaphore):
        async with semaphore:
            if twitter_info['tweet_id'] in (await self.get_all_replied_ids()):
                return  # 如果已经回复过，直接返回h
            twitter_info['tweet_content'] = re.sub(r'@\w+', "", twitter_info['tweet_content']).strip()
            language_result = await language_detection(twitter_info['tweet_content'])
            twitter_info['language'] = language_result.name
            if twitter_info['language'] == "ENGLISH":
                result = await gpt_analyze_service.twitter_name_analyzer(twitter_info['tweet_content'])
                api_dance_service.send_reply_to_twitter(twitter_content=result, twitter_id=twitter_info['tweet_id'])
            await self.add_to_replied_set(str(twitter_info['tweet_id']))

    async def process_all_twitter_info(self, response_list_required, gpt_analyze_service,
                                       api_dance_service, max_concurrent_tasks=10):
        semaphore = asyncio.Semaphore(max_concurrent_tasks)
        # 创建任务列表
        tasks = [
            self.process_twitter_info(twitter_info, gpt_analyze_service, api_dance_service, semaphore)
            for twitter_info in response_list_required
        ]
        # 并发运行所有任务
        await asyncio.gather(*tasks)

    async def user_mbti_analyzer(self, twitter_info):
        if twitter_info:
            user_twitter_id = twitter_info['id_str']
            user_twitter_data = await api_dance_service.get_user_twitter_article(user_twitter_id)
            print(user_twitter_data)
            user_mbti = await mbti_service.get_user_mbti_analyze(data=user_twitter_data,
                                                                 user_name=twitter_info['id_str'])
            api_dance_service.send_reply_to_twitter(twitter_content=user_mbti, twitter_id=twitter_info['tweet_id'])

    async def do_job(self):
        loguru.logger.info("---->{AutomaticallyReply} start")
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
