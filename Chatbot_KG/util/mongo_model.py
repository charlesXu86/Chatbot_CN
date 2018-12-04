#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: mongo_model.py
@desc: 连接mongoDB
@time: 2018/08/08
"""

import pprint
from pymongo import MongoClient

uri = 'mongodb://' + 'wusong' + ':' + 'wusong' + '@' + '10.0.0.8' + ':' + '27017' +'/'+ 'wusong'
client = MongoClient(uri)

class Mongo():
	clent = None
	db = None
	collection = None
	uri = 'mongodb://' + 'root' + ':' + '123456' + '@' + '47.96.15.176' + ':' + '27017' +'/'+ 'itslaw'
	def makeConnection(self):
		self.client = MongoClient('localhost',27017)
		# self.client = MongoClient(uri)

	def getDatabase(self,dbName):
		self.db = self.client[dbName]
		return self.db

	def getCollection(self,collectionName):
		self.collection = self.db[collectionName]
		return self.collection

def find_MONGO_one(ids):
	'''
	查询一条数据
	:param ids:
	:return:
	'''
	db = client.wusong
	collection = db.itslaw_collection
	datas = collection.find_one({'judgementId':ids})
	pprint.pprint(datas)

judgementId = 'cc37da75-3655-4155-9221-27bcae5bc393'
find_MONGO_one(judgementId)


