#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: bert_lstm_ner.py 
@desc:  bert优化ner
@time: 2019/05/09 
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import collections
import os
import tensorflow as tf
import codecs
import pickle

from bert_base.bert import modeling
from bert_base.bert import optimization
from bert_base.bert import tokenization

from bert_base.train.models import create_model, InputFeatures, InputExample


print(tf.__version__)

class DataProcessor(object):
    '''

    '''
    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    @classmethod
    def _read_data(cls, input_file):
        """Reads a BIO data."""
        with codecs.open(input_file, 'r', encoding='utf-8') as f:
            lines = []
            words = []
            labels = []
            for line in f:
                contends = line.strip()
                tokens = contends.split(' ')
                if len(tokens) == 2:
                    words.append(tokens[0])
                    labels.append(tokens[1])
                else:
                    if len(contends) == 0:
                        l = ' '.join([label for label in labels if len(label) > 0])
                        w = ' '.join([word for word in words if len(word) > 0])
                        lines.append([l, w])
                        words = []
                        labels = []
                        continue
                if contends.startswith("-DOCSTART-"):
                    words.append('')
                    continue
            return lines

