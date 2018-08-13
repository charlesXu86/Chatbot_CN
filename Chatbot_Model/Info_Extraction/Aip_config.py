# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Aip_config.py
   Description :   百度NLP接口调用配置文件
   Author :       charl
   date：          2018/8/13
-------------------------------------------------
   Change Activity: 2018/8/13:
-------------------------------------------------
"""

from aip import AipNlp
import pprint

APP_ID = '11669694'   # APp_ID
API_KEY = 'x0zIyYPYQfLAcOcx1DV8Gn8y'
SECRET_KEY = 'SFjtYcbsq8Zps6oKRsg8Q1quzdUTc7BO'


client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

text = "潘桃英2014年5月15号搬进了位于禹州市法院小区1号楼1单元14层1401号的新家"
re = client.lexer(text)
pprint.pprint(re)