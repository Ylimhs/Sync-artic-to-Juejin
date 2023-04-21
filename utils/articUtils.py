from utils.utils import logging
import time

from config.config import CSND_ARTIC_STATUS
from utils.const import failed_sysc_artic_list, success_sysc_artic_dict, success_sysc_artic_dratf_dict

"""
 检查掘金文章发布时，desc 是否满足要求，并更新
"""

def check_description(client, dratf_id, artic_info, description):
    if len(description) > 50:
        return True
    retry = 3
    while retry > 0:
        try:
            draft_abstract_result = client.get_article_draft_abstract(dratf_id)
            if draft_abstract_result.get("err_no") == 0 and draft_abstract_result.get("err_msg") == "success":
                draft_abstract_data = draft_abstract_result.get("data")
                text = draft_abstract_data.get('text')
                if len(text) < 50:
                    retry = 0
                    logging.info("failed to update_article_draft the draft_abstract is len < 50")
                    continue
                else:
                    artic_info.update({
                        "id": dratf_id,
                        "brief_content": description
                    })
                    result = client.update_article_draft(artic_info)
                    if result.get("err_no") == 0 and result.get("err_msg") == "success":
                        logging.info("update_article_draft success....")
                        return True
            else:
                logging.info(f"failed to get_article_draft_abstract for the {dratf_id} and retry.... ")
        except Exception as err:
            pass
        logging.info("failed to update_article_draft and retry....")
        retry += -1
        time.sleep(3)
    if retry == 0:
        logging.info("failed to auto update_article_draft....")
        logging.info("update_article_draft description copy agagin....")
        try:
            copyDecs = description
            while len(description) < 50:
                description += copyDecs
            if len(description) > 100:
                description = description[:100]
            artic_info.update({
                "id": dratf_id,
                "brief_content": description
            })
            result = client.update_article_draft(artic_info)
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
            logging.info(f"publish_article return is {result}")
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



def print_result():
    logging.info("----------------------------------------")
    logging.info("failed_get_artic_list:")
    logging.info(failed_sysc_artic_list)
    logging.info("failed_sysc_artic_list:")
    logging.info(failed_sysc_artic_list)
    for key, value in success_sysc_artic_dict.items():
        logging.info('sync {} to {} sccuess.'.format(key, value))
    for key, value in success_sysc_artic_dratf_dict.items():
        logging.info('sync {} to artic_dratf  {} sccuess.'.format(key, value))

    logging.info("----------------------------------------")
