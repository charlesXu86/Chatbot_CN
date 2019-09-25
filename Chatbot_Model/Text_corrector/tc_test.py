# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   tc_test.py
 
@Time    :   2019-05-30 20:05
 
@Desc    :   测试
 
'''

from Text_auto_correct_v1 import auto_correct_sentence


def test(msg):
    print("Test case 1:")
    correct_sent = auto_correct_sentence(msg)
    print("original sentence:" + msg + "\n==>\n" + "corrected sentence:" + correct_sent)


err_sent_1 = '我想买奥地'
test(msg=err_sent_1)