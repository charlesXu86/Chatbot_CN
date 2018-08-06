# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     data_helper
   Description : 数据预处理
   Author :       charl
   date：          2018/8/3
-------------------------------------------------
   Change Activity:
                   2018/8/3:
-------------------------------------------------
"""

import sys
import numpy as np
import pickle as pkl
import re
import itertools
import time
import gc
import gzip


from collections import Counter
from tensorflow.contrib import learn
from gensim.models.word2vec import Word2Vec
from random import random
from preprocess import MyVocabularyProcessor

class InputHelper(object):
    pre_emb = dict()
    vocab_processor = None

    def cleanText(self, s):
        s = re.sub(r"[^\x00-\x7F]+", " ", s)
        s = re.sub(r'[\~\!\`\^\*\{\}\[\]\#\<\>\?\+\=\-\_\(\)]+', "", s)
        s = re.sub(r'( [0-9,\.]+)', r"\1 ", s)
        s = re.sub(r'\$', " $ ", s)
        s = re.sub('[ ]+', ' ', s)
        return s.lower()

    def getVocab(self, vocab_path, max_document_length, filter_h_pad):
        if self.vocab_processor == None:
            print("Loading vocab")
            vocab_processor = MyVocabularyProcessor(max_document_length - filter_h_pad, min_frequency=0)
            self.vocab_processor = vocab_processor.restore(vocab_path)
        return self.vocab_processor

    def loadW2V(self, emb_path, type="bin"):
        print("Loading W2V data...")
        num_keys = 0
        if type == "textgz":
            for line in gzip.open(emb_path):
                l = line.strip().split()
                st = l[0].lower()
                self.pre_emb[st] = np.asarray(l[1:])
            num_keys = len(self.pre_emb)
        else:
            self.pre_emb = Word2Vec.load_word2vec_format(emb_path, binary=True)
            # self.wv.init_sims
            self.pre_emb.init_sims(replace=True)
            num_keys = len(self.pre_emb.vocab)
        print("Loaded word2vec len", num_keys)
        gc.collect()

    def deletePreEmb(self):
        self.pre_emb = dict()
        gc.collect()

    def getTsvData(self, filePath):
        print("Loading training data from" + filePath)
        x1 = []
        x2 = []
        y = []
        # positive samples from file
        for line in open(filePath):
            l = line.strip().split("\t")
            if len(l) < 2:
                continue
            if random() > 0.5:
                x1.append(l[0].lower())
                x2.append(l[1].lower())
            else:
                x1.append(l[1].lower())
                x2.append(l[2].lower())
            y.append(int(l[2]))
        return np.asarray(x1), np.asarray(x2), np.asarray(y)

    def getTsvDataCharBased(self, filepath):
        print("Loading training data from" + filepath)
        x1 = []
        x2 = []
        y = []

        # positive samples from file
        for line in open(filepath):
            l = line.strip().split("\t")
            if len(l) < 2:
                continue
            if random() > 0.5:
                x1.append(l[0].lower())
                x2.append(l[1].lower())
            else:
                x1.append(l[1].lower())
                x2.append(l[0].lower())
            y.append(1)  # np.array([0,1]))
        # generate random negative samples
        combined = np.asarray(x1 + x2)

        # 有时候我们有随机打乱一个数组的需求，例如训练时随机打乱样本，我们可以使用 numpy.random.shuffle() 或者 numpy.random.permutation() 来完成。
        # shuffle 的参数只能是 array_like，而 permutation 除了 array_like 还可以是 int 类型，如果是 int 类型，那就随机打乱 numpy.arange(int)。
        # shuffle 返回 None，这点尤其要注意，也就是说没有返回值，而 permutation 则返回打乱后的 array。
        shuffle_indices = np.random.permutation(np.arange(len(combined)))
        combined_shuff = combined[shuffle_indices]
        for i in range(len(combined)):
            x1.append(combined[i])
            x2.append(combined_shuff[i])
            y.append(0)  # np.array([1,0]))
        return np.asarray(x1), np.asarray(x2), np.asarray(y)

    def getTsvTestData(self, filepath):
        print("Loading testing/labelled data from " + filepath)
        x1 = []
        x2 = []
        y = []
        # positive samples from file
        for line in open(filepath):
            l = line.strip().split("\t")
            if len(l) < 3:
                continue
            x1.append(l[1].lower())
            x2.append(l[2].lower())
            y.append(int(l[0]))  # np.array([0,1]))
        return np.asarray(x1), np.asarray(x2), np.asarray(y)

    def batch_iter(self, data, batch_size, num_epochs, shuffle=True):
        '''
        Generate a batch iterators for a dataset
        :param data:
        :param batch_size:
        :param num_epochs:
        :param shuffle:
        :return:
        '''
        data = np.asarray(data)
        print(data)
        print(data.shape)
        data_size = len(data)
        num_batches_per_epoch = int(len(data) / batch_size) + 1
        for epoch in range(num_epochs):
            # Shuffle the data at each epoch
            if shuffle:
                shuffle_indices = np.random.permutation(np.arange(data_size))
                shuffled_data = data[shuffle_indices]
            else:
                shuffled_data = data
            for batch_num in range(num_batches_per_epoch):
                start_index = batch_num * batch_size
                end_index = min((batch_num + 1) * batch_size, data_size)
                yield shuffled_data[start_index : end_index]

    def dumpValidation(self, x1_text, x2_text, y, shuffled_index, dev_idx, i):
        print("Dunmping validation" + str(i))
        x1_shuffled = x1_text[shuffled_index]
        x2_shuffled = x2_text[shuffled_index]
        y_shuffled = y[shuffled_index]
        x1_dev = x1_shuffled[dev_idx:]
        x2_dev = x2_shuffled[dev_idx:]
        y_dev = y_shuffled[dev_idx:]
        del x1_shuffled
        del y_shuffled
        with open('validation.txt' + str(i), 'w') as f:
            for text1, text2, label in zip(x1_dev, x2_dev, y_dev):
                f.write(str(label) + "\t" + text1 + "\t" + text2 + "\n")
            f.close()
        del x1_dev
        del y_dev

    def getDataSets(self, training_paths, max_document_length, percent_dev, batch_size, is_char_based):
        if is_char_based:
            x1_text, x2_text, y = self.getTsvDataCharBased(training_paths)
        else:
            x1_text, x2_text, y = self.getTsvData(training_paths)

        #Build vocabulary
        print("Building vocabulary")
        vocab_processor = MyVocabularyProcessor(max_document_length, min_frequency=0, is_char_based=is_char_based)
        vocab_processor.fit_transform(np.concatenate((x2_text, x1_text), axis=0))
        print("Length of loaded vocabulary = {}".format(len(vocab_processor.vocabulary_)))
        il = 0
        train_set = []
        sum_no_of_batches = 0
        x1 = np.asarray(list(vocab_processor.transform(x1_text)))
        x2 = np.asarray(list(vocab_processor.transform(x2_text)))

        # Random shuffle data
        np.random.seed(131)
        shuffle_indices = np.random.permutation(np.arange(len(y)))
        x1_shuffled = x1[shuffle_indices]
        x2_shuffled = x2[shuffle_indices]
        y_shuffled = y[shuffle_indices]
        dev_idx = -1 * len(y_shuffled) * percent_dev // 100
        del x1
        del x2

        # split train/test data
        self.dumpValidation(x1_text, x2_text, y, shuffle_indices, dev_idx, 0)
        # TODO: This is very crude, should use cross-validation
        x1_train, x1_dev = x1_shuffled[:dev_idx], x1_shuffled[dev_idx:]
        x2_train, x2_dev = x2_shuffled[:dev_idx], x2_shuffled[dev_idx:]
        y_train, y_dev = y_shuffled[:dev_idx], y_shuffled[dev_idx:]
        print("Train/Dev split for {}: {:d}/{:d}".format(training_paths, len(y_train), len(y_dev)))
        sum_no_of_batches = sum_no_of_batches + (len(y_train) // batch_size)
        train_set = (x1_train, x2_train, y_train)
        dev_set = (x1_dev, x2_dev, y_dev)
        gc.collect()
        return train_set, dev_set, vocab_processor, sum_no_of_batches

    def getTestDataSet(self, data_path, vocab_path, max_document_length):
        x1_temp, x2_temp, y = self.getTsvTestData(data_path)

        # Build vocabulary
        vocab_processor = MyVocabularyProcessor(max_document_length, min_frequency=0)
        vocab_processor = vocab_processor.restore(vocab_path)
        print(len(vocab_processor.vocabulary_))

        x1 = np.asarray(list(vocab_processor.transform(x1_temp)))
        x2 = np.asarray(list(vocab_processor.transform(x2_temp)))
        # Randomly shuffle data
        del vocab_processor
        gc.collect()
        return x1, x2, y












