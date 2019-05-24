#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: classification_controller.py 
@desc: 文本分类接口(deep learning)
@time: 2019/05/23 
"""


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import gmtime, strftime

import numpy as np
import base64
import json


def text_classification_server(request):
    '''
    文本分类接口（深度学习）
    :param request: 前端传来的msg
    :return: 返回label对应的分类
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData["msg"]

        # 这里调用深度学习部分
        res = ''
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return JsonResponse({
            "desc": "Success",
            "ques": msg,
            "res": res,

            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)
