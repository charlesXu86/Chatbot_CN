#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: intent_detection_view.py 
@desc: 意图识别页面跳转
@time: 2019/05/07 
"""

from django.shortcuts import render

def intent_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'dialogue/intent_detection.html', context)


# def intent_detects(request):
#     '''
#     意图识别
#     :param request: 接受前台的query
#     :return:
#     '''
#     ctx = {}
#     if request.POST:
#         query = request.POST['query_text']
#
#     return render(request, "dialogue/intent_detection.html")
