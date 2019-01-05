#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/28 9:28
@Author  : wangjh
@File    : xingshi_list.py
@desc    : PyCharm
"""
import os
import random
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import os
import execjs
import json
import requests
import execjs.runtime_names
from util.headers import headers
from util import log
from util.re_req import re_request, re_requests
cur_dir = os.path.dirname(os.path.realpath(__file__))

wenshujs = os.path.join(cur_dir, "wenshu.js")


def get_guid():
    with open(wenshujs, 'r', encoding='utf-8') as fp:
        js = fp.read()
        ect = execjs.compile(js)
        guid = ect.call('guid')  # guid为js的函数名称
        return guid


def get_number(**kwargs):
    print("start get number......")
    guid = kwargs.get("guid")
    prox = kwargs.get("proxies", None)
    url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
    data = {'guid': guid}
    res = requests.post(url=url, headers=headers, data=data, proxies=prox, timeout=20)
    if res:
        number = res.text
        return number


def get_vjx(**kwargs):
    with open(wenshujs, 'r', encoding='utf-8') as fp:
        js = fp.read()
    ect = execjs.compile(js)
    url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
    while True:
        try:
            headers = {
                'User-Agent': 'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                'Cookie': None,
            }
            res1 = re_request(url=url, headers=headers)
            vjkl5 = res1.headers['Set-Cookie'].split(';')[0].split('=')[1]
            vl5x = ect.call('getKey', vjkl5)
            return vl5x, vjkl5
        except:
            pass


def get_data(**kwargs):
    key = kwargs.get('key')
    index = kwargs.get("index")
    v15x = kwargs.get('vl5x')
    number = kwargs.get('number')
    guid = kwargs.get('guid')
    vjk15 = kwargs.get('vjkl5')
    url = 'http://wenshu.court.gov.cn/List/ListContent'
    data = {
        'Param': '上传日期:{} TO {},案件类型:刑事案件'.format(key[0], key[1]),
        'Index': index,
        'Page': 10,
        'Order': '法院层级',
        'Direction': 'asc',
        'vl5x': v15x,
        'number': number,
        'guid': guid
    }
    headers = {
        'Cookie': 'vjkl5=' + vjk15,
        'User-Agent': 'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    }
    for _ in range(200):
        res = re_requests(url=url, data=data, headers=headers)
        try:
            s = res.json()
            if str(s) != 'remind':
                s_list = json.loads(s)
                return s_list
        except:
            continue


def main(**kwargs):
    guid = get_guid()
    # number = get_number(guid=guid, proxies=proxies)
    a = ['&gui', 'wens']
    number = random.choice(a)
    vl5x, vjkl5 = get_vjx()
    kwargs["number"] = number
    kwargs['vl5x'] = vl5x
    kwargs['vjkl5'] = vjkl5
    kwargs['guid'] = guid
    data_list = get_data(**kwargs)
    if data_list:
        return data_list


if __name__ == '__main__':
    index = 1
    key = ('2018-11-27', '2018-11-28')
    kwargs = dict(index=index, key=key)
    data = main(**kwargs)
    print(data)