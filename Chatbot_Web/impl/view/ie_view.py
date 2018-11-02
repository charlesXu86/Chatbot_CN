# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     ie_view.py
   Description :   信息抽取页面视图跳转
   Author :       charl
   date：          2018/11/2
-------------------------------------------------
   Change Activity: 2018/11/2:
-------------------------------------------------
"""

from django.shortcuts import render

def info_extraction_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'ie/info_extraction.html', context)