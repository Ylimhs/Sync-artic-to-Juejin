import time

from api.JuejinApi import JJClient
from api.zhihuApi import zhiHuClient
from config.config import JUEJIN_COOKIE, ZHIHU_COOKIE, SYNC_TO_DRAFT
from utils.articUtils import create_article_draft, check_description, publish_article, print_result
from utils.const import failed_sysc_artic_list, success_sysc_artic_dict, success_sysc_artic_dratf_dict
from utils.utils import logging, html_replace_image_links



def timeTOS(t):
    # 转换成时间数组
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp

def get_zhihu_zhuanlan_artics_info(zh_client, column_id,start_time, end_time):
    artic_info_list = list()
    # 获取总的文章数量
    res = zh_client.get_cl_artc_list(column_id)
    totals = res["paging"]["totals"]
    totalPage = totals // 100 + 1  # 获取总页数
    stop_get = False
    # totalPage = 1
    for i in range(totalPage and not stop_get):
        respage = zh_client.get_cl_artc_list(column_id, offset=i * 100)
        data = respage['data']
        for article in data:
            articleinfo = dict()
            title = article["title"]
            id = article["id"]
            excerpt = article["excerpt"]
            content = article["content"]
            created = article['created']
            articleinfo.update({
                "title": title,
                "id": id,
                "desc": excerpt,
                "content": content
            })
            if start_time is None and end_time is None:
                artic_info_list.append(articleinfo)
            elif start_time is not None and end_time is not None:
                if start_time <= created <= end_time:
                    artic_info_list.append(articleinfo)
                elif created < start_time:
                    stop_get = True
                    break

    return artic_info_list


def publish_zhihu_to_jj(client, zhihu_zhuanlan_artics_info):
    if not zhihu_zhuanlan_artics_info:
        return
    else:
        zhihu_zhuanlan_artics_info_new = []
        i = len(zhihu_zhuanlan_artics_info)
        while i > 0:
            zhihu_zhuanlan_artics_info_new.append(zhihu_zhuanlan_artics_info[i - 1])
            i -= 1
    logging.info("begin to publish_to_JJ ....")
    for artic in zhihu_zhuanlan_artics_info_new:
        artic_info = dict()
        article_id = artic.get("id")
        id = 0
        try:
            title = artic.get("title")
            description = artic.get("desc")
            content = artic.get("content")
            logging.info("Start dumping image url...")
            if content != "":
                content = html_replace_image_links(client, content)
            logging.info("Start dumping image url end...")

            changeFormatFlag = True
            logging.info(f"the format is html, so begin html2md change for the artic {article_id} ...")
            retry = 3
            while retry > 0:
                try:
                    result = client.html2md(content)
                except Exception as e:
                    logging.info(f"html2md change for the artic {article_id} failed and retry...")
                    continue
                if result.get("err_no") == 0 and result.get("err_msg") == "":
                    date = result.get("data")
                    content = date.get("text")
                    logging.info(f"html2md change for the artic {article_id} sucesss...")
                    break
                retry += -1
            if retry == 0:
                changeFormatFlag = False
            # "tag_ids": ["6809640642101116936"] - 人工智能
            # "tag_ids": ["6809641083107016712"] - 资讯
            artic_info.update({
                "category_id": "6809637773935378440",
                "tag_ids": ["6809641083107016712"],
                "title": title,
                "brief_content": description,
                "mark_content": content
            })
            if len(description) > 100:
                artic_info.update({
                    "brief_content": description[:100]
                })

            # with open(f'{article_id}.md', "w", encoding="utf-8") as f:
            #     f.write(content)
            # return
            id = create_article_draft(client, artic_info)
            if id is not None:
                logging.info(f"create_article_draft {article_id} to {id} sucesss.")
            else:
                logging.error(f" create_article_draft {article_id} to {id} failed.")
                failed_sysc_artic_list.append(article_id)
                continue
            time.sleep(3)

            # 检查简介是够符合
            changeFormatFlag = check_description(client, id, artic_info, description)

            # 发布
            logging.info("----------------------------------------------------")
            b = SYNC_TO_DRAFT
            logging.info(f"----------------SYNC_TO_DRAFT is {b}------------------------------------")

            if not SYNC_TO_DRAFT:
                logging.info("begin publish aticle ...")
                if changeFormatFlag:
                    ret = publish_article(client, id)
                    if ret:
                        logging.info(f"sync the artic {article_id} to {id} success...")
                        success_sysc_artic_dict.update({
                            article_id: id
                        })
                    else:
                        logging.error(f"sync the artic {article_id} to {id} falid...")
                        success_sysc_artic_dratf_dict.update({
                            article_id: id
                        })
                else:
                    logging.info(f"sync the artic {article_id} to {id} falid with the description to short...")
                    success_sysc_artic_dratf_dict.update({
                        article_id: id
                    })
                logging.info("end publish aticle ...")
            else:
                success_sysc_artic_dratf_dict.update({
                    article_id: id
                })
        except Exception as err:
            logging.error(f"sync the artic {article_id} to {id} falid... with {str(err)}")
            failed_sysc_artic_list.append(article_id)


def zhihu2JJ():
    logging.info("begin to sycn zhihu zhuanlan artic to jj")
    # ZHIHU_COOKIE 可以不需要
    zh_client = zhiHuClient(ZHIHU_COOKIE)
    jj_client = JJClient(JUEJIN_COOKIE)
    start_time = "2023-06-15 00:00:00"
    end_time = "2023-06-15 22:59:00"
    zhuanlanName = "qbitai"
    # zhihu_zhuanlan_artics_info = get_zhihu_zhuanlan_artics_info(zh_client, "jiqizhixin")
    zhihu_zhuanlan_artics_info = get_zhihu_zhuanlan_artics_info(zh_client, zhuanlanName, timeTOS(start_time), timeTOS(end_time))
    print(zhihu_zhuanlan_artics_info)
    print(len(zhihu_zhuanlan_artics_info))
    publish_zhihu_to_jj(jj_client, zhihu_zhuanlan_artics_info)
    # print_result()

if __name__ == '__main__':
    zhihu2JJ()
