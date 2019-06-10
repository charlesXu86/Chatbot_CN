#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: data_helper.py
@desc: fasttext文本分类数据处理
@time: 2019/05/23
"""


from Chatbot_Model.Text_Classification.Fasttext.parameters import parameters
from collections import Counter
import os
import json
import numpy as np
import re


def process_data(config):
    """
    文本格式
    :param config:
    :return:
    """
    data_path = config['data_path']
    sequence_length = config['sequence_length']
    X = []
    y = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            lis = line.strip().split('\t')
            ss = re.sub('\s+', '', lis[1])
            X.append(re.sub('\s+', '', lis[1])[:sequence_length])
            y.append(lis[0])
    return X, y


def generate_vocab(X, y, config):
    words = []
    for sent in X:
        words.extend(list(sent))
    words = Counter(words).most_common(config['vocab_size']-1)

    word_to_index = {}
    index_to_word = {}
    for i in range(len(words)):
        word_to_index[words[i][0]] = i+1
        index_to_word[int(i+1)] = words[i][0]

    word_to_index['UNK'] = 0
    index_to_word[int(0)] = 'UNK'

    label_to_index = {}
    index_to_label = {}
    labels = set(y)

    for i, label in enumerate(labels):
        label_to_index[label] = i
        index_to_label[int(i)] = label

    vocab_path = config['vocab_path']

    if not os.path.exists(vocab_path):
        os.mkdir(vocab_path)

    with open(os.path.join(vocab_path, 'word_to_index.json'), 'w', encoding='utf-8') as f:
        json.dump(word_to_index, f, ensure_ascii=False)

    with open(os.path.join(vocab_path, 'index_to_word.json'), 'w', encoding='utf-8') as f:
        json.dump(index_to_word, f, ensure_ascii=False)

    with open(os.path.join(vocab_path, 'label_to_index.json'), 'w', encoding='utf-8') as f:
        json.dump(label_to_index, f, ensure_ascii=False)

    with open(os.path.join(vocab_path, 'index_to_label.json'), 'w', encoding='utf-8') as f:
        json.dump(index_to_label, f, ensure_ascii=False)

    return word_to_index, label_to_index


def padding(X, y, config, word_to_index, label_to_index):
    '''
    padding 长度不够的文本会在后面补0
    :param X:
    :param y:
    :param config:
    :param word_to_index:
    :param label_to_index:
    :return:
    '''
    sequence_length = config['sequence_length']
    num_classes = config['num_classes']
    input_x = []
    for line in X:
        temp = []
        for item in list(line):
            temp.append(word_to_index.get(item, 0))
        input_x.append(temp[:sequence_length]+[0]*(sequence_length-len(temp)))
    if not y:
        return input_x

    input_y = []
    for item in y:
        temp = [0] * num_classes
        temp[label_to_index[item]] = 1
        input_y.append(temp)
    return input_x, input_y


def split_data(input_x, input_y, config):
    rate = config['train_test_dev_rate']
    shuffle_indices = np.random.permutation(np.arange(len(input_y)))
    # print(shuffle_indices)
    # print(input_y)
    x_shuffled = np.array(input_x)[shuffle_indices]
    y_shuffled = np.array(input_y)[shuffle_indices]
    x_train, y_train = x_shuffled[: int(rate[0]*len(input_y))], y_shuffled[: int(rate[0]*len(input_y))]
    x_test, y_test = x_shuffled[int(rate[0]*len(input_y)): int(sum(rate[:2])*len(input_y))], \
                     y_shuffled[int(rate[0]*len(input_y)): int(sum(rate[:2])*len(input_y))]
    x_dev, y_dev = x_shuffled[int(sum(rate[:2])*len(input_y)): ], y_shuffled[int(sum(rate[:2])*len(input_y)): ]
    return x_train, y_train, x_test, y_test, x_dev, y_dev


def generate_batchs(x_train, y_train, config, shuffle=True):
    '''
     生成batch数据
    :param x_train:
    :param y_train:
    :param config:
    :param shuffle:
    :return:
    '''
    data = np.array(list(zip(x_train, y_train)))
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/config['batch_size']) + 1
    for epoch in range(config['num_epochs']):
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffle_data = data[shuffle_indices]
        else:
            shuffle_data = data

        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * config['batch_size']
            end_index = min((batch_num+1)*config['batch_size'], data_size)
            yield shuffle_data[start_index: end_index]


def load_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.loads(f.read(), encoding='utf-8')


# if __name__ == '__main__':
#     generate_vocab(['abcd', 'dbgj'], [1, 0], config)