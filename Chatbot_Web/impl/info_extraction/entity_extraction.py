#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: entity_extraction.py 
@desc: 实体抽取:
        1、目前主要抽取时间(TIM)，地址(LOC)，机构(ORG)，人物(PER)
        2、采用序列标注方法，即不进行分词
        3、模型采用Bilstm + CRF
@time: 2019/01/27 
"""

from django.shortcuts import render


def sentence_post(request):
    '''
    对前端传过来的query进行实体抽取
    :param request: 前端传过来的值
    :return:
    '''
    ctx = {}
    if request.POST:
        sentence = request.POST['sentence_text']
        sentence = sentence.strip()

    return

