# -*- coding:utf-8 -*-
# Filename: convert_corpus.py
# Author：hankcs
# Date: 2017-08-08 AM10:45

"""
Convert and preprocess original space separated corpus to bmes tagged corpus
"""
import os
import re

from utils import make_sure_path_exists, append_tags


def normalize(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def preprocess(text):
    rNUM = u'(-|\+)?\d+((\.|·)\d+)?%?'
    rENG = u'[A-Za-z_.]+'
    sent = normalize(text.strip()).split()
    new_sent = []
    for word in sent:
        word = re.sub(u'\s+', '', word, flags=re.U)
        word = re.sub(rNUM, u'0', word, flags=re.U)
        word = re.sub(rENG, u'X', word)
        new_sent.append(word)
    return new_sent


def to_sentence_list(text, split_long_sentence=False):
    text = preprocess(text)
    delimiter = set()
    delimiter.update(u'。！？：；…、，,;!?、,')
    delimiter.add(u'……')
    sent_list = []
    sent = []
    for word in text:
        sent.append(word)
        if word in delimiter or (split_long_sentence and len(sent) >= 50):
            sent_list.append(sent)
            sent = []

    if len(sent) > 0:
        sent_list.append(sent)

    return sent_list


def convert_file(src, des, split_long_sentence=False):
    with open(src) as src, open(des, 'w') as des:
        for line in src:
            for sent in to_sentence_list(line, split_long_sentence):
                des.write(' '.join(sent) + '\n')
                # if len(''.join(sent)) > 200:
                #     print(' '.join(sent))


def split_train_dev(dataset):
    root = 'data/' + dataset + '/raw/'
    with open(root + 'train-all.txt') as src, open(root + 'train.txt', 'w') as train, open(root + 'dev.txt',
                                                                                           'w') as dev:
        lines = src.readlines()
        idx = int(len(lines) * 0.9)
        for line in lines[: idx]:
            train.write(line)
        for line in lines[idx:]:
            dev.write(line)


def combine_files(one, two, out):
    if os.path.exists(out):
        os.remove(out)
    with open(one) as one, open(two) as two, open(out, 'a') as out:
        for line in one:
            out.write(line)
        for line in two:
            out.write(line)


def bmes_tag(input_file, output_file):
    with open(input_file) as input_data, open(output_file, 'w') as output_data:
        for line in input_data:
            word_list = line.strip().split()
            for word in word_list:
                if len(word) == 1 or (len(word) > 2 and word[0] == '<' and word[-1] == '>'):
                    output_data.write(word + "\tS\n")
                else:
                    output_data.write(word[0] + "\tB\n")
                    for w in word[1:len(word) - 1]:
                        output_data.write(w + "\tM\n")
                    output_data.write(word[len(word) - 1] + "\tE\n")
            output_data.write("\n")


def make_bmes(dataset='pku'):
    path = 'data/' + dataset + '/'
    make_sure_path_exists(path + 'bmes')
    bmes_tag(path + 'raw/train.txt', path + 'bmes/train.txt')
    bmes_tag(path + 'raw/train-all.txt', path + 'bmes/train-all.txt')
    bmes_tag(path + 'raw/dev.txt', path + 'bmes/dev.txt')
    bmes_tag(path + 'raw/test.txt', path + 'bmes/test.txt')


def convert_bakeoff2005_dataset(dataset):
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')
    convert_file('data/bakeoff2005/{}_training.utf8'.format(dataset), 'data/{}/raw/train-all.txt'.format(dataset), True)
    convert_file('data/bakeoff2005/{}_test_gold.utf8'.format(dataset), 'data/{}/raw/test.txt'.format(dataset), False)
    split_train_dev(dataset)


def convert_sxu():
    dataset = 'sxu'
    print('Converting corpus {}'.format(dataset))
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')
    convert_file('data/bakeoff2008/{}/train.txt'.format(dataset), 'data/{}/raw/train-all.txt'.format(dataset), True)
    convert_file('data/bakeoff2008/{}/test.txt'.format(dataset), 'data/{}/raw/test.txt'.format(dataset), False)
    split_train_dev(dataset)
    make_bmes(dataset)


def convert_wiki():
    dataset = 'wiki'
    print('Converting corpus {}'.format(dataset))
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')
    convert_file('data/wiki/generated.train.txt', 'data/{}/raw/train.txt'.format(dataset), True)
    convert_file('data/wiki/generated.dev.txt', 'data/{}/raw/dev.txt'.format(dataset), True)
    convert_file('data/wiki/generated.test.txt', 'data/{}/raw/test.txt'.format(dataset), False)
    combine_files('data/{}/raw/train.txt'.format(dataset), 'data/{}/raw/dev.txt'.format(dataset),
                  'data/{}/raw/train-all.txt'.format(dataset))
    make_bmes(dataset)


def convert_ctb():
    dataset = 'ctb'
    print('Converting corpus {}'.format(dataset))
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')
    convert_file('data/ctb/ctb6.train.seg', 'data/{}/raw/train.txt'.format(dataset), True)
    convert_file('data/ctb/ctb6.dev.seg', 'data/{}/raw/dev.txt'.format(dataset), True)
    convert_file('data/ctb/ctb6.test.seg', 'data/{}/raw/test.txt'.format(dataset), False)
    combine_files('data/{}/raw/train.txt'.format(dataset), 'data/{}/raw/dev.txt'.format(dataset),
                  'data/{}/raw/train-all.txt'.format(dataset))
    make_bmes(dataset)


def convert_weibo():
    dataset = 'weibo'
    print('Converting corpus {}'.format(dataset))
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')
    convert_file('data/weibo/nlpcc2016-word-seg-train.dat', 'data/{}/raw/train.txt'.format(dataset), True)
    convert_file('data/weibo/nlpcc2016-wordseg-dev.dat', 'data/{}/raw/dev.txt'.format(dataset), True)
    # TODO the weibo test answer is missing
    convert_file('data/weibo/nlpcc2016-wordseg-dev.dat', 'data/{}/raw/test.txt'.format(dataset), False)
    combine_files('data/{}/raw/train.txt'.format(dataset), 'data/{}/raw/dev.txt'.format(dataset),
                  'data/{}/raw/train-all.txt'.format(dataset))
    make_bmes(dataset)


def remove_pos(src, out, delimiter='/'):
    # print(src)
    with open(src) as src, open(out, 'w') as out:
        for line in src:
            words = []
            for word_pos in line.split(' '):
                # if len(word_pos.split(delimiter)) != 2:
                #     print(line)
                word, pos = word_pos.split(delimiter)
                words.append(word)
            out.write(' '.join(words) + '\n')


def convert_zhuxian():
    dataset = 'zx'
    print('Converting corpus {}'.format(dataset))
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')
    remove_pos('data/zx/dev.zhuxian.wordpos', 'data/zx/dev.txt', '_')
    remove_pos('data/zx/train.zhuxian.wordpos', 'data/zx/train.txt', '_')
    remove_pos('data/zx/test.zhuxian.wordpos', 'data/zx/test.txt', '_')

    convert_file('data/zx/train.txt', 'data/{}/raw/train.txt'.format(dataset), True)
    convert_file('data/zx/dev.txt', 'data/{}/raw/dev.txt'.format(dataset), True)
    convert_file('data/zx/test.txt', 'data/{}/raw/test.txt'.format(dataset), False)
    combine_files('data/{}/raw/train.txt'.format(dataset), 'data/{}/raw/dev.txt'.format(dataset),
                  'data/{}/raw/train-all.txt'.format(dataset))
    make_bmes(dataset)


def convert_cncorpus():
    dataset = 'cnc'
    print('Converting corpus {}'.format(dataset))
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')
    remove_pos('data/cnc/train.txt', 'data/cnc/train-no-pos.txt')
    remove_pos('data/cnc/dev.txt', 'data/cnc/dev-no-pos.txt')
    remove_pos('data/cnc/test.txt', 'data/cnc/test-no-pos.txt')

    convert_file('data/cnc/train-no-pos.txt', 'data/{}/raw/train.txt'.format(dataset), True)
    convert_file('data/cnc/dev-no-pos.txt', 'data/{}/raw/dev.txt'.format(dataset), True)
    convert_file('data/cnc/test-no-pos.txt', 'data/{}/raw/test.txt'.format(dataset), False)
    combine_files('data/{}/raw/train.txt'.format(dataset), 'data/{}/raw/dev.txt'.format(dataset),
                  'data/{}/raw/train-all.txt'.format(dataset))
    make_bmes(dataset)


def extract_conll(src, out):
    words = []
    with open(src) as src, open(out, 'w') as out:
        for line in src:
            line = line.strip()
            if len(line) == 0:
                out.write(' '.join(words) + '\n')
                words = []
                continue
            cells = line.split()
            words.append(cells[1])


def convert_conll(dataset):
    print('Converting corpus {}'.format(dataset))
    root = 'data/' + dataset
    make_sure_path_exists(root)
    make_sure_path_exists(root + '/raw')

    extract_conll('data/{}/dev.conll'.format(dataset), 'data/{}/dev.txt'.format(dataset))
    extract_conll('data/{}/test.conll'.format(dataset), 'data/{}/test.txt'.format(dataset))
    extract_conll('data/{}/train.conll'.format(dataset), 'data/{}/train.txt'.format(dataset))

    convert_file('data/{}/train.txt'.format(dataset), 'data/{}/raw/train.txt'.format(dataset), True)
    convert_file('data/{}/dev.txt'.format(dataset), 'data/{}/raw/dev.txt'.format(dataset), True)
    convert_file('data/{}/test.txt'.format(dataset), 'data/{}/raw/test.txt'.format(dataset), False)
    combine_files('data/{}/raw/train.txt'.format(dataset), 'data/{}/raw/dev.txt'.format(dataset),
                  'data/{}/raw/train-all.txt'.format(dataset))
    make_bmes(dataset)


def make_joint_corpus(datasets, joint):
    parts = ['dev', 'test', 'train', 'train-all']
    for part in parts:
        old_file = 'data/{}/raw/{}.txt'.format(joint, part)
        if os.path.exists(old_file):
            os.remove(old_file)
        elif not os.path.exists(os.path.dirname(old_file)):
            os.makedirs(os.path.dirname(old_file))
        for name in datasets:
            append_tags(name, joint, part)


def convert_all_bakeoff2005(datasets):
    for dataset in datasets:
        print('Converting corpus {}'.format(dataset))
        convert_bakeoff2005_dataset(dataset)
        make_bmes(dataset)


if __name__ == '__main__':
    datasets = 'pku', 'msr', 'asSC', 'cityuSC'
    convert_all_bakeoff2005(datasets)
