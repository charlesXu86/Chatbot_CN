# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     data_helper
   Description : 数据预处理
   Author :       charl
   date：          2018/8/3
-------------------------------------------------
   Change Activity:
                   2018/8/3:
-------------------------------------------------
"""

import sys
import numpy as np
import pickle as pkl
import re
import itertools
import time
import gc
import gzip


from collections import Counter
from tensorflow.contrib import learn
from gensim.models.word2vec import Word2Vec
from random import random

