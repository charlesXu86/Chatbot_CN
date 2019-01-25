# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     ES_API.py
   Description :   py连接es
   Author :       charl
   date：          2018/9/4
-------------------------------------------------
   Change Activity: 2018/9/4:
-------------------------------------------------
"""

import sys
import json
import datetime

from datetime import datetime
from elasticsearch import Elasticsearch

# es = Elasticsearch([{'host':'test.npacn.com', 'port':9200, 'username':'admin', 'password': 'u1PJTXyzjVqT'}])
es = Elasticsearch(
    ['test.npacn.com:21180'],  # 192.168.11.251
    http_auth=('admin', 'gXvBgE43&B$8'),
    # ['192.168.11.211'],
    # port=9200,
    timeout= 30,
)
# 创建索引
es.indices.create(index='chatbotsss')

# 插入数据
# es.index(index='chatbot_cn_retrieval', doc_type='Retrieval_type')
# start = datetime.now()
for i in range(1000):
    es.index(index='chatbotsss', doc_type='Retrieval_type', body={'any': '张三是一个好人', 'timestamp': datetime.now()})
# end = datetime.now()
# costtime = (end - start).seconds
# 查询数据 get 和 search 两种方式
# res = es.get(index='zhizhuxia', doc_type='test_type', id='01')
# print(costtime)
# print(res['_source'])

# 删除数据
# es.delete(index='chatbot_cn_retrieval', doc_type='Retrieval_type', id='AWbs4IThcGOxL98BAcTo')

# 搜素所有数据
# es.search(index='chatbot_cn_retrieval', doc_type='Retrieval_type')

# 或者
# body = {"query": {"match_all":{}}}
# es.search(index='chatbot_cn_retrieval', doc_type='Retrieval_type', body=body)

# 删除索引
# es.indices.delete(index='chatbot')

