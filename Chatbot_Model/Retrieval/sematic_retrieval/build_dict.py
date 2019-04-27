# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     build_dict.py
   Description :  构建词典
   Author :       charl
   date：          2018/11/6
-------------------------------------------------
   Change Activity: 2018/11/6:
-------------------------------------------------
"""

import ahocorasick   # 字符串快速匹配
import pickle as pkl

from collections import defaultdict

data_path = 'F:\project\Chatbot_CN\Chatbot_Data\Semantic_retrieval_data\\'
entity_list_file =data_path + 'all_entity.txt'
entity_out_path =data_path + 'ent_ac.pkl'
attr_list_file =data_path + 'attr_mapping.txt'
attr_out_path =data_path + 'attr_ac.pkl'
val_list_file =data_path + 'Person_val.txt'


def dump_ac_entity_dict(list_file, out_path):
    '''

    :param list_file:
    :param out_path:
    :return:
    '''
    A = ahocorasick.Automaton()  # AC 自动机
    f = open(list_file)
    i = 0
    for line in f:
        word = line.strip()
        A.add_word(word, (i, word))
        i += 1
    A.make_automaton()
    pkl.dump(A, open(out_path, 'wb'))

def dump_ac_attr_dict(attr_mapping_file, out_path):
    '''

    :param attr_mapping_file:
    :param out_path:
    :return:
    '''
    A = ahocorasick.Automaton()
    f = open(attr_mapping_file)
    i = 0
    for line in f:
        parts = line.strip().split(" ")
        for p in parts:
            if p != "":
                A.add_word(p, (i,p))
                i += 1
    A.make_automaton()
    pkl.dump(A, open(out_path, 'wb'))

def load_ac_dict(out_path):
    A = pkl.load(open(out_path, 'rb'))
    return A

def load_attr_map(attr_mapping_file):
    f = open(attr_mapping_file, encoding='utf-8')
    mapping = defaultdict(list)
    for line in f:
        parts = line.strip().split(" ")
        for p in parts:
            if p != '':
                mapping[p].append(parts[0])
    return mapping

def load_entity_dict(entity_file):
    f = open(entity_file, encoding='utf-8')
    ents = {}
    for line in f:
        ents[line.strip()] = 1
    return ents

def load_val_dict(val_file):
    f = open(val_file)
    val_attr_map = {}
    for line in f:
        parts = line.strip().split(" ")
        val_attr_map[parts[0]] = parts[1]
    return val_attr_map

if __name__ == '__main__':
    dump_ac_attr_dict(attr_list_file, attr_out_path)
