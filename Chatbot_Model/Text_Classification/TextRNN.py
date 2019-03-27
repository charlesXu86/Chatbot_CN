# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     TextRNN.py
   Description :  TextRNN + Attention实现
   Author :       charlesXu
   date：          2019/1/9
-------------------------------------------------
   Change Activity: 2019/1/9:
-------------------------------------------------
"""

import datetime
import os
import pickle
from sklearn.model_selection import train_test_split

import tensorflow as tf
import numpy as np
import Text_preprocessing

logger = Text_preprocessing.PrintLog("TextRNN.log")

class TextRNN(object):
    """
    RNN with Attention mechanism for text classification
    """
    def __init__(self, vocab_size, embedding_size, rnn_size, num_layers,
        attention_size, num_classes, learning_rate, grad_clip):
        '''

        :param vocab_size: vocabulary size
        :param embedding_size: word embedding dimension
        :param sequence_length: sequence length after sentence padding, UNUSED
        :param rnn_size: hidden layer dimension
        :param num_layers: number of rnn layers
        :param attention_size: attention layer dimension
        :param num_classes: number of target labels
        :param learning_rate: initial learning rate
        :param grad_clip: gradient clipping threshold
        '''

        self.input_x = tf.placeholder(tf.int32, shape=[None, None], name='input_x')
        self.input_y = tf.placeholder(tf.float32, shape=[None, num_classes], name='input_y')
        self.seq_len = tf.placeholder(tf.int32, shape=[None], name='seq_len')
        self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')
        self.global_step = tf.Variable(0, trainable=False, name='global_step')

        # Define Basic RNN Cell
        def basic_rnn_cell(rnn_size):
            return tf.contrib.rnn.GRUCell(rnn_size)
            # return tf.contrib.rnn.LSTMCell(rnn_size)

        # Define Forward RNN Cell
        with tf.name_scope('fw_rnn'):
            fw_rnn_cell = tf.contrib.rnn.MultiRNNCell([basic_rnn_cell(rnn_size) for _ in range(num_layers)])
            fw_rnn_cell = tf.contrib.rnn.DropoutWrapper(fw_rnn_cell, output_keep_prob=self.keep_prob)

        # Define Backward RNN Cell
        with tf.name_scope('bw_rnn'):
            bw_rnn_cell = tf.contrib.rnn.MultiRNNCell([basic_rnn_cell(rnn_size) for _ in range(num_layers)])
            bw_rnn_cell = tf.contrib.rnn.DropoutWrapper(bw_rnn_cell, output_keep_prob=self.keep_prob)

        # Embedding layer
        with tf.name_scope('embedding'):
            self.embedding = tf.Variable(tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0), trainable=True, name='embeddings')
            # self.input_x shape: (batch_size, sequence_length)
            embedding_inputs = tf.nn.embedding_lookup(self.embedding, self.input_x)

        with tf.name_scope('bi_rnn'):
            # embedding_inputs shape: (batch_size, sequence_length, embedding_size)
            # rnn_output, _ = tf.nn.dynamic_rnn(fw_rnn_cell, inputs=embedding_inputs, sequence_length=self.seq_len, dtype=tf.float32)
            rnn_output, _ = tf.nn.bidirectional_dynamic_rnn(fw_rnn_cell, bw_rnn_cell, inputs=embedding_inputs, sequence_length=self.seq_len, dtype=tf.float32)

        # In case of Bi-RNN, concatenate the forward and the backward RNN outputs
        if isinstance(rnn_output, tuple):
            rnn_output = tf.concat(rnn_output, 2)

        # BahdanauAttention Layer
        with tf.name_scope('attention'):
		
            hidden_size = rnn_output.shape[2].value

            attention_w = tf.Variable(tf.truncated_normal([hidden_size, attention_size], stddev=0.1), name='attention_w')
            attention_b = tf.Variable(tf.constant(0.1, shape=[attention_size]), name='attention_b')
            attention_u = tf.Variable(tf.truncated_normal([attention_size], stddev=0.1), name='attention_u')

            v = tf.tanh(tf.tensordot(rnn_output, attention_w, axes=1) + attention_b)
            vu = tf.tensordot(v, attention_u, axes=1, name='vu')
            alphas = tf.nn.softmax(vu, name='alphas')
            attention_output = tf.reduce_sum(rnn_output * tf.expand_dims(alphas, -1), 1)
			
        # Add dropout
        with tf.name_scope('dropout'):
            # attention_output shape: (batch_size, hidden_size)
            self.final_output = tf.nn.dropout(attention_output, self.keep_prob)

        # Fully connected layer
        with tf.name_scope('output'):
            fc_w = tf.Variable(tf.truncated_normal([hidden_size, num_classes], stddev=0.1), name='fc_w')
            fc_b = tf.Variable(tf.zeros([num_classes]), name='fc_b')
            self.logits = tf.matmul(self.final_output, fc_w) + fc_b
            self.logits_softmax = tf.nn.softmax(self.logits)
            self.predictions = tf.argmax(self.logits, 1, name='predictions')

        # Calculate cross-entropy loss
        with tf.name_scope('loss'):
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.logits, labels=self.input_y)
            self.loss = tf.reduce_mean(cross_entropy)  # TODO: add params loss

        # Create optimizer
        with tf.name_scope('optimization'):
            optimizer = tf.train.AdamOptimizer(learning_rate)
            gradients, variables = zip(*optimizer.compute_gradients(self.loss))
            gradients, _ = tf.clip_by_global_norm(gradients, grad_clip)
            self.train_op = optimizer.apply_gradients(zip(gradients, variables), global_step=self.global_step)

        # Calculate accuracy
        with tf.name_scope('accuracy'):
            correct_pred = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

def train_rnn(X, y, batch_size, num_epoch, output_dir, val_X=None, val_y=None):
    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            rnn = TextRNN(  # TODO: tune params and put these params to train_rnn params
                vocab_size=100000,
                embedding_size=128,
                rnn_size=128,
                num_layers=2,
                attention_size=50,
                num_classes=3,
                learning_rate=1e-3,
                grad_clip=5
            )
            tf.summary.scalar("loss", rnn.loss)
            tf.summary.scalar("accuracy", rnn.accuracy)
            merged_summary = tf.summary.merge_all()

            print("Writing to {}...\n".format(output_dir))
            train_summary_dir = os.path.join(output_dir, "summaries", "train")
            val_summary_dir = os.path.join(output_dir, "summaries", "val")
            train_summaries_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)
            val_summaries_writer = tf.summary.FileWriter(val_summary_dir, sess.graph)

            # Checkpoint directory, will not create itself
            checkpoint_dir = os.path.join(output_dir, "checkpoints")
            checkpoint_prefix = os.path.join(checkpoint_dir, "model")
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
            saver = tf.train.Saver(tf.global_variables(), max_to_keep=5)  # how many model to save 

            # Initialize all variables
            sess.run(tf.global_variables_initializer())

            batches = Text_preprocessing.batch_iter(X, y, batch_size, num_epoch, shuffle=True)
            for x_batch, seq_lens, y_batch in batches:
                feed_dict = {rnn.input_x: x_batch, rnn.input_y: y_batch, rnn.seq_len: seq_lens, rnn.keep_prob: 0.5}
                _, global_step, train_summaries, train_loss, train_accuracy = sess.run(
                    [rnn.train_op, rnn.global_step, merged_summary, rnn.loss, rnn.accuracy],
                    feed_dict=feed_dict
                )
                time_str = datetime.datetime.now().isoformat()
                print("{}: step {}, train loss {:g}, train acc {:g}".format(time_str, global_step, train_loss, train_accuracy))
                train_summaries_writer.add_summary(summary=train_summaries, global_step=global_step)

                if global_step % 100 == 0:
                    path = saver.save(sess=sess, save_path=checkpoint_prefix, global_step=global_step)
                    print("Save model checkpoint to {}\n".format(path))

                if val_X is not None:
                    if global_step % 100 == 0:
                        x_val, val_seq_lens = Text_preprocessing.pad_sentence(val_X)
                        feed_dict = {rnn.input_x: x_val, rnn.input_y: val_y, rnn.seq_len: val_seq_lens,
                                     rnn.keep_prob: 1.0}
                        val_summaries, val_loss, val_accuracy = sess.run(
                            [merged_summary, rnn.loss, rnn.accuracy],
                            feed_dict=feed_dict
                        )
                        val_summaries_writer.add_summary(val_summaries, global_step=global_step)
                        print("global_step: {}, val loss: {:g}, val acc: {:g}".format(global_step, val_loss, val_accuracy))
						


def predict(x_test, y_test=None, checkpoint_dir=None):

    checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
    print(checkpoint_file)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=True,
            log_device_placement=False
        )
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            seq_len = graph.get_operation_by_name("seq_len").outputs[0]
            keep_prob = graph.get_operation_by_name("keep_prob").outputs[0]

            # Tensor we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            # Collect the predictions
            all_predictions = np.array([], dtype=np.int64)
            if y_test is not None:
                batches = Text_preprocessing.batch_iter(x_test, y_test, 64, 1, shuffle=False)
                for x_batch, seq_lens, _ in batches:  # _ stand for y_batch
                    feed_dict = {input_x: x_batch, seq_len: seq_lens, keep_prob: 1.0}
                    batch_prediction = sess.run(
                        predictions,
                        feed_dict=feed_dict
                    )
                    all_predictions = np.concatenate([all_predictions, batch_prediction])
                print("all predictions: ", all_predictions)
                correct_predictions = np.sum(all_predictions == np.argmax(y_test, axis=1))
                accuracy = correct_predictions / len(y_test)
                print("test data accuracy: ", accuracy)
            else:
                for i in range(0, len(x_test), 64):  # set batch_size to 64
                    padded_sentences, seq_lens = Text_preprocessing.pad_sentence(x_test[i:i + 64])
                    feed_dict = {input_x: padded_sentences, seq_len: seq_lens, keep_prob: 1.0}
                    batch_prediction = sess.run(
                        predictions,
                        feed_dict=feed_dict
                    )
                    all_predictions = np.concatenate([all_predictions, batch_prediction])

    return all_predictions



if __name__ == '__main__':
    with open("label_array.txt", 'rb') as f:
        labels = pickle.load(f)
    with open("indexed_words.txt", 'rb') as f:
        text_list = pickle.load(f)

    x_train, x_test, y_train, y_test = train_test_split(text_list, labels, train_size=0.8, random_state=1)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, train_size=0.9, random_state=1)
    train_rnn(x_train, y_train, 64, 5, "rnn", val_X=x_val, val_y=y_val)
    # model = TextRNN(vocab_size=8000, embedding_size=150, rnn_size=100, num_layers=2,
    #         attention_size=50, num_classes=30, learning_rate=0.001, grad_clip=5.0)