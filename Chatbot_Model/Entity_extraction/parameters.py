# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   parameters.py
 
@Time    :   2019-07-25 15:18
 
@Desc    :   模型超参数配置
 
'''
import os


parameters = {
    'seg_dim': 20,       #
    'char_dim': 100,            # 文本分类数
    'lstm_dim': 100,           # 字典大小
    'tag_schema': 'iob',        # embedding词向量维度
    'device': '/gpu:0',           # 设置device
    'clip': 5,             # batch大小
    'drop_out': 0.5,             # epoch数目
    'batch_size': 20,        # 每隔多少步打印一次验证集结果
    'lr': 0.001,      # 每隔多少步保存一次模型
    'optimizer': 'adam',         # 最多保存模型的个数
    'pre_emb': True,   # 是否允许程序自动选择备用device
    'zeros': False,  # 是否允许在终端打印日志文件
    'lower': True,
    'max_epoch': 100,
    'ckpt_path': os.path.join(os.path.dirname(__file__), 'ckpt'),
    'summary_path': 'summary',
    'log_file': 'train.log',
    'map_file': os.path.join(os.path.dirname(__file__), 'config/maps.pkl'), #'./config/maps.pkl',
    'vocab_file': 'vocab.json',
    'config_file': os.path.join(os.path.dirname(__file__), 'config/config_file'),
    'result_path': 'result',
    'emb_file': os.path.join(os.path.dirname(__file__), 'config/TX50W.vec'),
    'train_file': './data/example.train',
    'dev_file': './data/example.dev',
    'test_file': './data/example.test',
    'steps_check': 100

}