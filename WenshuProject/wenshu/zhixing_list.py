#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/15 14:46
@Author  : wangjh
@File    : zhixing_list.py
@desc    : PyCharm
"""
import os
import random
import sys
import time

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import os
import execjs
import json
import execjs.runtime_names
from util import log
from urllib import parse
from util.headers import my_headers
from util.re_req import re_requests, re_request

cur_dir = os.path.dirname(os.path.realpath(__file__))
wenshujs = os.path.join(cur_dir, "wenshu.js")


def get_guid():
    with open(wenshujs, 'r', encoding='utf-8') as fp:
        js = fp.read()
        ect = execjs.compile(js)
        guid = ect.call('guid')  # guid为js的函数名称
        return guid


def get_number(**kwargs):
    guid = kwargs.get("guid")
    url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
    data = {'guid': guid}
    import requests
    from util.headers import headers
    res = requests.post(url=url, headers=headers, data=data)
    if res:
        number = res.text
        return number


def get_vjx(**kwargs):
    with open(wenshujs, 'r', encoding='utf-8') as fp:
        js = fp.read()
    ect = execjs.compile(js)
    url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+5+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%89%A7%E8%A1%8C%E6%A1%88%E4%BB%B6'
    while True:
        try:
            headers = {
                'User-Agent': 'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                'Cookie': None,
                # 'Accept': '*/*',
                # 'User-Agent': random.choice(my_headers),
                # 'Accept-Encoding': 'gzip, deflate',
                # 'Accept-Language': 'zh-CN,zh;q=0.9',
                # 'Connection': 'keep-alive',
                # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'X-Requested-With': 'XMLHttpRequest',
                # 'Host': 'wenshu.court.gov.cn',
                # 'Origin': 'http://wenshu.court.gov.cn',
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
        'Param': '案件类型:执行案件,全文检索:%s' % key,
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
        # 'Accept': '*/*',
        # 'User-Agent': random.choice(my_headers),
        # 'Cookie': 'vjkl5=' + vjk15,
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Connection': 'keep-alive',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Host': 'wenshu.court.gov.cn',
        # 'Origin': 'http://wenshu.court.gov.cn',
        # 'Referer': 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid={}&conditions=searchWord+5+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:{}&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:{}'.format(guid, parse.quote('执行案件'), parse.quote(key))
    }
    # i = 0
    # while i < 10000:
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
    # number = get_number(guid=guid)
    a = ['&gui', 'wens']
    number = random.choice(a)
    # log.crawler.info('开始获取vl5x, vjkl5')
    vl5x, vjkl5 = get_vjx()
    kwargs["number"] = number
    kwargs['vl5x'] = vl5x
    kwargs['vjkl5'] = vjkl5
    kwargs['guid'] = guid
    data_list = get_data(**kwargs)
    if data_list:
        return data_list
    # retry = 0
    # while retry < 3:
    #     try:
    #         log.crawler.info('开始获取data_list')
    #         data_list = get_data(**kwargs)
    #         if data_list:
    #             return data_list
    #     except Exception as e:
    #         log.error.info(e)
    #         log.crawler.info("发生异常尝试get_data再次连接最多重连3次第{}次连接".format(retry + 1))
    #         retry += 1


if __name__ == '__main__':
    # # print(wenshujs)
    index = 1
    key = '债权'
    kwargs = dict(index=index, key=key)
    data = main(**kwargs)
    print(data)
