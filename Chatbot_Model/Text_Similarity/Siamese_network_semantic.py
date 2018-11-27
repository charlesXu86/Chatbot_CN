# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Siamese_network_semantic.py
   Description :  孪生网络
   Author :       charl
   date：          2018/11/27
-------------------------------------------------
   Change Activity: 2018/11/27:
-------------------------------------------------
"""

import tensorflow as tf

class SiameseLSTMw2v(object):
    '''
    A LSTM based deep Siamese network for text similarity.
    Used an word embedding layer (looks up in pre-trained w2v), followed by a biLSTm and Energy loss
    '''
    def __init__(self, sequence_length, vocab_size, embedding_size, hidden_units, l2_reg_lambda, batch_size, trainableEmbeddings):
        # Placeholders for input, output and dropout
        self.input_x1 = tf.placeholder(tf.int32, [None, sequence_length], name="input_x1")
        self.input_x2 = tf.placeholder(tf.int32, [None, sequence_length], name="input_x2")
        self.input_y = tf.placeholder(tf.float32, [None], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss
        l2_loss = tf.constant(0.0, name="l2_loss")

        # Embedding layer
        with tf.name_scope("embedding"):
            self.W = tf.Variable(
                tf.constant(0.0, shape=[vocab_size, embedding_size]),
                trainable=trainableEmbeddings, name="W"
            )
            self.embedded_words1 = tf.nn.embedding_lookup(self.W, self.input_x1) # 实际上tf.nn.embedding_lookup的作用就是找到要寻找的embedding data中的对应的行下的vector。
            self.embedded_words2 = tf.nn.embedding_lookup(self.W, self.input_x2)

        # Create a convolution + maxpool layer each filter size
        with tf.name_scope("output"):
            self.out1 = self.stackedRNN(self.embedded_words1, self.dropout_keep_prob, "side1", embedding_size,
                                        sequence_length, hidden_units)
            self.out2 = self.stackedRNN(self.embedded_words2, self.dropout_keep_prob, "side2", embedding_size,
                                        sequence_length, hidden_units)
            self.distance = tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(self.out1, self.out2)), 1, keep_dims=True))  # tf.subtract 减法操作
            self.distance = tf.div(self.distance, tf.add(tf.sqrt(tf.reduce_sum(tf.square(self.out1), 1, keep_dims=True)),
                                                         tf.sqrt(tf.reduce_sum(tf.square(self.out2), 1, keep_dims=True))))
            self.distance = tf.reshape(self.distance, [-1], name="distance")

        with tf.name_scope("loss"):
            self.loss = self.contrastive_loss(self.input_y, self.distance, batch_size)

        with tf.name_scope("accuracy"):
            self.temp_sim = tf.subtract(tf.ones_like(self.distance), tf.rint(self.distance))  # tf.rint 计算离X近的整数，若x为中间值，则取整数
            correct_predictions = tf.equal(self.temp_sim, self.input_y)
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")

        with tf.name_scope("f1"):
            ones_like_actuals = tf.ones_like(self.input_y)
            zeros_like_actuals = tf.zeros_like(self.input_y)
            ones_like_predictions = tf.ones_like(self.temp_sim)
            zeros_like_predictions = tf.zeros_like(self.temp_sim)

            tp = tf.reduce_sum(
                tf.cast(
                    tf.logical_and(
                        tf.equal(self.input_y, ones_like_actuals), tf.equal(self.temp_sim, ones_like_predictions)
                    ),
                    'float'
                )
            )

            tn = tf.reduce_sum(
                tf.cast(
                    tf.logical_and(
                        tf.equal(self.input_y, zeros_like_actuals), tf.equal(self.temp_sim, zeros_like_predictions)
                    ),
                    'float'
                )
            )

            fp = tf.reduce_sum(
                tf.cast(
                    tf.logical_and(
                        tf.equal(self.input_y, zeros_like_actuals), tf.equal(self.temp_sim, ones_like_predictions)
                    ),
                    'float'
                )
            )

            fn = tf.reduce_sum(
                tf.cast(
                    tf.logical_and(
                        tf.equal(self.input_y, ones_like_actuals), tf.equal(self.temp_sim, zeros_like_predictions)
                    ),
                    'float'
                )
            )

            precision = tp / (tp + fp) # 准确率
            recall = tp / (tp + fn)    # 召回率

            self.f1 = 2 * precision * recall / (precision + recall)   # F1-score
