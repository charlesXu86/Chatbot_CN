# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Train.py
   Description :
   Author :       charl
   date：          2018/11/27
-------------------------------------------------
   Change Activity: 2018/11/27:
-------------------------------------------------
"""
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import gc

from Input_helper import InputHelper
from Siamese_network_semantic import SiameseLSTMw2v


# Parameters, 采用已经训练好的word2vec模型
WORD2VEC_MODEL = ''

# 模型格式
WORD2VEC_FORMAT = 'bin'

# word2vec 词嵌入维数
EMBEDDING_DIM = 64

# dropout 比例设置
DROPOUT_KEEP_PROB = 0.8

# L2 正则化系数 (目前暂未生效)
L2_REG_LAMBDA = 0.0

# 训练数据
TRAIN_FILE_RAW = ''

#隐藏层单元数
HIDDEN_UNITS = 128

BATCH_SIZE = 1024

NUM_EPOCH = 1000000

# 模型评估周期 (每隔多少步)
EVALUATE_EVERY = 100

# 模型保存周期
CHECKOUTPOINT_EVERY = 1000

# 语句最大长度
MAX_DOCUMENT_LENGTH = 100

# 验证集比例
DEV_PERCENT = 10

# Misc Parameters
ALLOW_SOFT_PLACEMENT = True
LOG_DEVICE_PLACEMENT = False

print('训练开始....')
start_time = datetime.datetime.now()

inputH = InputHelper()
train_set, dev_set, vocab_processor, sum_no_of_batches = inputH.getDataSets(TRAIN_FILE_RAW,
                                                                            MAX_DOCUMENT_LENGTH,
                                                                            DEV_PERCENT,
                                                                            BATCH_SIZE)

with tf.Graph().as_default():
    session_conf = tf.ConfigProto(
        allow_soft_placement=ALLOW_SOFT_PLACEMENT,
        log_device_placement=LOG_DEVICE_PLACEMENT
    )
    sess = tf.Session(config=session_conf)

    with sess.as_default():
        siameseModel = SiameseLSTMw2v(
            sequence_length=MAX_DOCUMENT_LENGTH,
            vocab_size=len(vocab_processor.vocabulary_),
            embedding_size=EMBEDDING_DIM,
            hidden_units=HIDDEN_UNITS,
            l2_reg_lambda=L2_REG_LAMBDA,
            batch_size=BATCH_SIZE,
            trainableEmbeddings=False
        )
        # Define Training procedure
        global_step = tf.Variable(0, name="global_step", trainable=False)
        optimizer = tf.train.AdamOptimizer(1e-3)

    grads_and_vars = optimizer.compute_gradients(siameseModel.loss)
    tr_op_set = optimizer.apply_gradients(grads_and_vars, global_step=global_step)
    print('Defined Training_ops')

    # Keep track of gradient values and sparsity
    grad_summaries = []
    for g, v in grads_and_vars:
        if g is not None:
            grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name), g)
            # tf.nn.zero_fraction的作用是将输入的Tensor中0元素在所有元素中所占的比例计算并返回，因为Relu激活函数有时
            # 会将大面积的输入参数设为0，所以此函数可以有效衡量relu激活函数的有效性。
            sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
            grad_summaries.append(grad_hist_summary)
            grad_summaries.append(sparsity_summary)
    grad_summaries_merged = tf.summary.merge(grad_summaries)
    print('Defined gradient summaries')

    # Output directory for models and summaries
    timestamp = str(int(time.time()))
    out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
    print('Writing to {}\n'.format(out_dir))

    # Summaries for loss and accuracy
    loss_summary = tf.summary.scalar("loss", siameseModel.loss)
    acc_summary = tf.summary.scalar("accuracy", siameseModel.accuracy)
    f1_summary = tf.summary.scalar('f1', siameseModel.f1)

    # Train summaries
    train_summary_op = tf.summary.merge([loss_summary, acc_summary, f1_summary, grad_summaries_merged])
    train_summary_dir = os.path.join(out_dir, "summaries", "train")
    train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

    # Dev summaries
    dev_summary_op = tf.summary.merge([loss_summary, acc_summary, f1_summary])
    dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
    dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

    # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
    checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
    checkpoint_prefix = os.path.join(checkpoint_dir, "model")
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)
    saver = tf.train.Saver(tf.global_variables(), max_to_keep=100)

    # Write vocabulary
    vocab_processor.save(os.path.join(checkpoint_dir, "vocab"))

    # Initialize all variables
    sess.run(tf.global_variables_initializer())

    print("init all variables")
    graph_def = tf.get_default_graph().as_graph_def()
    graphpb_txt = str(graph_def)
    with open(os.path.join(checkpoint_dir, "graphpb.txt"), 'w') as f:
        f.write(graphpb_txt)

    # 加载word2vec
    inputH.loadW2V(WORD2VEC_MODEL, WORD2VEC_FORMAT)
    initW = np.random.uniform(0, 0, (len(vocab_processor.vocabulary_), EMBEDDING_DIM))
    print(initW)

    # Load any vectors from the word2vec
    print('Initializing initW with pre-trained word2vec embeddings')
    for index, w in enumerate(vocab_processor.vocabulary_._mapping):
        print('vocab-{}:{}'.format(initW, w))

        arr = []
        if w in inputH.pre_emb:
            arr = inputH.pre_emb[w]
            idx = vocab_processor.vocabulary_.get(w)
            initW[idx] = np.asarray(arr).astype(np.float32)
    print("Done assigning initW. len=", str(len(initW)))
    inputH.deletePreEmb()
    gc.collect()
    sess.run(siameseModel.W.assign(initW))

    def train_step(x1_batch, x2_batch, y_batch):
        '''
        A single training step
        :param x1_batch:
        :param x2_batch:
        :param y_batch:
        :return:
        '''
        feed_dict = {
            siameseModel.input_x1: x1_batch,
            siameseModel.input_x2: x2_batch,
            siameseModel.input_y: y_batch,
            siameseModel.dropout_keep_prob: DROPOUT_KEEP_PROB
        }
        _, step, loss, accuracy, f1, dist, sim, summaries = sess.run(
            [tr_op_set, global_step, siameseModel.loss, siameseModel.accuracy, siameseModel.f1, siameseModel.distance,
             siameseModel.temp_sim, train_summary_op], feed_dict)
        time_str = datetime.datetime.now().isoformat()
        print("TRAIN {}: step {}, loss {:g}, acc {:g}, f1 {:g}".format(time_str, step, loss, accuracy, f1))
        train_summary_writer.add_summary(summaries, step)
        print(y_batch, dist, sim)

    def dev_step(x1_batch, x2_batch, y_batch):
        feed_dict = {
            siameseModel.input_x1 : x2_batch,
            siameseModel.input_x2 : x1_batch,
            siameseModel.input_y : y_batch,
            siameseModel.dropout_keep_prob : 1.0
        }
        step, loss, accuracy, f1, sim, summaries = sess.run(
            [global_step, siameseModel.loss, siameseModel.accuracy, siameseModel.f1, siameseModel.temp_sim, dev_summary_op],
            feed_dict
        )
        time_str = datetime.datetime.now().isoformat()
        print("DEV {}: step {}, loss {:g}, acc {:g}, f1 {:g}".format(time_str, step, loss, accuracy, f1))
        dev_summary_writer.add_summary(summaries, step)
        print(y_batch, sim)
        return accuracy

    # Generate batches
    batches = inputH.batch_iter(
        list(zip(train_set[0], train_set[1], train_set[2])), BATCH_SIZE, NUM_EPOCH)

    ptr = 0
    max_validation_acc = 0.0
    for nn in range(sum_no_of_batches * NUM_EPOCH):
        batch = batches.next()
        if len(batch) < 1:
            continue
        x1_batch, x2_batch, y_batch = zip(*batch)
        if len(y_batch) < 1:
            continue
        train_step(x1_batch, x2_batch, y_batch)
        current_step = tf.train.global_step(sess, global_step)
        sum_acc = 0.0
        cnt = 0
        if current_step % EVALUATE_EVERY == 0:
            print("\nEvaluation:")
            dev_batches = inputH.batch_iter(list(zip(dev_set[0], dev_set[1], dev_set[2])), BATCH_SIZE, 1)
            for db in dev_batches:
                if len(db) < 1:
                    continue
                x1_dev_b, x2_dev_b, y_dev_b = zip(*db)
                if len(y_dev_b) < 1:
                    continue
                acc = dev_step(x1_dev_b, x2_dev_b, y_dev_b)
                sum_acc = sum_acc + acc
                cnt += 1

            sum_acc /= cnt
            print("sum_acc= {}".format(sum_acc))
        if current_step % CHECKOUTPOINT_EVERY == 0:
            if sum_acc >= max_validation_acc:
                max_validation_acc = sum_acc

            # 临时逻辑
            saver.save(sess, checkpoint_prefix, global_step=current_step)
            tf.train.write_graph(sess.graph.as_graph_def(), checkpoint_prefix, "graph" + str(nn) + ".pb",
                                 as_text=False)
            print("Saved model {} with sum_accuracy={} checkpoint to {}\n".format(nn, max_validation_acc,
                                                                                  checkpoint_prefix))

        print('max_validation_acc(each batch)= {}'.format(max_validation_acc))

end_time = datetime.datetime.now()
train_duration = end_time - start_time

print('训练开始时间： {}'.format(start_time))
print('训练结束时间： {}'.format(end_time))
print('训练结束，总耗时： {}'.format(train_duration))




