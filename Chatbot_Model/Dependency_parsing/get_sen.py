#!/usr/bin/env python
# coding=utf-8

import os
import sys
import re
import codecs

def read_file(filename="./data/test1"):
    file = codecs.open(filename + '.txt', encoding='utf-8')
    file_sen = codecs.open(filename + '_sen.txt', "w", encoding='utf-8')
    word = []
    for line in file:
        word_line = re.split(' ', line)
        if len(word_line) == 1:
            word.append(u".\n")
            #print "1 space sentence", word_line
        else:
            word.append(word_line[1])
    file_sen.write(" ".join(word))
    return word
    
read_file("./data/sen")
