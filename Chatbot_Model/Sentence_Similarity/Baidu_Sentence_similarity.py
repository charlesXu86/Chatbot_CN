# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Baidu_Sentence_similarity.py
   Description :  调用百度接口的短文本相似度分析
   Author :       charl
   date：          2018/11/28
-------------------------------------------------
   Change Activity: 2018/11/28:
-------------------------------------------------
"""

from Chatbot_Model.utils import Baidu_Aip_conf

import pprint


def get_Sentence_similarity(text1, text2):
    prob = Baidu_Aip_conf.client.simnet(text1, text2)
    pprint.pprint(prob)

text1 = "你多大了？"
text2 = "你今年几岁？"
get_Sentence_similarity(text1, text2)