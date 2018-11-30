# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Configure.py
   Description :  读取配置信息
   Author :       charl
   date：          2018/11/30
-------------------------------------------------
   Change Activity: 2018/11/30:
-------------------------------------------------
"""

class Configure:
    def __init__(self, conf_file='config.cfg'):
        self.config = {}
        for line in open(conf_file):
            line = line.strip().split()
            if len() < 3:
                continue
            key, value, type = line
            self.config[key] = eval(type + "('" + value + "')")

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, item):
        return self.config