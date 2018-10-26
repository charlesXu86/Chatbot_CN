# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     pre_load.py
   Description :   预加载
   Author :       charl
   date：          2018/10/26
-------------------------------------------------
   Change Activity: 2018/10/26:
-------------------------------------------------
"""
import thulac
import csv
import sys
import os
sys.path.append("..")

from Chatbot_KG.util.neo_models import Neo4j
from Chatbot_KG.util.mongo_model import Mongo
from Chatbot_KG.toolkit.vec_API import word_vector_model
from Chatbot_KG.toolkit.tree_API import TREE
	
pre_load_thu = thulac.thulac()  #默认模式
print('thulac open!')

neo_con = Neo4j()   #预加载neo4j
neo_con.connectDB()
print('neo4j connected!')

predict_labels = {}   # 预加载实体到标注的映射字典
filePath = os.getcwd()
with open(filePath+'/toolkit/predict_labels.txt','r',encoding="utf-8") as csvfile:
	reader = csv.reader(csvfile, delimiter=' ')
	for row in reader:
		predict_labels[str(row[0])] = int(row[1])
print('predicted labels load over!')

# 读取word vector
wv_model = word_vector_model()
#wv_model.read_vec('toolkit/vector_5.txt') # 测试用，节约读取时间
#wv_model.read_vec('toolkit/vector.txt')

wv_model.read_vec(filePath+'/toolkit/vector_15.txt') # 降到15维了	   

# 读取农业层次树
tree = TREE()
tree.read_edge(filePath+'/toolkit/micropedia_tree.txt')
tree.read_leaf(filePath+'/toolkit/leaf_list.txt')
		
print('level tree load over~~~')

		
# 预加载mongodb
mongo = Mongo()
mongo.makeConnection()
print("mongodb connected")
#连接数据库
mongodb = mongo.getDatabase("agricultureKnowledgeGraph")
print("connect to agricultureKnowledgeGraph")
# 得到collection
collection = mongo.getCollection("train_data")
print("get connection train_data")

testDataCollection = mongo.getCollection("test_data")
print("get connection test_data")