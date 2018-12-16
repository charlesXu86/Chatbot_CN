# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     RelationDataProcessing.py
   Description :  实体的关系处理并写入Neo4J
   Author :       charl
   date：          2018/12/12
-------------------------------------------------
   Change Activity: 2018/12/12:
-------------------------------------------------
"""

import json
import re

from py2neo import Node, Relationship, Graph
from Langconv import *

class LoadDatatoNeo4J(object):
    graph = None

    def __init__(self):
        print("start load data ...")

    def connectDB(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="123456")
        print("connect neo4j success!")

    def readData(self):
        count = 0
        with open("new_node.csv", 'w') as fw:
            fw.write("title,lable" + '\n')
        with open("wikidata_relation.csv", "w") as fw:
            fw.write("HudongItem1,relation,HudongItem2" + '\n')
        with open("wikidata_relation2.csv", "w") as fw:
            fw.write("HudongItem,relation,NewNode" + '\n')
        with open("../wikidataRelation/entityRelation.json","r") as fr:
            with open("new_node.csv", 'a') as fwNewNode:
                with open("wikidata_relation.csv", 'a') as fwWikidataRelation:
                    with open("wikidata_relation2.csv", 'a') as fwWikidataRelation2:
                        newNodeList = []
                        for line in fr:
                            print(line)
                            entityRelationJson = json.loads(line)
                            entity1 = entityRelationJson['entity1']
                            entity2 = entityRelationJson['entity2']
                            # 搜索entity1
                            find_entity1_result = self.graph.find_one(
                                property_key = "title",
                                property_value = entity1,
                                label = "NerItem"    # 这里的标签
                            )
                            # 搜索entity2
                            find_entity2_result = self.graph.find_one(
                                property_key = "title",
                                property_value = entity2,
                                label = "NerItem"
                            )
                            count += 1
                            print(count)

                            # 如果entity1不在实体列表中，结束
                            if (find_entity1_result is None):
                                continue

                            # 去掉entityRelationJson['relation']中的逗号和双引号
                            entityRelationList = re.split(",|\"",entityRelationJson['relation'])
                            entityRelation = ""
                            for item in entityRelationList:
                                entityRelation = entityRelation + item

                            # 如果entity2既不在实体列表中，又不在NewNode中，则新建一个节点，该节点的lable为newNode，然后添加关系
                            if (find_entity2_result is None):
                                if (entity2 not in newNodeList):
                                    fwNewNode.write(entity2 + "," + "newNode" + '\n')
                                    newNodeList.append(entity2)
                                fwWikidataRelation2.write(entity1 + "," + entityRelation + "," + entity2 + '\n')
                            # 如果entity2在实体列表中，直接查询关系
                            else:
                                fwWikidataRelation.write(entity1 + "," + entityRelation + "," + entity2 + '\n')


if __name__ == "__main__":
	loadData = LoadDatatoNeo4J()
	loadData.connectDB()
	loadData.readData()