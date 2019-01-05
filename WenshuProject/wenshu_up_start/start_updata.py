#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/28 10:27
@Author  : wangjh
@File    : start_updata.py
@desc    : PyCharm
"""
import datetime
import os
import sys
from threading import Thread

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from monitor.tasks_updata import start_up_minshi, start_up_xingshi, start_up_xingzheng, start_up_peichang, start_up_zhixing

while True:
    now = datetime.datetime.now()
    if now.hour == 17 and now.minute == 20:
        t1 = Thread(target=start_up_minshi)
        t1.start()
        t2 = Thread(target=start_up_xingshi)
        t2.start()
        t3 = Thread(target=start_up_xingzheng)
        t3.start()
        t4 = Thread(target=start_up_peichang)
        t4.start()
        t5 = Thread(target=start_up_zhixing)
        t5.start()
        t5.join()