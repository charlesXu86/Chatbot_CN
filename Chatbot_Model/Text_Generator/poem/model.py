# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     model.py
   Description :   model
   Author :       charlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""
import tensorflow as tf
# import setting
import functools

from tensorflow.python.ops.rnn import dynamic_rnn
from tensorflow.python.ops.rnn_cell_impl import BasicLSTMCell,BasicRNNCell,MultiRNNCell,GRUCell


def rnn_model(model, input_data, output_data, vocab_size, rnn_size=128, num_layers=2, batch_size=64,
              learning_rate=0.01):
    """
    构建RNN模型
    construct rnn seq2seq model.
    :param model: model class
    :param input_data: input data placeholder
    :param output_data: output data placeholder
    :param vocab_size:
    :param rnn_size: LSTM隐藏结点个数
    :param num_layers: RNN深度
    :param batch_size:
    :param learning_rate:
    :return:
    """
    end_points = {}

    if model == 'rnn':
        cell_fun = BasicRNNCell
    elif model == 'gru':
        cell_fun = GRUCell
    elif model == 'lstm':
        cell_fun = BasicLSTMCell

    cell = cell_fun(rnn_size, state_is_tuple=True)
    cell = MultiRNNCell([cell] * num_layers, state_is_tuple=True)

    if output_data is not None:
        initial_state = cell.zero_state(batch_size, tf.float32)
    else:
        initial_state = cell.zero_state(1, tf.float32)

    with tf.device("/cpu:0"):
        embedding = tf.get_variable('embedding', initializer=tf.random_uniform(
            [vocab_size + 1, rnn_size], -1.0, 1.0))   # 把每个字向量化
        inputs = tf.nn.embedding_lookup(embedding, input_data)

    # [batch_size, ?, rnn_size] = [64, ?, 128]
    outputs, last_state = dynamic_rnn(cell, inputs, initial_state=initial_state)
    output = tf.reshape(outputs, [-1, rnn_size])

    weights = tf.Variable(tf.truncated_normal([rnn_size, vocab_size + 1]))
    bias = tf.Variable(tf.zeros(shape=[vocab_size + 1]))
    logits = tf.nn.bias_add(tf.matmul(output, weights), bias=bias)
    # [?, vocab_size+1]

    if output_data is not None:
        # output_data must be one-hot encode
        labels = tf.one_hot(tf.reshape(output_data, [-1]), depth=vocab_size + 1)
        # should be [?, vocab_size+1]

        # 定义损失函数
        loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits)
        # loss shape should be [?, vocab_size+1]
        total_loss = tf.reduce_mean(loss)
        train_op = tf.train.AdamOptimizer(learning_rate).minimize(total_loss)

        end_points['initial_state'] = initial_state
        end_points['output'] = output
        end_points['train_op'] = train_op
        end_points['total_loss'] = total_loss
        end_points['loss'] = loss
        end_points['last_state'] = last_state
    else:
        prediction = tf.nn.softmax(logits)   # softmax的公式

        end_points['initial_state'] = initial_state
        end_points['last_state'] = last_state
        end_points['prediction'] = prediction

    return end_points


HIDDEN_SIZE = 128  # LSTM隐藏节点个数
NUM_LAYERS = 2  # RNN深度

