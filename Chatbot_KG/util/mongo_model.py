#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: mongo_model.py
@desc: 连接mongoDB
@time: 2018/08/08
"""


from pymongo import MongoClient

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

