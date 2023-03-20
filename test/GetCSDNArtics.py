import time

from api.CsdnApi import CsdnClient
from config.config import CSND_COOKIE

client = CsdnClient(CSND_COOKIE)


def get_csdn_artic_list_info():
    artic_info_list = list()

    print("-----------get artic id list -------------")
    artic_id_list = client.get_article_list()
    print(artic_id_list)
    data = artic_id_list.get('data')
    print("-----------get artic id list end-------------")

    for id in data.get("list"):
        print(id.get("articleId"))

    print("-----------get artic info -------------")
    for aid in data.get("list"):
        articleId = aid.get("articleId")
        arc_info = client.get_article_content(articleId)
        print(f"get articleId {articleId} content info is {arc_info}\n")
        time.sleep(1)
        artic_info_list.append(arc_info['data'])
    print("-----------get artic info end -------------")
    return artic_info_list

if __name__ == '__main__':
    get_csdn_artic_list_info()
