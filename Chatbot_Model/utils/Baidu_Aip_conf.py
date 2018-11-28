# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Baidu_Aip_conf.py
   Description :
   Author :       charl
   date：          2018/11/28
-------------------------------------------------
   Change Activity: 2018/11/28:
-------------------------------------------------
"""

from aip import AipNlp


APP_ID = '14966163'   # APp_ID
API_KEY = 'MAgY5KObFySpBmrHddhb17pI'
SECRET_KEY = 'ZXGZOkpsgyyixxZeNrWqUH81KwD4EGTX '

# 新建一个客户端
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)