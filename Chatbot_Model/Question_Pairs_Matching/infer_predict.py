# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   LogUtils2.py

@Time    :   2019-06-13 17:51

@Desc    :

'''

import tensorflow.contrib.learn as learn
import tensorflow as tf
import numpy as np

from Chatbot_Model.Question_Pairs_Matching import data_prepare

data_pre = data_prepare.Data_Prepare()


class Infer(object):
    """
        ues model to predict classification.
    """
    def __init__(self):
        self.vocab_processor = learn.preprocessing.VocabularyProcessor.restore('./Chatbot_Model/Question_Pairs_Matching/save_model/esim/vocab.pickle')
        self.checkpoint_file = tf.train.latest_checkpoint('./Chatbot_Model/Question_Pairs_Matching/save_model/esim')
        graph = tf.Graph()
        with graph.as_default():
            session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
            self.sess = tf.Session(config=session_conf)
            with self.sess.as_default():
                # Load the saved meta graph and restore variables
                saver = tf.train.import_meta_graph("{}.meta".format(self.checkpoint_file))
                saver.restore(self.sess, self.checkpoint_file)

                # Get the placeholders from the graph by name
                self.text_a = graph.get_operation_by_name("esim_model/text_a").outputs[0]
                self.text_b = graph.get_operation_by_name("esim_model/text_b").outputs[0]
                self.a_length = graph.get_operation_by_name("esim_model/a_length").outputs[0]
                self.b_length = graph.get_operation_by_name("esim_model/b_length").outputs[0]
                self.drop_keep_prob = graph.get_operation_by_name("esim_model/dropout_keep_prob").outputs[0]

                # Tensors we want to evaluate
                self.prediction = graph.get_operation_by_name("esim_model/output/prediction").outputs[0]
                self.score = graph.get_operation_by_name("esim_model/output/score").outputs[0]

    def infer(self, sentenceA, sentenceB):
        # transfer to vector
        sentenceA = [data_pre.pre_processing(sentenceA)]
        sentenceB = [data_pre.pre_processing(sentenceB)]
        vector_A = np.array(list(self.vocab_processor.transform(sentenceA)))
        vector_B = np.array(list(self.vocab_processor.transform(sentenceB)))
        feed_dict = {
            self.text_a: vector_A,
            self.text_b: vector_B,
            self.drop_keep_prob: 1.0,
            self.a_length: np.array([len(sentenceA[0].split(" "))]),
            self.b_length: np.array([len(sentenceB[0].split(" "))])
        }
        y, s = self.sess.run([self.prediction, self.score], feed_dict)
        score = s[0][1]
        return score


# if __name__ == '__main__':
#     infer = Infer()
#     sentencea = '你点击详情'
#     sentenceb = '您点击详情'
#     print(infer.infer(sentencea, sentenceb))







