import asyncio
import json
import random

import loguru
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import con.config
from base import BaseJob
from models.twitter_celebrities_model import TwitterCelebritiesModel
from services.apidance_service import api_dance_service
from services.mention_users_service import mention_users_service
from services.twitter_service import twitter_service

engine = create_async_engine(
    con.config.settings.DATABASE_URI,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)

SessionFactory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class AutomaticallyFollowingFetcher(BaseJob):
    def __init__(self):
        pass

    def init(self):
        loguru.logger.info("Initializing AutomaticallyFollowingFetcher")

    def get_scheduler(self):
        return {
            "trigger": "cron",
            "second": "0",  # 指定秒数为0
            "minute": "0",
            "hour": "0",  # 任意小时
            "day": "*",  # 任意日期
            "month": "*",  # 任意月份
            "day_of_week": "*",  # 任意星期
            "timezone": "UTC",
            "misfire_grace_time": 600,
        }

    async def find_unfetched_following(self):
        async with SessionFactory() as session:
            result = await session.execute(
                select(TwitterCelebritiesModel).where(TwitterCelebritiesModel.is_following == False)
            )
            unused_celebrities = result.scalars().all()

            if unused_celebrities:
                return unused_celebrities

    async def following_fetcher(self):
        user_list = await automatically_following_fetcher.find_unfetched_following()
        user_data = random.choices(user_list)
        await mention_users_service.update_user_following_data(user_data[0].twitter_id)
        user_info = {
            'user_id': user_data[0].twitter_id,
            'user_name': user_data[0].twitter_username,
            "user_username": user_data[0].twitter_name
        }
        while True:
            search_results = api_dance_service.get_user_following(user_info)
            if search_results != "local_rate_limited":
                if 'Rate limit exceeded.' not in search_results:
                    break

        # next_cursor备用
        user_info_list, next_cursor = twitter_service.following_data_analysis(json.loads(search_results))

        for user_info in user_info_list:
            await mention_users_service.insert_twitter_celebrities_data(user_info)


    async def do_job(self):
        loguru.logger.info("---->{AutomaticallyFollowingFetcher} start")
        await self.twitter_bot()


automatically_following_fetcher = AutomaticallyFollowingFetcher()


async def main():
    automatically_following_fetcher = AutomaticallyFollowingFetcher()
    await automatically_following_fetcher.following_fetcher()


if __name__ == '__main__':
    asyncio.run(main())
