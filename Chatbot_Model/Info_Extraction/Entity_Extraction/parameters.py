# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   parameters.py
 
@Time    :   2019-07-09 19:33
 
@Desc    :   实体识别超参数设置
 
'''

parameters = {
    'sequence_length': 200,       # 文本长度，当文本大于该长度则截断
    'vocab_size': 5000,           # 字典大小
    'embedding_size': 100,        # embedding词向量维度
    'embedding_path':'./data/wiki_100.utf8',
    'update_embedding': True,
    'device': '/gpu:0',           # 设置device
    'batch_size': 64,             # batch大小
    'num_epochs': 10,             # epoch数目
    'hidden_dim': 300,
    'shuffle': True,
    'word2id': './data/word2id.pkl',
    'evaluate_every': 100,        # 每隔多少步打印一次验证集结果
    'checkpoint_every': 20,      # 每隔多少步保存一次模型
    'num_checkpoints': 5,         # 最多保存模型的个数
    'allow_soft_placement': True,   # 是否允许程序自动选择备用device
    'log_device_placement': False,  # 是否允许在终端打印日志文件
    'dropout': 0.5,
    'clip': 5.0,
    'CRF': True,
    'optimizer': 'Adam',
    'data_path': './data/train_data_BAK',    # 数据路径  格式：标签\t文本
    'max_learning_rate': 0.005,
    'min_learning_rate': 0.0001,
    'decay_coefficient': 2.5, # learning_rate的衰减系数
    'learning_rate': 0.003,             # 学习率
    'l2_reg_lambda': 0.0,
    'dropout_keep_prob': 1.0
}