# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     dialogue_view.py
   Description :   人机对话页面视图
   Author :       charl
   date：          2019/1/25
-------------------------------------------------
   Change Activity: 2019/1/25:
-------------------------------------------------
"""

from django.shortcuts import render

def dialogue_page(request):
    context = {}
    return render(request, 'dialogue.html', context)