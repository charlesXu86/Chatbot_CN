# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     gaode_py.py
   Description :   利用高德地图web服务api实现地理/逆地址编码
   Author :       charl
   date：          2018/9/6
-------------------------------------------------
   Change Activity: 2018/9/6:
-------------------------------------------------
"""

import requests


def geocode(address):
    parameters = {'address': address, 'key': '85d3ed3aceaf0a259f81d5ae47a32e59'}
    # 这个参数为地址解析
    base1 = 'http://restapi.amap.com/v3/geocode/geo'

    # 关键字搜索
    # base2 = 'http://restapi.amap.com/v3/place/'
    response = requests.get(base1, parameters)
    answer = response.json()
    print(address + "的经纬度：\n", answer['geocodes'][0]['location'])

if __name__=='__main__':
    address = input('请输入地址：')
    geocode(address)