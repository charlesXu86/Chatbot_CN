#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: utils.py
@desc: 信息抽取程序主入口
@time: 2018/08/08
"""

import tensorflow as tf
import numpy as np
import os, argparse, time, random
import pymysql
import split_sentence
import Aip_config

from Entity_Extraction import proprecess_money
from Entity_Extraction.Enext_model import BiLSTM_CRF
from Entity_Extraction.utils import str2bool, get_logger, get_entity
from Entity_Extraction.data import read_corpus, read_dictionary, tag2label, random_embedding


## Session configuration
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # default: 0
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.2  # need ~700MB GPU memory


## hyperparameters
parser = argparse.ArgumentParser(description='BiLSTM-CRF for Chinese NER task')
parser.add_argument('--train_data', type=str, default='D:\project\Chatbot_CN\Chatbot_Data\Info_Extraction', help='train data source')
parser.add_argument('--test_data', type=str, default='D:\project\Chatbot_CN\Chatbot_Data\Info_Extraction', help='test data source')
parser.add_argument('--batch_size', type=int, default=64, help='#sample of each minibatch')
parser.add_argument('--epoch', type=int, default=40, help='#epoch of training')
parser.add_argument('--hidden_dim', type=int, default=300, help='#dim of hidden state')
parser.add_argument('--optimizer', type=str, default='Adam', help='Adam/Adadelta/Adagrad/RMSProp/Momentum/SGD')
parser.add_argument('--CRF', type=str2bool, default=True, help='use CRF at the top layer. if False, use Softmax')
parser.add_argument('--lr', type=float, default=0.001, help='learning rate')
parser.add_argument('--clip', type=float, default=5.0, help='gradient clipping')
parser.add_argument('--dropout', type=float, default=0.5, help='dropout keep_prob')
parser.add_argument('--update_embedding', type=str2bool, default=True, help='update embedding during training')
parser.add_argument('--pretrain_embedding', type=str, default='random', help='use pretrained char embedding or init it randomly')
parser.add_argument('--embedding_dim', type=int, default=300, help='random init char embedding_dim')
parser.add_argument('--shuffle', type=str2bool, default=True, help='shuffle training data before each epoch')
parser.add_argument('--mode', type=str, default='demo', help='train/test/demo')
parser.add_argument('--demo_model', type=str, default='1521112368', help='model for test and demo')
args = parser.parse_args()


## get char embeddings
word2id = read_dictionary(os.path.join('.', args.train_data, 'word2id.pkl'))
if args.pretrain_embedding == 'random':
    embeddings = random_embedding(word2id, args.embedding_dim)
else:
    embedding_path = 'pretrain_embedding.npy'
    embeddings = np.array(np.load(embedding_path), dtype='float32')


## read corpus and get training data
if args.mode != 'demo':
    train_path = os.path.join('.', args.train_data, 'train_data')
    test_path = os.path.join('.', args.test_data, 'test_data')
    train_data = read_corpus(train_path)
    test_data = read_corpus(test_path);
    test_size = len(test_data)


## paths setting
paths = {}
timestamp = str(int(time.time())) if args.mode == 'train' else args.demo_model
output_path = os.path.join('.', args.train_data+"_save", timestamp)
if not os.path.exists(output_path): os.makedirs(output_path)
summary_path = os.path.join(output_path, "summaries")
paths['summary_path'] = summary_path
if not os.path.exists(summary_path): os.makedirs(summary_path)
model_path = os.path.join(output_path, "checkpoints/")
if not os.path.exists(model_path): os.makedirs(model_path)
ckpt_prefix = os.path.join(model_path, "model")
paths['model_path'] = ckpt_prefix
result_path = os.path.join(output_path, "results")
paths['result_path'] = result_path
if not os.path.exists(result_path): os.makedirs(result_path)
log_path = os.path.join(result_path, "log.txt")
paths['log_path'] = log_path
get_logger(log_path).info(str(args))


## training Entity Extraction model
if args.mode == 'train':
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, paths, config=config)
    model.build_graph()

    ## hyperparameters-tuning, split train/dev
    # dev_data = train_data[:5000]; dev_size = len(dev_data)
    # train_data = train_data[5000:]; train_size = len(train_data)
    # print("train data: {0}\ndev data: {1}".format(train_size, dev_size))
    # model.train(train=train_data, dev=dev_data)

    ## train model on the whole training data
    print("train data: {}".format(len(train_data)))
    model.train(train=train_data, dev=test_data)  # use test_data as the dev_data to see overfitting phenomena

## testing model
elif args.mode == 'test':
    ckpt_file = tf.train.latest_checkpoint(model_path)
    print(ckpt_file)
    paths['model_path'] = ckpt_file
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, paths, config=config)
    model.build_graph()
    print("test data: {}".format(test_size))
    model.test(test_data)

## demo
elif args.mode == 'demo':
    model_path = 'D:\project\Chatbot_CN\Chatbot_Data\Info_Extraction_save\\1533871370\checkpoints'
    ckpt_file = tf.train.latest_checkpoint(model_path)
    # print('>>>>>>>>>>>',ckpt_file)
    paths['model_path'] = ckpt_file
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, paths, config=config)
    model.build_graph()
    saver = tf.train.Saver()
    with tf.Session(config=config) as sess:
        print('============= demo =============')
        saver.restore(sess, ckpt_file)
        # saver.restore(sess, tf.train.latest_checkpoint("Chatbot_Data/Info_Extraction_save"))
        # while(1):
            # print('Please input your sentence:')
            # demo_sent = input()

            # 连接mysql
        db = pymysql.Connect("localhost", "root", "Aa123456", "zhizhuxia")
        cursor = db.cursor()
        sql = "SELECT doc_result from doc_test LIMIT 2"
        # try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            demo_sent = result[0]
            text_sent = split_sentence.split_sentence_thr(demo_sent)
            for text in text_sent:
                print(text)
                to_str = str(text)
                if text == '' or text.isspace():
                    print('See you next time!')
                    break
                else:
                    text = list(text.strip())
                    demo_data = [(text, ['O'] * len(text))]
                    tag = model.demo_one(sess, demo_data)
                    PER, LOC, ORG = get_entity(tag, text)

                    # 获取时间和LOC
                    # DATE, LOC_ITEM = Aip_config.get_LOC_DATE(to_str)

                    # 调用money处理方法，获取金额实体
                    tr = proprecess_money.wash_data(to_str)
                    sent = proprecess_money.split_sentence(tr)
                    MON = []
                    for sentence in sent:
                        money = proprecess_money.get_properties_and_values(sentence)
                        MON.append(money)

                    print('PER: {}\nLOC: {}\nORG: {}\nMON: {}'.format(PER, LOC, ORG, MON))
                    # print('DATE: {}\nLOC_ITEM: {}'.format(DATE, LOC_ITEM))
        # except:
        #     print("Error: unable to fecth data")

        db.close()
