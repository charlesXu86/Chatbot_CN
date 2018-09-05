# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Inverted_index_cn.py
   Description :   结合jieba的倒排索引实现
   Author :       charl
   date：          2018/9/5
-------------------------------------------------
   Change Activity: 2018/9/5:
-------------------------------------------------
"""

import os
import jieba
import re
import sys
import unicodedata

from functools import reduce

_WORD_MIN_LENGTH = 3
_STOP_WORDS = frozenset([
    'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
    'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although',
    'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another',
    'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as',
    'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been',
    'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
    'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can',
    'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
    'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
    'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
    'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
    'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
    'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
    'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
    'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
    'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
    'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
    'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
    'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
    'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
    'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
    'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
    'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
    'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
    'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
    'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
    'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
    'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
    'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
    'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
    'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
    'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
    'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
    'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
    'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
    'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
    'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
    'yourselves', 'the'])

def word_split(text):
    """
    Split a text in words. Returns a list of tuple that contains
    (word, location) location is the starting byte position of the word.
    """
    word_list = []
    wcurrent = []
    windex = None

    for i, c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
            windex = i
        elif wcurrent:
            word = u''.join(wcurrent)
            word_list.append((windex - len(word) + 1, word))
            wcurrent = []

    if wcurrent:
        word = u''.join(wcurrent)
        word_list.append((windex - len(word) + 1, word))

    return word_list

def words_cleanup(words):
    """
    Remove words with length less then a minimum and stopwords.
    """
    cleaned_words = []
    for index, word in words:
        if len(word) < _WORD_MIN_LENGTH or word in _STOP_WORDS:
            continue
        cleaned_words.append((index, word))
    return cleaned_words

def words_normalize(words):
    """
    Do a normalization precess on words. In this case is just a tolower(),
    but you can add accents stripping, convert to singular and so on...
    """
    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
        normalized_words.append((index, wnormalized))
    return normalized_words

def word_index(text):
    """
    Just a helper method to process a text.
    It calls word split, normalize and cleanup.
    """
    words = word_split(text)
    words = words_normalize(words)
    words = words_cleanup(words)
    return words

def inverted_index(text):
    """
    Create an Inverted-Index of the specified text document.
        {word:[locations]}
    """
    inverted = {}

    for index, word in word_index(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)

    return inverted

def inverted_index_add(inverted, doc_id, doc_index):
    """
    Add Invertd-Index doc_index of the document doc_id to the
    Multi-Document Inverted-Index (inverted),
    using doc_id as document identifier.
        {word:{doc_id:[locations]}}
    """
    for word, locations in doc_index.items():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted

def search(inverted, query):
    """
    Returns a set of documents id that contains all the words in your query.
    """
    words = [word for _, word in word_index(query) if word in inverted]
    results = [set(inverted[word].keys()) for word in words]
    return reduce(lambda x, y: x & y, results) if results else []

if __name__ == '__main__':
    doc1 = """
Niners head coach Mike Singletary will let Alex Smith remain his starting 
quarterback, but his vote of confidence is anything but a long-term mandate.
Smith now will work on a week-to-week basis, because Singletary has voided 
his year-long lease on the job.
"I think from this point on, you have to do what's best for the football team,"
Singletary said Monday, one day after threatening to bench Smith during a 
27-24 loss to the visiting Eagles.
"""

    doc2 = """
The fifth edition of West Coast Green, a conference focusing on "green" home 
innovations and products, rolled into San Francisco's Fort Mason last week 
intent, per usual, on making our living spaces more environmentally friendly 
- one used-tire house at a time.
To that end, there were presentations on topics such as water efficiency and 
the burgeoning future of Net Zero-rated buildings that consume no energy and 
produce no carbon emissions.
"""

    # Build Inverted-Index for documents
    inverted = {}
    documents = {'doc1':doc1, 'doc2':doc2}
    for doc_id, text in documents.items():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

    # Print Inverted-Index
    for word, doc_locations in inverted.items():
        print(word, doc_locations)

    # Search something and print results
    queries = ['Week', 'Niners week', 'West-coast Week']
    for query in queries:
        result_docs = search(inverted, query)
        print("Search for '%s': %r" % (query, result_docs))
        for _, word in word_index(query):
            def extract_text(doc, index):
                return documents[doc][index:index+20].replace('\n', ' ')

            for doc in result_docs:
                for index in inverted[word][doc]:
                    print('   - %s...' % extract_text(doc, index))
        print()



