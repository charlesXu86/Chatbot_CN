#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: LoadModel.py
@desc:
@time: 2019/03/08
"""

import sys, os
import pickle
from predict import ModelLoader
from predict import show_result
from pipeline import merge_cws
import tensorflow as tf

path = os.path.split(os.path.realpath(__file__))[0] + r'/../lexical_analysis/nnetwork'

class LoadModel(object):
    def __init__(self, model_type='ner'):
        self.session = tf.Session()
        self.model = ModelLoader(path + r'/ckpt/' + model_type + '/bi-lstm.ckpt-6', model_type)
        with open(path + r'/data/' + model_type + '/pkl/dict.pkl', 'rb') as inp:
            self.word2id = pickle.load(inp)
            _ = pickle.load(inp)
            _ = pickle.load(inp)
            self.id2tag = pickle.load(inp)

    def predict(self, sentence):
        return self.model.predict(sentence, self.word2id, self.id2tag)

def show_cws(tag):
    return merge_cws(tag)

def show_pos(tag):
    return show_result(tag)
