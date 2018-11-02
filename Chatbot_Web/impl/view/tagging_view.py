# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     tagging_view.py
   Description :   POS-Tagging页面视图跳转
   Author :       charl
   date：          2018/11/2
-------------------------------------------------
   Change Activity: 2018/11/2:
-------------------------------------------------
"""

from django.shortcuts import render

def tagging_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'tagging/tagging.html', context)