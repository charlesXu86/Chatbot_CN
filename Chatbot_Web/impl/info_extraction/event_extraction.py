#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: event_extraction.py 
@desc: 事件抽取：
         1、主要利用动态多池化
@time: 2019/01/27 
"""

from django.shortcuts import render

def event_post(request):
    '''
    对前端query进行事件抽取
    :param request:
    :return:
    '''
    ctx = {}
    if request.POST:
        sentence = request.POST['sentence_text']
        sentence = sentence.strip()