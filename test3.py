import requests
from requests_oauthlib import OAuth1

# 替换为你的 Twitter API 凭证
API_KEY = 'uWnGuLyesxISLTsQnQPhs2IL1'
API_SECRET = 'NPHDSvo6aWzCKP7SWXA7fIwoh41Pngl3Tp9BaOi9fkfj1tDHMt'
ACCESS_TOKEN = '4654805796-5pnsYTo4Ux9dDfhXRvBhDiozOlppNw66iXyyaMt'
ACCESS_SECRET = 'BiAvZ8oWWN2gJXwMOQynOABD5KSn8LSOZfOi0kgIFIUto'

# 设置 OAuth1 身份验证
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# Twitter API URL
url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'

# 请求参数
params = {
    'count': 5,
    'since_id': '1700000'  # 替换为你想要的 since_id
}
headers = {
    'Content-Type': 'application/json',
    'AuthToken': "efb2cd709ed756e8ef34ba30ce7981af2addf6ca"
}

# 发起 GET 请求
response = requests.get(url, auth=auth, params=params, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 成功请求
    mentions = response.json()
    for mention in mentions:
        print(f"User: {mention['user']['screen_name']}, Tweet: {mention['text']}")
else:
    # 请求失败
    print(f"Failed to fetch mentions: {response.status_code}")
    print(response.text)
