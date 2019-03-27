#-*- coding: utf-8 -*-
# @Author  : CharlesXu
# @File    : Text_preprocessing.py
# Desc     : 数据预处理

import logging
import pickle
import re
import time

import jieba.posseg as pseg
import jieba.analyse
import numpy as np
import sklearn

with open('stopwords.txt', 'rb') as f:
    STOPWORDS = pickle.load(f)

DIGITS = re.compile(r"\d+")
CHARS = re.compile(r"[a-zA-Z]+")
SPACES = re.compile(r"\s+")

def rawdata_split(rawdata, wrangledtext_path, segdlabel_path):
    '''
    split rawdata into wrangled text and labels, rawdata contains labels in the first column and
    texts in the second column which separated by `##TAP##`
    :param rawdata:
    :param wrangledtext_path:
    :param segdlabel_path:
    :return:
    '''
    labels = []
    with open(rawdata, 'r', encoding='utf-8') as rf:
        with open(wrangledtext_path, 'w', encoding='utf-8') as wf:
            cnt = 0
            for i, line in enumerate(rf.readlines()):
                split_line = line.split("##TAP##")
                try:
                    label = int(split_line[0])
                except ValueError:
                    print("The first column is not label，strip %s" % (i+1))
                    continue
                except Exception as e:
                    print("wrong: ",e)
                    continue
                try:
                    if len(split_line) == 3:
                        wf.write(split_line[1] + split_line[2])
                        labels.append(label)
                        cnt += 1
                except Exception as e:
                    print(e)
    label_array = np.zeros((len(labels), 3))
    for i in range(len(labels)):
        if labels[i] == 1:
            label_array[i,0] = 1
        elif labels[i] == -1:
            label_array[i,1] = 1
        else:
            label_array[i,2] = 1

    with open(segdlabel_path, 'wb') as f:
        pickle.dump(label_array, f)
    print("write row：%s, labels length: %s" % (cnt,len(label_array)))


def remove_words(word_list):
    words_list = (pair.word for pair in word_list if pair.word not in STOPWORDS and pair.word != " " and len(pair.word)>=2
    and pair.flag not in ['w', 'ns', 'nr', 'nz', 't', 'r', 'u', 'e', 'y', 'o', 'f', 'q', 'un'])

    return words_list


def seg_words(sentence):

    sent = re.sub(SPACES, ' ', sentence)
    sent = re.sub(DIGITS, ' ', sent)
    sent = re.sub(CHARS, ' ', sent)

    word_gen = pseg.cut(sent.strip())
    words_list = remove_words(word_gen)

    return words_list


def text_preprocess(sentences, segedtext_path):
    with open(segedtext_path, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            words = seg_words(sentence)
            f.write(" ".join(words) + ' \n')


def yield_line(file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            yield line


def build_vocab(seged_text, save_path, vocab_size=100000):
    text = open(seged_text, 'r', encoding='utf-8').read()
    tfidf = jieba.analyse.extract_tags(text, topK=vocab_size, withWeight=False)
    word2index = {}
    for i, word in enumerate(tfidf):
        word2index[word] = i+1
    word2index['UNK'] = 0
    with open(save_path, 'wb') as f:
        pickle.dump(word2index, f)


def index_word(seged_text, word2index_path, save_indexed_word_path):
    textlist = []
    with open(word2index_path, 'rb') as f:
        word2index = pickle.load(f)

    with open(seged_text, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            sep_line = line.split(" ")
            textlist.append([word2index[word] if word in word2index else word2index['UNK'] for word in sep_line])

    with open(save_indexed_word_path, 'wb') as f:
        pickle.dump(textlist, f)


def pad_sentence(sentence_batch, pad_int=0):
    max_len = max(len(sentence) for sentence in sentence_batch)
    padded_sentences = []
    seq_len = []
    for sentence in sentence_batch:
        padded_sentences.append(sentence + [pad_int] * (max_len - len(sentence)))
        seq_len.append(len(sentence))
    return padded_sentences, seq_len


def batch_iter(X, y, batch_size, num_epoch, shuffle=True):
    '''

    :param X: 
    :param y: 
    :param batch_size: batch size
    :param num_epoch: 
    :param shuffle: defualt True
    :return:
    '''
    if shuffle:
        data_list = sklearn.utils.shuffle(X, y)
    else:
        data_list = [X, y]
    cnt = 1
    for epoch in range(num_epoch):
        print("epoch: {}".format(cnt))
        for i in range(0, len(X), batch_size):
            padded_sentences, seq_lens = pad_sentence(data_list[0][i:i + batch_size])
            label_y = data_list[1][i:i + batch_size]

            yield padded_sentences, seq_lens, label_y

        cnt += 1


def PrintLog(log_name):
    # Logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_log = logging.FileHandler(log_name, mode='w')
    file_log.setLevel(level=logging.INFO)
    console_log = logging.StreamHandler()
    console_log.setLevel(level=logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    file_log.setFormatter(formatter)
    console_log.setFormatter(formatter)
    logger.addHandler(file_log)
    logger.addHandler(console_log)

    return logger



if __name__ == "__main__":
    t = time.time()
    # rawdata_split('raw_data.txt', 'wrangled_text.txt', 'label_array.txt')
    # print("split data time：", time.time()-t)
    # t = time.time()
    # text_preprocess(yield_line('wrangled_text.txt'), 'seged_text.txt')
    # build_vocab("seged_text.txt","word2index.txt")
    index_word('seged_text.txt', 'word2index.txt', 'indexed_words.txt')
    print("time ", time.time()-t)

