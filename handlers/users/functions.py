import datetime
import random

import requests


def code_generator():
    return str(random.randint(1000, 9999))


def get_time():
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M:%S")
    return today


def send_sms(phone_number):  # SMS Send Function. Playmobile service intergration
    x_code = code_generator()
    header = {'Accept': 'application/json', 'Authorization': '',
              'Content-Type': 'application/json'}
    data = {'messages': [{'recipient': phone_number.replace('+', ''), 'message-id': 'STRING',
                          'sms': {'originator': 'NAME', 'content': {'text': 'MESSAGE'}}}]}
    requests.post('PLAYMOBILE_API_URL', json=data, headers=header)
    return x_code
