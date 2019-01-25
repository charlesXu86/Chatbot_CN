# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     settings_view.py
   Description :  系统设置页面
   Author :       charl
   date：          2019/1/25
-------------------------------------------------
   Change Activity: 2019/1/25:
-------------------------------------------------
"""

from django.shortcuts import render

def settings_page(request):
    context = {}
    return render(request, 'settings.html', context)