#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: predict.py
@desc: fasttext文本分类预测，加载模型，测试
@time: 2019/05/23
"""

import tensorflow as tf

from Chatbot_Model.Text_Classification.Fasttext.parameters import parameters
from Chatbot_Model.Text_Classification.Fasttext.data_helper import load_json, padding


class Predict():
    def __init__(self, config=parameters, model='/Users/charlesxu/PycharmProjects/Chatbot_CN/Chatbot_Model/Text_Classification/Fasttext/runs/1559726102', word_to_index='/Users/charlesxu/PycharmProjects/Chatbot_CN/Chatbot_Model/Text_Classification/Fasttext/vocabs/word_to_index.json',
                 index_to_label='/Users/charlesxu/PycharmProjects/Chatbot_CN/Chatbot_Model/Text_Classification/Fasttext/vocabs/index_to_label.json'):
        self.word_to_index = load_json(word_to_index)
        self.index_to_label = load_json(index_to_label)

        graph = tf.Graph()
        with graph.as_default():
            session_conf = tf.ConfigProto(
                allow_soft_placement=config['allow_soft_placement'],
                log_device_placement=config['log_device_placement'])
            self.sess = tf.Session(config=session_conf)
            with self.sess.as_default():
                # 加载训练好的pb模型
                tf.saved_model.loader.load(self.sess, ['tag_string'],model)

                # Get the placeholders from the graph by name
                self.input_x = graph.get_operation_by_name("input_x").outputs[0]

                self.dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

                # Tensors we want to evaluate
                self.predictions = graph.get_operation_by_name("output/predictions").outputs[0]

    def fc_predicts(self, msg):
        input_x = padding(msg, None, parameters, self.word_to_index, None)
        feed_dict = {
            self.input_x: input_x,
            self.dropout_keep_prob: 1    # 设置为1就是保留全部结果，所以这个只有在训练的时候用。
        }
        predictions = self.sess.run(self.predictions, feed_dict=feed_dict)
        return [self.index_to_label[str(idx)] for idx in predictions]


# if __name__ == '__main__':
#     prediction = Predict(parameters)
#     result = prediction.fc_predicts(["""我破产了"""])
#     print(result)
