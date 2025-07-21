import http.client
import urllib.parse
import json
import os

app_id = os.getenv("APP_ID")
refresh_token = os.getenv("REFRESH_TOKEN")

# 获取 access_token
conn = http.client.HTTPSConnection("api.locyanfrp.cn")
payload = urllib.parse.urlencode({
    "app_id": app_id,
    "refresh_token": refresh_token
})
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
conn.request("POST", "/v2/auth/oauth/access-token", payload, headers)
res = conn.getresponse()
data = res.read().decode("utf-8")

try:
    result = json.loads(data)
    if result.get("status") != 200:
        print("❌ 获取 access_token 失败:", result.get("message", "未知错误"))
    else:
        access_token = result["data"]["access_token"]
        user_id = result["data"]["user_id"]
        print("✅ access_token:", access_token)
        print("✅ user_id:", user_id)

        # 获取签到信息
        conn2 = http.client.HTTPSConnection("api.locyanfrp.cn")
        headers2 = {"Authorization": f"Bearer {access_token}"}
        conn2.request("GET", f"/v2/sign?user_id={user_id}", "", headers2)
        sign_result = conn2.getresponse().read().decode("utf-8")

        try:
            sign_data = json.loads(sign_result)
            print(f"📅 签到天数: {sign_data['data']['sign_count']}")
            print(f"📦 签到流量: {sign_data['data']['total_get_traffic']} MiB")
        except Exception as e:
            print("❌ 签到错误:", e)
            print("原始返回:", sign_result)

except Exception as e:
    print("❌ access_token 响应解析失败:", e)
    print("响应内容:", data)
