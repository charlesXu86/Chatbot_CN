#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: get_data.py
@desc: 连接数据库
@time: 2018/08/08
"""

import pymysql


def get_addr():
    conn = pymysql.connect(host='localhost',
                           # host='192.168.11.251',
                           # host='data.npacn.com',
                           port=3306,
                           user='root',
                           password='Aa123456',
                           # password='youtong123',
                           # password='mysql',
                           database='zhizhuxia',
                           # database='sipai_backup',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:

        # sql1 = """SELECT id, doc_assets FROM sm_document_copy WHERE doc_assets not like "%\'name\': None%" limit 100;"""
        sql1 = """SELECT id,obligors,doc_result from sm_document limit 100"""

        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        yield results

def conn():
    conn = pymysql.connect(  # host='localhost',
        # host='192.168.11.251',
        host='data.npacn.com',
        port=3306,
        user='youtong',
        password='duc06LEQpgoP',
        # password='youtong123',
        # password='mysql',
        database='sipai',
        # database='sipai_backup',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构
    return conn

