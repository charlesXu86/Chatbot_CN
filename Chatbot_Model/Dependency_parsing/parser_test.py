#!/usr/bin/env python
# coding=utf-8
import os
import time
import sys
import tensorflow as tf
import numpy as np
from base_model import Model
from Params_init import random_uniform_initializer, random_normal_initializer, xavier_initializer

sys.path.append(r'../utils/')

from general_utils import Progbar
from general_utils import get_minibatches
from feature_extraction import load_datasets, DataConfig, Flags, punc_pos, pos_prefix
from tf_utils import visualize_sample_embeddings
from Parser_model import ParserModel


ckpt_path = tf.train.latest_checkpoint(os.path.join(DataConfig.data_dir_path,
                                                    DataConfig.model_dir))

def highlight_string(temp):
    print 80 * "="
    print temp
    print 80 * "="

class ParserLoader(object):
    def __init__(self, ckpt_path, word, pos):
        self.sess = tf.Session()
        self.ckpt_path = ckpt_path
        self.list_word = word
        self.list_pos = pos

        highlight_string("INITIALIZING")
        print "loading data.."
      
        #self.list_word = [u"世界", u"第", u"八", u"大", u"奇迹", u"出现"]
        #self.list_pos = [u"n",u"m",u"m",u"a",u"n",u"v"]

        self.dataset = load_datasets(self.list_word, self.list_pos, False, True)
        self.config = self.dataset.model_config
                       
        if not os.path.exists(os.path.join(DataConfig.data_dir_path, DataConfig.model_dir)):
            os.makedirs(os.path.join(DataConfig.data_dir_path, DataConfig.model_dir))              
        print "Building network...",
        start = time.time()
        with tf.variable_scope("par_model") as model_scope:
            self.model = ParserModel(self.config, self.dataset.word_embedding_matrix, 
                                     self.dataset.pos_embedding_matrix, self.dataset.dep_embedding_matrix)
            saver = tf.train.Saver()

        if ckpt_path is not None:               
            print "Found checkpoint! Restoring variables.."
            saver.restore(self.sess, ckpt_path)
        else:                      
            print 'Model not found, creat with fresh parameters....'
            self.sess.run(tf.global_variables_initializer()) 

    def predict(self, model, dataset ):
        highlight_string("Testing.....")         
        model.compute_dependencies(self.sess, dataset.test_data, dataset)
        test_UAS,test_LAS, token_num, token_dep = model.get_UAS(dataset.test_data)
        #self.print_conll(token_num, token_dep)
        return test_UAS, test_LAS, token_num, token_dep
    
    def print_conll(self, token_num, token_dep):
        for i in range(len(self.list_word)):
            print str(i+1) + " " + str(self.list_word[i]) + \
                    " " + str(self.list_word[i]) +" " + str(self.list_pos[i])\
                    + " " + str(self.list_pos[i]) + " " + "_" + " " + \
                    str(token_num[i]+1) + " " + str(token_dep[0][i].split(":")[1])



def main():

    word = [u"世界", u"第", u"八", u"大", u"奇迹", u"出现"]
    pos = [u"n",u"m",u"m",u"a",u"n",u"v"]
    parser = ParserLoader(ckpt_path, word, pos)
    UAS, LAS, token_num, token_dep =  parser.predict(parser.model, parser.dataset)
    parser.print_conll(token_num, token_dep)

if __name__ == '__main__':
    main()
