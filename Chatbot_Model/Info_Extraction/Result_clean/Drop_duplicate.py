# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Drop_duplicate.py
   Description :   利用pandas去除csv的重复行
   Author :       charlesXu
   date：          2019/1/11
-------------------------------------------------
   Change Activity: 2019/1/11:
-------------------------------------------------
"""

import pandas as pd
import re

def drop_duplicate_data(file):
    '''
    删除csv文件里的重复数据
    :param file:
    :return:
    '''
    df = pd.read_csv(file, header=None, quoting=3, encoding='utf-8', error_bad_lines=False)
    # print(df)
    df = df.drop_duplicates(subset=None, keep='first', inplace=False)
    df.to_csv('D:\ZhizhuxiaItem\\beijing\\Ner_node_beijing2.csv')
    print(df)

def drop_speci_data(file):
    '''
    删除含有特定字符的行
    :param file:
    :return:
    '''

    pass




if __name__ == '__main__':
    data_path = 'D:\ZhizhuxiaItem\\beijing\\Ner_node_beijing.csv'
    drop_duplicate_data(data_path)
