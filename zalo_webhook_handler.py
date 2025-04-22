import os

import requests

# Lấy token từ biến môi trường hoặc gán cứng để test
ZALO_OA_TOKEN = os.getenv("ZALO_OA_TOKEN")

def send_zalo_reply(user_id, text):
    url = "https://openapi.zalo.me/v2.0/oa/message"
    headers = {
        "access_token": ZALO_OA_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"user_id": user_id},
        "message": {"text": text}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📤 Gửi phản hồi về Zalo:", response.status_code, response.text)
    return response.ok
