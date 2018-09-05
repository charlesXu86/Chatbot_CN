#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: amap_lbs_api.py
@desc: 百度地图调用工具类
@time: 2018/08/08
"""

import hashlib
import json
import pymysql
from urllib import parse

from util import Utils


class amapApi:

    def __init__(self):
        self.__key = 'de8ace14954ed68f1ac43e2a83aa30de'  # 'e6a367641f945e3769947abb18dfee92';
        self.__ak = 'xFhGfVWGXvytUT6IMAULlLiUaCC0r2Kp'
        # SK
        self.__sk = '1FqrZvwxshXw0qTjhvvHZKlTuv0a5KgX'
        # 打开数据库连接
        self.__conn = pymysql.connect("localhost", "root", "Aa123456", "chatbot_cn")

    # https://restapi.amap.com/v3/place/text?keywords=北京大学&city=beijing&output=xml&offset=20&page=1&key=<用户的key>&extensions=all
    def get_url(self, keywords, city, types):
        if city is None:
            queryStr = '/v3/place/text?keywords=%s&types=%s&output=json&offset=20&page=1&extensions=all' \
                       % (keywords, types)
        else:
            queryStr = '/v3/place/text?keywords=%s&city=%s&types=%s&output=json&offset=20&page=1&extensions=all' \
                       % (keywords, city, types)
        url = parse.quote("https://restapi.amap.com" + queryStr + "&key=" + self.__key, safe="/:=&?#+!$,;'@()*[]")
        return url;

    def get_poi(self, keywords, city, types):
        res = Utils.http_url(self.get_url(keywords, city, types))
        data = json.loads(res.decode())
        print(keywords + '|' + data['count'])
        if data['count'] != '0':
            params = []
            # 打开数据库连接
            db = pymysql.connect("localhost", "root", "Aa123456", "chatbot_cn")
            for poi in data['pois']:
                params.append(
                    [str(poi['id']),
                     str(poi['name']),
                     str(poi['type']),
                     str(poi['typecode']),
                     str(poi['address']),
                     str(poi['location']),
                     str(poi['pcode']),
                     str(poi['pname']),
                     str(poi['citycode']),
                     str(poi['cityname']),
                     str(poi['adcode']),
                     str(poi['adname'])])
            try:
                # 使用cursor()方法获取操作游标
                cursor = db.cursor()
                sql = """INSERT INTO lbs_poi
                            (id,name,type,typecode,address,location,pcode,pname,citycode,cityname,adcode,adname) 
                          VALUES 
                            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                # 执行sql语句
                cursor.executemany(sql, params)
                # 提交到数据库执行
                db.commit()
                cursor.close()
            except Exception as e:
                print(e)
                # 如果发生错误则回滚
                # self.db.rollback()
            # 关闭数据库连接
            db.close()

    def get_railway_poi(self, keyword):
        self.get_poi(keyword, None, '150400|150700');

    def get_geoconv(self, location):
        queryStr = '/geoconv/v1/?coords=%s&from=1&to=5&output=json&ak=%s' % (location, self.__ak)
        encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
        rawStr = encodedStr + self.__sk
        # 计算sn
        sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
        url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")

        data = json.loads(Utils.http_url(url).decode())
        if 'result' in data:
            # print('%s:%s' % ('处理经纬度:', location))
            return data['result'][0]
        return None

    def merge_location(self):
        try:
            # 使用cursor()方法获取操作游标
            cursor = self.__conn.cursor()
            sql = """select id,location from lbs_poi where bd_location is null"""
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            data = []
            for row in results:
                location = self.get_geoconv(row[1])
                data.append(['%s,%s' % (location['x'], location['y']), row[0]])
                print('当前处理进度:%s,更新id=%s' % (len(data), row[0]))
                if len(data) == 1000:
                    self.update_location(data)
                    data = []
            self.update_location(data)
            cursor.close()
        except Exception as e:
            print(e)
        self.__conn.close()

    def update_location(self, rows):

        # 使用cursor()方法获取操作游标
        cursor = self.__conn.cursor()
        # SQL 更新语句
        sql = "UPDATE lbs_poi SET bd_location = %s WHERE id = %s"
        try:
            # 执行SQL语句
            cursor.executemany(sql, rows)
            # 提交到数据库执行
            self.__conn.commit()
            cursor.close()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.__conn.rollback()


if __name__ == '__main__':
    api = amapApi()
    #
    # railway_config = '../config/500.txt'
    # stations = Utils.get_txt_config(railway_config)
    # Utils.async_task(api.get_railway_poi, stations)

    api.merge_location();
