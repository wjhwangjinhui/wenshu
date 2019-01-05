#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import traceback
import importlib
import time
import random
from util import log
from util.ipproxy import get_proxies_from_redis
crawler_map = {
    'minshi_list': 'wenshu.minshi_list',
    'minshi_detail': 'wenshu.minshi_detail',
    'xingshi_list': 'wenshu.xingshi_list',
    'xingshi_detail': 'wenshu.xingshi_detail',
    'xingzheng_list': 'wenshu.xingzheng_list',
    'xingzheng_detail': 'wenshu.xingzheng_detail',
    'zhixing_list': 'wenshu.zhixing_list',
    'zhixing_detail': 'wenshu.zhixing_detail',
    'peichang_list': 'wenshu.peichang_list',
    'peichang_detail': 'wenshu.peichang_detail',
    'minshi_up_list': 'wenshu_updata.minshi_list',
    'xingshi_up_list': 'wenshu_updata.xingshi_list',
    'xingzheng_up_list': 'wenshu_updata.xingzheng_list',
    'zhixing_up_list': 'wenshu_updata.zhixing_list',
    'peichang_up_list': 'wenshu_updata.peichang_list',
}


# 代理在这里给
def start(**kwargs):
    """
    :param kwargs: 参数字典必须包含prov键与data键根据prov的值找到对应的脚本代理在这里给
                   data的值为爬虫脚本需要的参数
    :return:
    """
    # 拿代理
    # log.crawler.info("获取的代理数量为:%d"%len(ip_pool))
    module = kwargs.get("module")
    if module is None or module not in crawler_map:
        raise ValueError("请求的modul参数有异常")
    data = kwargs.get("data")
    if data is None or not isinstance(data, dict):
        raise ValueError("请求的modul参数有异常")

    spider_module = importlib.import_module(
        crawler_map[module]
    )
    # 发生异常实现重试3次
    retry = 0
    while retry < 3:
        try:
            result = spider_module.main(**data)
            return result
        except Exception as e:
            time.sleep(random.uniform(1, 2))
            log.crawler.info("发生异常尝试再次连接最多重连3次第{}次连接".format(retry + 1))
            retry += 1
            if retry == 3:
                log.error.info("发生异常,参数为:%s\n,信息为:%s" % (kwargs, traceback.format_exc()))
                raise e
def start2(**kwargs):
    """
    :param kwargs: 参数字典必须包含prov键与data键根据prov的值找到对应的脚本代理在这里给
                   data的值为爬虫脚本需要的参数
    :return:
    """
    # 拿代理
    # log.crawler.info("获取的代理数量为:%d"%len(ip_pool))
    is_proxies = kwargs.get("proxies", False)
    module = kwargs.get("module")
    if module is None or module not in crawler_map:
        raise ValueError("请求的modul参数有异常")
    data = kwargs.get("data")
    if data is None or not isinstance(data, dict):
        raise ValueError("请求的modul参数有异常")

    spider_module = importlib.import_module(
        crawler_map[module]
    )
    # 发生异常实现重试3次
    retry = 0
    while retry < 3:
        try:
            if is_proxies:
                ip_pool = get_proxies_from_redis()
                if ip_pool:
                    proxies = random.choice(ip_pool)
                    log.crawler.info(proxies)
                    data['proxies'] = proxies
            result = spider_module.main(**data)
            return result
        except Exception as e:
            time.sleep(random.uniform(1, 2))
            log.crawler.info("发生异常尝试再次连接最多重连3次第{}次连接".format(retry + 1))
            retry += 1
            if retry == 3:
                log.error.info("发生异常,参数为:%s\n,信息为:%s" % (kwargs, traceback.format_exc()))
                raise e
