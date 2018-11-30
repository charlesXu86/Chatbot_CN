# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     data_read_POS.py
   Description :   POS-tagging预处理
   Author :       charl
   date：          2018/9/12
-------------------------------------------------
   Change Activity: 2018/9/12:
-------------------------------------------------
"""

import os, re
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf

from collections import Counter

tf.app.flags.DEFINE_string('corpus_path', '/2014', 'corpus path')
tf.app.flags.DEFINE_string('dict_path', 'data/pos.pkl', 'dict path')

pos = pd.read_csv('./pos.csv')


vocab_to_int_l = {label: ii for ii, label in enumerate(list(pos['POS']), 1)}

FLAGS = tf.app.flags.FLAGS

class DataHandler(object):
    def __init__(self, rootDir=FLAGS.corpus_path):
        self.rootDir = rootDir

    def loadRowData(self):
        self.all_sentences = list()   # 全文词集合（有一定格式）
        self.all_labels = list()      # 全文词性集合（有一定格式）
        self.labels = list()          # 全文词性统计
        self.words = list()           # 全文字统计

        if self.rootDir:
            for dirName, subdirList, fileList in os.walk(self.rootDir):
                for file in fileList:
                    if file.endswith(".txt"):

                        curFile = os.path.join(dirName, file)
                        print("processing:%s" % (curFile))
                        with open(curFile, "r", encoding='utf-8') as fp:
                            for line in fp.readlines():  # 段
                                if len(line) > 1:  # 消除空句影响
                                    line = line.strip()
                                    self.processLine(line)

            print('number of words is %d' % len(self.words))
            print('number of sentences is %d' % len(self.all_sentences))
            print('Example of sentences: ', self.all_sentences[9])
            print('Example of labels:', self.all_labels[9])

    # 处理数据中'['、']'等无效符号
    def processLine(self, line):
        self.sentence = list()  # 句集合
        self.label_p_sent = list()  # 句词性集合

        word = line.split(' ')
        if len(word) > 1:
            for i in word:
                if len(i) > 1:
                    i = i.replace('[', '').replace(']', '')

                    token = i.split('/')
                    if len(token) > 1:
                        self.words.append(token[0])  # 为实现字计数以及word2int
                        self.sentence.append(token[0])
                        if token[1] in vocab_to_int_l:
                            self.labels.append(token[1])  # 为实现词性计数以及label2int
                            self.label_p_sent.append(token[1])
                        else:
                            self.labels.append('n')  # 容忍性错标，已统计错标率非常小，不影响训练误差。
                            self.label_p_sent.append('n')

        self.all_sentences.append(self.sentence)
        self.all_labels.append(self.label_p_sent)

data = DataHandler()
data.loadRowData()


counts_w = Counter(data.words)
vocab_w = sorted(counts_w, key=counts_w.get(), reverse=True)
vocab_to_int_w = {word: ii for ii, word in enumerate(vocab_w, 1)}

words_ints = []
labels_ints = []

for each in data.all_sentences:
    words_ints.append([vocab_to_int_w[word] for word in each])  # 生成word2id
for each in data.all_labels:
    labels_ints.append([vocab_to_int_l[label] for label in each]) # 生成label2id

non_zero_idx = [ii for ii, sent in enumerate(words_ints) if len(sent) != 0]

words_ints = [words_ints[ii] for ii in non_zero_idx]
labels_ints = [labels_ints[ii] for ii in non_zero_idx]

seq_len = 200
features_ = np.zeros((len(words_ints), seq_len), dtype=int)
labels_ = np.zeros((len(labels_ints), seq_len), dtype=int)

for i, row in enumerate(words_ints):
    features_[i, :len(row)] = np.array(row)[:seq_len]
for i, row in enumerate(labels_ints):
    labels_[i :len(row)] = np.array(row)[:seq_len]

save_p = FLAGS.dict_path
with open(save_p, 'wb') as outp:
    pickle.dump(features_, outp)
    pickle.dump(labels_, outp)
    pickle.dump(vocab_to_int_w, outp)
    pickle.dump(vocab_to_int_l, outp)
    print('** Finished saving the data.')






