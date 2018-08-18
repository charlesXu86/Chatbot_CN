# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Aip_config.py
   Description :   百度NLP接口调用配置文件
   Author :       charl
   date：          2018/8/13
-------------------------------------------------
   Change Activity: 2018/8/13:
-------------------------------------------------
"""

from aip import AipNlp
import pprint

APP_ID = '11669694'   # APp_ID
API_KEY = 'x0zIyYPYQfLAcOcx1DV8Gn8y'
SECRET_KEY = 'SFjtYcbsq8Zps6oKRsg8Q1quzdUTc7BO'


# client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


text2 = "没收朱万强在2018年3月17日竞买瑞金市象湖镇内环路以西连接323国道西XX号地的房屋第一层店面"
# res = client.lexer(text)
# DATE = re['ne']
# info_more = list(res)[0]
# key = list(res)[0]
# value = list(res.values())[0]
# ne = value['ne']

# pprint.pprint(value)
# print(ne)

# pprint.pprint(DATE)

def get_LOC_DATE(text):
    try:
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        res = client.lexer(text)
        key = list(res)[0]
        value = list(res.values())[0]
        for i in range(len(value)):
            if value[i]['ne'] == "TIME":
                time_items = value[i]['item']
            if value[i]['ne'] == "LOC":
                loc_items = value[i]['item']
    except:
        pass
    return time_items, loc_items

    # print(value)
text = "潘桃英2014年5月15号搬进了位于禹州市法院小区1号楼1单元14层1401号的新家"
value = get_LOC_DATE(text)
pprint.pprint(value)
