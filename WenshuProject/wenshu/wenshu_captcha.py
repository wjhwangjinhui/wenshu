#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/27 9:49
@Author  : wangjh
@File    : wenshu_captcha.py
@desc    : PyCharm
"""
import os
import sys


cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import math
import random
import requests
from util import log
from util.ipproxy import get_proxies_from_redis
from wenshu.captcha_method import Recognize

r = Recognize()

def rec_cap(proxies):
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Cookie': None,
    }
    img_url = 'http://wenshu.court.gov.cn/User/ValidateCode/{}'.format(math.floor(random.random() * 10000))
    resq = requests.get(url=img_url, headers=headers, proxies=proxies,timeout=10)
    a = resq.content
    b = math.floor(random.random() * 1000000)
    filename = str(b) + '.jpg'
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    img = os.path.join(os.path.join(cur_dir, 'captcha'), filename)
    with open(img, 'wb')as f:
        f.write(a)
    result, pic_id = r.recognize_captcha(img, 1902)
    url = 'http://wenshu.court.gov.cn/Content/CheckVisitCode'
    s = result
    data = {
        'ValidateCode': s
    }
    res = requests.post(url=url, data=data, headers=headers,proxies=proxies,timeout=10)
    res.encoding = res.apparent_encoding
    content = res.text
    if int(content) == 1:
        log.crawler.info('验证码输入正确')
    else:
        log.crawler.info('验证码输入错误！！！')
        r.report_err(pic_id)
if __name__ == '__main__':
    ip_pool = get_proxies_from_redis()
    for proxies in ip_pool:
        url = 'http://www.baidu.com'
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
            'Cookie': None,
        }
        res = requests.get(url=url,headers=headers)
        if res.status_code == 200:
            try:
                rec_cap(proxies)
            except Exception as e:
                log.crawler.info(e)
        else:
            continue