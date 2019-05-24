#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: urls.py 
@desc: 接口url
@time: 2019/05/10 
"""


# ===============
#
#   apis 下面的路由
#
# ===============

from django.urls import path

from intent_rest_controller import intent_controller
from entity_extraction_controller import entity_ext_controller
from bot_controller import get_chat_msg    # 聊天
from time_convert_server import time_convert  # 时间转换器


urlpatterns = [

    path('entity', entity_ext_controller), # 实体抽取
    path('intent', intent_controller),     # 意图识别
    path('chat', get_chat_msg),            # chatbot接口
    path('time_convert', time_convert)     # 时间转换器
]