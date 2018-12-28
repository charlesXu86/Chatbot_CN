# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Fake_data.py
   Description :   生成一些假数据
   Author :       CharlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""

import random
import numpy as np
from Word_sequence import WordSequence

def generate(max_len=10, size=1000, same_len=False, seed=0):
    """生成虚假数据
    """

    dictionary = {
        'a': '1',
        'b': '2',
        'c': '3',
        'd': '4',
        'aa': '1',
        'bb': '2',
        'cc': '3',
        'dd': '4',
        'aaa': '1',
    }

    if seed is not None:
        random.seed(seed)

    input_list = sorted(list(dictionary.keys()))

    x_data = []
    y_data = []

    for _ in range(size):
        a_len = int(random.random() * max_len) + 1
        x = []
        y = []
        for _ in range(a_len):
            word = input_list[int(random.random() * len(input_list))]
            x.append(word)
            y.append(dictionary[word])
            if not same_len:
                if y[-1] == '2':
                    y.append('2')
                elif y[-1] == '3':
                    y.append('3')
                    y.append('4')
        x_data.append(x)
        y_data.append(y)

    ws_input = WordSequence()
    ws_input.fit(x_data)# + y_data)
    # ws_target = ws_input
    ws_target = WordSequence()
    ws_target.fit(y_data)
    return x_data, y_data, ws_input, ws_target

def test():
    """测试自身"""
    x_data, y_data, ws_input, ws_target = generate()
    print(len(x_data))
    assert len(x_data) == 1000
    print(len(y_data))
    assert len(y_data) == 1000
    print(np.max([len(x) for x in x_data]))
    assert np.max([len(x) for x in x_data]) == 10
    print(len(ws_input))
    assert len(ws_input) == 14
    print(len(ws_target))
    assert len(ws_target) == 9
    print('done')

if __name__ == '__main__':
    test()