# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     WordEmbeddings.py
   Description :
   Author :       charl
   date：          2018/11/30
-------------------------------------------------
   Change Activity: 2018/11/30:
-------------------------------------------------
"""

import numpy as np

class WordEmbeddings:
    def __init__(self, file_name, word2cnt=None):
        self.id2word = {}
        self.word2id = {}
        self.embeddings = {}

        if word2cnt:
            self.load_based_word2cnt(file_name, word2cnt)
        else:
            self.load_from_file(file_name)

        self.word2id["<UNK>"] = len(self.word2id)
        self.id2word[self.word2id["<UNK>"]] = "<UNK>"
        self.embeddings.append(self.get_zero_vector(len(self.embeddings[0])))

    def get_unk_id(self):
        return self.word2id['<UNK>']

    def get_padding_id(self):
        return self.word2id['<PADDING>']

    def words_to_ids(self,words, maxlen=50, padding=True):
        ids = []
        for w in words:
            if not w in self.word2id:
                ids.append(self.word2id["<UNK>"])
                continue
            ids.append(self.word2id[w])
        length = len(ids)
        if padding:
            while len(ids) < maxlen:
                ids.append(self.word2id["<PADDING>"])
            ids = ids[:maxlen]
        length = min(length, len(ids))
        return ids, length

    def ids_to_words(self, ids):
        words = []
        for i in ids:
            words.append(self.id2word[i])
        return words

    def get_init_vector(self, dim):
        scale = 0.1
        vec = np.random.uniform(low=-scale, high=scale, size=[dim])
        vec = vec / np.sqrt(np.sum(vec * vec))
        assert abs(np.sum(vec * vec) - 1.0) < 0.1
        return list(vec)

    def get_embeddings(self):
        return np.array(self.embeddings)

    def get_zero_vector(self, dim):
        return [0.0] * dim





