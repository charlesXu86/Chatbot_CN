#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: entity_extraction_controller.py 
@desc: 实体抽取控制器
@time: 2019/05/15 
"""

import json
import logging
import datetime

from django.http import JsonResponse
# from Chatbot_Model.Info_Extraction.Entity_Extraction.Info_Ext_main import NER_predict
from Chatbot_Rest.Api.util import LogUtils2

logger = logging.getLogger(__name__)

def entity_ext_controller(request):
    '''
    实体抽取接口
    :param request:
    :return:
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        try:
            msg = jsonData["msg"]

            # res = NER_predict(msg)
            res = ''
            localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dic = {
                "desc": "Success",
                "ques": msg,
                "res": res,
                "time": localtime,
            }
            log_res = json.dumps(dic, ensure_ascii=False)
            logger.info(log_res)
            return JsonResponse(dic)
        except Exception as e:
            logger.info(e)
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)


