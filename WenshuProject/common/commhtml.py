#!/usr/bin/env python
# encoding: utf-8
import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import os
from util import url_requests
from util.headers import headers
from requests.utils import dict_from_cookiejar

current_dir = os.path.dirname(os.path.realpath(__file__))


class baseSpider(object):
    def __init__(self, host):
        """

        :param host: 头文件
        """
        self.headers = headers
        self.headers.update(Host=host)

    def getHtml(self, url, proxies=None, data=None, cookies=None):

        res = url_requests.get(url=url, headers=self.headers, params=data, proxies=proxies, cookies=cookies)
        if res.status_code == 200:
            res.encoding = res.apparent_encoding
            return res.text

    def getbytes(self, url, proxies=None, data=None, cookies=None):
        res = url_requests.get(url=url, headers=self.headers, params=data, proxies=proxies, cookies=cookies)
        res.encoding = res.apparent_encoding
        return res.content

    def postHtml(self, url, data=None, proxies=None):
        res = url_requests.post(url=url, data=data, headers=self.headers, proxies=proxies)
        if res:
            return res.text
        else:
            print("post请求没有获取到数据.......")

    def get_cookeis(self, url):
        res = url_requests.get(url=url, headers=self.headers)
        return dict_from_cookiejar(res.cookies)

    def write_file(self, file, content):
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

    def read_file(self, file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            return content
