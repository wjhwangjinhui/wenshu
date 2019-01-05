#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/30 15:20
@Author  : wangjh
@File    : ws_minshi.py
@desc    : PyCharm
"""
import os
import sys
import time
from threading import Thread
import psutil

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from monitor.tasks import start_save_minshi
from util import log

while True:
    pid = os.getpid()
    p = psutil.Process(pid)
    num = p.num_threads()
    if num <= 20:
        try:
            # log.crawler.info('民事的线程数 : %s' % num)
            t = Thread(target=start_save_minshi)
            t.start()
        except Exception as e:
            continue
    if num > 20:
        time.sleep(1)
