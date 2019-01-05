#!/usr/bin/env python
# encoding: utf-8

import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import platform
import pymysql
from util import log

pl = platform.system()


class DbHandle(object):
    '''数据库操作类'''

    def __init__(self):
        '''初始化数据库连接'''
        self.__db_port = 3306
        if pl == "Windows":
            self.__db_host = 'localhost'
            self.__db_user = 'root'
            self.__db_passwd = 'root'

        else:
            self.__db_host = 'localhost'
            self.__db_user = 'root'
            self.__db_passwd = 'root'
        self.__db_name = 'tax'
        self.__conn = None  # 数据库连接
        self.__cur = None  # 操作游标

        self.__conn = pymysql.connect(host=self.__db_host, user=self.__db_user,
                                      passwd=self.__db_passwd, db=self.__db_name,
                                      port=self.__db_port, charset='utf8')
        self.__cur = self.__conn.cursor()

    def __db_connect(self):
        '''连接数据库'''
        try:
            self.__conn = pymysql.connect(host=self.__db_host, user=self.__db_user,
                                          passwd=self.__db_passwd, db=self.__db_name,
                                          port=self.__db_port, charset='utf8')
            self.__cur = self.__conn.cursor()
        except Exception as e:
            raise e

    def __db_close(self):
        '''关闭数据库'''
        try:
            self.__cur.close()
            self.__conn.close()
        except Exception as e:
            raise e

    def db_conn_close(func):
        def wrapper(self, **kwargs):
            # 创建数据库连接
            self.__db_connect()
            r = func(self, **kwargs)
            # 关闭数据库连接
            self.__db_close()
            return r

        return wrapper

    def insert_db_func(self, **kwargs):
        sql = kwargs.get("sql")
        try:
            self.__cur.execute(sql)
            self.__conn.commit()
            log.crawler.info("insert db success")
        except Exception as err:
            # log.detail.info(sql)
            log.error.info(err)
            self.__conn.rollback()

    @db_conn_close
    def get_table_fields(self, **kwargs):
        fields = []
        table_name = kwargs.get('tname')
        self.__cur.execute('desc {}'.format(table_name))
        results = self.__cur.fetchall()
        for r in results:
            fields.append(r[0])
        return fields

    @db_conn_close
    def find_data_from_db(self, **kwargs):
        sql = kwargs.get("sql")
        try:
            self.__cur.execute(sql)
            data = self.__cur.fetchall()
            return data
        except Exception as err:
            raise err


if __name__ == '__main__':
    db = DbHandle()
    tname = "tb_qsgg"
    print(db.get_table_fields(tname=tname))
