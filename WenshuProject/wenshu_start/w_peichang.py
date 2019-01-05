#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/30 15:18
@Author  : wangjh
@File    : w_peichang.py
@desc    : PyCharm
"""
import os
import sys
import time
from threading import Thread
import psutil

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from monitor.tasks import start_peichang
from util import log

while True:
    pid = os.getpid()
    p = psutil.Process(pid)
    num = p.num_threads()
    if num <= 10:
        try:
            # log.crawler.info('赔偿线程数 : %s' % num)
            t = Thread(target=start_peichang)
            t.start()
        except Exception as e:
            continue
    if num > 10:
        time.sleep(1)
