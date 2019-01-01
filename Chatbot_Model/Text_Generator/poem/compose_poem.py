# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     compose_poem.py
   Description :   生成
   Author :       charlesXu
   date：          2018/12/28
-------------------------------------------------
   Change Activity: 2018/12/28:
-------------------------------------------------
"""
import tensorflow as tf
from model import rnn_model
from poems import process_poems
import numpy as np

start_token = 'B'
end_token = 'E'
model_dir = './model/'
corpus_file = 'F:\project\Chatbot_CN\Chatbot_Data\Text_generator\poem\poems.txt'

lr = 0.0002


def to_word(predict, vocabs):
    predict = predict[0]       
    predict /= np.sum(predict)
    sample = np.random.choice(np.arange(len(predict)), p=predict)
    if sample > len(vocabs):
        return vocabs[-1]
    else:
        return vocabs[sample]


def gen_poem(begin_word):
    batch_size = 1
    print('## loading corpus from %s' % model_dir)
    poems_vector, word_int_map, vocabularies = process_poems(corpus_file)

    input_data = tf.placeholder(tf.int32, [batch_size, None])

    end_points = rnn_model(model='lstm', input_data=input_data, output_data=None, vocab_size=len(
        vocabularies), rnn_size=128, num_layers=2, batch_size=64, learning_rate=lr)

    saver = tf.train.Saver(tf.global_variables())
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)

        checkpoint = tf.train.latest_checkpoint(model_dir)
        saver.restore(sess, checkpoint)

        x = np.array([list(map(word_int_map.get, start_token))])

        [predict, last_state] = sess.run([end_points['prediction'], end_points['last_state']],
                                         feed_dict={input_data: x})
        if begin_word:
            word = begin_word
        else:
            word = to_word(predict, vocabularies)
        poem_ = ''

        i = 0
        while word != end_token:
            poem_ += word
            i += 1
            if i >= 24:
                break
            x = np.zeros((1, 1))
            x[0, 0] = word_int_map[word]
            [predict, last_state] = sess.run([end_points['prediction'], end_points['last_state']],
                                             feed_dict={input_data: x, end_points['initial_state']: last_state})
            word = to_word(predict, vocabularies)

        return poem_


def pretty_print_poem(poem_):
    poem_sentences = poem_.split('。')
    for s in poem_sentences:
        if s != '' and len(s) > 10:
            print(s + '。')

# 古诗生成主入口
if __name__ == '__main__':
    begin_char = input('## please input the first character:')
    poem = gen_poem(begin_char)
    pretty_print_poem(poem_=poem)