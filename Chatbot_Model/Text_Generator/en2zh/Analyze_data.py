import jieba
import matplotlib.pyplot as plt
import nltk
from tqdm import tqdm

from Config import *
from Utils import normalizeString


def analyze_zh():
    translation_path = os.path.join(train_translation_folder, train_translation_zh_filename)

    with open(translation_path, 'r') as f:
        sentences = f.readlines()

    sent_lengths = []

    for sentence in tqdm(sentences):
        seg_list = list(jieba.cut(sentence.strip()))
        # Update word frequency
        sent_lengths.append(len(seg_list))

    num_bins = 100
    n, bins, patches = plt.hist(sent_lengths, num_bins, facecolor='blue', alpha=0.5)
    title = 'Chinese Sentence Lengths Distribution'
    plt.title(title)
    plt.show()


def analyze_en():
    translation_path = os.path.join(train_translation_folder, train_translation_en_filename)

    with open(translation_path, 'r') as f:
        sentences = f.readlines()

    sent_lengths = []

    for sentence in tqdm(sentences):
        sentence_en = sentence.strip().lower()
        tokens = [normalizeString(s) for s in nltk.word_tokenize(sentence_en)]
        seg_list = list(jieba.cut(sentence.strip()))
        # Update word frequency
        sent_lengths.append(len(seg_list))

    num_bins = 100
    n, bins, patches = plt.hist(sent_lengths, num_bins, facecolor='blue', alpha=0.5)
    title = 'English Sentence Lengths Distribution'
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    analyze_zh()
    analyze_en()
