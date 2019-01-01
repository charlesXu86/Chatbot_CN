# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Pre_process.py
   Description :   数据处理
   Author :       charlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""

import json
import os
import xml.etree.ElementTree
from collections import Counter

import jieba
import nltk
from tqdm import tqdm

from Config import output_lang_vocab_size, input_lang_vocab_size, max_len, UNK_token
from Config import train_translation_folder, train_translation_zh_filename, train_translation_en_filename
from Config import valid_translation_folder, valid_translation_zh_filename, valid_translation_en_filename
from Utils import normalizeString, encode_text


def build_wordmap_zh():
    translation_path = os.path.join(train_translation_folder, train_translation_zh_filename)

    with open(translation_path, 'r') as f:
        sentences = f.readlines()

    word_freq = Counter()

    for sentence in tqdm(sentences):
        seg_list = jieba.cut(sentence.strip())
        # Update word frequency
        word_freq.update(list(seg_list))

    # Create word map
    # words = [w for w in word_freq.keys() if word_freq[w] > min_word_freq]
    words = word_freq.most_common(output_lang_vocab_size - 4)
    word_map = {k[0]: v + 4 for v, k in enumerate(words)}
    word_map['<pad>'] = 0
    word_map['<start>'] = 1
    word_map['<end>'] = 2
    word_map['<unk>'] = 3
    print(len(word_map))
    print(words[:10])

    with open('data/WORDMAP_zh.json', 'w') as file:
        json.dump(word_map, file, indent=4)


def build_wordmap_en():
    translation_path = os.path.join(train_translation_folder, train_translation_en_filename)

    with open(translation_path, 'r') as f:
        sentences = f.readlines()

    word_freq = Counter()

    for sentence in tqdm(sentences):
        sentence_en = sentence.strip().lower()
        tokens = [normalizeString(s) for s in nltk.word_tokenize(sentence_en) if len(normalizeString(s)) > 0]
        # Update word frequency
        word_freq.update(tokens)

    # Create word map
    # words = [w for w in word_freq.keys() if word_freq[w] > min_word_freq]
    words = word_freq.most_common(input_lang_vocab_size - 4)
    word_map = {k[0]: v + 4 for v, k in enumerate(words)}
    word_map['<pad>'] = 0
    word_map['<start>'] = 1
    word_map['<end>'] = 2
    word_map['<unk>'] = 3
    print(len(word_map))
    print(words[:10])

    with open('data/WORDMAP_en.json', 'w') as file:
        json.dump(word_map, file, indent=4)


def extract_valid_data():
    valid_translation_path = os.path.join(valid_translation_folder, 'valid.en-zh.en.sgm')
    with open(valid_translation_path, 'r') as f:
        data_en = f.readlines()
    data_en = [line.replace(' & ', ' &amp; ') for line in data_en]
    with open(valid_translation_path, 'w') as f:
        f.writelines(data_en)

    root = xml.etree.ElementTree.parse(valid_translation_path).getroot()
    data_en = [elem.text.strip() for elem in root.iter() if elem.tag == 'seg']
    with open(os.path.join(valid_translation_folder, 'valid.en'), 'w') as out_file:
        out_file.write('\n'.join(data_en) + '\n')

    root = xml.etree.ElementTree.parse(os.path.join(valid_translation_folder, 'valid.en-zh.zh.sgm')).getroot()
    data_zh = [elem.text.strip() for elem in root.iter() if elem.tag == 'seg']
    with open(os.path.join(valid_translation_folder, 'valid.zh'), 'w') as out_file:
        out_file.write('\n'.join(data_zh) + '\n')


def build_samples():
    word_map_zh = json.load(open('data/WORDMAP_zh.json', 'r'))
    word_map_en = json.load(open('data/WORDMAP_en.json', 'r'))

    for usage in ['train', 'valid']:
        if usage == 'train':
            translation_path_en = os.path.join(train_translation_folder, train_translation_en_filename)
            translation_path_zh = os.path.join(train_translation_folder, train_translation_zh_filename)
            filename = 'data/samples_train.json'
        else:
            translation_path_en = os.path.join(valid_translation_folder, valid_translation_en_filename)
            translation_path_zh = os.path.join(valid_translation_folder, valid_translation_zh_filename)
            filename = 'data/samples_valid.json'

        print('loading {} texts and vocab'.format(usage))
        with open(translation_path_en, 'r') as f:
            data_en = f.readlines()

        with open(translation_path_zh, 'r') as f:
            data_zh = f.readlines()

        print('building {} samples'.format(usage))
        samples = []
        for idx in tqdm(range(len(data_en))):
            sentence_zh = data_zh[idx].strip()
            seg_list = jieba.cut(sentence_zh)
            input_zh = encode_text(word_map_zh, list(seg_list))

            sentence_en = data_en[idx].strip().lower()
            tokens = [normalizeString(s) for s in nltk.word_tokenize(sentence_en) if len(normalizeString(s)) > 0]
            output_en = encode_text(word_map_en, tokens)

            if len(input_zh) <= max_len and len(
                    output_en) <= max_len and UNK_token not in input_zh and UNK_token not in output_en:
                samples.append({'input': list(input_zh), 'output': list(output_en)})

        with open(filename, 'w') as f:
            json.dump(samples, f, indent=4)

        print('{} {} samples created at: {}.'.format(len(samples), usage, filename))


if __name__ == '__main__':
    build_wordmap_zh()
    build_wordmap_en()
    extract_valid_data()
    build_samples()
