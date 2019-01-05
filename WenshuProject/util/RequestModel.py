#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import os
import platform
import re
from pyquery import PyQuery
from util import url_requests
import requests
from util.headers import headers
from lxml import etree


class baseSpider(object):
    def __init__(self, proxies):
        self.headers = headers
        self.proxies = proxies

    def getHtml(self, url, proxies=None, data=None, cookies=None):
        res = url_requests.get(url=url, headers=self.headers, params=data, proxies=proxies, cookies=cookies)
        res.encoding = res.apparent_encoding
        return res.text

    def postHtml(self, url, data):
        res = url_requests.post(url=url, data=data, headers=self.headers, proxies=self.proxies)
        if res:
            return res.text
        else:
            print("post请求没有获取到数据.......")

    def get_session(self):
        session = requests.Session()
        return session

    def get_response(self, url):
        res = url_requests.get(url=url, headers=self.headers, proxies=self.proxies)
        return res

    def get_meta(self, html):
        p = r'.+charset=(.*)\W*'
        pq = PyQuery(html)
        chaset = None
        metas = pq('head')('meta')
        for meta in metas:
            for key in meta.keys():
                if key == 'content':
                    try:
                        chaset = meta.get('content')
                        chaset = re.match(p, chaset)
                        chaset = chaset.group(1)
                    except:
                        continue
                elif key == "charset":
                    chaset = meta.get('charset')
                if chaset:
                    break

        return chaset

    def getBytes(self, url):
        res = url_requests.get(url=url, headers=self.headers, proxies=self.proxies)
        res.encoding = res.apparent_encoding
        return res.content

    def gettag(self, html, path):
        try:
            tree = etree.HTML(html)
            tag = tree.xpath(path)
            if tag:
                return tag
            else:
                return None
        except Exception as e:
            pass

    def getTree(self, html):
        tree = etree.HTML(html)
        return tree

    def write_file(self, file, content):
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

    def read_file(self, file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            return content

    def getsystem(self):
        pl = platform.system()
        return pl

    def get_FileSize(self, filePath):
        fsize = os.path.getsize(filePath)
        return fsize


if __name__ == '__main__':
    b = baseSpider(proxies=None)
    url = "http://www.baidu.com"
    html = b.getHtml(url)
