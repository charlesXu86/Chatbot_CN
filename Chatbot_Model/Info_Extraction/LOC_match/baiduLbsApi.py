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
import urllib.request
from urllib import parse

ak = 'e8IGpl0CaVuGCBCLPdW9U1rIffWfBezi'
# SK
sk = 'YN98qF06L4VqG7PmSpudEcTqZ63EDEEL'


# 正向地理编码服务 参见文档http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
def get_urt(addtress):
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStr = '/geocoder/v2/?address=%s&output=json&ak=%s' % (addtress, ak)
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    rawStr = encodedStr + sk
    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    return url


# 行政区划区域检索 参加文档:http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
def get_region_place(query, region, page_size, page_num):
    # 坐标类型，1（wgs84ll即GPS经纬度），2（gcj02ll即国测局经纬度坐标），3（bd09ll即百度经纬度坐标），4（bd09mc即百度米制坐标）
    coord_type = 3
    # http://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京&output=json&ak=您的ak //GET请求
    queryStr = '/place/v2/search?query=%s&region=%s&city_limit=true&coord_type=%s&output=json&scope=1&ak=%s' \
               '&page_size=%s&page_num=%s' % (query, region, coord_type, ak, page_size, page_num)
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + sk
    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    # print('行政区划区域检索:%s' % url)
    return url


# 圆形区域检索 文档参加行政区域检索
def get_location_place(query, location, radius, page_size, page_num):
    # http://api.map.baidu.com/place/v2/search?query=银行&location=39.915,116.404&radius=2000&output=xml&ak=您的密钥 //GET请求
    queryStr = '/place/v2/search?query=%s&location=%s&radius=%s&output=json&scope=1&ak=%s&page_size=%s&page_num=%s' % (
        query, location, radius, ak, page_size, page_num)
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + sk
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")

    return url


def get_bounds_place(query, loc, page_size, page_num):
    queryStr = '/place/v2/search?query=%s&bounds=%s&output=json&ak=%s&page_size=%s&page_num=%s' % (
        query, loc, ak, page_size, page_num)
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + sk
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")

    return url


def http_url(url):
    req = urllib.request.urlopen(url)
    # res_data = urllib.urlopen(req)
    res = req.read()
    return res


def write_local_file(file_name, data):
    f = open(file_name, 'w', encoding='utf8')
    f.write(data)
    f.close()


def get_full_region_data(query, region):
    # print(http_url(get_urt('金盾饭店')));
    keys = query.split(',')

    for key in keys:
        total_data = []  # 总的数据
        page_num = 0
        page_size = 20

        res = http_url(get_region_place(key, region, page_size, page_num));

        data = json.loads(res.decode())
        prev_total = len(data['results'])  # 前一次数据总量
        total_data.extend(reconstruct_dict(data['results']))

        try:
            while prev_total > 0:
                page_num = page_num + 1
                res = http_url(get_region_place(key, region, page_size, page_num));

                data = json.loads(res.decode())
                prev_total = len(data['results'])
                # print('total:%s,page_num:%s,page_size:%s' % (prev_total, page_num, page_size))

                total_data.extend(reconstruct_dict(data['results']))
                # time.sleep(1)  # 规避方案,因为百度接口的并发访问检测为秒级
        except Exception:
            print('错误:%s' % (data['message']))
        if not os.path.exists(key):
            os.mkdir(key)
        write_local_file(key + '/' + region + '_' + key + '.txt', json.dumps(total_data, ensure_ascii=False, indent=4))


def get_full_bounds_data(query, loc):
    keys = query.split(',')
    total_data = []  # 总的数据

    for key in keys:
        page_num = 0
        page_size = 20

        res = http_url(get_bounds_place(key, loc, page_size, page_num));

        data = json.loads(res.decode())
        prev_total = len(data['results'])  # 前一次数据总量
        total_data.extend(data['results'])

        try:
            while prev_total > 0:
                page_num = page_num + 1
                res = http_url(get_bounds_place(key, loc, page_size, page_num));

                data = json.loads(res.decode())
                prev_total = len(data['results'])
                total_data.extend(data['results'])
                # time.sleep(1)  # 规避方案,因为百度接口的并发访问检测为秒级
        except Exception:
            print('错误:%s' % (data['message']))
    write_local_file(key + '.txt', json.dumps(total_data, ensure_ascii=False, indent=4))


class LocaDiv(object):
    def __init__(self, loc_all):
        self.loc_all = loc_all

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lat_list.append(lat_sw + 0.1 * i)  # 0.05
        lat_list.append(lat_ne)
        return lat_list

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lng_list.append(lng_sw + 0.1 * i)  # 0.1为网格大小，可更改
        lng_list.append(lng_ne)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0, len(l1) - 1):
            for i in range(0 + len(l1) * n, len(l2) + (len(l2)) * n - 1):
                a = ls_com_v[i]
                b = ls_com_v[i + len(l2) + 1]
                ab = a + ',' + b
                ls.append(ab)
        return ls


def next_area(key, data):
    for node in data:
        if 'sub' in node:
            next_area(key, node['sub'])
        else:
            if node['name'] == '请选择':
                continue
            else:
                if not os.path.exists(node['name'] + '_' + key + '.txt'):
                    print(node['name'])
                    get_full_region_data(key, node['name'])


def reconstruct_dict(array_data):
    _array_data = []
    for d in array_data:
        if 'street_id' in d:
            del d['street_id']
        if 'detail' in d:
            del d['detail']
        if 'uid' in d:
            del d['uid']
        _array_data.append(d)
    return _array_data


if __name__ == '__main__':
    #print(http_url(get_urt('一门闸')));
    # key = '公交车站'
    # f = open('config/nj.txt', 'r', encoding='utf8')
    #
    # data = json.loads(f.read())
    # next_area(key, data)
    #
    # f.close()
    get_full_region_data('上海吴淞口站', '上海市')

    # 按矩形区域检索
    # loc = LocaDiv('29.8255, 115.367400, 30.2194, 115.8287')
    # locs_to_use = loc.ls_row()
    #
    # for loc_to_use in locs_to_use:
    #     print(loc_to_use)
    #     get_full_bounds_data('购物',loc_to_use)
