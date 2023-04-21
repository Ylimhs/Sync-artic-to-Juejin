from api.zhihuApi import zhiHuClient
import requests
import json

headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://gitee.com',
        'Referer': 'https://gitee.com/api/v5/swagger',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

def test():
    cli = zhiHuClient("")
    result = cli.get_cl_artc_list()
    print(result)


def downloadZhuanLanToLocalHtml(zhuanLan,md):
    """
    下载知乎专栏文章存入html
    :param zhuanLan: 专栏地址  https://www.zhihu.com/column/c_1341718720926887936  地址是c_1341718720926887936
    :htmlSavePath: html文件存放路径
    """
    # 获取总的文章数量
    urlIndex=f"https://www.zhihu.com/api/v4/columns/{zhuanLan}/items"
    res=requests.get(urlIndex,headers=headers)
    # 知乎比较友好，返回的是json
    totals=json.loads(res.text)["paging"]["totals"]
    totalPage=totals//100+1  # 获取总页数
    for i in range(totalPage):
        # limit最大是100,超过会报错
        urlpage = 'https://www.zhihu.com/api/v4/columns/{}/items?limit={}&offset={}'.format(zhuanLan, 100, 100*i)
        respage = requests.get(urlpage, headers=headers)
        data=json.loads(respage.content)['data']
        for article in data:
            title=article["title"]
            content=article["content"]
            # 替换标题中的特殊符号，不然创建文件会报错
            with open(f'{htmlSavePath}\\{title.replace("?","").replace("？","")}.html',"w",encoding="utf-8") as f:
                f.write(content)
    print("下载完成")





if __name__ == '__main__':
    test()
    # downloadZhuanLanToLocalHtml("awesome-iot","./tt")