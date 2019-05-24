# -*- coding: utf-8 -*-

import tensorflow as tf


class FastText():
    def __init__(self, config):
        self.sequence_length = config['sequence_length']
        self.num_classes = config['num_classes']
        self.vocab_size = config['vocab_size']
        self.embedding_size = config['embedding_size']
        self.device = config['device']

        # placeholder
        self.input_x = tf.placeholder(tf.int32, [None, self.sequence_length], name='input_x')
        self.input_y = tf.placeholder(tf.float32, [None, self.num_classes], name='input_y')
        self.dropout_keep_prob = tf.placeholder(tf.float32, name='dropout_keep_prob')

        # embedding layer
        with tf.device(self.device), tf.name_scope('embedding'):
            self.W = tf.Variable(
                tf.random_uniform([self.vocab_size, self.embedding_size], -1.0, 1.0),
                name='W'
            )
            self.embedded_chars = tf.nn.embedding_lookup(self.W, self.input_x)

            # average vectors, to get the representation of the sentence
            self.embedded_chars_mean = tf.reduce_mean(self.embedded_chars, axis=1)

        # final scores and predictions
        with tf.name_scope('output'):
            W = tf.get_variable(
                "W",
                shape=[self.embedding_size, self.num_classes],
                initializer=tf.contrib.layers.xavier_initializer()
            )
            b = tf.Variable(tf.constant(0.1, shape=[self.num_classes]), name='b')
            self.scores = tf.nn.xw_plus_b(self.embedded_chars_mean, W, b, name='scores')
            self.predictions = tf.argmax(self.scores, 1, name='predictions')

        # loss
        with tf.name_scope('loss'):
            losses = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.scores, labels=self.input_y)
            self.loss = tf.reduce_mean(losses)

        # accuracy
        with tf.name_scope('accuracy'):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.float32), name='accuracy')