# class TrainModel(object):
#     """
#     训练模型
#     """
#
#     def __init__(self, data, labels, emb_keep, rnn_keep):
#         self.data = data  # 数据
#         self.labels = labels  # 标签
#         self.emb_keep = emb_keep  # embedding层dropout保留率
#         self.rnn_keep = rnn_keep  # lstm层dropout保留率
#
#
#     def cell(self):
#         """
#         rnn网络结构
#         :return:
#         """
#         lstm_cell = [
#             tf.nn.rnn_cell.DropoutWrapper(tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE), output_keep_prob=self.rnn_keep) for
#             _ in range(NUM_LAYERS)]
#         cell = tf.nn.rnn_cell.MultiRNNCell(lstm_cell)
#         return cell
#
#     def predict(self):
#         """
#         定义前向传播
#         :return:
#         """
#         # 创建词嵌入矩阵权重
#         embedding = tf.get_variable('embedding', shape=[setting.VOCAB_SIZE, HIDDEN_SIZE])
#         # 创建softmax层参数
#         if setting.SHARE_EMD_WITH_SOFTMAX:
#             softmax_weights = tf.transpose(embedding)
#         else:
#             softmax_weights = tf.get_variable('softmaweights', shape=[HIDDEN_SIZE, setting.VOCAB_SIZE])
#         softmax_bais = tf.get_variable('softmax_bais', shape=[setting.VOCAB_SIZE])
#         # 进行词嵌入
#         emb = tf.nn.embedding_lookup(embedding, self.data)
#         # dropout
#         emb_dropout = tf.nn.dropout(emb, self.emb_keep)
#         # 计算循环神经网络的输出
#         self.init_state = self.cell.zero_state(setting.BATCH_SIZE, dtype=tf.float32)
#         outputs, last_state = dynamic_rnn(self.cell, emb_dropout, scope='d_rnn', dtype=tf.float32,
#                                                 initial_state=self.init_state)
#         outputs = tf.reshape(outputs, [-1, HIDDEN_SIZE])
#         # 计算logits
#         logits = tf.matmul(outputs, softmax_weights) + softmax_bais
#         return logits
#
#     def loss(self):
#         """
#         定义损失函数
#         :return:
#         """
#         # 计算交叉熵
#         outputs_target = tf.reshape(self.labels, [-1])
#         loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.predict, labels=outputs_target, )
#         # 平均
#         cost = tf.reduce_mean(loss)
#         return cost
#
#     def global_step(self):
#         """
#         global_step
#         :return:
#         """
#         global_step = tf.Variable(0, trainable=False)
#         return global_step
#
#     def optimize(self):
#         """
#         定义反向传播过程
#         :return:
#         """
#         # 学习率衰减
#         learn_rate = tf.train.exponential_decay(setting.LEARN_RATE, self.global_step, setting.LR_DECAY_STEP,
#                                                 setting.LR_DECAY)
#         # 计算梯度，并防止梯度爆炸
#         trainable_variables = tf.trainable_variables()
#         grads, _ = tf.clip_by_global_norm(tf.gradients(self.loss, trainable_variables), setting.MAX_GRAD)
#         # 创建优化器，进行反向传播
#         optimizer = tf.train.AdamOptimizer(learn_rate)
#         train_op = optimizer.apply_gradients(zip(grads, trainable_variables), self.global_step)
#         return train_op
#
#
# class EvalModel(object):
#     """
#     验证模型
#     """
#
#     def __init__(self, data, emb_keep, rnn_keep):
#         self.data = data  # 输入
#         self.emb_keep = emb_keep  # embedding层dropout保留率
#         self.rnn_keep = rnn_keep  # lstm层dropout保留率
#
#
#     def cell(self):
#         """
#         rnn网络结构
#         :return:
#         """
#         lstm_cell = [
#             tf.nn.rnn_cell.DropoutWrapper(BasicLSTMCell(HIDDEN_SIZE), output_keep_prob=self.rnn_keep) for
#             _ in range(NUM_LAYERS)]
#         cell = MultiRNNCell(lstm_cell)
#         return cell
#
#     def predict(self):
#         """
#         定义前向传播过程
#         :return:
#         """
#         embedding = tf.get_variable('embedding', shape=[setting.VOCAB_SIZE, HIDDEN_SIZE])
#
#         if setting.SHARE_EMD_WITH_SOFTMAX:
#             softmax_weights = tf.transpose(embedding)
#         else:
#             softmax_weights = tf.get_variable('softmaweights', shape=[HIDDEN_SIZE, setting.VOCAB_SIZE])
#         softmax_bais = tf.get_variable('softmax_bais', shape=[setting.VOCAB_SIZE])
#
#         emb = tf.nn.embedding_lookup(embedding, self.data)
#         emb_dropout = tf.nn.dropout(emb, self.emb_keep)
#         # 与训练模型不同，这里只要生成一首古体诗，所以batch_size=1
#         self.init_state = self.cell.zero_state(1, dtype=tf.float32)
#         outputs, last_state = dynamic_rnn(self.cell, emb_dropout, scope='d_rnn', dtype=tf.float32,
#                                                 initial_state=self.init_state)
#         outputs = tf.reshape(outputs, [-1, HIDDEN_SIZE])
#
#         logits = tf.matmul(outputs, softmax_weights) + softmax_bais
#         # 与训练模型不同，这里要记录最后的状态，以此来循环生成字，直到完成一首诗
#         self.last_state = last_state
#         return logits
#
#     def prob(self):
#         """
#         softmax计算概率
#         :return:
#         """
#         probs = tf.nn.softmax(self.predict)
#         return probs

