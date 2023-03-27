import json
from utils.utils import request


class JJClient(object):
    def __init__(self, juejin_cookie, uuid):
        self.cookie = juejin_cookie
        self.uuid = uuid

    """
    创建草稿箱文章
    """

    def create_article_draft(self, artic_info):
        title = artic_info['title']
        brief_content = artic_info['brief_content']
        mark_content = artic_info['mark_content']
        edit_type = 10
        html_content = "deprecated"
        if artic_info.get("tag_ids") is None:
            tag_ids = list()
            tag_ids.append("6809640407484334000")
        else:
            tag_ids = artic_info.get("tag_ids")
            # tag 前端
        if artic_info.get("category_id") is None:
            # 前端
            category_id = "6809637767543259144"
        else:
            category_id = artic_info.get("category_id")
        if artic_info.get("cover_image") is None:
            cover_image = ""
        else:
            cover_image = artic_info.get("cover_image")
        if artic_info.get("link_url") is None:
            link_url = ""
        else:
            link_url = artic_info.get("link_url")

        url = "https://api.juejin.cn/content_api/v1/article_draft/create?aid=2608&uuid=" + self.uuid

        payload = json.dumps({
            "category_id": category_id,
            "tag_ids": tag_ids,
            "link_url": link_url,
            "cover_image": cover_image,
            "title": title,
            "brief_content": brief_content,
            "edit_type": edit_type,
            "html_content": html_content,
            "mark_content": mark_content
        })
        headers = {
            'authority': 'api.juejin.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': self.cookie,
            'origin': 'https://juejin.cn',
            'referer': 'https://juejin.cn/',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        return request("POST", url, headers=headers, payload=payload).json()
    """
       更新草稿箱文章
    """

    def update_article_draft(self, artic_info):
        title = artic_info['title']
        brief_content = artic_info['brief_content']
        mark_content = artic_info['mark_content']
        edit_type = 10
        html_content = "deprecated"
        if artic_info.get("tag_ids") is None:
            tag_ids = list()
            tag_ids.append("6809640407484334000")
        else:
            tag_ids = artic_info.get("tag_ids")
            # tag 前端
        if artic_info.get("category_id") is None:
            # 前端
            category_id = "6809637767543259144"
        else:
            category_id = artic_info.get("category_id")
        if artic_info.get("cover_image") is None:
            cover_image = ""
        else:
            cover_image = artic_info.get("cover_image")
        if artic_info.get("link_url") is None:
            link_url = ""
        else:
            link_url = artic_info.get("link_url")

        url = "https://api.juejin.cn/content_api/v1/article_draft/update?aid=2608&uuid=" + self.uuid

        payload = json.dumps({
            "category_id": category_id,
            "tag_ids": tag_ids,
            "link_url": link_url,
            "cover_image": cover_image,
            "title": title,
            "brief_content": brief_content,
            "edit_type": edit_type,
            "html_content": html_content,
            "mark_content": mark_content
        })
        headers = {
            'authority': 'api.juejin.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': self.cookie,
            'origin': 'https://juejin.cn',
            'referer': 'https://juejin.cn/',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        return request("POST", url, headers=headers, payload=payload).json()


        """
        发布草稿箱文章
        """

    def publish_article(self, draft_id, column_ids=None):
        if column_ids is None:
            column_ids = list()
        url = "https://api.juejin.cn/content_api/v1/article/publish?aid=2608&uuid=" + self.uuid
        payload = json.dumps({
            "draft_id": draft_id,
            "sync_to_org": False,
            "column_ids": column_ids
        })
        headers = {
            'Host': 'api.juejin.cn',
            'Cookie': self.cookie,
            'content-type': 'application/json',
            'accept': '*/*',
            'accept-language': 'zh-cn',
            'x-secsdk-csrf-token': '000100000001425a8f1c60849db0c53f293dc3fb7962cab718203de596a73865c4ac2bb33940174e73053f750002',
            'origin': 'https://juejin.cn',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15',
            'referer': 'https://juejin.cn/'
        }

        return request("POST", url, headers=headers, payload=payload).json()

    """
    html2md 转换
    """

    def html2md(self, content):
        url = "https://juejin.cn/markdown/html2md"
        payload = json.dumps({
            "text": content
        })
        headers = {
            'authority': 'juejin.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'cookie': self.cookie,
            'origin': 'https://juejin.cn',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        return request("POST", url, headers=headers, payload=payload).json()

    """
    通过草稿箱 获取 文章的摘要简介(掘金发布要求不少于50字)
    
    """
    def get_article_draft_abstract(self, draft_id):
        url = "https://api.juejin.cn/content_api/v1/article_draft/abstract?draft_id=" + draft_id + "&aid=2608&uuid=" + self.uuid
        payload = {}
        headers = {
            'authority': 'api.juejin.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': self.cookie,
            'origin': 'https://juejin.cn',
            'referer': 'https://juejin.cn/',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        return request("GET", url, headers=headers, payload=payload).json()
   
    """
    图片转存
    """
    def img_urlSave(self, imgUrl):
        url = "https://juejin.cn/image/urlSave"

        payload = json.dumps({
            "url": imgUrl
        })
        headers = {
            'authority': 'juejin.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': self.cookie,
            'origin': 'https://juejin.cn',
            'referer': 'https://juejin.cn/editor/drafts/7214758560459014201',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        return request("POST", url, headers=headers, payload=payload).json()
    
