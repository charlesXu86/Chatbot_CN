# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     index_view.py
   Description :   首页预览
   Author :       charl
   date：          2018/11/2
-------------------------------------------------
   Change Activity: 2018/11/2:
-------------------------------------------------
"""

from django.shortcuts import render

def index_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'welcome.html', context)