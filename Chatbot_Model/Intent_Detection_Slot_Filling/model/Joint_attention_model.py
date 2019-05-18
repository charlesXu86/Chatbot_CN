#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Joint_attention_model.py 
@desc:  基于seq2seq和attention机制的模型层
@time: 2019/05/09 
"""

import tensorflow as tf
import numpy as np
import tensorflow.contrib as tf_contrib
import random
import os

from seq2seq_attention import rnn_decoder_with_attention, extract_argmax_and_embed, attention_util


class seq2seq_attention_model:
    def __init__(self,
                 intent_num_classes,
                 learning_rate,
                 batch_size,
                 decay_steps,
                 decay_rate,
                 sequence_length,
                 voacab_size,
                 embed_size,
                 hidden_size,
                 sequence_length_batch,
                 slots_num_classes,
                 is_training,
                 filter_size=[1,2,3],
                 num_filters = 128,
                 decoder_sent_length = 30,
                 initializer=tf.random_normal_initializer(stddev=0.1),
                 clip_gradients=5.0,
                 l2_lambda=0.0001,
                 use_beam_search=False):     # 这里为什么不用beam_search
        '''
         初始化所有超参数
        :param intent_num_classes:
        :param learning_rate:
        :param batch_size:
        :param decay_steps:
        :param decay_rate:
        :param sequence_length:
        :param voacab_size:
        :param embed_size:
        :param hidden_size:
        :param sequence_length_batch:
        :param slots_num_classes:
        :param is_training:
        :param filter_size:
        :param num_filters:
        :param decoder_sent_length:
        :param initializer:
        :param clip_gradients:
        :param l2_lambda:
        :param use_beam_search:
        '''
        # 设置超参数
        self.intent_num_classes = intent_num_classes


