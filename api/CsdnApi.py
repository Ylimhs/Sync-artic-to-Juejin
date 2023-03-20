# -*- coding: utf-8 -*-
# @Desc   :  csdn 使用接口
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
import urllib.parse

from utils.utils import request, generate_uuid, get_sign


class CsdnClient(object):
    def __init__(self, csdn_cookie):
        self.cookie = csdn_cookie

    """
        GET
    application/json, text/plain, */*
    
    
    
    x-ca-key:203803574
    x-ca-nonce:754a95be-abb1-4692-b4ae-2414b122d644
    /blog/phoenix/console/v1/article/list?pageSize=20&status=enable
    获取文章列表(全部可见)
    """

    def get_article_list(self, status="all", pageSize=20):
        url = "https://bizapi.csdn.net/blog/phoenix/console/v1/article/list?status=" + status + "&pageSize=" + str(
            pageSize)
        nonce = generate_uuid()
        signature = get_sign(nonce, url)
        headers = {
            'authority': 'bizapi.csdn.net',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': self.cookie,
            'origin': 'https://mp.csdn.net',
            'referer': 'https://mp.csdn.net/mp_blog/manage/article?spm=3001.5298',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'x-ca-key': '203803574',
            'x-ca-nonce': nonce,
            'x-ca-signature': signature,
            'x-ca-signature-headers': 'x-ca-key,x-ca-nonce'
        }
        return request("GET", url, headers=headers).json()

    def get_article_content(self, articleId):
        url = "https://bizapi.csdn.net/blog-console-api/v1/editor/getArticle?id=" + str(articleId)
        nonce = generate_uuid()
        signature = get_sign(nonce, url)
        headers = {
            'authority': 'bizapi.csdn.net',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': self.cookie,
            'origin': 'https://mp.csdn.net',
            'referer': 'https://mp.csdn.net/mp_blog/manage/article?spm=3001.5298',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'x-ca-key': '203803574',
            'x-ca-nonce': nonce,
            'x-ca-signature': signature,
            'x-ca-signature-headers': 'x-ca-key,x-ca-nonce'
        }
        result = ""
        try:
            result = request("GET", url, headers=headers).json()
        except Exception as errr:
            raise Exception(str(result))
        else:
            if result.get("msg") != "success":
                raise Exception(str(result))
        return result
