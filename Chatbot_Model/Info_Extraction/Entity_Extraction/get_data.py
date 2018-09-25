#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: get_data.py
@desc: 连接数据库
@time: 2018/08/08
"""

import pymysql
import split_sentence


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
        sql1 = """SELECT doc_result from doc_test limit 10"""

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


# 从数据库获取数据
def get_datas():
    result_list = []
    db = pymysql.Connect("data.npacn.com", "youtong", "duc06LEQpgoP", "sipai")
    # db = pymysql.Connect("localhost", "root", "Aa123456", "zhizhuxia")
    cursor = db.cursor()
    sql = "SELECT doc_result from sm_document"
    # sql = "SELECT doc_result FROM ner_test where id=2"
    # sql = "SELECT doc_result from doc_test where id like '%DE%'"
    # sql = "SELECT doc_content from doc_test where uuid=666"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            demo_sent = result[0]
            text_sent = split_sentence.split_sentence_thr(demo_sent)
            for text in text_sent:
                result_list.append(text)

                to_str = str(text)
                # if text == '' or text.isspace():
                #     print('See you next time!')
                #     break
                # else:
                #     text = list(text.strip())
        # print(result_list)
        return result_list

    except:
        print("Error: unable to fecth data")
    db.close()

def write_data():
    db = pymysql.Connect("localhost", "root", "Aa123456", "zhizhuxia")
    cursor = db.cursor()
    insert_ner_result = ("INSERT INTO doc_result(per, loc, org, re_loc)" "VALUES(%s, %s, %s, %s)")

    cursor.execute(insert_ner_result)

get_datas()

