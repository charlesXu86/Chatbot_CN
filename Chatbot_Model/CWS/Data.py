#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Data.py 
@desc: 数据处理
@time: 2018/08/18 
"""

import numpy as np

from collections import OrderedDict    # OrderedDict，实现了对字典对象中元素的排序。

class Data(object):
    def __init__(self, path_lookup_table, wordVecLen, path_train_data, path_test_data,
                 flag_random_lookup_table, dic_label, use_bigram_feature, random_seed, flag_toy_data,
                 path_dev_data=None):
        self.rng = np.random.RandomState(random_seed)
        self.dic_c2idx = {}
        self.dic_idx2c = {}
        self.wordVecLen = wordVecLen
        f = open(path_lookup_table, 'r')
        li = f.readline()
        li = li.split()
        n_dict = int(li[0])
        self.n_unigram = n_dict
        v_lt = self.rng.normal(loc=0.0, scale=0.01, size=(n_dict, wordVecLen))
        # lookup_table = np.zeros([n_dict, 25],dtype = np.float32)
        self.unigram_table = np.asarray(v_lt, dtype=np.float32)
        n_dim = int(li[1])