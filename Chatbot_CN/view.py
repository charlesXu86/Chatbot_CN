# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     view
   Description :
   Author :       charl
   date：          2018/8/1
-------------------------------------------------
   Change Activity:
                   2018/8/1:
-------------------------------------------------
"""

from django.http import HttpResponse

def hello(request):
    return HttpResponse("您好，欢迎来到聊天机器人开发实战！")