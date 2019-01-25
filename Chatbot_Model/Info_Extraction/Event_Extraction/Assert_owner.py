# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Assert_owner.py
   Description :  资产所有者提取   正则 + 深度学习
   Author :       charl
   date：          2018/10/17
-------------------------------------------------
   Change Activity: 2018/10/17:
-------------------------------------------------
"""

import re

from Entity_Extraction.utils import get_entity

def get_assert_owner(judge_res):
    addr = ''
    match_addr3 = re.search(r'(名下位于)', judge_res)
    pass

def judge_owner():
    LOC = get_entity()
    pass
