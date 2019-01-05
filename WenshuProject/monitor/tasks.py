#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from util import log
from control_spider import start
from model.handle_redis import HandleRedis
from wenshu.doc_decrypt import get_aes_key
r = HandleRedis(1)

def get_item(kwargs):
    a = 0
    while a < 15:
        items = start(**kwargs)
        if items:
            if len(items) > 1:
                run_eval = items[0]['RunEval']
                aes_key = get_aes_key(run_eval)
                log.crawler.info(aes_key)
                if not str(aes_key)[0].isupper():
                    return items
                else:
                    a += 1
            if a > 10:
                items = [{'RunEval': ''}]
                return items

def start_minshi(**kwargs):
    index = 1
    key = r.get_data_redis("TB_WENSHU_MINSHI")
    if key:
        a = 0
        while True:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="minshi_list", data=dict(index=index, key=key))
                items = get_item(kwargs)
                if items:
                    run_eval = items[0]['RunEval']
                else:
                    break
                if len(items) == 1:
                    break
                log.crawler.info("获取%s第%d页的文件ID长度为:%d" % (key, index, len(items) - 1))
                for item in items[1:]:
                    data = {}
                    data["docid"] = item.get('文书ID')
                    data["CASE_TYPE"] = item.get('案件类型', '')
                    data["CASE_TIME"] = item.get('裁判日期', '')
                    data["CASE_NAME"] = item.get('案件名称', '')
                    data["CASE_NUM"] = item.get('案号', '')
                    data["COURT_NAME"] = item.get('法院名称', '')
                    data['runeval'] = run_eval
                    hr = HandleRedis(1)
                    table = "MINSHI_DATA"
                    hr.cache_dict_redis(table, data)
                index += 1
                if len(items) - 1 < 10:
                    break
            except Exception as e:
                log.error.info('请求数据出现{}'.format(e))
                a += 1
                if a == 3:
                    # log.error.info('请求数据出现{}'.format(e))
                    break
    else:
        log.crawler.info('TB_WENSHU_MINSHI遍历完毕.....')


def start_save_minshi(**kwargs):
    data = r.get_data_redis("MINSHI_DATA")
    if data:
        kwargs = dict(module="minshi_detail", data=ast.literal_eval(data))
        start(**kwargs)
    else:
        log.crawler.info('MINSHI_DATA遍历完毕.....')


def start_xingshi(**kwargs):
    index = 1
    key = r.get_data_redis("TB_WENSHU_XINGSHI")
    if key:
        a = 0
        while True:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="xingshi_list", data=dict(index=index, key=key))
                items = get_item(kwargs)
                if items:
                    run_eval = items[0]['RunEval']
                else:
                    break
                if len(items) == 1:
                    break
                log.crawler.info("获取%s第%d页的文件ID长度为:%d" % (key, index, len(items) - 1))
                for item in items[1:]:
                    data = {}
                    data["docid"] = item.get('文书ID')
                    data["CASE_TYPE"] = item.get('案件类型', '')
                    data["CASE_TIME"] = item.get('裁判日期', '')
                    data["CASE_NAME"] = item.get('案件名称', '')
                    data["CASE_NUM"] = item.get('案号', '')
                    data["COURT_NAME"] = item.get('法院名称', '')
                    data['runeval'] = run_eval
                    hr = HandleRedis(1)
                    table = "XINGSHI_DATA"
                    hr.cache_dict_redis(table, data)
                index += 1
                if len(items) - 1 < 10:
                    break
            except Exception as e:
                log.error.info('请求数据出现{}'.format(e))
                a += 1
                if a == 3:
                    # log.error.info('请求数据出现{}'.format(e))
                    break
    else:
        log.crawler.info('TB_WENSHU_XINGSHI遍历完毕.....')


def start_save_xingshi(**kwargs):
    data = r.get_data_redis("XINGSHI_DATA")
    if data:
        kwargs = dict(module="xingshi_detail", data=ast.literal_eval(data))
        start(**kwargs)
    else:
        log.crawler.info('XINGSHI_DATA遍历完毕.....')


