##此方案已废弃

import os
import requests
from fake_useragent import UserAgent


app_ids_str = os.getenv("APP_ID", "")
refresh_tokens_str = os.getenv("REFRESH_TOKEN", "")
app_ids = [line.strip() for line in app_ids_str.strip().splitlines() if line.strip()]
refresh_tokens = [line.strip() for line in refresh_tokens_str.strip().splitlines() if line.strip()]


ua = UserAgent().chrome
base_url = 'https://api.locyanfrp.cn/v2'
sign_url = "/sign"
check_sign_url = "/sign"
get_access_token_url = '/auth/oauth/access-token'

if len(app_ids) != len(refresh_tokens):
    print("错误：APP_ID 与 REFRESH_TOKEN 数量不匹配！")
    exit(1)

accounts = []
for i in range(len(app_ids)):
    accounts.append({
        'app_id': app_ids[i],
        'refresh_token': refresh_tokens[i],
    })


def sign(token, user_id):
    url = f'{base_url}{sign_url}'
    headers = {
        "User-Agent": ua,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': f'Bearer {token}',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'Referer': 'https://preview.locyanfrp.cn/',
    }
    data = {
        'user_id': user_id,
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.json()
    except Exception as e:
        return {'status': False, 'message': str(e)}


def get_access_token(refresh_token="", app_id=""):
    url = f'{base_url}{get_access_token_url}'
    headers = {
        "User-Agent": ua,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'Referer': 'https://preview.locyanfrp.cn/',
    }
    data = {
        'refresh_token': refresh_token,
        'app_id': app_id
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.json()
    except Exception as e:
        return {'status': False, 'message': str(e)}


def check_sign(token, user_id=None):
    url = f'{base_url}{check_sign_url}'
    headers = {
        "User-Agent": ua,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': f'Bearer {token}',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'Referer': 'https://preview.locyanfrp.cn/',
    }
    params = {}
    if user_id is not None:
        params['user_id'] = user_id
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        return {'status': False, 'message': str(e)}


if __name__ == "__main__":
    for idx, account in enumerate(accounts, 1):
        print(f"开始处理第{idx}个账号")

        refresh_token = account.get('refresh_token', '')
        app_id = account.get('app_id', '')

        token_result = get_access_token(refresh_token, app_id)
        if token_result.get("status") == 200 and "data" in token_result and "access_token" in token_result["data"]:
            access_token = token_result["data"]["access_token"]
            user_id = token_result["data"]["user_id"]

            print(f"获取Access Token成功，用户ID：{user_id}，Access Token：{access_token}")

            check_result = check_sign(access_token, user_id)
            if check_result.get("status") == 200:
                data = check_result.get("data", {})
                sign_status = data.get("status", False)
                sign_count = data.get("sign_count", 0)
                total_traffic = data.get("total_get_traffic", 0)
                
                if sign_status:
                    print(f"签到状态：已签到")
                    print(f"累计签到次数：{sign_count}，累计获得流量：{total_traffic}")
                    print("今日已签到，无需重复签到。")
                else:
                    print(f"签到状态：未签到")
                    print(f"累计签到次数：{sign_count}，累计获得流量：{total_traffic}")
                    sign_result = sign(access_token, user_id)
                    if sign_result.get("status") == 200:
                        get_traffic = sign_result.get("data", {}).get("get_traffic", 0)
                        print(f"签到成功，获得流量：{get_traffic}")
                    else:
                        print(f"签到失败，原因：{sign_result.get('message', '未知错误')}")
            else:
                print(f"签到状态检查失败，原因：{check_result.get('message', '未知错误')}")
        else:
            print(f"获取Access Token失败，原因：{token_result.get('message', '未知错误')}，跳过签到")

        print("=" * 40)
