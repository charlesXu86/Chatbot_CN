# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     split_sentence.py
   Description :   分句策略
   Author :       charl
   date：          2018/8/10
-------------------------------------------------
   Change Activity:
                   2018/8/10:
-------------------------------------------------
"""

import re

# 分句方式一
def cut_sentence_one(self, sentence):
    not_cuts = re.compile(u'[。.？！\?!]')
    result = []
    start = 0
    for seg_sign in not_cuts.finditer(sentence):
        result.extend(self.simple_cut(sentence[start:seg_sign.start()], self.sess))
        result.append(sentence[seg_sign.start():seg_sign.end()])
        start = seg_sign.end()
    result.extend(self.simple_cut(sentence[start:], self.sess))

    return result

# 分句方式2
def cut_sentence_two(self, line, max_len):
    newLine = []
    tags_result = []
    # 小写转大写、去空格、去/n /t
    line = line.replace(' ', '').strip('"').replace('"', '“').replace('!', '！').replace('?', '？').strip()
    print(' ')
    print('TEXT:', line)
    # 去段尾句号
    line = line.strip('.').strip('。')
    # 分句，还原句号
    line = re.split(r'[。？！]', line)
    line = [i + '。' for i in line]

    # 超过最大句长max_len进行逗号分句
    def segSent(sentence):
        sli = sentence.split('，')
        lenSli = [len(i) for i in sli]
        sLen = 0
        for i in lenSli:
            sLen += i + 1
            if sLen > max_len:
                sLen -= i + 1
                break
        newLine.append(sentence[:sLen])
        if len(sentence[sLen:]) > max_len:
            segSent(sentence[sLen:])
        else:
            newLine.append(sentence[sLen:])
        return newLine

    for sentence in line:
        if len(sentence) > max_len:
            segSent(sentence)
        else:
            newLine.append(sentence)

    for sentence in newLine:
        tags_result.extend(self.simple_cut(sentence, self.sess))

    return tags_result