from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TwitterCelebritiesModel(Base):
    __tablename__ = 'twitter_celebrities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_id = Column(String)
    twitter_name = Column(String)
    twitter_username = Column(String)
    is_used = Column(SmallInteger)


