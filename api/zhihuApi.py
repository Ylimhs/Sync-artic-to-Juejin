from utils.utils import request


class zhiHuClient(object):
    def __init__(self, zhihu_cookie):
        self.cookie = zhihu_cookie

    def get_cl_artc_list(self, column_id=None, limit=100, offset=0):
        url = 'https://www.zhihu.com/api/v4/columns/{}/items?limit={}&offset={}'.format(column_id, limit, offset)
        payload = {}
        headers = {
            'authority': 'www.zhihu.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cookie': '_zap=c1ee13e5-c835-4af0-b83a-45345655962e; _xsrf=vpUPW3xQDVCeMGhjCmquz39DGXYob04L; d_c0="AFAf4MGvRBOPTqq2lSMGUAmmA7aAC09zd8M=|1623806990"; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=AEBxH5EFNjJFURQBRUd62Edcf0EyrAeK; q_c1=8c4a3c318eb14ef4acc9bd0a602cd3ce|1626255149000|1626255149000; __snaker__id=fme3NCG1eamVQuXO; gdxidpyhxdE=o4BzWHHfyBBodHI15eQTrKzM%2FLJYyUyu2RRY1RJBfEAEWmYCAfV2S8X0WeMCG%5Cxu20pBIHkOSDLaPXqy3HBinwZPRysP%2BxJdybvdat99O%2FvpVvoCUWb%2B81yoLtEnW8KZnEpc6jR4x0lWQWPsNrvvtzV5Rzqxng7460CopCAXXDuahGCT%3A1656919590187; YD00517437729195%3AWM_NI=e3Oqf8DV%2BDRUBeps0VwziEZ9k%2FSHeLIucqjvqKnC7UYftZZcmwHsq%2FWrbd0KMIZ%2BGX6hY7c%2Bx3IZHE4Id6ATu3T1AgQPv4a6GBuFb3Bfxh4rNdZD1dRAhL98Tvv36mmiNUQ%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee8bd421f1ba8785d03388b08fa2d14e878b9ab1c85ef58c9ab2d94af4ea9abbec2af0fea7c3b92aa7ed8192e534888ae5a5d15f82bbc094b35eb5a6a7a6d933a9f19da9e8488babad92e97eb395a2a4b65f9bbabcbbd969afa98894f42595aeae85b3418f9796ccc654f6b897d8e221bced87bbcb4ff897acd7c460b7ed9cd2c46d9390bad5e43e859ebba7e13982bab889b77a8ebc96a5b470929fa8adbc3498aabad4b567afb782b6d437e2a3; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1680571275,1680751584,1681353960,1682044474; tst=r; SESSIONID=kWuszYrbi558OKSxjAuAITjUVjbhOl7sGy8GM1R5jVf; JOID=VlwRBkie-fuTx-ihGJ_-JP0CRuIL9a6P5rqx03vwzM6qjqTyYBkNvfbA6KAfQUUHgmb0QC9cNt-WTLcquNsFR64=; osd=VlASB06e9fiSweitG574JPEBR-QL-a2O4Lq90Hr2zMKpj6LybBoMu_bM66EZQUkEg2D0TCxdMN-aT7YsuNcGRqg=; z_c0=2|1:0|10:1682044298|4:z_c0|80:MS4xM0s4VkFnQUFBQUFtQUFBQVlBSlZUVUc2SkdYcTVFVFZBbGV6Q3gzOXloam9FMnhBMC1IeFB3PT0=|b72f97987382cb098f2fe1ed612745fe9c1139a078d48d994dd45095bcfce732; KLBRSID=9d75f80756f65c61b0a50d80b4ca9b13|1682044325|1682044291; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1682044506; KLBRSID=9d75f80756f65c61b0a50d80b4ca9b13|1682044497|1682044291',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-ab-param': '',
            # 'x-ab-pb': 'CkYbAD8ARwC0AGkBagF0ATsCzALXAtgCtwPWBFEFiwWMBZ4FMQbrBicHdAh5CGAJ9AlrCr4KcQuHC+AL5QvmC3EMjwzDDPgMEiMAAAAAAgAAAgAAAAAAAQAAAQEAAAAGAQMAAAAAAAAABgACAA==',
            'x-requested-with': 'fetch',
            'x-zse-93': '101_3_3.0'
        }
        return request("GET", url, headers=headers, payload=payload).json()
