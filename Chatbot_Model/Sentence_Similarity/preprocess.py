# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     preprocess
   Description :  数据预处理
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

class MyVocabularyProcessor(learn.preprocessing.VocabularyProcessor):
    '''

    '''
    def __init__(self,
                 max_document_length,   # 最大文档长度，超过会切割，不够会补0
                 min_frequency=0,       # 最小词频值，出现次数小于词频则不会收录到词表中
                 vocabulary=None,
                 is_char_based=True):
        if is_char_based:
            tokenizer_fn = tokenizer_char   # tokenizer_fn 分词函数
        else:
            tokenizer_fn = tokenizer_word
        self.sup = super(MyVocabularyProcessor, self)
        self.sup.__init__(max_document_length, min_frequency, vocabulary, tokenizer_fn)

    def transform(self, raw_documents):
        """Transform documents to word-id matrix.
                Convert words to ids with vocabulary fitted with fit or the one
                provided in the constructor.
                Args:
                  raw_documents: An iterable which yield either str or unicode.
                Yields:
                  x: iterable, [n_samples, max_document_length]. Word-id matrix.
                """
        for tokens in self._tokenizer(raw_documents):
            word_ids = np.zeros(self.max_document_length, np.int64)
            for idx, token in enumerate(tokens):
                if idx >= self.max_document_length:
                    break
                word_ids[idx] = self.vocabulary_.get(token)
            yield word_ids