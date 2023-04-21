# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45

from config.config import CSND_COOKIE, JUEJIN_COOKIE
from convert.csdn2JJ import sync_csdn_to_jj
from utils.utils import logging

"""
检查必须的参数
"""

def check_env_parmas():
    check_flag = True
    if CSND_COOKIE is None:
        logging.info("the CSDN_COOKIE is require,please set it.")
        return False
    if JUEJIN_COOKIE is None:
        logging.info("the JUEJIN_COOKIE is require,please set it.")
        check_flag = False
    logging.info("check_env_parmas success.")
    return check_flag

def main():
    if not check_env_parmas():
        return
    sync_csdn_to_jj()


if __name__ == '__main__':
    main()
