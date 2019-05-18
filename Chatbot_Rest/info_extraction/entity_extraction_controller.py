#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: entity_extraction_controller.py 
@desc: 实体抽取控制器
@time: 2019/05/15 
"""

import json

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from time import gmtime, strftime

def entity_ext_controller(request):
    '''
    实体抽取接口
    :param request:
    :return:
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData['msg']

        res = '中国'
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        return JsonResponse({
            "desc": "Success",
            "query": msg,
            "res": res,
            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)


