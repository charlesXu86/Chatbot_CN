#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: util.py
@desc: 百度地图调用工具类
@time: 2018/08/08
"""

import csv
import time
import urllib.request

from concurrent.futures import ThreadPoolExecutor


class Utils:

    @staticmethod
    def http_url(url):
        req = urllib.request.urlopen(url)
        res = req.read()
        return res

    @staticmethod
    def get_txt_config(path):
        f = open(path, 'r', encoding='utf8')
        line = f.readline()
        data = []
        while line:
            data.append(line.strip())
            line = f.readline()
        f.close()
        return data

    @staticmethod
    def write_file(file_name, data, mode):
        f = open(file_name, mode, encoding='utf8')
        f.write(data)
        f.close()

    @staticmethod
    def write_csv(file_name, row, model='w'):
        with open(file_name, model, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            f.close()

    @staticmethod
    def async_task(callback, params):
        start_time = time.time()
        with ThreadPoolExecutor(4) as executor:
            executor.map(callback, params)
        print('%d second' % (time.time() - start_time))
