#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import os
import sys
from datetime import date, timedelta

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from util import log
from control_spider import start
from model.handle_redis import HandleRedis
from wenshu_updata.doc_decrypt import get_aes_key
r = HandleRedis(1)
def nowt_time():
    today = (date.today()).strftime("%Y-%m-%d")
    yesterday1 = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%d")
    key = (today, yesterday1)
    return str(key)
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
    key = r.get_data_redis("day_time3")
    if key:
        while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="minshi_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "MINSHI_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
    else:
        log.crawler.info('day_time3遍历完毕.....')
def start_xingshi(**kwargs):
    index = 1
    key = r.get_data_redis("day_time4")
    if key:
        while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="xingshi_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "XINGSHI_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
    else:
        log.crawler.info('day_time4遍历完毕.....')
def start_xingzheng(**kwargs):
    index = 1
    key = r.get_data_redis("day_time5")
    if key:
        while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="xingzheng_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "XINGZHENG_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
    else:
        log.crawler.info('day_time5遍历完毕.....')
def start_peichang(**kwargs):
    index = 1
    key = r.get_data_redis("day_time")
    if key:
        while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="peichang_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "PEICHANG_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
    else:
        log.crawler.info('day_time遍历完毕.....')
def start_zhixing(**kwargs):
    index = 1
    key = r.get_data_redis("day_time2")
    if key:
        while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="zhixing_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "ZHIXING_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
    else:
        log.crawler.info('day_time2遍历完毕.....')

def start_up_minshi(**kwargs):
    index = 1
    key = nowt_time()
    while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="minshi_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "MINSHI_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
def start_up_xingshi(**kwargs):
    index = 1
    key = nowt_time()
    while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="xingshi_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "XINGSHI_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
def start_up_xingzheng(**kwargs):
    index = 1
    key = nowt_time()
    while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="xingzheng_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "XINGZHENG_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
def start_up_peichang(**kwargs):
    index = 1
    key = nowt_time()
    while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="peichang_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "PEICHANG_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
def start_up_zhixing(**kwargs):
    index = 1
    key = nowt_time()
    while index < 101:
            try:
                log.crawler.info("*" * 80)
                log.crawler.info("start crawler %s page is:%d" % (key, index))
                kwargs = dict(module="zhixing_up_list", data=dict(index=index, key=ast.literal_eval(key)))
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
                    data["docid"] = item["文书ID"]
                    data["CASE_TYPE"] = item["案件类型"]
                    data["CASE_TIME"] = item["裁判日期"]
                    data["CASE_NAME"] = item["案件名称"]
                    data["CASE_NUM"] = item["案号"]
                    data["COURT_NAME"] = item["法院名称"]
                    data['runeval'] = run_eval
                    table = "ZHIXING_DATA"
                    r.cache_dict_redis(table, data)
                index += 1
            except Exception as e:
                log.error.info('请求list出现：{}'.format(e))
if __name__ == '__main__':
    start_minshi()
    #start_xingshi()
    #start_xingzheng()
    #start_peichang()
    #start_zhixing()
    # start_up_minshi()
    # start_up_xingshi()
    # start_up_xingzheng()
    # start_up_peichang()
    # start_up_zhixing()
