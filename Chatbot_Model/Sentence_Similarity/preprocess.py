# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     preprocess
   Description :
   Author :       charl
   date：          2018/8/3
-------------------------------------------------
   Change Activity:
                   2018/8/3:
-------------------------------------------------
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import numpy as np
import six

from tensorflow.contrib import learn
from tensorflow.python.platform import gfile
from tensorflow.contrib import learn

TOKENIZER_RE = re.compile(r"[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",
                          re.UNICODE)

def tokenizer_char(iterator):
    for value in iterator:
        yield list(value)

def tokenizer_word(iterator):
    for value in iterator:
        yield TOKENIZER_RE.findall(value)