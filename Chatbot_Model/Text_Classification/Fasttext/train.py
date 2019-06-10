# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   train.py

@Time    :   2019-05-30 15:20

@Desc    :

'''

import tensorflow as tf
from Chatbot_Model.Text_Classification.Fasttext.fast_text import FastText
from Chatbot_Model.Text_Classification.Fasttext.parameters import parameters
import time
import os
import datetime
import json

from Chatbot_Model.Text_Classification.Fasttext import data_helper


def train(config):
    print('parameters: ')
    print(json.dumps(parameters, indent=4, ensure_ascii=False))

    # load data
    print('load data .....')
    X, y = data_helper.process_data(parameters)

    # make vocab
    print('make vocab .....')
    word_to_index, label_to_index = data_helper.generate_vocab(X, y, parameters)

    # padding data
    print('padding data .....')
    input_x, input_y = data_helper.padding(X, y, parameters, word_to_index, label_to_index)

    # split data
    print('split data .....')
    x_train, y_train, x_test, y_test, x_dev, y_dev = data_helper.split_data(input_x, input_y, parameters)

    print('length train: {}'.format(len(x_train)))
    print('length test: {}'.format(len(x_test)))
    print('length dev: {}'.format(len(x_dev)))

    print('training .....')
    with tf.Graph().as_default():
        sess_config = tf.ConfigProto(
            allow_soft_placement=config['allow_soft_placement'],       # 如果你指定的设备不存在，则允许TF自动分配设备
            log_device_placement=config['log_device_placement']        # 石佛打印设备分配日志
        )
        with tf.Session(config=sess_config) as sess:
            fast_text = FastText(config)

            # training procedure
            global_step = tf.Variable(0, name='global_step', trainable=False)
            optimizer = tf.train.AdamOptimizer(config['learning_rate'])
            grads_and_vars = optimizer.compute_gradients(fast_text.loss)
            train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

            # keep track of gradient values and sparsity
            grad_summaries = []
            for g, v in grads_and_vars:
                if g is not None:
                    grad_hist_summary = tf.summary.histogram('{}/grad/hist'.format(v.name), g)
                    sparsity_summary = tf.summary.scalar('{}/grad/sparsity'.format(v.name), tf.nn.zero_fraction(g))
                    grad_summaries.append(grad_hist_summary)
                    grad_summaries.append(sparsity_summary)
            grad_summaries_merged = tf.summary.merge(grad_summaries)

            # output dir for models and summaries
            timestamp = str(int(time.time()))
            outdir = os.path.abspath(os.path.join(os.path.curdir, 'runs', timestamp))
            print('writing to {}'.format(outdir))

            # summary for loss and accuracy
            loss_summary = tf.summary.scalar('loss', fast_text.loss)
            acc_summary = tf.summary.scalar('accuracy', fast_text.accuracy)

            # train summary
            train_summary_op = tf.summary.merge([loss_summary, acc_summary, grad_summaries_merged])
            # train_summary_dir = os.path.join(outdir, 'summaries', 'train')
            # train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

            # dev summary
            dev_summary_op = tf.summary.merge([loss_summary, acc_summary])
            # dev_summary_dir = os.path.join(outdir, 'summaries', 'dev')
            # dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

            # 保存模型
            # saver = tf.train.Saver(tf.global_variables(), max_to_keep=config['num_checkpoints'])

            sess.run(tf.global_variables_initializer())

            # 将模型保存为pb格式，调用SavedModelBuilder类,
            builder = tf.saved_model.builder.SavedModelBuilder(outdir)   # 目录不用预先创建

            # 导入graph的信息及变量，这个方法假设变量已经初始化好了，对于每个SavedModelBuilder这个方法一定要执行一次用于导入第一个meta graph。
            # 第一个参数传入当前的session，包含了graph的结构与所有变量。
            # 第二个参数是给当前需要保存的meta graph一个标签，标签名可以自定义，在之后载入模型的时候，需要根据这个标签名去查找对应的MetaGraphDef，
            # 找不到就会报如RuntimeError: MetaGraphDef associated with tags 'foo' could not be found in SavedModel这样的错。
            # 标签也可以选用系统定义好的参数，如tf.saved_model.tag_constants.SERVING与tf.saved_model.tag_constants.TRAINING。
            builder.add_meta_graph_and_variables(sess, ['tag_string'])
            builder.save()

            def train_step(x_batch, y_batch):
                feed_dict = {
                    fast_text.input_x: x_batch,
                    fast_text.input_y: y_batch,
                }

                _, step, summaries, loss, accuracy = sess.run(
                    [train_op, global_step, train_summary_op, fast_text.loss, fast_text.accuracy],
                    feed_dict=feed_dict
                )

                time_str = datetime.datetime.now().isoformat()
                print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
                # train_summary_writer.add_summary(summaries, step)

            def dev_step(x_batch, y_batch, writer=None):
                feed_dic = {
                    fast_text.input_x: x_batch,
                    fast_text.input_y: y_batch,
                    fast_text.dropout_keep_prob: 1.0
                }

                step, summaries, loss, accuracy = sess.run(
                    [global_step, dev_summary_op, fast_text.loss, fast_text.accuracy],
                    feed_dict=feed_dic
                )

                time_str = datetime.datetime.now().isoformat()
                print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
                if writer:
                    writer.add_summary(summaries, step)

            # generate batches
            batches = data_helper.generate_batchs(x_train, y_train, config)
            for batch in batches:
                x_batch, y_batch = zip(*batch)
                train_step(x_batch, y_batch)
                current_step = tf.train.global_step(sess, global_step)
                # if current_step % config['evaluate_every'] == 0:
                #     print('Evaluation:')
                #     dev_step(x_dev, y_dev, writer=dev_summary_writer)

                # if current_step % config['checkpoint_every'] == 0:
                    # path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                    # print('save model checkpoint to {}'.format(path))

            # test accuracy
            test_accuracy = sess.run([fast_text.accuracy], feed_dict={
                fast_text.input_x: x_test, fast_text.input_y: y_test, fast_text.dropout_keep_prob: 1.0})
            print('Test dataset accuracy: {}'.format(test_accuracy))


if __name__ == '__main__':
    train(parameters)



