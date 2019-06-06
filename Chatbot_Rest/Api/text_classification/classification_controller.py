#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: classification_controller.py 
@desc: 文本分类接口(deep learning)
@time: 2019/05/23 
"""

import json

from django.http import HttpResponse, JsonResponse
from time import gmtime, strftime

from Chatbot_Model.Text_Classification.Fasttext.predict import Predict
from Chatbot_Model.Text_Classification.Fasttext import parameters




def text_classification_server_fc(request):
    '''
    意象度分类接口（深度学习）
    :param request: 前端传来的msg
    :return: 返回label对应的分类
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData["msg"]

        fc = Predict()
        res = fc.fc_predicts(msg)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return JsonResponse({
            "desc": "Success",
            "ques": msg,
            "res": res,
            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)
