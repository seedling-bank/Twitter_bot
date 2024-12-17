import asyncio
import json
import re
import time
import traceback
from asyncio import Lock

import loguru

import con.config
from base import BaseJob
from services.apidance_service import api_dance_service
from services.gpt_analyze_services import gpt_analyze_service
from services.mbti_service import mbti_service
from services.twitter_service import twitter_service
from utils.content_generation import twitter_content_generation
from utils.language_detection import language_detection
from utils.search_term import get_search_term


class AutomaticallyReply(BaseJob):

    def __init__(self):
        self.replied_id_list = []  # 定义已回复list
        self.lock = Lock()

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
            loguru.logger.error(f"self.replied_id_list----------------_{self.replied_id_list}")
            if response_list_required:
                for twitter_info in response_list_required:
                    if twitter_info['tweet_id'] in self.replied_id_list:
                        return  # 如果已经回复过，直接返回h
                    if "@lyricpaxsrks 我的MBTI" in twitter_info['tweet_content']:
                        language_result = await language_detection(twitter_info['tweet_content'])
                        twitter_info['language'] = language_result.name
                        asyncio.create_task(self.user_mbti_analyzer(twitter_info))
                        self.replied_id_list.append(twitter_info['tweet_id'])
                        return
                await self.process_all_twitter_info(response_list_required, gpt_analyze_service, api_dance_service)
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    async def process_twitter_info(self, twitter_info, gpt_analyze_service, api_dance_service, semaphore):
        async with self.lock:  # 确保检查和更新是原子操作
            if twitter_info['tweet_id'] in self.replied_id_list:
                return  # 如果已经回复过，直接返回h

            twitter_info['tweet_content'] = re.sub(r'@\w+', "", twitter_info['tweet_content']).strip()
            language_result = await language_detection(twitter_info['tweet_content'])
            twitter_info['language'] = language_result.name
            result = await gpt_analyze_service.twitter_name_analyzer(twitter_info['tweet_content'])
            data = await gpt_analyze_service.get_gpt_translation(result, twitter_info['language'])
            api_dance_service.send_reply_to_twitter(twitter_content=data, twitter_id=twitter_info['tweet_id'])
            self.replied_id_list.append(twitter_info['tweet_id'])



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
            user_mbti = await mbti_service.get_user_mbti_analyze(data=user_twitter_data, user_name=twitter_info['id_str'])
            data = await gpt_analyze_service.get_gpt_translation(user_mbti, twitter_info['language'])
            print(data)
            print(twitter_info['tweet_id'])
            api_dance_service.send_reply_to_twitter(twitter_content=data, twitter_id=twitter_info['tweet_id'])

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
