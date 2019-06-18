#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: enum.py 
@desc: 状态码枚举
@time: 2019/05/10 
"""

from enum import Enum, unique



@unique
class ErrorCode(Enum):
    # base
    正确 = 0
    参数错误 = 1
    请求方法错误 = 2
    认证错误 = 3