# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     kg_view.py
   Description :  知识图谱页面跳转
   Author :       charl
   date：          2018/11/28
-------------------------------------------------
   Change Activity: 2018/11/28:
-------------------------------------------------
"""

from django.shortcuts import render

def knowledge_graph_view(request):  # 知识图谱主页面跳转
    context = {}
    return render(request, 'knowledge_graph/knowledge_graph.html', context)

def relation_search_view(request):  # 跳转到关系搜索页面
    context = {}
    return render(request, 'knowledge_graph/relation_search.html', context)

def entity_search_view(request):    # 跳转到实体查询页面
    context = {}
    return render(request, 'knowledge_graph/entity_search.html', context)