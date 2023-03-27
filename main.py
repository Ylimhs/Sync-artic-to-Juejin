# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
import time

from api.CsdnApi import CsdnClient
from api.JuejinApi import JJClient
from config.config import CSND_COOKIE, JUEJIN_COOKIE, JUEJIN_UUID, SYNC_TO_DRAFT
from utils.utils import logging

# 从CSDN 获取失败的文章
failed_get_artic_list = list()
# 同步到掘金失败的文章列表
failed_sysc_artic_list = list()
# 成功 同步 发布到掘金的文章
success_sysc_artic_dict = dict()
# 成功同步到掘金草稿箱的文章
success_sysc_artic_dratf_dict = dict()

"""
检查必须的参数
"""


def check_env_parmas():
    if CSND_COOKIE is None:
        logging.info("the CSDN_COOKIE is require,please set it.")
        return False
    if JUEJIN_COOKIE is None:
        logging.info("the JUEJIN_COOKIE is require,please set it.")
        return False
    if JUEJIN_UUID is None or JUEJIN_UUID == "":
        logging.info("the JUEJIN_UUID is require,please set it.")
        return False
    logging.info("check_env_parmas success.")
    return True


"""
同步CSDN 到掘金
"""


def get_csdn_artics_info(client):
    artic_info_list = list()
    failed_get_artics_list = list()
    logging.info("begin to get csdn artics list info...")
    try:
        logging.info("begin to get csdn articleId list info...")
        artic_id_list_info = client.get_article_list()
        if artic_id_list_info.get("code") != 200 or artic_id_list_info.get("message") != "success":
            logging.error(
                f"get_article_list return code {artic_id_list_info.get('code')} and  message is {artic_id_list_info.get('message')}...")
            return None
        logging.info("end to get csdn articleId list info success...")
        logging.info("begin to get csdn artic info by the articleId...")
        data = artic_id_list_info.get('data')
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


"""
 检查掘金文章发布时，desc 是否满足要求，并更新
"""


def check_description(client, artic_info, description):
    if len(description) > 50:
        return True

    retry = 3
    while retry > 0:
        try:
            result = client.create_article_draft(artic_info)
            if result.get("err_no") == 0 and result.get("err_msg") == "success":
                logging.info("update_article_draft success....")
                return True
        except:
            pass
        logging.info("failed to update_article_draft and retry....")
        retry += -1
        time.sleep(3)
    if retry == 0:
        logging.info("failed to auto update_article_draft....")
        logging.info("update_article_draft description copy agagin....")
        try:
            while len(description) < 50:
                description += description
            artic_info.update({
                "brief_content": description,
            })
            result = client.create_article_draft(artic_info)
            if result.get("err_no") == 0 and result.get("err_msg") == "success":
                logging.info("update_article_draft description copy success....")
                return True
        except:
            pass
    return False


"""
创建 草稿箱 文章
"""


def create_article_draft(client, artic_info):
    retry = 3
    while retry > 0:
        try:
            result = client.create_article_draft(artic_info)
            if result.get("err_no") == 0 and result.get("err_msg") == "success":
                data = result.get("data")
                return data.get("id")
        except:
            logging.info("failed to create_article_draft....")
            pass
        retry += -1
        time.sleep(3)
    return None


"""
发布草稿箱文章
"""


def publish_article(client, id):
    retry = 3
    while retry > 0:
        try:
            column_ids = list()
            result = client.publish_article(id, column_ids)
            if result.get("err_no") == 0 and result.get("err_msg") == "success":
                return True
        except:
            pass
        logging.info("failed to publish_article and retry....")
        retry += -1
        time.sleep(3)
    if retry == 0:
        logging.info(f"failed to publish_article for {id}....")
    return False


"""
同步CSDN文章到掘金
"""


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
            id = create_article_draft(client, artic_info)
            if id is not None:
                logging.info(f"create_article_draft {article_id} to {id} sucesss.")
            else:
                logging.error(f" create_article_draft {article_id} to {id} failed.")
                failed_sysc_artic_list.append(article_id)
            time.sleep(3)

            # 检查简介是够符合
            changeFormatFlag = check_description(client, artic_info, description)

            # 发布
            logging.info("----------------------------------------------------")
            logging.info("begin publish aticle ...")
            if not SYNC_TO_DRAFT:
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
            else:
                success_sysc_artic_dratf_dict.update({
                    article_id: id
                })
        except Exception as err:
            logging.error(f"sync the artic {article_id} to {id} falid... with {str(err)}")
            failed_sysc_artic_list.append(article_id)

    return


"""
打印文章同步结果
"""


def print_result():
    pass


def sync_csdn_to_jj():
    logging.info("begin to sycn csdn artic to jj")
    cs_client = CsdnClient(CSND_COOKIE)
    jj_client = JJClient(JUEJIN_COOKIE, JUEJIN_UUID)
    csdn_artics_info = get_csdn_artics_info(cs_client)
    # push to JJ article_draft
    publish_csdn_to_jj(jj_client, csdn_artics_info)

    # print result
    print_result()


def main():
    if not check_env_parmas():
        return
    sync_csdn_to_jj()


if __name__ == '__main__':
    main()