def start_xingzheng(**kwargs):
    index = 1
    key = r.get_data_redis("TB_WENSHU_XINGZHENG")
    if key:
        a = 0
        while True:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="xingzheng_list", data=dict(index=index, key=key))
                items = get_item(kwargs)
                if items:
                    run_eval = items[0]['RunEval']
                else:
                    break
                if len(items) == 1:
                    break
                log.crawler.info("获取%s第%d页的文件ID长度为:%d" % (key, index, len(items) - 1))
                for item in items[1:]:
                    data = {}
                    data["docid"] = item.get('文书ID')
                    data["CASE_TYPE"] = item.get('案件类型', '')
                    data["CASE_TIME"] = item.get('裁判日期', '')
                    data["CASE_NAME"] = item.get('案件名称', '')
                    data["CASE_NUM"] = item.get('案号', '')
                    data["COURT_NAME"] = item.get('法院名称', '')
                    data['runeval'] = run_eval
                    hr = HandleRedis(1)
                    table = "XINGZHENG_DATA"
                    hr.cache_dict_redis(table, data)
                index += 1
                if len(items) - 1 < 10:
                    break
            except Exception as e:
                log.error.info('请求数据出现{}'.format(e))
                a += 1
                if a == 3:
                    # log.error.info('请求数据出现{}'.format(e))
                    break
    else:
        log.crawler.info('TB_WENSHU_XINGZHENG遍历完毕.....')


def start_save_xingzheng(**kwargs):
    data = r.get_data_redis("XINGZHENG_DATA")
    if data:
        kwargs = dict(module="xingzheng_detail", data=ast.literal_eval(data))
        start(**kwargs)
    else:
        log.crawler.info('XINGZHENG_DATA遍历完毕.....')


def start_zhixing(**kwargs):
    index = 1
    key = r.get_data_redis("TB_WENSHU_ZHIXING")
    if key:
        a = 0
        while True:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="zhixing_list", data=dict(index=index, key=key))
                items = get_item(kwargs)
                if items:
                    run_eval = items[0]['RunEval']
                else:
                    break
                if len(items) == 1:
                    break
                log.crawler.info("获取%s第%d页的文件ID长度为:%d" % (key, index, len(items) - 1))
                for item in items[1:]:
                    data = {}
                    data["docid"] = item.get('文书ID')
                    data["CASE_TYPE"] = item.get('案件类型', '')
                    data["CASE_TIME"] = item.get('裁判日期', '')
                    data["CASE_NAME"] = item.get('案件名称', '')
                    data["CASE_NUM"] = item.get('案号', '')
                    data["COURT_NAME"] = item.get('法院名称', '')
                    data['runeval'] = run_eval
                    hr = HandleRedis(1)
                    table = "ZHIXING_DATA"
                    hr.cache_dict_redis(table, data)
                index += 1
                if len(items) - 1 < 10:
                    break
            except Exception as e:
                log.error.info('请求数据出现{}'.format(e))
                a += 1
                if a == 3:
                    # log.error.info('请求数据出现{}'.format(e))
                    break
    else:
        log.crawler.info('TB_WENSHU_ZHIXING遍历完毕.....')


def start_save_zhixing(**kwargs):
    data = r.get_data_redis("ZHIXING_DATA")
    if data:
        kwargs = dict(module="zhixing_detail", data=ast.literal_eval(data))
        start(**kwargs)
    else:
        log.crawler.info('ZHIXING_DATA遍历完毕.....')


def start_peichang(**kwargs):
    index = 1
    key = r.get_data_redis("TB_WENSHU_PEICHANG")
    if key:
        a = 0
        while True:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="peichang_list", data=dict(index=index, key=key))
                items = get_item(kwargs)
                if items:
                    run_eval = items[0]['RunEval']
                else:
                    break
                if len(items) == 1:
                    break
                log.crawler.info("获取%s第%d页的文件ID长度为:%d" % (key, index, len(items) - 1))
                for item in items[1:]:
                    data = {}
                    data["docid"] = item.get('文书ID')
                    data["CASE_TYPE"] = item.get('案件类型', '')
                    data["CASE_TIME"] = item.get('裁判日期', '')
                    data["CASE_NAME"] = item.get('案件名称', '')
                    data["CASE_NUM"] = item.get('案号', '')
                    data["COURT_NAME"] = item.get('法院名称', '')
                    data['runeval'] = run_eval
                    hr = HandleRedis(1)
                    table = "PEICHANG_DATA"
                    hr.cache_dict_redis(table, data)
                index += 1
                if len(items) - 1 < 10:
                    break
            except Exception as e:
                log.error.info('请求数据出现{}'.format(e))
                a += 1
                if a == 3:
                    # log.error.info('请求数据出现{}'.format(e))
                    break
    else:
        log.crawler.info('TB_WENSHU_PEICHANG遍历完毕.....')


def start_save_peichang(**kwargs):
    data = r.get_data_redis("PEICHANG_DATA")
    if data:
        kwargs = dict(module="peichang_detail", data=ast.literal_eval(data))
        start(**kwargs)
    else:
        log.crawler.info('PEICHANG_DATA遍历完毕.....')


if __name__ == '__main__':
    start_minshi()
    # start_save_minshi()
    # start_xingshi()
    # start_save_xingshi()
    # start_xingzheng()
    # start_save_xingzheng()
    # start_zhixing()
    # start_save_zhixing()
    # start_peichang()
    # start_save_peichang()
