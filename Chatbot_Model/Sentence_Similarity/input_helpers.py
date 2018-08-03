# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     data_helper
   Description : 数据预处理
   Author :       charl
   date：          2018/8/3
-------------------------------------------------
   Change Activity:
                   2018/8/3:
-------------------------------------------------
"""

import numpy as np
import pickle as pkl

from nltk.tokenize import word_tokenize

def load_set(embed, datapath, embed_dim):
    '''

    :param embed:
    :param datapath:
    :param embed_dim:
    :return:
    '''
    with open(datapath, 'rb') as f:
