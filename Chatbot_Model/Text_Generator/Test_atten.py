# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Test_atten.py
   Description :   测试并展示attention
   Author :       charlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import tensorflow as tf

from tqdm import tqdm

from Sequence_to_sequence import SequenceToSequence
from Data_utils import batch_flow

from Fake_data import generate

def test(bidirectional, cell_type, depth, attention_type):
    """
     测试并展示attention图
    """

    # 获取一些假数据
    x_data, y_data, ws_input, ws_target = generate(size=10000)

    # 训练部分

    split = int(len(x_data) * 0.9)
    x_train, x_test, y_train, y_test = (
        x_data[:split], x_data[split:], y_data[:split], y_data[split:])
    n_epoch = 2
    batch_size = 32
    steps = int(len(x_train) / batch_size) + 1

    config = tf.ConfigProto(
        device_count={'CPU': 1, 'GPU': 0},
        allow_soft_placement=True,
        log_device_placement=False
    )

    save_path = '/tmp/s2ss_atten.ckpt'

    with tf.Graph().as_default():

        model = SequenceToSequence(
            input_vocab_size=len(ws_input),
            target_vocab_size=len(ws_target),
            batch_size=batch_size,
            learning_rate=0.001,
            bidirectional=bidirectional,
            cell_type=cell_type,
            depth=depth,
            attention_type=attention_type,
            parallel_iterations=1
        )
        init = tf.global_variables_initializer()

        with tf.Session(config=config) as sess:
            sess.run(init)
            for epoch in range(1, n_epoch + 1):
                costs = []
                flow = batch_flow(
                    [x_train, y_train], [ws_input, ws_target], batch_size
                )
                bar = tqdm(range(steps),
                           desc='epoch {}, loss=0.000000'.format(epoch))
                for _ in bar:
                    x, xl, y, yl = next(flow)
                    cost = model.train(sess, x, xl, y, yl)
                    costs.append(cost)
                    bar.set_description('epoch {} loss={:.6f}'.format(
                        epoch,
                        np.mean(costs)
                    ))

            model.save(sess, save_path)

    # attention 展示 不能用 beam search 的
    # 所以这里只是用 greedy

    with tf.Graph().as_default():
        model_pred = SequenceToSequence(
            input_vocab_size=len(ws_input),
            target_vocab_size=len(ws_target),
            batch_size=1,
            mode='decode',
            beam_width=0,    # beam_width为0就表示不用Beam Search
            bidirectional=bidirectional,
            cell_type=cell_type,
            depth=depth,
            attention_type=attention_type,
            parallel_iterations=1
        )
        init = tf.global_variables_initializer()

        with tf.Session(config=config) as sess:
            sess.run(init)
            model_pred.load(sess, save_path)

            pbar = batch_flow([x_test, y_test], [ws_input, ws_target], 1)
            t = 0
            for x, xl, y, yl in pbar:
                pred, atten = model_pred.predict(
                    sess,
                    np.array(x),
                    np.array(xl),
                    attention=True
                )
                ox = ws_input.inverse_transform(x[0])
                oy = ws_target.inverse_transform(y[0])
                op = ws_target.inverse_transform(pred[0])
                print(ox)
                print(oy)
                print(op)

                fig, ax = plt.subplots()
                cax = ax.matshow(atten.reshape(
                    [atten.shape[0], atten.shape[2]]
                ), cmap=cm.coolwarm)
                ax.set_xticks(np.arange(len(ox)))
                ax.set_yticks(np.arange(len(op)))
                ax.set_xticklabels(ox)
                ax.set_yticklabels(op)
                fig.colorbar(cax)
                plt.show()

                print('-' * 30)


                t += 1
                if t >= 10:
                    break


if __name__ == '__main__':

    # for bidirectional in (True, False):
    #     for cell_type in ('gru', 'lstm'):
    #         for depth in (1, 2, 3):
    #             for attention_type in ('Luong', 'Bahdanau'):
    #                 print(
    #                     'bidirectional, cell_type, depth, attention_type',
    #                     bidirectional, cell_type, depth, attention_type
    #                 )
    test(bidirectional=True, cell_type='lstm',
         depth=2, attention_type='Bahdanau')
