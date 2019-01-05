#!/usr/bin/env python
# -*- coding: utf-8 -*-


import platform
import pymysql

pl = platform.system()


class DbHandle(object):
    '''数据库操作类'''

    def __init__(self):
        '''初始化数据库连接'''
        self.__db_port = 3306

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

    @db_conn_close
    def get_data_from_shixin_person(self, **kwargs):
        sql = "select pname from TB_SHIXIN_PERSON"
        try:
            self.__cur.execute(sql)
            data = self.__cur.fetchall()
            return data
        except Exception as err:
            raise err


if __name__ == '__main__':
    f = open("court_shixin_words.txt", "wenshu", encoding="utf-8")
    datas = DbHandle().get_data_from_shixin_person()
    print(len(datas))
    for data in datas:
        words = data[0]
        if len(words) == 2:
            f.write(words + '\n')
        elif len(words) > 2:
            f.write(words[:2] + '\n')
        else:
            pass
