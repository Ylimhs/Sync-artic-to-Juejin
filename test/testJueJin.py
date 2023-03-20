# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
from api.JuejinApi import JJClient
from config.config import JUEJIN_COOKIE, JUEJIN_UUID

client = JJClient(JUEJIN_COOKIE, JUEJIN_UUID)


def create_article_draft(artic_info):
    # artic_info = {
    #     "category_id": "6809637767543259144",
    #     "tag_ids": ["6809640407484334093"],
    #     "link_url": "",
    #     "cover_image": "",
    #     "title": "apitestapitest",
    #     "brief_content": "",
    #     "edit_type": 10,
    #     "html_content": "deprecated",
    #     "mark_content": "apitestapitestapitestapitestapitestapitestapitest"
    # }
    result = client.create_article_draft(artic_info)
    if result.get("err_no") == 0 and result.get("err_msg") == "success":
        data = result.get("data")
        return data.get("id")
    return None


def html2md(content):
    result = client.html2md(content);
    if result.get("err_no") == 0 and result.get("err_msg") == "":
        data = result.get("data")
        return data.get("text")


def publish_article(id):
    column_ids = list()
    result = client.publish_article(id, column_ids)
    return result


if __name__ == '__main__':
    create_article_draft()
