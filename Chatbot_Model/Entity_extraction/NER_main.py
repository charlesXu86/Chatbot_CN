# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   NER_main.py
 
@Time    :   2019-07-25 15:32
 
@Desc    :
 
'''

import os
import pickle
import json
import itertools
import tensorflow as tf
import numpy as np

from collections import OrderedDict
from model import Model
from loader import load_sentences, update_tag_scheme
from loader import char_mapping, tag_mapping
from loader import augment_with_pretrained, prepare_dataset
from utils import get_logger, make_path, clean, create_model, save_model
from utils import print_config, save_config, load_config, test_ner
from data_utils import load_word2vec, create_input, input_from_line, BatchManager

from parameters import parameters

class NER():

    def __init__(self):
        self.seg_dim = parameters['seg_dim']
        self.char_dim = parameters['char_dim']
        self.lstm_dim = parameters['lstm_dim']
        self.tag_schema = parameters['tag_schema']
        self.clip = parameters['clip']
        self.dropout = parameters['drop_out']
        self.batch_size = parameters['batch_size']
        self.lr = parameters['lr']
        self.optimizer = parameters['optimizer']
        self.pre_emb = parameters['pre_emb']
        self.zeros = parameters['zeros']
        self.lower = parameters['lower']
        self.max_epoch = parameters['max_epoch']
        self.ckpt_path = parameters['ckpt_path']
        self.summary_path = parameters['summary_path']
        self.log_file = parameters['log_file']
        self.map_file = parameters['map_file']
        self.vocab_file = parameters['vocab_file']
        self.config_file = parameters['config_file']
        self.result_path = parameters['result_path']
        self.emb_file = parameters['emb_file']
        self.train_file = parameters['train_file']
        self.dev_file = parameters['dev_file']
        self.test_file = parameters['test_file']
        self.steps_check = parameters['steps_check']


    def config_model(self, char_to_id, tag_to_id):
        config = OrderedDict()
        config["num_chars"] = len(char_to_id)
        config["num_tags"] = len(tag_to_id)
        config["char_dim"] = self.char_dim

        config["seg_dim"] = self.seg_dim
        config["lstm_dim"] = self.lstm_dim
        config["batch_size"] = self.batch_size

        config["emb_file"] = self.emb_file
        config["clip"] = self.clip
        config["dropout_keep"] = 1.0 - self.dropout
        config["optimizer"] = self.optimizer
        config["lr"] = self.lr
        config["tag_schema"] = self.tag_schema
        config["pre_emb"] = self.pre_emb
        config["zeros"] = self.zeros
        config["lower"] = self.lower
        return config

    def train(self):
        # load data sets
        train_sentences = load_sentences(self.train_file, self.lower, self.zeros)
        dev_sentences = load_sentences(self.dev_file, self.lower, self.zeros)
        test_sentences = load_sentences(self.test_file, self.lower, self.zeros)

        # Use selected tagging scheme (IOB / IOBES)
        update_tag_scheme(train_sentences, self.tag_schema)
        update_tag_scheme(test_sentences, self.tag_schema)

        # create maps if not exist
        if not os.path.isfile(self.map_file):
            # create dictionary for word
            if self.pre_emb:
                dico_chars_train = char_mapping(train_sentences, self.lower)[0]
                dico_chars, char_to_id, id_to_char = augment_with_pretrained(
                    dico_chars_train.copy(),
                    self.emb_file,
                    list(itertools.chain.from_iterable(
                        [[w[0] for w in s] for s in test_sentences])
                    )
                )
            else:
                _c, char_to_id, id_to_char = char_mapping(train_sentences, self.lower)

            # Create a dictionary and a mapping for tags
            _t, tag_to_id, id_to_tag = tag_mapping(train_sentences)
            with open(self.map_file, "wb") as f:
                pickle.dump([char_to_id, id_to_char, tag_to_id, id_to_tag], f)
        else:
            with open(self.map_file, "rb") as f:
                char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)

        # prepare data, get a collection of list containing index
        train_data = prepare_dataset(
            train_sentences, char_to_id, tag_to_id, self.lower
        )
        dev_data = prepare_dataset(
            dev_sentences, char_to_id, tag_to_id, self.lower
        )
        test_data = prepare_dataset(
            test_sentences, char_to_id, tag_to_id, self.lower
        )
        print("%i / %i / %i sentences in train / dev / test." % (
            len(train_data), 0, len(test_data)))

        train_manager = BatchManager(train_data, self.batch_size)
        dev_manager = BatchManager(dev_data, 100)
        test_manager = BatchManager(test_data, 100)
        # make path for store log and model if not exist
        # make_path(FLAGS)
        if os.path.isfile(self.config_file):
            config = load_config(self.config_file)
        else:
            config = self.config_model(char_to_id, tag_to_id)
            save_config(config, self.config_file)

        log_path = os.path.join("log", self.log_file)
        logger = get_logger(log_path)
        print_config(config, logger)

        # limit GPU memory
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        steps_per_epoch = train_manager.len_data
        with tf.Session(config=tf_config) as sess:
            model = create_model(sess, Model, self.ckpt_path, load_word2vec, config, id_to_char, logger)
            logger.info("start training")
            loss = []
            for i in range(100):
                for batch in train_manager.iter_batch(shuffle=True):
                    step, batch_loss = model.run_step(sess, True, batch)
                    loss.append(batch_loss)
                    if step % self.steps_check == 0:
                        iteration = step // steps_per_epoch + 1
                        logger.info("iteration:{} step:{}/{}, "
                                    "NER loss:{:>9.6f}".format(
                            iteration, step % steps_per_epoch, steps_per_epoch, np.mean(loss)))
                        loss = []

                best = self.evaluate(sess, model, "dev", dev_manager, id_to_tag, logger)
                if best:
                    save_model(sess, model, self.ckpt_path, logger)
                self.evaluate(sess, model, "test", test_manager, id_to_tag, logger)

    def evaluate(self, sess, model, name, data, id_to_tag, logger):
        logger.info("evaluate:{}".format(name))
        ner_results = model.evaluate(sess, data, id_to_tag)
        eval_lines = test_ner(ner_results, self.result_path)
        for line in eval_lines:
            logger.info(line)
        f1 = float(eval_lines[1].strip().split()[-1])

        if name == "dev":
            best_test_f1 = model.best_dev_f1.eval()
            if f1 > best_test_f1:
                tf.assign(model.best_dev_f1, f1).eval()
                logger.info("new best dev f1 score:{:>.3f}".format(f1))
            return f1 > best_test_f1
        elif name == "test":
            best_test_f1 = model.best_test_f1.eval()
            if f1 > best_test_f1:
                tf.assign(model.best_test_f1, f1).eval()
                logger.info("new best test f1 score:{:>.3f}".format(f1))
            return f1 > best_test_f1

    def evaluate_line(self, msg):
        config = load_config(self.config_file)
        logger = get_logger(self.log_file)
        # limit GPU memory
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        with open(self.map_file, "rb") as f:
            char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
        with tf.Session(config=tf_config) as sess:
            model = create_model(sess, Model, self.ckpt_path, load_word2vec, config, id_to_char, logger)
            result = model.evaluate_line(sess, input_from_line(msg, char_to_id), id_to_tag)

            return result
