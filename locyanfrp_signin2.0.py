import os
import http.client
import urllib.parse
import json

def get_access_token(app_id, refresh_token):
    conn = http.client.HTTPSConnection("api.locyanfrp.cn")
    payload = urllib.parse.urlencode({
        "app_id": app_id,
        "refresh_token": refresh_token
    })
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    conn.request("POST", "/v2/auth/oauth/access-token", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    return json.loads(data)

def check_sign(access_token, user_id):
    conn = http.client.HTTPSConnection("api.locyanfrp.cn")
    headers = {"Authorization": f"Bearer {access_token}"}
    path = f"/v2/sign?user_id={user_id}"
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    return json.loads(data)

def do_sign(access_token, user_id):
    conn = http.client.HTTPSConnection("api.locyanfrp.cn")
    payload = urllib.parse.urlencode({"user_id": user_id})
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }
    conn.request("POST", "/v2/sign", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    return json.loads(data)

def main():
    # 环境变量直接多行，每行一个账号或token
    app_ids = os.getenv("APP_ID", "").splitlines()
    refresh_tokens = os.getenv("REFRESH_TOKEN", "").splitlines()

    # 去除空行和空白符
    app_ids = [x.strip() for x in app_ids if x.strip()]
    refresh_tokens = [x.strip() for x in refresh_tokens if x.strip()]

    if len(app_ids) != len(refresh_tokens):
        print("错误：APP_ID 与 REFRESH_TOKEN 数量不匹配！")
        return

    for idx, (app_id, refresh_token) in enumerate(zip(app_ids, refresh_tokens), 1):
        print(f"\n==== 开始处理第 {idx} 个账号 ====")
        token_result = get_access_token(app_id, refresh_token)
        if token_result.get("status") != 200:
            print("❌ 获取 access_token 失败:", token_result.get("message", "未知错误"))
            continue

        access_token = token_result["data"]["access_token"]
        user_id = token_result["data"]["user_id"]
        print("✅ access_token:", access_token)
        print("✅ user_id:", user_id)

        check_result = check_sign(access_token, user_id)
        if check_result.get("status") != 200:
            print("❌ 查询签到状态失败:", check_result.get("message", "未知错误"))
            continue

        data = check_result.get("data", {})
        if data.get("status", False):
            print(f"今日已签到，累计签到次数：{data.get('sign_count', 0)}，累计获得流量：{data.get('total_get_traffic', 0)}")
        else:
            print("未签到，开始签到...")
            sign_result = do_sign(access_token, user_id)
            if sign_result.get("status") == 200:
                print(f"签到成功，获得流量：{sign_result['data'].get('get_traffic', 0)}")
            else:
                print("签到失败：", sign_result.get("message", "未知错误"))

if __name__ == "__main__":
    main()
