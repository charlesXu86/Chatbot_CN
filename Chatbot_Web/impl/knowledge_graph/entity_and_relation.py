# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     entity_and_relation.py
   Description :  实体和关系查询
   Author :       charl
   date：          2018/12/6
-------------------------------------------------
   Change Activity: 2018/12/6:
-------------------------------------------------
"""
import json

from django.shortcuts import render
from Chatbot_KG.toolkit.pre_load import neo_con  # KG模块下的neo4j连接


relationCountDict = {}

filePath = 'D:\project\Chatbot_CN\Chatbot_KG\label_data\\'

with open(filePath + 'relationStaticResult.txt', 'r') as f:
    for line in f:
        relationNameCount = line.split(",")
        relationName = relationNameCount[0][2:-1]
        relationCount = relationNameCount[1][1:-2]
        relationCountDict[relationName] = int(relationCount)

def sortDict(relationDict):
    for i in range(len(relationDict)):
        relationName = relationDict[i]['rel']['type']
        relationCount = relationCountDict.get(relationName)
        if(relationCount is None):
            relationCount = 0
        relationDict[i]['relationCount'] = relationCount

    return relationDict

def search_entity(request):
    '''
     实体查询
    :param request: 接收前台传过来的值
    :return:
    '''
    ctx = {}
    # 根据传入的实体名称搜索出关系
    if (request.GET):
        entity = request.GET['entity_text']
        db = neo_con # 连接neo4j数据库
        entityRelation = db.getEntityRelationbyEntity(entity)
        if len(entityRelation) == 0:
            # 若数据库中没有该实体，则返回数据库中无该实体
            ctx = {'title' : '<h1>数据库中暂未添加该实体</h1>'}
            return render(request, 'knowledge_graph/entity_search.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})
        else:
            # 返回查询结果
            # 将查询结果按照“关系出现次数”的统计结果进行排序
            entityRelation = sortDict(entityRelation)

            return render(request, 'knowledge_graph/entity_search.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})
    return render(request, 'knowledge_graph/entity_search.html', {'ctx': ctx})

def search_relation(request):
    '''
    关系查询
    :param request: 接收前台传入的query
    :return:
    '''
    ctx = {}
    if (request.GET):
        db = neo_con
        entity1 = request.GET['entity1_text'] # 传入的实体1
        relation = request.GET['relation_name_text'] # 传入的实体对的关系
        entity2 = request.GET['entity2_text'] # 传入的实体2
        relation = relation.lower()
        searchResult = {}

        # 若只输入entity1， 则返回与entity1有直接关系的实体和关系
        if(len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0):
            searchResult = db.findRelationByEntity(entity1)
            searchResult = sortDict(searchResult)
            if (len(searchResult) > 0):
                return render(request, 'knowledge_graph/relation_search.html', {'searchResult':json.dumps(searchResult, ensure_ascii=False)})

        # 若只输入entity2， 则返回与entity2有直接关系的实体和关系
        if (len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0):
            searchResult =db.findRelationByEntity2(entity2)
            searchResult = sortDict(searchResult)
            if (len(searchResult) > 0):
                return render(request, 'knowledge_graph/relation_search.html', {'searchResult':json.dumps(searchResult,ensure_ascii=False)})

        # 若输入entity1和relation，则输出与entity1具有relation关系的其他实体
        if (len(entity1) != 0 and len(relation) != 0 and len(entity2) == 0):
            searchResult = db.findOtherEntities(entity1, relation)
            searchResult = sortDict(searchResult)
            if (len(searchResult) > 0):
                return render(request, 'knowledge_graph/relation_search.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 若只输入entity2和relation，则输出与entity2具有relation关系的实体
        if (len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0):
            searchResult = db.findOtherEntities2(entity2, relation)
            searchResult = sortDict(searchResult)
            if (len(searchResult) > 0):
                return render(request, 'knowledge_graph/relation_search.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 若输入entity1和entity2，则输出entity1和entity2之间的关系
        if (len(entity1) != 0 and len(relation) == 0 and len(entity2) != 0):
            searchResult = db.findRelationByEntities(entity1, entity2)
            searchResult = sortDict(searchResult)
            if (len(searchResult) > 0):
                return render(request, 'knowledge_graph/relation_search.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 若输入entity1、entity2和relation，则输出entity1、entity2是否具有相应的关系
        if (len(entity1) != 0 and len(relation) != 0 and len(entity2) != 0):
            print('Input relation is:',relation)
            searchResult = db.findEntityRelation(entity1, relation, entity2)
            searchResult = sortDict(searchResult)
            if (len(searchResult) > 0):
                return render(request, 'knowledge_graph/relation_search.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 全为空, 不做任何操作
        if (len(entity1) == 0 and len(relation) == 0 and len(entity2) == 0):
            pass
        ctx = {'title' : '<h1>暂未找到相应的匹配</h1>'}
        return render(request, 'knowledge_graph/relation_search.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

    return render(request, 'knowledge_graph/relation_search.html', {'ctx': ctx})



