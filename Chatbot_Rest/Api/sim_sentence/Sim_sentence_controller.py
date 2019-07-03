# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Sensitive_word_controller.py
 
@Time    :   2019-06-06 16:22
 
@Desc    :   短文本相似度接口
 
'''

import json
import datetime
import logging

from django.http import JsonResponse
from Chatbot_Model.Question_Pairs_Matching.infer_predict import Infer


logger = logging.getLogger(__name__)

infer = Infer()

def sim_sentence_controller(request):
    '''
    短文本相似度
    :param request:
    :return: 返回json数据
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        # msg = jsonData['msg']
        msgA = jsonData['msg1']
        msgB = jsonData['msg2']

        # infer = Infer()
        res = str(infer.infer(msgA, msgB))

        localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return JsonResponse({
            "desc" : "Success",
            "texts" : jsonData,
            "score" : res,
            "time": localtime,
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)