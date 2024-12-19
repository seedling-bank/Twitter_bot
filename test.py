import http.client
import json
import ssl
import urllib.parse  # 用于处理 URL 编码

# 定义参数
base_url = "/graphql/Following"
params = {
    "userId": "44196397",  # 用户 ID
    "count": 20,  # 获取的关注数量
    "includePromotedContent": False  # 是否包含推广内容
}

variables = json.dumps(params)  # 使用 json.dumps 确保是合法的 JSON 格式

# 对 JSON 字符串进行 URL 编码
query_string = urllib.parse.urlencode({"variables": variables})

url = f"{base_url}?{query_string}"  # 拼接完整的路径
print(url)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
# 创建一个 HTTPS 连接对象
conn = http.client.HTTPSConnection("api.apidance.pro", context=context)

# 请求的有效负载（此处为空字符串，因为是 GET 请求）
payload = ''

# 请求头，包含 API 密钥（需要替换为实际的 API 密钥）
headers = {
    'apikey': 'veyizsgc0f5x4mbl5k4xmajxvkhjex'  # 在这里填入您的 API 密钥
}

# 发送 GET 请求
conn.request("GET", url, payload, headers)

# 获取响应
res = conn.getresponse()

# 读取响应数据
data = res.read()

# 将字节数据解码为字符串并打印
result = data.decode("utf-8")

# 关闭连接
conn.close()

result = json.loads(result)

for instruction in result.get("data").get('user').get('result').get('timeline').get('timeline').get('instructions'):
    if instruction.get('type') == "TimelineAddEntries":
        entries = instruction.get('entries')[:-2]
        for entry in entries:
            try:
                rest_id = entry.get('content').get('itemContent').get('user_results').get('result').get('rest_id')
                name = entry.get('content').get('itemContent').get('user_results').get('result').get('legacy').get('name')
                screen_name = entry.get('content').get('itemContent').get('user_results').get('result').get('legacy').get('screen_name')
                print(rest_id, name, screen_name)
                print('------------------------')
            except Exception as e:
                pass


