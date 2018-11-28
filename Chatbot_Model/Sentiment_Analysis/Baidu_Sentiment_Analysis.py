# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Baidu_Sentiment_Analysis.py
   Description :  调用百度接口的情感倾向分析
   Author :       charl
   date：          2018/11/28
-------------------------------------------------
   Change Activity: 2018/11/28:
-------------------------------------------------
"""

from Chatbot_Model.utils import Baidu_Aip_conf
import pprint


def get_Sentiment_analysis(text):
    '''
    输出 sentiment: 0 : 负， 1：中性， 2：正向
        confidence
    :param text:
    :return:
    '''
    res = Baidu_Aip_conf.client.sentimentClassify(text)
    pprint.pprint(res)


text1 = "我这款华为手机非常好用。"
text2 = "这个苹果手机真垃圾"
get_Sentiment_analysis(text2)