#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from PublicSpider.common import getmd5
from db.basic_db import DbHandle

db = DbHandle()


def startupdatedb():
    id = 1
    while id < 135710:
        print("start find db num is:%d" % id)
        sql = "select id,case_no,org_code from tb_xzcf where id={id}".format(id=id)
        datas = db.find_data_from_db(sql=sql)
        if datas:
            hashstr = ''
            data = datas[0]
            id, case_no, org_code = data
            hashstr = str(id) + case_no + org_code
            hashvalue = getmd5(hashstr)
            usql = "update tb_xzcf set hash='{hashvalue}' where id={id}".format(hashvalue=hashvalue, id=id)
            print(usql)
            r = db.insert_db_func(sql=usql)
            if r:
                id += 1
                print("update tb tb_xzcf success......")
        else:
            id += 1
            continue
