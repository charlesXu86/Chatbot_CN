#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: BiLingual_Evaluation_Understudy.py 
@desc: BLEU实现
@time: 2019/01/01 
"""
import sys
import os
import re
from math import exp, log


def get_file_lines(f_path):
    with open(f_path, 'rb') as f:
         lines = [line.strip() for line in f]
    return lines

def tokenize(sentence):
    # tokens = re.sub('[\W_]+', ' ', sentence, flags=re.UNICODE).lower().split()
    tokens = sentence.lower().split()
    return tokens

def concat_tokens(list_tokens):
    str = list_tokens[0]
    for token in list_tokens[1:]:
        str += " " + token
    return str


def compute_grams(tokens, N = 4):
    grams = [concat_tokens( tokens[i:i + N] ) for i in range(len(tokens) - (N - 1))]
    return grams

def create_words_dict(tokens):
    dict = {}
    for token in tokens:
        if token not in dict:
            dict[token] = 1
        else:
            dict[token] += 1

    return dict

def sum_clip_counts(dict_cand, list_dict_refs):
    sum = 0
    for word in dict_cand:
        max_count_word_occurrences = 0

        for dict_ref in list_dict_refs:
            if word in dict_ref:
                count_word_occurrences = min(dict_cand[word], dict_ref[word])
                if count_word_occurrences > max_count_word_occurrences:
                    max_count_word_occurrences = count_word_occurrences

        sum += max_count_word_occurrences

    return sum


def count_clip(cand_ngrams, list_ref_ngrams):
    dict_cand = create_words_dict(cand_ngrams)
    list_dict_ref = [create_words_dict(ref_tokens) for ref_tokens in list_ref_ngrams]
    return sum_clip_counts(dict_cand, list_dict_ref)


def modified_precision_score(sum_count_clip_candidates, sum_count_candidates):
    return float(sum_count_clip_candidates) / float(sum_count_candidates)

def best_match_length(cand_words_length, list_ref_words_length):
    best_match_diff = abs(cand_words_length - list_ref_words_length[0])
    best_match = list_ref_words_length[0]

    for j in range(1, len(list_ref_words_length)):
        diff = abs(cand_words_length - list_ref_words_length[j])

        if diff < best_match_diff:
            best_match_diff = diff
            best_match = list_ref_words_length[j]

    return best_match


def compute_modified_precision_score(num_sentences, cand_tokens, list_ref_tokens, n):
    sum_count_clip_candidates = 0
    sum_count_candidates = 0

    for i in range(num_sentences):
        cand_grams = compute_grams(cand_tokens[i], n)
        list_ref_grams = [compute_grams(ref_tokens, n) for ref_tokens in list_ref_tokens[i]]
        # print cand_grams
        # print list_ref_tokens
        # print count_clip(cand_tokens, list_ref_tokens)
        # print
        sum_count_clip_candidates += count_clip(cand_grams, list_ref_grams)
        sum_count_candidates += len(cand_grams)

    return modified_precision_score(sum_count_clip_candidates, sum_count_candidates)



# Example 1
candidate1 = "It is a guide to action which ensures that the military always obeys the commands of the party."
candidate2 = "It is to insure the troops forever hearing the activity guidebook that party direct."
reference1 = "It is a guide to action that ensures that the military will forever heed Party commands."
reference2 = "It is the guiding principle which guarantees the military forces always being under the command of the Party."
reference3 = "It is the practical guide for the army always to heed the directions of the party."
list_cand = [candidate1, candidate2]
list_refs = [reference1, reference2, reference3]

# Example 2
# candidate1 = "the the the the the the the."
# reference1 = "The cat is on the mat."
# reference2 = "There is a cat on the mat."
# list_cand = [candidate1]
# list_refs = [reference1, reference2]


if __name__ == "__main__":

    # get sentences from command line
    if (len(sys.argv) != 3):
        print("You must provide 2 arguments: " + """program takes two paths as parameters:
        path to the candidate translation (single file),
        a path reference translations (single file, or a directory if there are multiple reference translations)""")
        print("\nUsage: python calculatebleu.py /path/to/candidate /path/to/reference")
        exit(1)

    cand_path = sys.argv[1]
    ref_path = sys.argv[2]
    list_ref_files = []

    if os.path.isdir(ref_path):
        for f in os.listdir(ref_path):
            f_full_path = os.path.join(ref_path, f)
            if os.path.isfile(f_full_path):
                list_ref_files.append(f_full_path)

    else:
        list_ref_files.append(ref_path)

    # print list_ref_files

    cand_sentences = get_file_lines(cand_path)
    list_ref_sentences = [get_file_lines(ref_file) for ref_file in list_ref_files]


    # BLEU computation
    N = 4
    c = 0
    r = 0
    weight = 1.0 / float(N)
    num_sentences = len(cand_sentences)
    cand_tokens = [None] * num_sentences
    list_ref_tokens = [None] * num_sentences

    for i in range(num_sentences): # for each sentence
        cand_tokens[i] = tokenize(cand_sentences[i])
        list_ref_tokens[i] = [tokenize(ref_sentences[i]) for ref_sentences in list_ref_sentences]

        # values for BP (Brevity Penalty) computation
        cand_words_length = len(cand_tokens[i])
        list_ref_words_length = [len(ref_tokens) for ref_tokens in list_ref_tokens[i]]
        r += best_match_length(cand_words_length, list_ref_words_length)
        c += cand_words_length

    exp_arg = 0
    for n in range(1, N + 1):
        precision_score = compute_modified_precision_score(num_sentences, cand_tokens, list_ref_tokens, n)
        # print precision_score
        exp_arg += (weight * log(precision_score))

    if c > r: brevity_penalty = 1
    else: brevity_penalty = exp(1.0 - (float(r)/float(c)))

    bleu_score = brevity_penalty * exp(exp_arg)

    with open("bleu_out.txt", "w") as outfile:
        outfile.write(str(bleu_score))