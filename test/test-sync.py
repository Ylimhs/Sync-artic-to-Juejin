# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
import time

from test.GetCSDNArtics import get_csdn_artic_list_info
from test.testJueJin import html2md, create_article_draft, publish_article


def get_csdn_artics_info():
    return get_csdn_artic_list_info()


def publish_to_JJ(csdn_artics_info):
    print("------------------- publish_to_JJ -----------------")
    for artic in csdn_artics_info:
        artic_info = dict()
        article_id = artic.get("article_id")
        title = artic.get("title")
        description = artic.get("description")
        content = artic.get("content")
        markdowncontent = artic.get("markdowncontent")
        if markdowncontent == "":
            print("----------------html2md-------------")
            content = html2md(content)

        print("------------- content ---------------")
        print(content)
        artic_info.update({
            "category_id": "6809637767543259144",
            "tag_ids": ["6809640407484334093"],
            "title": title,
            "brief_content": description*10,
            "mark_content": content

        })
        id = create_article_draft(artic_info)
        if id is not None:
            print(f"sync {article_id} to {id} sucesss.")
        else:
            print(f"sync {article_id} to {id} failed.")
        time.sleep(3)
        #### 发布：
        if article_id =="129185833":
            ret = publish_article(id)
            print(f" publish_article {article_id} to {id}  ret is {ret}.")

        print("#####################")


def sync_to_jj():
    # get csdn artics info
    csdn_artics_info = get_csdn_artics_info()
    # push to JJ article_draft
    publish_to_JJ(csdn_artics_info)


if __name__ == '__main__':
    sync_to_jj()
