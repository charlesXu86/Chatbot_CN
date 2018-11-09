# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     welcome_view.py
   Description :   欢迎页视图跳转
   Author :       charl
   date：          2018/11/9
-------------------------------------------------
   Change Activity: 2018/11/9:
-------------------------------------------------
"""

from django.shortcuts import render

def welcome_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'index.html', context)