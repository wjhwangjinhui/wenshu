#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import random
import requests
from util.ipproxy import get_proxies_from_redis
from util.headers import headers
from util import log
from model.handle_redis import HandleRedis

h = HandleRedis(6)

def re_request(url,headers=None):
    i = 0
    while i < 200:
        try:
            # ip_pool = get_proxies_from_redis()
            # global proxies
            # proxies = random.choice(ip_pool)
            proxies = None
            res = requests.get(url=url, headers=headers, proxies=proxies, timeout=30)
            status_code = res.status_code
            if status_code == 200:
                return res
            # elif status_code == 502:
            #     log.crawler.info('请求不成功，状态码为：502')
                # h.spop_data_from_redis(proxies)
            else:
                time.sleep(random.uniform(3, 5))
                log.crawler.info('请求不成功，状态码为：{}'.format(status_code))
        except Exception as e:
            i += 1
            a = re.findall(r": (.*?). \(read timeout=30\)", str(e))
            if not a:
                h.spop_data_from_redis(proxies)
            # log.crawler.error(e)
            time.sleep(random.uniform(3, 5))


def re_requests(url, data, headers=None):
    i = 0
    while i < 200:
        # time.sleep(0.5)
        try:
            # ip_pool = get_proxies_from_redis()
            # global proxies
            # proxies = random.choice(ip_pool)
            # log.crawler.info(proxies)
            proxies = None
            res = requests.post(url=url, params=data, headers=headers, proxies=proxies, timeout=30)
            status_code = res.status_code
            if status_code == 200:
                return res
            # elif status_code == 502:
            #     log.crawler.info('请求不成功，状态码为：502')
            #     h.spop_data_from_redis(proxies)
            else:
                time.sleep(random.uniform(3, 5))
                log.crawler.info('请求不成功，状态码为：{}'.format(status_code))
        except Exception as e:
            i += 1
            a = re.findall(r": (.*?). \(read timeout=30\)", str(e))
            if not a:
                h.spop_data_from_redis(proxies)
            # log.crawler.error(e)
            time.sleep(random.uniform(3, 5))
