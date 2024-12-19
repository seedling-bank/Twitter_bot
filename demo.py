import asyncio
import json
import traceback

import httpx
import loguru
import requests
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import con.config
from models.twitter_celebrities_model import TwitterCelebritiesModel

usernames = [
    # "elonmusk",
    # "BarackObama",
    # "justinbieber",
    # "Cristiano",
    # "rihanna",
    # "katyperry",
    # "taylorswift13",
    # "narendramodi",
    # "realDonaldTrump",
    # "ladygaga",
    # "EllenDeGeneres",
    # "nasa",
    # "kimkardashian",
    # "selenagomez",
    # "billgates",
    # "neymarjr",
    # "jtimberlake",
    # "imvkohli",
    # "britneyspears",
    # "shakira",
    # "ddlovato",
    # "kingjames",
    # "jimmyfallon",
    # "ChampionsLeague",
    # "srbachchan",
    # "bts_twt",
    # "realmadrid",
    # "fcbarcelona",
    # "espn",
    # "mileycyrus",
    # "akshaykumar",
    # "beingsalmankhan",
    # "jlo",
    # "NBA",
    # "iamsrk",
    # "bts_bighit",
    # "oprah",
    # "sportscenter",
    # "premierleague",
    # "niallofficial",
    # "kyliejenner",
    # "MattWallace888",
    # "milesdeutscher",
    # "Noahhweb3",
    # "_kaitoai",
    # "BinanceAfrica",
    # "immunefi",
    # "rowancheung",
    # "0xzerebro",
    # "anothercohen",
    # "Austen",
    # "zebulgar",
    # "agazdecki",
    # "ankurnagpal",
    # "paulg",
    # "AtomSilverman",
    # "hc_capital",
    # "0xDepressionn",
    # "kevxalchemy",
    # "isabellasg3",
    # "RobinNakamoto",
    # "cz_binance",
    # "jimcramer",
    # "okx",
    # "WORLD3_AI",
    # "justinsuntron",
    # "crypto",
    # "BinanceWallet",
    # "rushimanche",
    # "PentagonGamesXP",
    # "Ashcryptoreal",
    # "KookCapitalLLC",
    # "ionet",
    # "0xcryptowizard",
    # "BTC_Archive",
    # "Cointelegraph",
    # "CarlBMenger",
    # "pudgypenguins",
    # "SaharaLabsAI",
    # "binance",
    # "heyibinance",
    # "DujunX",
    # "bitfish1",
    # "MicroStrategy",
    # "saylor",
    # "pumpdotfun",
    # "luna_virtuals",
    # "OpenAI",
    # "GoogleAI",
    # "ai16zdao",
    # "virtuals_io",
    # "aixbt_agent",
    # "truth_terminal",
    # "opensea",
    # "AndyTang_nova",
    "Gemini",
    "adam3us",
    "KMbappe",
    "ErlingHaaland",
    "StephenCurry30",
    "KDTrey5",
    "iamcardib"
]

engine = create_async_engine(
    con.config.settings.DATABASE_URI,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)

SessionFactory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_twitter_headers(auth_token):
    try:
        url = "https://twitter.com/i/api/graphql/nK1dw4oV3k4w5TdtcAdSww/SearchTimeline"

        headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
                             "%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "cookie": f"auth_token={auth_token};ct0=",
            "pragma": "no-cache",
            "referer": "https://twitter.com/",
            "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/113.0.0.0 Safari/537.36",
            "x-csrf-token": "",  # ct0
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "zh-cn",
        }

        client = httpx.Client(headers=headers)

        res1 = client.get(url)
        print(f"{res1.status_code} {res1.text}")
        # 第一次访问用于获取response cookie中的ct0字段，并添加到x-csrf-token与cookie中
        ct0 = res1.cookies.get("ct0")

        client.headers.update(
            {"x-csrf-token": ct0, "cookie": f"auth_token={auth_token};ct0={ct0}"}
        )

        return client.headers

    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


async def get_user_twitter_id_by_api(username: str):
    """
    直接获取twitter id
    :param username:
    :return:
    """
    try:
        # 1. 请求的 URL
        url = "https://x.com/i/api/graphql/-0XdHI-mrHWBQd8-oLo1aA/ProfileSpotlightsQuery"

        # 2. 请求的变量
        variables = {
            "screen_name": f"{username}"  # 替换为你需要查询的用户名
        }
        auth_token = "e924a598897db19027037310e1df54b35e938611"
        # 3. 请求头
        headers = await get_twitter_headers(auth_token=auth_token)
        # 4. 发送请求
        response = requests.get(url, headers=headers, params={"variables": json.dumps(variables)})

        # 5. 处理响应
        if response.status_code == 200:
            data = response.json()
            if data:
                user_id = data.get('data').get('user_result_by_screen_name').get('result').get('rest_id')
                user_name = data.get('data').get('user_result_by_screen_name').get('result').get('legacy').get('name')
                user_username = data.get('data').get('user_result_by_screen_name').get('result').get('legacy').get(
                    'screen_name')
                information = {
                    "twitter_id": user_id,
                    "twitter_name": user_username,
                    "twitter_username": user_name,
                }
                return information
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


async def insert_twitter_celebrities_data(twitter_info):
    async with SessionFactory() as session:
        # 创建插入语句
        stmt = insert(TwitterCelebritiesModel).values(
            twitter_id=twitter_info['twitter_id'],
            twitter_name=twitter_info['twitter_name'],
            twitter_username=twitter_info['twitter_username'],
            is_used=0
        )
        await session.execute(stmt)  # 执行插入语句
        await session.commit()  # 提交事务


async def main():
    for i in usernames:
        result = await get_user_twitter_id_by_api(i)
        await insert_twitter_celebrities_data(result)


if __name__ == '__main__':
    asyncio.run(main())
