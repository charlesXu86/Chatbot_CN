# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     cws_view.py
   Description :   中文分词视图跳转
   Author :       charl
   date：          2018/11/2
-------------------------------------------------
   Change Activity: 2018/11/2:
-------------------------------------------------
"""

from django.shortcuts import render

def cws_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'cws/cws.html', context)