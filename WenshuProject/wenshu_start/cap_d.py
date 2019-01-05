#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/27 13:32
@Author  : wangjh
@File    : cap_d.py
@desc    : PyCharm
"""
import os
import psutil
from threading import Thread
import sys
import time
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from util import log
from wenshu.wenshu_captcha import rec_cap
from util.ipproxy import get_proxies_from_redis


while True:
    ip_pool = get_proxies_from_redis()
    for proxies in ip_pool:
        try:
            t = Thread(target=rec_cap, args=(proxies,))
            t.start()
            pid = os.getpid()
            p = psutil.Process(pid)
            num = p.num_threads()
            if num >= 5:
                time.sleep(10)
        except Exception as e:
            log.crawler.info(e)
    time.sleep(100)






