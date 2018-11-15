# -*- coding:utf-8 -*-
# Filename: official_scorer.py
# Author：hankcs
# Date: 2017-08-17 上午10:22

import os
import sys
import tempfile
import argparse

parser = argparse.ArgumentParser(description='Bundled SIGHAN official score script')
parser.add_argument("--gold-file", required=True, dest="gold_file",
                    help="Test data .txt file, e.g. data/msr/raw/test.txt")
parser.add_argument("--test-out", required=True, dest="test_out",
                    help="Test output .txt file, e.g. result/msr/cnn/2017-11-12_10-52-44/test-out.txt")
parser.add_argument("--joint", dest="joint", action="store_true", help="Score joint learning outputs")
options = parser.parse_args()


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


tmpdir = tempfile.TemporaryDirectory()
root = tmpdir.name
datasets = {}
if options.joint:
    print('Spliting joint test out file into seperate files w.r.t dataset name...')
    with open(options.test_out) as src:
        for line in src:
            sentence = line.split(' ')
            dataset_name = sentence[0][1:-1]
            dataset_path = '{}/{}.txt'.format(root, dataset_name)
            if dataset_name not in datasets:
                datasets[dataset_name] = ('data/{}/raw/test.txt'.format(dataset_name), dataset_path)
            with open(dataset_path, 'a') as des:
                des.write(' '.join(sentence[1:-1]))
                des.write('\n')
else:
    if options.gold_file.endswith('test_gold.utf8'):
        eprint('Gold file must be preprocessed ones (data/$dataset/raw/test.txt), e.g. data/pku/raw/test.txt')
        exit(1)
    name = 'unknown'
    if options.gold_file.startswith('data/') and options.test_out.startswith('result/'):
        gold_name = options.gold_file.split('/')[1]
        test_name = options.test_out.split('/')[1]
        if gold_name != test_name:
            eprint('Gold file [{}] not match with test file [{}]'.format(gold_name, test_name))
            exit(2)
        name = gold_name

    datasets[name] = (options.gold_file, options.test_out)

print('Evaluating {} using official SIGHAN score script...'.format(list(datasets.keys()).__str__().replace('\'', '')))
for dataset_name, (gold_file, test_out) in datasets.items():
    print(dataset_name)
    dic_path = '{}/{}-dic.txt'.format(root, dataset_name)
    dic = set()
    with open(gold_file) as src:
        for line in src:
            sentence = line.split(' ')
            dic.update(sentence)
    with open(dic_path, 'w') as des:
        for word in dic:
            des.write(word)
            des.write('\n')

    cmd = './score {} {} {} > tmp'.format(dic_path, gold_file, test_out)
    os.system(cmd)
    cmd = 'grep \'F MEASURE\' tmp '
    os.system(cmd)
    cmd = 'rm tmp'
    os.system(cmd)
