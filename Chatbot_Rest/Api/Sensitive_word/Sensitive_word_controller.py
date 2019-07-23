# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Sensitive_word_controller.py
 
@Time    :   2019-06-06 16:22
 
@Desc    :   敏感词检测接口
 
'''

import json

from django.http import JsonResponse
from time import gmtime, strftime

from Chatbot_Model.utils.Sensitive_word_filter import DFAFilter


data = 'Chatbot_CN/Chatbot_Data/Sensitive_word/keywords'
def sensitive_controller(request):
    '''
    敏感词检测
    :param request:
    :return: 返回json数据
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData['msg']

        sw = DFAFilter()
        sw.parse(data)

        res = sw.filter(msg)   # 这里调用模型返回的结果
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        return JsonResponse({
            "desc" : "Success",
            "ques" : msg,
            "res" : res,
            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)