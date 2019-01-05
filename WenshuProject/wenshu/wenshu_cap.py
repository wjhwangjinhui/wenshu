#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/29 13:56
@Author  : wangjh
@File    : wenshu_cap.py
@desc    : PyCharm
"""
import os
import sys
from io import BytesIO
from threading import Thread

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
    try:
        resq = requests.get(url=img_url, headers=headers, proxies=proxies, timeout=10)
        a = resq.content
        url = "http://127.0.0.1:8888/b"
        files = {'image_file': ('captcha.jpg', BytesIO(a), 'application')}
        con = requests.post(url=url, files=files)
        result_json = con.json()
        result = result_json['value']
        url = 'http://wenshu.court.gov.cn/Content/CheckVisitCode'
        s = result
        data = {
            'ValidateCode': s
        }
        try:
            res = requests.post(url=url, data=data, headers=headers,proxies=proxies,timeout=10)
            res.encoding = res.apparent_encoding
            content = res.text
            if int(content) == 1:
                # log.crawler.info('验证码输入正确')
                filename = str(result) + '.jpg'
                img = os.path.join(os.path.join(cur_dir, 'captcha'), filename)
                with open(img, 'wb')as f:
                    f.write(a)
                    log.crawler.info('验证码保存成功')
            else:
                log.crawler.info('验证码输入错误！！！')
                rec_cap(proxies)
        except Exception as e:
            log.crawler.error('第二次请求：{}'.format(e))
    except Exception as e:
        log.crawler.error('第一次请求：{}'.format(e))



if __name__ == '__main__':
    while True:
        ip_pool = get_proxies_from_redis()
        for proxies in ip_pool:
            try:
                t = Thread(target=rec_cap, args=(proxies,))
                t.start()
            except Exception as e:
                log.crawler.error(e)

