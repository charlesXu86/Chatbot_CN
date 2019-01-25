# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     specification_view.py
   Description :  系统说明页面
   Author :       charl
   date：          2019/1/25
-------------------------------------------------
   Change Activity: 2019/1/25:
-------------------------------------------------
"""

from django.shortcuts import render

def specification_page(request):
    context = {}
    return render(request, 'specification.html', context)