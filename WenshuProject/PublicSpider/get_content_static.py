#!/usr/bin/env python
# encoding: utf-8

import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import random
from util import log
from common.commhtml import baseSpider
from db.basic_db import DbHandle
from urllib.parse import urlparse
from util.ipproxy import get_proxies_from_redis

db = DbHandle()


class PublicSpider(baseSpider):
    def get_request_content(self, **kwargs):
        url = kwargs.get("url")
        method = kwargs.get("method", "get")
        data = kwargs.get("data", None)
        proxies = kwargs.get("proxies", None)
        try:
            if method == "post":
                content = self.postHtml(url=url, data=data, proxies=proxies)
                return content
            elif method == "get":
                content = self.getHtml(url=url, data=data, proxies=proxies)
                return content
        except Exception as e:
            raise e


class HandDb(object):
    original_sql = "insert into {table_name}({columns}) values {column_values}"

    def __init__(self, table):
        self.table = table

    def generate_sql_dict(self, item):
        """
        生产单条sql插入语句
        :param table: 表名
        :param item: 数据字典形式
        :return:
        """
        print(item)
        if self.table == "tb_credit":
            item['credit_level'] = 'A'
        dbcol = []
        values = []
        for k in item:
            dbcol.append(k)
            values.append(item.get(k, ""))
        print(values)
        sql = self.original_sql.format(table_name=self.table, columns=",".join(dbcol), column_values=tuple(values))
        print(sql)
        return sql

    def generate_sql_list(self, data, cols):
        """

        :param data: list
        :param cols: list
        :return:
        """
        if self.table == "tb_credit" and 'credit_level' not in cols:
            cols.append('credit_level')
            data.append("A")
        sql = self.original_sql.format(table_name=self.table, columns=",".join(cols), column_values=tuple(data))
        print(sql)
        return sql


def get_html(**kwargs):
    ip_pool = get_proxies_from_redis()
    num = 3
    while num > 0:
        try:
            proxies = random.choice(ip_pool)
            method = kwargs.get("method", 'get')
            data = kwargs.get("data", None)
            url = kwargs.get("url")
            r = urlparse(url)
            host = r.netloc
            p = PublicSpider(host)
            html = p.get_request_content(method=method, url=url, data=data, proxies=proxies)
            if html:
                return html
        except Exception as err:
            num -= 1
            log.crawler.info("发生连接异常尝试再次连接,第%d次重连" % (3 - num))
            if num == 0:
                raise err


if __name__ == '__main__':
    pass
