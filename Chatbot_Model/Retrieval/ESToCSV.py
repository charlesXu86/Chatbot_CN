# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     ESToCSV.py
   Description :  从es中导出数据到csv，构建知识库
   Author :       charl
   date：          2018/12/12
-------------------------------------------------
   Change Activity: 2018/12/12:
-------------------------------------------------
"""

from elasticsearch import Elasticsearch
from elasticsearch import helpers


def getData():
    '''
    ES连接
    :return:
    '''
    es = Elasticsearch(["192.168.11.211:9200"])
    query = {
        "query":{"match_all":{}}
    }
    scanResp = helpers.scan(client=es,
                            query=query,
                            scroll="3m",
                            index='zhizhuxia_guizhou',
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
        try:
            f.write(k['_source']['judgementId'].encode(encoding="utf-8")) # 写入Id
            f.write(b',')
            opp = k['_source']['opponents']
            if len(opp) == 0:
                pass
            else:
                opps = '、'.join(opp)
                f.write(opps.encode(encoding="utf-8"))  # 写入被告
            f.write(b',')
            f.write(k['_source']['court'].encode(encoding="utf-8"))
            f.write(b',')
            keywords = k['_source']['keywords']
            keyw = '、'.join(keywords)
            if keyw is not '':
                f.write(keyw.encode(encoding="utf-8"))
            f.write(b',')

            money = k['_source']['MON']
            for i in range(len(money)):
                print(money[i])
                mkey = list(money[i].keys())[0]
                mval = list(money[i].values())[0]
                print(mkey, mval)

                f.write(mkey.encode(encoding="utf-8"))
                f.write(mval.encode(encoding="utf-8"))
            f.write(b',')

            text = k['_source']['judge_text']
            f.write(text.encode(encoding="utf-8"))
            f.write(b',')
            f.write(b'\n')
            f.flush()
        except Exception as e:
            print('Error is', e)


def write_file_attr(k):
    '''
    写入图数据库要求的属性
    :param k:
    :return:
    '''
    with open('D:\project\Chatbot_CN\\Ner_attr.csv', 'ab') as f:
        k = dict(k)
        try:
            opp = k['_source']['opponents']
            if len(opp) == 0:
                pass
            else:
                opps = '、'.join(opp)
                f.write(opps.encode(encoding="utf-8"))  # 写入被告
            f.write(b',')
            f.write(k['_source']['judgementId'].encode(encoding="utf-8"))  # 写入Id
            f.write(b',')
            f.write('被告'.encode(encoding="utf-8"))
            f.write(b',')
            f.write(b'\n')

            pro = k['_source']['opponents']
            if len(pro) == 0:
                pass
            else:
                pros = '、'.join(pro)
                f.write(pros.encode(encoding="utf-8"))  # 写入被告
            f.write(b',')
            f.write(k['_source']['judgementId'].encode(encoding="utf-8"))  # 写入Id
            f.write(b',')
            f.write('原告'.encode(encoding="utf-8"))
            f.write(b',')
            f.write(b'\n')
        except Exception as e:
            print('Error is', e)


def write_file_relation(k):
    '''
    写入图数据库需要的关系
    :param k:
    :return:
    '''
    with open('D:\project\Chatbot_CN\\Ner_relation.csv', 'ab') as f:
        k = dict(k)
        try:
            opp = k['_source']['opponents']
            if len(opp) == 0:
                f.write(' '.encode(encoding="utf-8"))
            else:
                opps = '、'.join(opp)
                f.write(opps.encode(encoding="utf-8"))
            f.write(b',')

            f.write('has'.encode(encoding="utf-8"))
            f.write(b',')

            loc = k['_source']['LOC']
            if len(loc) == 0:
                f.write(' '.encode(encoding="utf-8"))
            else:
                loc = '、'.join(loc)
                f.write(loc.encode(encoding="utf-8"))
            f.write(b',')
            f.write(b'\n')
            f.flush()
        except Exception as e:
            print('Error is', e)


def write_file_node(k):
    '''
    写入图数据库的节点表 （测试成功）
    :param k:
    :return:
    '''
    with open('D:\project\Chatbot_CN\\Ner_node.csv', 'ab') as f:
        k = dict(k)
        try:
            opp = k['_source']['opponents']
            if len(opp) == 0:
                pass
            else:
                for i in range(len(opp)):
                    f.write(opp[i].encode(encoding="utf-8"))
                    f.write(b'\n')
            # f.write(b'\n')
            loc = k['_source']['LOC']  # 写入地址
            if len(loc) == 0:
                pass
            else:
                for i in range(len(loc)):
                    f.write(loc[i].encode(encoding="utf-8"))
                    f.write(b'\n')
            print(loc)
            f.flush()
        except Exception as e:
            print('Error is', e)



if __name__=='__main__':
    datas = getData()
    for index, k in enumerate(datas, 1):
        write_file_detail(k)
        write_file_relation(k)
        write_file_node(k)
        write_file_attr(k)
        print('正在导出' + str(index) + '条数据')