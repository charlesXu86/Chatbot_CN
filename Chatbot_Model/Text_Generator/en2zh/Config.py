# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Config.py
   Description :   模型参数配置文件
   Author :       charlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""

import json
import os

import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Configure training/optimization
clip = 50.0
teacher_forcing_ratio = .5
learning_rate = 0.0001
n_iteration = 4000
print_every = 100
save_every = 1
workers = 1
max_len = 10  # Maximum sentence length to consider
min_word_freq = 20  # Minimum word count threshold for trimming
save_dir = 'models'
input_lang_vocab_size = 5000
output_lang_vocab_size = 5000

# Configure models
model_name = 'cb_model'
attn_model = 'general'
start_epoch = 0
epochs = 120
hidden_size = 500
encoder_n_layers = 2
decoder_n_layers = 2
dropout = 0.05
chunk_size = 100
train_split = 0.9

train_folder = 'data/ai_challenger_translation_train_20170912'
valid_folder = 'data/ai_challenger_translation_validation_20170912'
test_a_folder = 'data/ai_challenger_translation_test_a_20170923'
test_b_folder = 'data/ai_challenger_translation_test_b_20171128'
train_translation_folder = os.path.join(train_folder, 'translation_train_20170912')
valid_translation_folder = os.path.join(valid_folder, 'translation_validation_20170912')
train_translation_en_filename = 'train.en'
train_translation_zh_filename = 'train.zh'
valid_translation_en_filename = 'valid.en'
valid_translation_zh_filename = 'valid.zh'

# num_train_samples = 8206380
# num_valid_samples = 7034

# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token
UNK_token = 3

start_word = '<start>'
stop_word = '<end>'
unknown_word = '<unk>'


class Lang:
    def __init__(self, filename):
        word_map = json.load(open(filename, 'r'))
        self.word2index = word_map
        self.index2word = {v: k for k, v in word_map.items()}
        self.n_words = len(word_map)



