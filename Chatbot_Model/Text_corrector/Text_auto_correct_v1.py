# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Text_auto_correct_v1.py
 
@Time    :   2019-05-30 19:56
 
@Desc    :   文本纠错
 
'''

import pinyin
import jieba
import string


FILE_PATH = "./resource/token_freq_pos_jieba.txt"
PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）"


def construct_dict(file_path):
    word_freq = {}
    with open(file_path, "r", encoding='utf-8') as f:
        for line in f:
            info = line.split()
            word = info[0]
            frequency = info[1]
            word_freq[word] = frequency

    return word_freq

phrase_freq = construct_dict(FILE_PATH)

def load_cn_words_dict(file_path):
    cn_words_dict = ""
    with open(file_path, "r") as f:
        for word in f:
            cn_words_dict += word.strip()
    return cn_words_dict


def edits1(phrase, cn_words_dict):
    "All edits that are one edit away from `phrase`."
    phrase = phrase
    splits = [(phrase[:i], phrase[i:]) for i in range(len(phrase) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in cn_words_dict]
    inserts = [L + c + R for L, R in splits for c in cn_words_dict]
    return set(deletes + transposes + replaces + inserts)


def known(phrases):
    '''

    :param phrases:
    :return:
    '''
    return set(phrase for phrase in phrases if phrase in phrase_freq)


def get_candidates(error_phrase):
    candidates_1st_order = []
    candidates_2nd_order = []
    candidates_3nd_order = []

    error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/")
    cn_words_dict = load_cn_words_dict("./resource/cn_dict.txt")
    candidate_phrases = list(known(edits1(error_phrase, cn_words_dict)))

    for candidate_phrase in candidate_phrases:
        candidate_pinyin = pinyin.get(candidate_phrase, format="strip", delimiter="/")
        if candidate_pinyin == error_pinyin:
            candidates_1st_order.append(candidate_phrase)
        elif candidate_pinyin.split("/")[0] == error_pinyin.split("/")[0]:
            candidates_2nd_order.append(candidate_phrase)
        else:
            candidates_3nd_order.append(candidate_phrase)

    return candidates_1st_order, candidates_2nd_order, candidates_3nd_order


def auto_correct(error_phrase):
    c1_order, c2_order, c3_order = get_candidates(error_phrase)
    # print c1_order, c2_order, c3_order
    if c1_order:
        return max(c1_order, key=phrase_freq.get)
    elif c2_order:
        return max(c2_order, key=phrase_freq.get)
    else:
        return max(c3_order, key=phrase_freq.get)


def auto_correct_sentence(error_sentence, verbose=True):
    jieba_cut = jieba.cut(error_sentence, cut_all=False)
    seg_list = "\t".join(jieba_cut).split("\t")

    correct_sentence = ""

    for phrase in seg_list:

        correct_phrase = phrase
        # check if item is a punctuation
        if phrase not in PUNCTUATION_LIST:
            # check if the phrase in our dict, if not then it is a misspelled phrase
            if phrase not in phrase_freq.keys():
                correct_phrase = auto_correct(phrase)
                if verbose:
                    print(phrase, correct_phrase)

        correct_sentence += correct_phrase

    return correct_sentence

