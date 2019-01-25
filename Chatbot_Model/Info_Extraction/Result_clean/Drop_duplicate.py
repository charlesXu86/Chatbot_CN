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
    df = df.drop_duplicates(subset=['item1'], keep='first', inplace=False)
    df.to_csv('D:\ZhizhuxiaItem\\guizhou\\Ner_relation_guizhou2.csv')
    print(df)

def drop_speci_data(file):
    '''
    删除含有特定字符的行
    :param file:
    :return:
    '''

    pass

def drop_na(file):
    '''

    :param file:
    :return:
    '''
    df = pd.read_csv(file, header=None, quoting=3, encoding='utf-8', error_bad_lines=False)
    df = df.dropna(subset=['item1'])
    df.to_csv('D:\ZhizhuxiaItem\\guizhou\\Ner_relation_guizhouNA.csv')




if __name__ == '__main__':
    data_path = 'D:\ZhizhuxiaItem\\guizhou\\Ner_relation_guizhou.csv'
    # drop_duplicate_data(data_path)
    drop_na(data_path)
