# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     ESToCSV.py
   Description :  从es中导出数据到csv
   Author :       charl
   date：          2018/12/12
-------------------------------------------------
   Change Activity: 2018/12/12:
-------------------------------------------------
"""

from elasticsearch import Elasticsearch
from elasticsearch import helpers
def getData():
    es = Elasticsearch(["192.168.11.211:9200"])
    query = {
        "query":{"match_all":{}}
    }
    scanResp = helpers.scan(client=es,
                            query=query,
                            scroll="3m",
                            index='zhizhuxia',
                            doc_type='ner_type',
                            timeout="3m")
    for k in scanResp:
        yield k

def write_file_detail(k):
    '''
    这个方法写入图数据库要求的详情表
    :param k:
    :return:
    '''
    with open('D:\project\Chatbot_CN\\Ner_detail.csv', 'ab') as f:
        k = dict(k)
        f.write(k['_source']['judgementId'].encode(encoding="utf-8")) # 写入Id
        f.write(b',')
        f.write(k['_source']['opponents'].encode(encoding="utf-8"))  # 写入被告
        f.write(b',')
        f.write(k['_source']['court'].encode(encoding="utf-8"))
        f.write(b',')
        keywords = k['_source']['keywords']
        keyw = '、'.join(keywords)
        if keyw is not '':
            f.write(keyw.encode(encoding="utf-8"))
        f.write(b',')

        text = k['_source']['judge_text']
        f.write(text.encode(encoding="utf-8"))
        f.write(b',')
        f.write(b'\n')
        f.flush()

def write_file_attr(k):
    '''
    写入图数据库要求的属性
    :param k:
    :return:
    '''

def write_file_relation(k):
    '''
    写入图数据库需要的关系
    :param k:
    :return:
    '''
    with open('D:\project\Chatbot_CN\\Ner_relation.csv', 'ab') as f:
        k = dict(k)
        f.write(k['_source']['opponents'].encode(encoding="utf-8"))  # 写入被告
        f.write(b',')

        f.write('has'.encode(encoding="utf-8"))
        f.write(b',')

        loc = k['_source']['LOC']
        loc = '、'.join(loc)
        f.write(loc.encode(encoding="utf-8"))
        f.write(b',')
        f.write(b'\n')
        f.flush()


def write_file_node(k):
    '''
    写入图数据库的节点表 （测试成功）
    :param k:
    :return:
    '''
    with open('D:\project\Chatbot_CN\\Ner_node.csv', 'ab') as f:
        k = dict(k)
        opp = k['_source']['opponents']
        f.write(opp.encode(encoding="utf-8"))  # 写入被告
        # for i in range(len(opp)):
        #     f.write(opp[i].encode(encoding="utf-8"))
        #     f.write(b'\n')
        # print(opp)
        f.write(b'\n')
        loc = k['_source']['LOC']  # 写入地址
        if len(loc) == 0:
            pass
        if len(loc) >= 1:
            for i in range(len(loc)):
                f.write(loc[i].encode(encoding="utf-8"))
                f.write(b'\n')
        print(loc)
        f.flush()



if __name__=='__main__':
    datas = getData()
    for index, k in enumerate(datas, 1):
        # write_file_detail(k)
        write_file_relation(k)
        # write_file_node(k)
        print('正在导出' + str(index) + '条数据')