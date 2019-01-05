#!/usr/bin/env python
# encoding: utf-8
def generate_db_sql(table, item):
    """
    生产单条sql插入语句
    :param table: 表名
    :param item: 数据字典形式
    :return:
    """
    original_sql = "insert into {table_name}({columns}) values {column_values}"
    dbcol = []
    values = []
    for k in item:
        dbcol.append(k)
        values.append(item.get(k, ''))
    sql = original_sql.format(table_name=table, columns=','.join(dbcol), column_values=tuple(values))
    return sql
