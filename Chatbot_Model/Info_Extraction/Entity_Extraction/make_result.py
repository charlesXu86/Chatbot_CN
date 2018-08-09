# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     make_result
   Description :   生成金额提取的result.csv
   Author :       charl
   date：          2018/8/9
-------------------------------------------------
   Change Activity:
                   2018/8/9:
-------------------------------------------------
"""

import log
from proprecess_money import JIO

try:
    jio = JIO('Chatbot_Data/Info_Extraction/1万篇训练数据集.csv', 'result.csv')
    jio.write_result()
finally:
    log.commit()


