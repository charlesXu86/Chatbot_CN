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
import jieba
import pprint

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

def my_split(str):
    seg_list = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '、']
    cut_list = []
    cut_text = jieba.lcut(str)
    for i in range(len(cut_text) - 2):
        cut_after_0 = cut_text[i]   #
        cut_after_1 = cut_text[i+1]
        cut_after_2 = cut_text[i+2]

        if cut_after_0 in seg_list and cut_after_1 in seg_list and cut_after_2 not in seg_list:
            txt = cut_after_0 + cut_after_1
            cut_list.append(txt)
    return cut_list

def split_sentence_thr(text):
    cut = ['一、','二、', '三、', '四、', '五、', '六、', '七、', '1、', '2、', '3、', '4、', '5、']
    lists = []
    for i in cut[1:]:
        txt1 = text.split(i)[0]
        text = text.replace(txt1, "")
        lists.append(txt1)
    while '' in lists:
        lists.remove('')
    return lists




# text = '一、被告浙江驰江工贸有限公司于本十日内归还原告中国；二、原告中国银行股份有限公司武行优先受偿权；三、被告浙江驰江工贸有限公司十行股份；四、被限公司对上述款江驰有限公司追偿。五、司达之日起十院递交上诉状上诉于浙江省金华市中级人民法院。"'
# text = my_split(text)
# text2 = split_sentence_thr(text)
# print(te)
# print(t)