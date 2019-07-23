# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   bilstm_crf.py
 
@Time    :   2019-07-09 18:25
 
@Desc    :
 
'''

import tensorflow as tf
import os


class BiLSTM_CRF(object):

    def __init__(self, embedded_chars, hidden_unit, cell_type, num_layers, dropout_rate, initializers,
                 num_labels, max_seq_length, labels, lengths, is_training):
        '''

        :param embedded_chars:
        :param hidden_unit: LSTM的隐藏单元个数
        :param cell_type: RNN类型（LSTM OR GRU DICNN will be add in feature）
        :param num_layers: RNN的层数
        :param dropout_rate:
        :param initializers:
        :param num_labels:  标签数量
        :param max_seq_length: 序列最大长度
        :param labels: 真实标签
        :param lengths: [batch_size] 每个batch下序列的真实长度
        :param is_training: 是否是训练过程
        '''


    def train(self):
        pass


