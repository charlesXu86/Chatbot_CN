#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: log.py
@desc: 金额提取日志记录
@time: 2018/08/08
"""

from datetime import datetime
import operator

__logs = []
__properties = {}
__new_p = {}
__articles = {}


def d(tag, string):
    __logs.append((datetime.now(), tag, string))
    print(datetime.now(), tag, string)


def a(d_id, pr, v):
    if d_id not in __articles:
        __articles[d_id] = []
    __articles[d_id].append((pr, v))


def p(seg):
    """
    记录一个款项类别
    """
    if seg in __properties:
        __properties[seg] += 1
    else:
        __properties[seg] = 1
    # print('Property:', seg)   # 此处打印金额提取的属性信息

def n(seg):
    """
    记录一个新的款项类别
    """
    if seg in __new_p:
        __new_p[seg] += 1
    else:
        __new_p[seg] = 1


def commit():
    with open('logs.txt', 'w') as w:
        for record in __logs:
            w.write(' '.join(record))

    sorted_pro = sorted(__properties.items(), key=operator.itemgetter(1))
    with open('prop.txt', 'w')as w:
        for (k, v) in sorted_pro:
            w.write("%s %s\n" % (k, v))

    sorted_n_pro = sorted(__new_p.items(), key=operator.itemgetter(1))
    with open('new_prop.txt', 'w')as w:
        for (k, v) in sorted_n_pro:
            w.write("%s %s\n" % (k, v))

    print('write articles:\n')
    with open('articles.txt', 'w') as w:
        for (d, l) in __articles.items():
            w.write('id:%s\n' % d)
            for item in l:
                w.write('%s %s\n' % (item[0], item[1]))
