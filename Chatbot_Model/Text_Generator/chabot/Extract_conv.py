# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Extract_conv.py
   Description :  把 dgk_shooter_min.conv 文件格式转换为可训练格式
   Author :       charl
   date：          2018/12/12
-------------------------------------------------
   Change Activity: 2018/12/12:
-------------------------------------------------
"""

import re
import sys
import pickle
import jieba
import numpy as np

from tqdm import tqdm
from word_sequence import WordSequence

# sys.path.append('..')


def make_split(line):
    """构造合并两个句子之间的符号
    """
    if re.match(r'.*([，。…？！～\.,!?])$', ''.join(line)):
        return []
    return ['，']


def good_line(line):
    """判断一个句子是否好"""
    if len(re.findall(r'[a-zA-Z0-9]', ''.join(line))) > 2:
        return False
    return True


def regular(sen):
    """整理句子"""
    sen = re.sub(r'\.{3,100}', '…', sen)
    sen = re.sub(r'…{2,100}', '…', sen)
    sen = re.sub(r'[,]{1,100}', '，', sen)
    sen = re.sub(r'[\.]{1,100}', '。', sen)
    sen = re.sub(r'[\?]{1,100}', '？', sen)
    sen = re.sub(r'[!]{1,100}', '！', sen)
    return sen


def main(limit=20, x_limit=3, y_limit=6):
    """执行程序
    Args:
        limit: 只输出句子长度小于limit的句子
    """
    print('load pretrained vec')
    word_vec_path = 'D:\project\Chatbot_CN\Chatbot_Data\Text_generator\word_vec.pkl'
    word_vec = pickle.load(open(word_vec_path, 'rb'))

    print('extract lines')
    data_path = 'D:\project\Chatbot_CN\Chatbot_Data\Text_generator\dgk_shooter_min.conv'
    # fp = open('dgk_shooter_min.conv', 'r', errors='ignore')
    fp = open(data_path, 'r', encoding='utf-8', errors='ignore')
    last_line = None
    groups = []
    group = []
    for line in tqdm(fp):
        if line.startswith('M '):
            line = line.replace('\n', '')
            if '/' in line:
                line = line[2:].split('/')
            else:
                line = list(line[2:])
            line = line[:-1]
            group.append(jieba.lcut(regular(''.join(line))))
        else: # if line.startswith('E'):
            last_line = None
            if group:
                groups.append(group)
                group = []
    if group:
        groups.append(group)
        group = []
    print('extract groups')
    x_data = []
    y_data = []
    for group in tqdm(groups):
        for i, line in enumerate(group):
            last_line = None
            if i > 0:
                last_line = group[i - 1]
                if not good_line(last_line):
                    last_line = None
            next_line = None
            if i < len(group) - 1:
                next_line = group[i + 1]
                if not good_line(next_line):
                    next_line = None
            next_next_line = None
            if i < len(group) - 2:
                next_next_line = group[i + 2]
                if not good_line(next_next_line):
                    next_next_line = None

            if next_line:
                x_data.append(line)
                y_data.append(next_line)
            # if last_line and next_line:
            #     x_data.append(last_line + make_split(last_line) + line)
            #     y_data.append(next_line)
            # if next_line and next_next_line:
            #     x_data.append(line)
            #     y_data.append(next_line + make_split(next_line) \
            #         + next_next_line)

    print(len(x_data), len(y_data))
    for ask, answer in zip(x_data[:20], y_data[:20]):
        print(''.join(ask))
        print(''.join(answer))
        print('-' * 20)

    data = list(zip(x_data, y_data))
    data = [
        (x, y)
        for x, y in data
        if len(x) < limit \
        and len(y) < limit \
        and len(y) >= y_limit \
        and len(x) >= x_limit
    ]
    x_data, y_data = zip(*data)

    print('refine train data')

    train_data = x_data + y_data

    # good_train_data = []
    # for line in tqdm(train_data):
    #     good_train_data.append([
    #         x for x in line
    #         if x in word_vec
    #     ])
    # train_data = good_train_data

    print('fit word_sequence')

    ws_input = WordSequence()

    ws_input.fit(train_data, max_features=100000)

    print('dump word_sequence')

    pickle.dump(
        (x_data, y_data, ws_input),
        open('chatbot.pkl', 'wb')
    )

    print('make embedding vecs')

    emb = np.zeros((len(ws_input), len(word_vec['</s>'])))

    np.random.seed(1)
    for word, ind in ws_input.dict.items():
        if word in word_vec:
            emb[ind] = word_vec[word]
        else:
            emb[ind] = np.random.random(size=(300,)) - 0.5

    print('dump emb')

    pickle.dump(
        emb,
        open('emb.pkl', 'wb')
    )

    print('done')


if __name__ == '__main__':
    main()
