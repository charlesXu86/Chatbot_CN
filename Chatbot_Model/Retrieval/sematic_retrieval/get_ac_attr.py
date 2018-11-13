# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     get_ac_attr.py
   Description :  将映射文件转换为AC形式数据
   Author :       charl
   date：          2018/11/13
-------------------------------------------------
   Change Activity: 2018/11/13:
-------------------------------------------------
"""
import ahocorasick
import pickle as pkl

data_path = 'D:\project\Chatbot_CN\Chatbot_Data\Semantic_retrieval_data\\'
attr_map = data_path + "attr_mapping.txt"
out_path_file = data_path + "attr_ac.pkl"

def dump_ac_attr_dict(attr_mapping_file = attr_map, out_path = out_path_file ):
    '''
    将数据转换成ac自动机形式的数据
    :param attr_mapping_file: 被转换的文件
    :param out_path: 转换后的文件
    :return:
    '''
    A = ahocorasick.Automaton()  #
    f = open(attr_mapping_file, encoding='utf-8')
    i = 0
    for line in f:
        parts = line.strip().split(" ")
        for p in parts:
            if p != "":
                A.add_word(p, (i, p))
                i += 1
    A.make_automaton()
    pkl.dump(A, open(out_path, 'wb'))
    print('Done')

if __name__ == '__main__':
    dump_ac_attr_dict()