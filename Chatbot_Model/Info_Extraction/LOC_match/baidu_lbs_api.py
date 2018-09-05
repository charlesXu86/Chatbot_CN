#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: util.py
@desc: 百度地图调用工具类
@time: 2018/08/08
"""

import hashlib
import json
import os
from urllib import parse

from util import Utils


class LbsApi:

    def __init__(self):
        self.__ak = 'e8IGpl0CaVuGCBCLPdW9U1rIffWfBezi'
        # SK
        self.__sk = 'YN98qF06L4VqG7PmSpudEcTqZ63EDEEL'
        self.__REGION = '南京'

    # 根据关键字检索匹配地点
    def get_place(self, query, region,tag):
        queryStr = '/place/v2/search?query=%s&region=%s&tag=%s&city_limit=true&output=json&scope=1&ak=%s' % (
            query, region,tag, self.__ak)
        encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
        rawStr = encodedStr + self.__sk
        # 计算sn
        sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
        url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
        return url

    def __get_place(self, region, station,tag, path):
        res = Utils.http_url(self.get_place(station, region,tag))
        data = json.loads(res.decode())
        if 'results' in data and len(data['results']) > 0:
            print(station + '|' + str(len(data['results'])))
            Utils.write_csv('statistics.csv', [station, str(len(data['results']))], 'a+')
            if not os.path.exists(path):
                os.mkdir(path)
            Utils.write_file(path + '/' + station + '.txt', json.dumps(data['results'], ensure_ascii=False, indent=4),
                             'a+')
        else:
            Utils.write_csv('no_place_' + path + '.csv', [station], 'a+')

    def get_bus_place(self, station):
        self.__get_place(self.__REGION, station,'长途汽车站,公交车站', 'bus')

    def get_railway_place(self, station):
        self.__get_place(self.__REGION, station,'火车站', 'railway')


if __name__ == '__main__':
    api = LbsApi()

    # bus_config = 'config/busStationNoGroup.txt'
    # stations = Utils.get_txt_config(bus_config)
    # Utils.async_task(api.get_bus_place, stations)

    railway_config = '../config/trainStationNoGroup.txt'
    stations = Utils.get_txt_config(railway_config)
    Utils.async_task(api.get_railway_place, stations)
    # 合并文件
