# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Baidu_Aip_conf.py
   Description :  百度自然语言处理api调用全局配置
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
token = '24.c78dfdf76c97b7df0163376ee1873a8e.2592000.1545979551.282335-14966163'  # access_token

# 新建一个客户端
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)