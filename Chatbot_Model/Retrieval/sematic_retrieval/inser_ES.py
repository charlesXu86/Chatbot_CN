# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     inser_ES.py
   Description :   将一个知识图谱中的数据导入elastic search,须提前新建index和type
   Author :       charl
   date：          2018/11/7
-------------------------------------------------
   Change Activity: 2018/11/7:
-------------------------------------------------
"""

import sys
import requests
import json

def bulk_insert(base_url, data):
    response = requests.post(base_url, headers={"Content-Type":"application/x-ndjson"}, data=data)

def begin_inset_job(index_name, type_name, json_filepath, bulk_size=1000):
    base_url = "http://192.168.11.251:9200/" + index_name + "/" + type_name + "/bulk"
    f = open(json_filepath)
    cnt, es_id = 0, 1
    data = ""
    for line in f:
        action_meta = '{"index": {"_id":"' + str(es_id) + '"}}'
        data = data + action_meta + "\n" + line

        es_id += 1
        cnt += 1
        if cnt >= bulk_size:
            bulk_insert(base_url, data)
            cnt, data = 0, ""
        if not (es_id % bulk_size):
            print(es_id)
        if cnt:
            bulk_insert(base_url, data)

if __name__ == '__main__':
    data = 'D:\project\Chatbot_CN\Chatbot_Data\Semantic_retrieval_data\Person.json'
    begin_inset_job("chatbot_cn_retrieval", "Retrieval_type", data)
