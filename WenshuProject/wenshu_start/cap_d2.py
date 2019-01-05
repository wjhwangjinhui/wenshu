#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/29 14:50
@Author  : wangjh
@File    : cap_d2.py
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
from wenshu.wenshu_cap import rec_cap
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
            if num >= 15:
                time.sleep(5)
        except Exception as e:
            log.crawler.error(e)
    time.sleep(20)






