#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: time_convert_server.py 
@desc: 时间转换器接口
@time: 2019/05/24 
"""

import json

from django.http import HttpResponse, JsonResponse
from time import gmtime, strftime
from Chatbot_Model.Time_Convert.TimeNormalizer import TimeNormalizer

def time_convert(request):
    '''
    时间转换API
    :param request:
    :return:
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData["msg"]

        tn = TimeNormalizer()
        res = tn.parse(msg)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return JsonResponse({
            "desc": "Success",
            "ques": msg,
            "res": res,
            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)
