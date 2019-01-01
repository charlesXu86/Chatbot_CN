# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Extract.py
   Description :   提取训练和验证样本
   Author :       charlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""
import zipfile

from Config import *
from Utils import ensure_folder


def extract(folder):
    filename = '{}.zip'.format(folder)
    print('Extracting {}...'.format(filename))
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('data')


if __name__ == '__main__':
    ensure_folder('data')

    if not os.path.isdir(train_folder):
        extract(train_folder)

    if not os.path.isdir(valid_folder):
        extract(valid_folder)

    if not os.path.isdir(test_a_folder):
        extract(test_a_folder)

    if not os.path.isdir(test_b_folder):
        extract(test_b_folder)
