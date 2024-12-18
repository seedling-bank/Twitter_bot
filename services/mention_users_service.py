import asyncio
import random

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import con.config
from models.twitter_celebrities_model import TwitterCelebritiesModel

engine = create_async_engine(
    con.config.settings.DATABASE_URI,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)

SessionFactory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class MentionUsersService:
    def __init__(self):
        pass

    async def get_twitter_celebrities_data(self):
        async with SessionFactory() as session:
            result = await session.execute(
                select(TwitterCelebritiesModel).where(TwitterCelebritiesModel.is_used == False)
            )
            unused_celebrities = result.scalars().all()

            if unused_celebrities:
                return unused_celebrities

    async def update_twitter_celebrities_data(self, twitter_id):
        async with SessionFactory() as session:
            result = await session.execute(
                update(TwitterCelebritiesModel)
                .where(TwitterCelebritiesModel.twitter_id == twitter_id)
                .values(is_used=1)
            )
            await session.commit()


mention_users_service = MentionUsersService()


async def main():
    results = await mention_users_service.get_twitter_celebrities_data()

    result = random.choices(results)
    print(result[0].twitter_id)
    print(result[0].twitter_name)


if __name__ == '__main__':
    asyncio.run(main())
