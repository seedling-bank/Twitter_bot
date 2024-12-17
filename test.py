import time

import requests
from requests_oauthlib import OAuth1

# 你的 Twitter/X API 凭据
API_KEY = "bxVqLNzMRUmGUY5dTRCPDb2Sg"
API_SECRET_KEY = "riCChKdLJLk9n5gsv2dvRypqmsQKXbkxflqgPRavMU3jiT3P5U"
ACCESS_TOKEN = "1709536223294017537-JeEQZG5ASNrekt6S8PA8OUuMirDphP"
ACCESS_TOKEN_SECRET = "5mu7Chce1ijRSI8lBNEI7ChFN6N0aAWSQyJctmeffUxdJ"


def get_user_tweets(user_id):
    # 你的 Bearer Token
    # BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPcWxgEAAAAAAu3Jg4rwziCG811BICOvgN3oV%2Fg%3DfSdcuOVFiEB96leKJUKF6mb2QQgK0zVZf4kCbC1chLwEuMVvo8"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAGOuwEAAAAA4QtVadeOZlMXxJdWNynSjnXxuTs%3DwY3bUZwP0deo6vCTKjN5WusxYLZ2ZqfK9z8kPk0zM8zEDjh4iA"

    # 请求 URL
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"


    # 请求头
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    # 请求参数
    params = {
        "max_results": 100  # 获取最多 100 条推文
    }

    # 发送 GET 请求
    response = requests.get(url, headers=headers, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        # 请求成功，解析 JSON 数据
        tweets = response.json()
        return tweets
    elif response.status_code == 429:
        # 速率限制，解析响应头
        reset_time = int(response.headers.get("x-rate-limit-reset", time.time()))
        current_time = int(time.time())
        wait_time = reset_time - current_time

        print("Rate limit exceeded.")
        print(f"Rate limit will reset in {wait_time} seconds (at {time.ctime(reset_time)}).")

        # 等待限制解除
        time.sleep(wait_time + 1)  # 多等 1 秒，确保限制已解除
        return get_user_tweets(user_id)  # 重试请求
    else:
        # 请求失败，打印错误信息
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    result = get_user_tweets(4654805796)
    print(result)

