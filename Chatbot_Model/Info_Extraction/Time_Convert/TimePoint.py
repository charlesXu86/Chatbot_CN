#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/20 15:37
# @Author  : zhm
# @File    : TimePoint.py
# @Software: PyCharm


#  * 时间表达式单元规范化对应的内部类,
#  * 对应时间表达式规范化的每个字段，
#  * 六个字段分别是：年-月-日-时-分-秒，
#  * 每个字段初始化为-1
class TimePoint:
    def __init__(self):
        self.tunit = [-1, -1, -1, -1, -1, -1]
