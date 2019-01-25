# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     blue.py
   Description :  bleu测试
   Author :       charl
   date：          2019/1/3
-------------------------------------------------
   Change Activity: 2019/1/3:
-------------------------------------------------
"""

from nltk.translate.bleu_score import sentence_bleu
from tqdm import tqdm

def test_bleu(count):
    '''
     Test BLEU
    :param count:
    :return:
    '''
    print('BLEU test mode')
    print('准备数据...')
