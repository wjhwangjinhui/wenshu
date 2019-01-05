#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/28 10:25
@Author  : wangjh
@File    : start_dpeichang.py
@desc    : PyCharm
"""
import os
import sys
import time
from threading import Thread
import psutil

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from monitor.tasks_updata import start_peichang
from util import log

while True:
    pid = os.getpid()
    p = psutil.Process(pid)
    num = p.num_threads()
    if num <= 3:
        try:
            t = Thread(target=start_peichang)
            t.start()
        except Exception as e:
            continue
    if num > 3:
        time.sleep(1)