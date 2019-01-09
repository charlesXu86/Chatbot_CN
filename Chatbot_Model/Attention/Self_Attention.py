# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Self_Attention.py
   Description :  Attention Is All You Need 部分方法实现
   Author :       charlesXu
   date：          2019/1/9
-------------------------------------------------
   Change Activity: 2019/1/9:
-------------------------------------------------
"""

import tensorflow as tf

def Position_Embedding(inputs, position_size):
    '''

    :param inputs: 是一个形如(batch_size, seq_len, word_size)的张量
    :param position_size:
    :return: 函数返回一个形如(batch_size, seq_len, position_size)的位置张量
    '''
    batch_size, seq_len = tf.shape(inputs)[0], tf.shape(inputs)[1]
    position_j = 1. / tf.pow(10000.,2 * tf.range(position_size / 2, dtype=tf.float32 ) / position_size)
    position_j = tf.expand_dims(position_j, 0)
    position_i = tf.range(tf.cast(seq_len, tf.float32), dtype=tf.float32)
    position_i = tf.expand_dims(position_i, 0)   # Inserts a dimension of 1 into a tensor's shape.
    position_ij = tf.matmul(position_i, position_j)
    position_ij = tf.concat([tf.cos(position_ij), tf.sin(position_ij)], 1)
    position_embedding = tf.expand_dims(position_ij, 0) + tf.zeros((batch_size, seq_len, position_size))

    return position_embedding

def Mask(inputs, seq_len, mode='mul'):
    '''

    :param inputs: 一个二阶以上的张量，代表输入序列，比如形如(batch_size, seq_len, input_size)的张量；
    :param seq_len: 是一个形如(batch_size,)的张量，代表每个序列的实际长度，多出部分都被忽略；
    :param mode: mode分为mul和add，mul是指把多出部分全部置零，一般用于全连接层之前；
                                 add 是指把多出去的部分减去一个大的常数，一般用于softmax之前
    :return:
    '''
    if seq_len == None:
        return inputs
    else:
        mask = tf.cast(tf.sequence_mask(seq_len), tf.float32)
        for _ in range(len(inputs.shape) - 2):
            mask = tf.expand_dims(mask, 2)
        if mode == 'mul':
            return inputs * mask
        if mode == 'add':
            return inputs - (1 - mask) * 1e12

def Dense(inputs, ouput_size, bias=True, seq_len=None):
    '''
    普通的全连接
    只对最后一个维度做矩阵乘法，即输出一个形如(batch_size,...,ouput_size)的张量。
    :param inputs: 是一个二阶或二阶以上的张量，即形如(batch_size,...,input_size)。
    :param ouput_size:
    :param bias:
    :param seq_len:
    :return:
    '''
    input_size = int(inputs.shape[-1])
    W = tf.Variable(tf.random_uniform([input_size, ouput_size], -0.05, 0.05))
    if bias:
        b = tf.Variable(tf.random_uniform([ouput_size], -0.05, 0.05))
    else:
        b = 0
    outputs = tf.matmul(tf.reshape(inputs, (-1, input_size)), W) + b
    outputs = tf.reshape(outputs, tf.concat([tf.shape(inputs)[:-1], [ouput_size]], 0))
    if seq_len != None:
        outputs = Mask(outputs, seq_len, 'mul')
    return outputs


def Attention(Q, K, V, nb_head, size_per_head, Q_len=None, V_len=None):
    '''
    Multi-Head Attention的实现
    '''
    #对Q、K、V分别作线性映射
    Q = Dense(Q, nb_head * size_per_head, False)
    Q = tf.reshape(Q, (-1, tf.shape(Q)[1], nb_head, size_per_head))
    Q = tf.transpose(Q, [0, 2, 1, 3])
    K = Dense(K, nb_head * size_per_head, False)
    K = tf.reshape(K, (-1, tf.shape(K)[1], nb_head, size_per_head))
    K = tf.transpose(K, [0, 2, 1, 3])
    V = Dense(V, nb_head * size_per_head, False)
    V = tf.reshape(V, (-1, tf.shape(V)[1], nb_head, size_per_head))
    V = tf.transpose(V, [0, 2, 1, 3])
    #计算内积，然后mask，然后softmax
    A = tf.matmul(Q, K, transpose_b=True) / tf.sqrt(float(size_per_head))
    A = tf.transpose(A, [0, 3, 2, 1])
    A = Mask(A, V_len, mode='add')
    A = tf.transpose(A, [0, 3, 2, 1])
    A = tf.nn.softmax(A)
    #输出并mask
    O = tf.matmul(A, V)
    O = tf.transpose(O, [0, 2, 1, 3])
    O = tf.reshape(O, (-1, tf.shape(O)[1], nb_head * size_per_head))
    O = Mask(O, Q_len, 'mul')
    return O