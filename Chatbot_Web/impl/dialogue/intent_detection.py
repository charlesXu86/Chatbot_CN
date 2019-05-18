#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: intent_detection.py 
@desc: 意图识别控制器
@time: 2019/05/08 
"""

from django.shortcuts import render
from django.views.decorators import csrf

from Chatbot_Model.Intent_Detection_Slot_Filling.Intent_detection import get_INTENT

def intent_post(request):
    '''
    意图识别数据交互，
    :param request: 接受前台的query
    :return:
    '''
    ctx = {}
    if request.POST:
        query = request.POST['query_text']

        # 在这里对query进行简单处理 => 包括去掉空格，如果需要分词的话进行分词。等等
        query = query.strip()

        # 调用训练好的模型，接收模型返回的结果(json)，再放进包装器返回页面
        intent_result = get_INTENT(query)

        ctx['intent'] = intent_result

    return render(request, "dialogue/intent_detection.html", ctx)

