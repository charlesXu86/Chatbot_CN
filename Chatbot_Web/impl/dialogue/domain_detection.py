#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: intent_detection.py 
@desc: 领域识别控制器
@time: 2019/05/08 
"""

from django.shortcuts import render
from django.views.decorators import csrf

def intent_post(request):
    '''
    意图识别
    :param request: 接受前台的query
    :return:
    '''
    ctx = {}
    if request.POST:
        query = request.POST['query_text']

    return render(request, "dialogue/intent_detection.html")

