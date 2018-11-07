# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     semantic_retrieval_views.py
   Description :   语义检索视图跳转
   Author :       charl
   date：          2018/11/7
-------------------------------------------------
   Change Activity: 2018/11/7:
-------------------------------------------------
"""

from django.shortcuts import render

def semantic_retrieval_view(request):
    return render(request, "retrieval/semantic_retrieval.html", {})


