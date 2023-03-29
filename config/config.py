# -*- coding: UTF-8 -*-
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def str_to_bool(str):
    return True if str.lower() == 'true' else False
# load from env
# JueJin Config
JUEJIN_COOKIE = os.getenv("JUEJIN_COOKIE")
JUEJIN_UUID = os.getenv("JUEJIN_UUID")
CSND_COOKIE = os.getenv("CSND_COOKIE")
SYNC_TO_DRAFT = os.getenv("SYNC_TO_DRAFT")
CSND_ARTIC_STATUS = os.getenv("CSND_ARTIC_STATUS")

if SYNC_TO_DRAFT is None or SYNC_TO_DRAFT == "":
    SYNC_TO_DRAFT = True
else:
    SYNC_TO_DRAFT = str_to_bool(SYNC_TO_DRAFT)
if CSND_ARTIC_STATUS is None:
    CSND_ARTIC_STATUS = "enable"

if __name__ == '__main__':
    print(JUEJIN_COOKIE)
    print(JUEJIN_UUID)
    print(SYNC_TO_DRAFT)
