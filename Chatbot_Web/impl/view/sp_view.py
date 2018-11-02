# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     sp_view.py
   Description :   语义分析视图跳转
   Author :       charl
   date：          2018/11/2
-------------------------------------------------
   Change Activity: 2018/11/2:
-------------------------------------------------
"""

from django.shortcuts import render

def sp_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'semantic_parsing/semantic_parsing.html', context)