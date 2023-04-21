import logging
import time

from api.CsdnApi import CsdnClient
from api.JuejinApi import JJClient

from config.config import SYNC_TO_DRAFT, CSND_COOKIE, JUEJIN_COOKIE
from utils.const import failed_sysc_artic_list, success_sysc_artic_dict, success_sysc_artic_dratf_dict
from utils.articUtils import create_article_draft, check_description, publish_article, print_result
from utils.utils import html_replace_image_links


def publish_csdn_to_jj(client, csdn_artics_info):
    if not csdn_artics_info:
        return
    logging.info("begin to publish_to_JJ ....")
    for artic in csdn_artics_info:
        artic_info = dict()
        article_id = artic.get("article_id")
        id = 0
        try:
            title = artic.get("title")
            description = artic.get("description")
            content = artic.get("content")
            markdowncontent = artic.get("markdowncontent")

            logging.info("Start dumping image url...")
            if content != "":
                content = html_replace_image_links(client, content)
            if markdowncontent != "":
                markdowncontent = html_replace_image_links(client, markdowncontent)
            logging.info("Start dumping image url end...")

            changeFormatFlag = True
            if markdowncontent == "":
                logging.info(f"the format is html, so begin html2md change for the artic {article_id} ...")
                retry = 3
                while retry > 0:
                    try:
                        result = client.html2md(content)
                    except:
                        logging.info(f"html2md change for the artic {article_id} failed and retry...")
                    if result.get("err_no") == 0 and result.get("err_msg") == "":
                        date = result.get("data")
                        content = date.get("text")
                        logging.info(f"html2md change for the artic {article_id} sucesss...")
                        break;
                    retry += -1
                if retry == 0:
                    changeFormatFlag = False
            else:
                content = markdowncontent
            artic_info.update({
                "category_id": "6809637767543259144",
                "tag_ids": ["6809640407484334093"],
                "title": title,
                "brief_content": description,
                "mark_content": content
            })
            if len(description) > 100:
                artic_info.update({
                    "brief_content": description[:100]
                })
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

    return


def get_csdn_artics_info(client):
    artic_info_list = list()
    page = 0
    size = 20
    total = 20
    logging.info("begin to get csdn artics list info...")
    try:
        logging.info("begin to get csdn articleId list info...")
        while page == 0 or page * size < total:
            artic_id_list_info = client.get_article_list(status=CSND_ARTIC_STATUS, page=page)
            if artic_id_list_info.get("code") != 200 or artic_id_list_info.get("message") != "success":
                logging.error(
                    f"get_article_list return code {artic_id_list_info.get('code')} and  message is {artic_id_list_info.get('message')}...")
                return None
            logging.info("end to get csdn articleId list info success...")
            logging.info("begin to get csdn artic info by the articleId...")
            data = artic_id_list_info.get('data')
            page = data.get("page")
            size = data.get("size")
            total = data.get("total")
            for aid in data.get("list"):
                articleId = aid.get("articleId")
                arc_info = ""
                try:
                    arc_info = client.get_article_content(articleId)
                except Exception as err:
                    logging.error(f"fail to get the airtic info for the {articleId} with err is {str(err)}")
                    failed_sysc_artic_list.append(articleId)
                    continue
                    time.sleep(1)
                logging.info(f"get articleId {articleId} content info is {arc_info} success ....")
                logging.info(f"get articleId {articleId} content info success...")
                artic_info_list.append(arc_info['data'])
                time.sleep(1)
        logging.info("end to get csdn artics list info...")
    except Exception as err:
        logging.error("Failed to get the csde artics list info with err is " + str(err))
    return artic_info_list


def sync_csdn_to_jj():
    logging.info("begin to sycn csdn artic to jj")
    cs_client = CsdnClient(CSND_COOKIE)
    jj_client = JJClient(JUEJIN_COOKIE)
    csdn_artics_info = get_csdn_artics_info(cs_client)
    # push to JJ article_draft
    publish_csdn_to_jj(jj_client, csdn_artics_info)

    # print result
    print_result()
