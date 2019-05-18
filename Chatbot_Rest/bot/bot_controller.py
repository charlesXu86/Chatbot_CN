#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: bot_controller.py 
@desc: bot对话接口
@time: 2019/05/18 
"""

import json

from django.http import JsonResponse
from time import gmtime, strftime
from Chatbot_Model.Bot import Chatbot as bot


def get_chat_msg(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData["msg"]
        # res = bot.ChatBot.getBot().response(msg)
        res = '您好，我是小笨'
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return JsonResponse({
            "desc": "Success",
            "ques": msg,
            "res": res,
            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)
