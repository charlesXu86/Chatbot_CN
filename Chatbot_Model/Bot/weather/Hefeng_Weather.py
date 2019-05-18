#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Hefeng_Weather.py 
@desc: 调用和风天气api
@time: 2019/05/18 
"""

import os
import urllib
import urllib.request as ur
import json
from datetime import date
from os import path
import sys
import platform
import configparser


heKey = '8a439a7e0e034cdcb4122c918f55e5f3'   #
# heKey = '9dc30f9838b64439805c40d26d727255'
city = "CN101230201"  #上海徐汇天气代码



#返回和风天气数据
def get_city_weather(search_type=1):
    if search_type == 1:
        search = 'weather'
    elif search_type == 0:
        search = 'attractions'
    else:
        return -1
    heAPI = 'https://free-api.heweather.com/v5/'
    global heKey,city
    url_weather = heAPI + 'weather'+'?city='+city+'&key='+heKey
    print(url_weather)
    req = ur.Request(url_weather)
    resp = ur.urlopen(req)
    context = resp.read()
    weather_json = json.loads(context, encoding='utf-8')
    # fp = open("./test.txt", 'w')
    # fp.write(context)
    # fp.close()
    if search_type == 1:
        weather = weather_json["HeWeather5"][0]['daily_forecast'][1]
    else:
        weather = weather_json
    return weather

#获取需要的数据
def get_wat():
    city_weather = get_city_weather()
    a= city_weather['tmp']['max']
    b= city_weather['tmp']['min']
    c= city_weather['cond']['txt_d']
    d= city_weather['cond']['txt_n']
    e= city_weather['date']
    f= city_weather['wind']['dir']
    g= city_weather['wind']['sc']
    h= city_weather['pop']
    return "天气预报  今天是 {}   最高温度{} 最低温度{} 日间天气{} 夜间天气{} {}{} 降水概率百分之{}".format(e,a,b,c,d,f,g,h)

def UsePlatform():
    sysstr = platform.system()
    if(sysstr =="Windows"):
        print ("Call Windows tasks")
    elif(sysstr == "Linux"):
        print ("Call Linux tasks")
    elif(sysstr == "Darwin"):
        print ("Call Mac tasks")
    else:
        print ("Other System tasks")
    print(sysstr)
    return sysstr

def broadcast():
    weather=get_wat()



if __name__ == '__main__':
    broadcast()