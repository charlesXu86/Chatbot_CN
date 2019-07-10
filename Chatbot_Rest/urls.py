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

from Chatbot_Rest.Api.intent_detection.intent_rest_controller import intent_controller
from Chatbot_Rest.Api.info_extraction.entity_extraction_controller import entity_ext_controller
from Chatbot_Rest.Api.bot.bot_controller import get_chat_msg    # 聊天
from Chatbot_Rest.Api.time_convert.time_convert_server import time_convert  # 时间转换器

from Chatbot_Rest.Api.Sensitive_word.Sensitive_word_controller import sensitive_controller

from Chatbot_Rest.Api.sim_sentence import Sim_sentence_controller


urlpatterns = [

    path('entity', entity_ext_controller), # 实体抽取
    path('intent', intent_controller),     # 意图识别
    path('chat', get_chat_msg),            # chatbot接口
    path('time', time_convert),     # 时间转换器
    path('sensitive', sensitive_controller),          # 敏感词检测
    path('sim_sentence', Sim_sentence_controller.sim_sentence_controller),   # 短文本相似度
]