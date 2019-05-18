#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: intent_rest_controller.py
@desc: 意图识别REST接口
@time: 2019/05/10 
"""

import json

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from time import gmtime, strftime

def intent_controller(request):
    '''
    意图识别接口
    :param request:
    :return: 返回json数据
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData['msg']

        res = 'a'    # 这里调用模型返回的结果
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        return JsonResponse({
            "desc" : "Success",
            "ques" : msg,
            "res" : res,
            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)