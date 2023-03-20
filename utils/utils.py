# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
# -*- coding: UTF-8 -*-
import datetime
import json
import logging
import os
import hashlib
import hmac
import random
from base64 import b64encode
from urllib.parse import urlparse, urlencode
import urllib.parse
import requests


# 配置日志显示
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='log/task.log',
#                     filemode='a',
#                     encoding='utf-8')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    encoding='utf-8')

class LarkException(Exception):
    def __init__(self, code=0, msg=None):
        self.code = code
        self.msg = msg

    def __str__(self) -> str:
        return "{}:{}".format(self.code, self.msg)

    __repr__ = __str__


def request(method, url, headers, payload=None, data=None):
    if payload is None:
        payload = {}
    logging.info("URL: " + url)
    # logging.info("headers:\n" + json.dumps(headers, indent=2, ensure_ascii=False))
    logging.info("payload: " + json.dumps(payload, indent=2, ensure_ascii=False))
    # response = requests.request(method, url, headers=headers, json=payload)
    response = requests.request(method, url, headers=headers, data=payload)
    if response.status_code >= 400:
        response.raise_for_status()
    return response


"""
CSDN 接口请求生成 x-ca-nonce
"""


def generate_uuid():
    uuid_format = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    uuid = ''
    for char in uuid_format:
        if char == 'x':
            uuid += random.choice('0123456789abcdef')
        elif char == 'y':
            uuid += random.choice(['8', '9', 'a', 'b'])
        else:
            uuid += char
    return uuid


"""
CSDN 接口参数 x-ca-signature 生成
"""


def get_sign(uuid, url):
    parsed_url = urlparse(url)
    if parsed_url.query:
        query_params = dict(x.split('=') for x in parsed_url.query.split('&'))
        sorted_params = sorted(query_params.items())
        new_query_string = urlencode(sorted_params)
        new_path = parsed_url.path + '?' + new_query_string
    else:
        new_path = parsed_url.path
    ekey = "9znpamsyl2c7cdrr9sas0le9vbc3r6ba".encode()
    to_enc = f"GET\napplication/json, text/plain, */*\n\n\n\nx-ca-key:203803574\nx-ca-nonce:{uuid}\n{new_path}".encode()
    # print(to_enc)
    sign = b64encode(hmac.new(ekey, to_enc, digestmod=hashlib.sha256).digest()).decode()
    return sign


if __name__ == '__main__':
    # m7yvw8o9pdn/0EbTOFxYHfQnc6myGHTYzehbUe7l3pM=
    print(get_sign("c6590c52-0713-476a-9ee7-97aa4ae86a2a",
                   "https://bizapi.csdn.net/blog/phoenix/console/v1/article/list?pageSize=20&status=enable"))
