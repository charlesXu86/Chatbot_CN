# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   LogUtils2.py
 
@Time    :   2019-06-13 17:51
 
@Desc    :
 
'''

import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    all_log = 'all.log'
    info_log = 'info.log'

    def __init__(self,filename,level='info',when='D',backCount=None,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=self.all_log,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        th.setLevel(logging.DEBUG)
        fh = handlers.TimedRotatingFileHandler(filename=self.info_log, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        fh.setLevel(logging.INFO)
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        fh.setFormatter(format_str)
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
        self.logger.addHandler(fh)


log = Logger(None)
