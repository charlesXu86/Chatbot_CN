# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     history.py
   Description :   记录keras的训练过程
   Author :       charl
   date：          2018/8/11
-------------------------------------------------
   Change Activity: 2018/8/11:
-------------------------------------------------
"""

from keras.callbacks import Callback

class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))