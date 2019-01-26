#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: info_extraction_view.py 
@desc:  信息抽取视图跳转
@time: 2019/01/25 
"""

from django.shortcuts import render

def entity_extraction_page(request):  # 知识图谱主页面跳转
    context = {}
    return render(request, 'info_extraction/entity.html', context)


def event_extraction_page(request):  # 知识图谱主页面跳转
    context = {}
    return render(request, 'info_extraction/event.html', context)

def relation_extraction_page(request):  # 知识图谱主页面跳转
    context = {}
    return render(request, 'info_extraction/relation.html', context)