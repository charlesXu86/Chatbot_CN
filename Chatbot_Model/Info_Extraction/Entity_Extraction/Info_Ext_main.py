#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: Utils.py
@desc: 信息抽取程序主入口
@time: 2018/08/08
"""

import tensorflow as tf
import numpy as np
import os, argparse, time, random

import re
from datetime import datetime

from tensorflow.python.framework import graph_util

# os.environ['CUDA_VISIBLE_DEVICES']='0'   # 设置只用一块显卡

from Entity_Extraction.Enext_model import BiLSTM_CRF
from Entity_Extraction.utils import str2bool, get_entity, get_MON_entity
from Entity_Extraction.data import tag2label

from Entity_Extraction.parameters import parameters


## Session configuration
os.environ['CUDA_VISIBLE_DEVICES'] = '1,2,3'  # 设置只用一块显卡
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # default: 0
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
# config.gpu_options.per_process_gpu_memory_fraction = 0.6 # need ~700MB GPU memory


## training Entity Extraction model
def train(config):

    print('Loading data...')
    print("Trainning Beginning....")

    with tf.Graph().as_default():
        sess_config = tf.ConfigProto(
            allow_soft_placement=config['allow_soft_placement'],  # 如果你指定的设备不存在，则允许TF自动分配设备
            log_device_placement=config['log_device_placement']  # 是否打印设备分配日志
        )
        ner_model = BiLSTM_CRF(config=config)
        ner_model.build_graph()

    ## hyperparameters-tuning, split train/dev
    # dev_data = train_data[:5000]; dev_size = len(dev_data)
    # train_data = train_data[5000:]; train_size = len(train_data)
    # print("train data: {0}\ndev data: {1}".format(train_size, dev_size))
    # model.train(train=train_data, dev=dev_data)

    ## train model on the whole training data
        print("train data: {}".format(len(train_data)))
        ner_model.train(train=train_data, dev=test_data)  # use test_data as the dev_data to see overfitting phenomena

## testing model
def test():
    ckpt_file = tf.train.latest_checkpoint(model_path)
    print(ckpt_file)
    paths['model_path'] = ckpt_file
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, paths, config=config)
    model.build_graph()
    print("test data: {}".format(test_size))
    model.test(test_data)

## demo
# elif args.mode == 'demo':
def NER_predict(msg):
    # 这里指定了模型路径
    model_path = '/Users/charlesxu/PycharmProjects/Chatbot_CN/Chatbot_Data/Info_Extraction_save/1562204195/checkpoints'
    ckpt_file = tf.train.latest_checkpoint(model_path)
    # print('>>>>>>>>>>>',ckpt_file)
    paths['model_path'] = ckpt_file
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, paths, config=config)
    model.build_graph()
    saver = tf.train.Saver()

    with tf.Session(config=config) as sess:
        print('============= demo =============')
        saver.restore(sess, ckpt_file)

        demo_sent = msg
        if demo_sent == '' or demo_sent.isspace():
            print('See you next time!')
        else:
            demo_sent = list(demo_sent.strip())
            demo_data = [(demo_sent, ['O'] * len(demo_sent))]
            tag = model.demo_one(sess, demo_data)
            PER, LOC, ORG = get_entity(tag, demo_sent)
            print('PER: {}\nLOC: {}\nORG: {}'.format(PER, LOC, ORG))


if __name__ == '__main__':
    train(parameters)