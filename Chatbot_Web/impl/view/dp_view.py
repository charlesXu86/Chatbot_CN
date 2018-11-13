# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     dp_view.py
   Description :  句法分析视图
   Author :       charl
   date：          2018/11/2
-------------------------------------------------
   Change Activity: 2018/11/2:
-------------------------------------------------
"""

from django.shortcuts import render

def dp_page(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'dependency_parsing/dependency_parsing.html', context)