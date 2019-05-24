#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: TimePoint.py
@desc: 时间表达式单元规范化对应的内部类
@time: 2019/05/24
"""


#  * 时间表达式单元规范化对应的内部类,
#  * 对应时间表达式规范化的每个字段，
#  * 六个字段分别是：年-月-日-时-分-秒，
#  * 每个字段初始化为-1
class TimePoint:
    def __init__(self):
        self.tunit = [-1, -1, -1, -1, -1, -1]
