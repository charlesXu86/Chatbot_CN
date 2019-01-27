#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: relation_extraction.py 
@desc: 关系抽取接口：
          主要采用：1、远程监督
                  2、句法分析
                  3、强化学习
@time: 2019/01/27 
"""

from django.shortcuts import render

def relation_post(request):
    '''
    对前端query进行事件抽取
    :param request:
    :return:
    '''
    ctx = {}
    if request.POST:
        sentence = request.POST['sentence_text']
        sentence = sentence.strip()