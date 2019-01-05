#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/15 14:50
@Author  : wangjh
@File    : peichang_detail.py
@desc    : PyCharm
"""
import os
import random
import sys
import time



cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import platform
import socket
import os
import re
from util import log
from wenshu.doc_decrypt import doc_id_decyrpt
from PublicSpider.common import getmd5
from model.handle_redis import HandleRedis
from util.re_req import re_request
from PublicSpider.get_content_static import get_html
from wenshu.get_docid import doc_id
from util.headers import my_headers
hr = HandleRedis(7)
pl = platform.system()


def get_detail_info(**kwargs):
    run_eval = kwargs.get("runeval")
    doc_id_src = kwargs.get("docid")
    result = doc_id_decyrpt(run_eval, doc_id_src)
    # result = doc_id(run_eval, doc_id_src)
    # log.crawler.info("密钥为：%s" % result)
    url_doc = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=' + result
    item = {"data_source": "http://wenshu.court.gov.cn/"}
    item["CASE_NAME"] = kwargs.get("CASE_NAME", "")
    item["CASE_TIME"] = kwargs.get("CASE_TIME", "")
    item["CASE_TYPE"] = kwargs.get("CASE_TYPE", "")
    item["CASE_NUM"] = kwargs.get("CASE_NUM", "")
    item["COURT_NAME"] = kwargs.get("COURT_NAME", "")
    hashstr = item["CASE_NAME"] + item["CASE_TIME"]
    hashvalue = getmd5(hashstr)
    item["hash"] = hashvalue
    if pl == "Windows":
        filedir = "D:\\workplace\\wenshu_peichang"
    else:
        filedir = "/data/wenshu_peichang"
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    item["IP"] = myaddr
    file = hashvalue + ".html"
    file_name = os.path.join(filedir, file)
    item["DOC_DIR"] = file_name
    # i = 0
    # while i < 10:
    for _ in range(1000):
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
            'Cookie': None,
            # 'Accept': 'text/javascript, application/javascript, */*',
            # 'User-Agent': random.choice(my_headers),
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'X-Requested-With': 'XMLHttpRequest',
            # 'Host': 'wenshu.court.gov.cn',
            # 'Referer': 'http://wenshu.court.gov.cn/content/content?DocID={}&KeyWord='.format(result)
        }
        resp = re_request(url=url_doc, headers=headers)
        resp.encoding = resp.apparent_encoding
        a = resp.text
        # a = get_html(method='get', url=url_doc)
        text1 = re.findall(r'\\"Html\\":\\"(.*?)\\"}";', a)
        if len(text1) > 0:
            t2 = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
            %s
            </body>
            </html>
            """
            a = t2 % text1[0]
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(a)
            log.crawler.info('数据保存成功......')
            table = "TB_WENSHU_PEICHANG"
            hr.cache_dict_redis(table, item)
            return



def main(**kwargs):
    result = get_detail_info(**kwargs)
    return result


if __name__ == '__main__':
    data = []
    run_eval = data[0]['RunEval']
    for i in range(1, len(data)):
        id = data[i]['文书ID']
        get_detail_info(runeval=run_eval, docid=id)
        break
