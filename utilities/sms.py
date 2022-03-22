import requests
import json


def send_sms(number, text, sms_id):
    """
    :param number: str; enter number without "+" sign, example: 998941234567
    :param text: str; enter text you want
    :param sms_id: int; sms id from backend
    :return:
    """
    username = "fastechnika"
    password = "M@4cVt$O3"

    url = "http://91.204.239.44/broker-api/send"
    data = {
        "messages": [
            {
                "recipient": f"{number}",
                "message-id": f"{sms_id}",
                "sms": {
                    "originator": "3700",
                    "content": {
                        "text": text
                    }
                }
            }]
    }
    r = requests.post(url, auth=(username, password), json=data)
    return r.text
