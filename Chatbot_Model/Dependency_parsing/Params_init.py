#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: Params_init.py
@desc: 参数初始化
@time: 2019/03/08
"""

import tensorflow as tf
import math


def random_uniform_initializer(shape, name, val, trainable=True):
    out = tf.get_variable(shape=list(shape), dtype=tf.float32,
                          initializer=tf.random_uniform_initializer(minval=-val, maxval=val, dtype=tf.float32),
                          trainable=trainable, name=name)
    return out


def xavier_initializer(shape, name, trainable=True):
    val = math.sqrt(6. / sum(shape))
    return random_uniform_initializer(shape, name, val, trainable=trainable)


def random_normal_initializer(shape, name, mean=0., stddev=1, trainable=True):
    return tf.get_variable(shape = list(shape), dtype=tf.float32,
                           initializer=tf.random_normal(shape=shape, mean=mean, stddev=stddev, dtype=tf.float32),
                           trainable=trainable, name=name)

