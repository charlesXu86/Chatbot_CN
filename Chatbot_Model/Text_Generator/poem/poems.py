# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     poems.py
   Description :   数据处理
   Author :       charlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""
import collections
import numpy as np

start_token = 'B'
end_token = 'E'


def process_poems(file_name):
    # poems -> list of numbers
    poems = []
    with open(file_name, "r", encoding='utf-8') as f:
        for line in f.readlines():
            try:
                title, content = line.strip().split(':')
                content = content.replace(' ', '')
                if '_' in content or '(' in content or '（' in content or '《' in content or '[' in content or \
                        start_token in content or end_token in content:
                    continue
                if len(content) < 5 or len(content) > 79:
                    continue
                content = start_token + content + end_token
                poems.append(content)
            except ValueError as e:
                print('Error is:', e)
    # poems = sorted(poems, key=len)

    all_words = [word for poem in poems for word in poem]   # 统计每个字出现的次数
    counter = collections.Counter(all_words)
    count_pairs = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    words, _ = zip(*count_pairs)

    words = words + (' ',)
    word_int_map = dict(zip(words, range(len(words))))  # 生成单词到id的映射
    poems_vector = [list(map(lambda word: word_int_map.get(word, len(words)), poem)) for poem in poems]  # 把诗转换成向量形式

    return poems_vector, word_int_map, words


def generate_batch(batch_size, poems_vec, word_to_int):
    """

    :param batch_size:
    :param poems_vec:
    :param word_to_int:
    :return:
    """
    n_chunk = len(poems_vec) // batch_size
    x_batches = []
    y_batches = []
    for i in range(n_chunk):
        start_index = i * batch_size
        end_index = start_index + batch_size

        batches = poems_vec[start_index:end_index]
        length = max(map(len, batches))
        x_data = np.full((batch_size, length), word_to_int[' '], np.int32)
        for row, batch in enumerate(batches):
            x_data[row, :len(batch)] = batch
        y_data = np.copy(x_data)
        y_data[:, :-1] = x_data[:, 1:]
        """
        x_data             y_data
        [6,2,4,6,9]       [2,4,6,9,9]
        [1,4,2,8,5]       [4,2,8,5,5]
        """
        x_batches.append(x_data)
        y_batches.append(y_data)
    return x_batches, y_batches
