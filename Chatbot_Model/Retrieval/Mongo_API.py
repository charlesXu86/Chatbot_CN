# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Mongo_API.py
   Description :  MONGO db 数据库操作
   Author :       charl
   date：          2018/11/26
-------------------------------------------------
   Change Activity: 2018/11/26:
-------------------------------------------------
"""
import pymongo
from pymongo import MongoClient


# 从数据库获取数据  mongo
uri = 'mongodb://' + 'root' + ':' + '123456' + '@' + '47.96.15.176' + ':' + '27017' +'/'+ 'itslaw'
client = MongoClient(uri)

def Conn_MONGO():
    '''

    :return:
    '''
    result = {}
    try:
        db = client.itslaw
        collection = db.itslaw_collection
        # datas = collection.find({}, {'caseType': '民事'})
        datas = collection.find()
    except Exception as e:
        print('Mongo error is ', e)
    print(datas)


Conn_MONGO()