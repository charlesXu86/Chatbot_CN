#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: Parser_model.py
@desc: 解析模型   (训练部分)
@time: 2019/03/08
"""

import os
import time
import tensorflow as tf
import numpy as np
from Base_model import Model
from Params_init import random_uniform_initializer, random_normal_initializer, xavier_initializer
from util.General_utils import Progbar
from util.General_utils import get_minibatches
from Feature_extraction import DataConfig, Flags, punc_pos, pos_prefix, load_datasets
from util.Tf_utils import visualize_sample_embeddings


class ParserModel(Model):
    def __init__(self, config, word_embeddings, pos_embeddings, dep_embeddings):
        self.word_embeddings = word_embeddings
        self.pos_embeddings = pos_embeddings
        self.dep_embeddings = dep_embeddings
        self.config = config
        self.build()


    def add_placeholders(self):

        with tf.variable_scope("input_placeholders"):
            self.word_input_placeholder = tf.placeholder(shape=[None, self.config.word_features_types],
                                                         dtype=tf.int32, name="batch_word_indices")
            self.pos_input_placeholder = tf.placeholder(shape=[None, self.config.pos_features_types],
                                                        dtype=tf.int32, name="batch_pos_indices")
            self.dep_input_placeholder = tf.placeholder(shape=[None, self.config.dep_features_types],
                                                        dtype=tf.int32, name="batch_dep_indices")
        with tf.variable_scope("label_placeholders"):
            self.labels_placeholder = tf.placeholder(shape=[None, self.config.num_classes],
                                                     dtype=tf.float32, name="batch_one_hot_targets")
        with tf.variable_scope("regularization"):
            self.dropout_placeholder = tf.placeholder(shape=(), dtype=tf.float32, name="dropout")


    def create_feed_dict(self, inputs_batch, labels_batch=None, keep_prob=1):

        feed_dict = {
            self.word_input_placeholder: inputs_batch[0],
            self.pos_input_placeholder: inputs_batch[1],
            self.dep_input_placeholder: inputs_batch[2],
            self.dropout_placeholder: keep_prob
        }

        if labels_batch is not None:
            feed_dict[self.labels_placeholder] = labels_batch

        return feed_dict


    def write_gradient_summaries(self, grad_tvars):
        with tf.name_scope("gradient_summaries"):
            for (grad, tvar) in grad_tvars:
                mean = tf.reduce_mean(grad)
                stddev = tf.sqrt(tf.reduce_mean(tf.square(grad - mean)))
                tf.summary.histogram("{}/hist".format(tvar.name), grad)
                tf.summary.scalar("{}/mean".format(tvar.name), mean)
                tf.summary.scalar("{}/stddev".format(tvar.name), stddev)
                tf.summary.scalar("{}/sparsity".format(tvar.name), tf.nn.zero_fraction(grad))


    def add_embedding(self):
        with tf.variable_scope("feature_lookup"):
            self.word_embedding_matrix = random_uniform_initializer(self.word_embeddings.shape, "word_embedding_matrix",
                                                                    0.01, trainable=True)
            self.pos_embedding_matrix = random_uniform_initializer(self.pos_embeddings.shape, "pos_embedding_matrix",
                                                                   0.01, trainable=True)
            self.dep_embedding_matrix = random_uniform_initializer(self.dep_embeddings.shape, "dep_embedding_matrix",
                                                                   0.01, trainable=True)

            word_context_embeddings = tf.nn.embedding_lookup(self.word_embedding_matrix, self.word_input_placeholder)
            pos_context_embeddings = tf.nn.embedding_lookup(self.pos_embedding_matrix, self.pos_input_placeholder)
            dep_context_embeddings = tf.nn.embedding_lookup(self.dep_embedding_matrix, self.dep_input_placeholder)

            word_embeddings = tf.reshape(word_context_embeddings,
                                         [-1, self.config.word_features_types * self.config.embedding_dim],
                                         name="word_context_embeddings")
            pos_embeddings = tf.reshape(pos_context_embeddings,
                                        [-1, self.config.pos_features_types * self.config.embedding_dim],
                                        name="pos_context_embeddings")
            dep_embeddings = tf.reshape(dep_context_embeddings,
                                        [-1, self.config.dep_features_types * self.config.embedding_dim],
                                        name="dep_context_embeddings")

        with tf.variable_scope("batch_inputs"):
            embeddings = tf.concat([word_embeddings, pos_embeddings, dep_embeddings], 1, name="batch_feature_matrix")

        return embeddings, word_embeddings, pos_embeddings, dep_embeddings


    def add_cube_prediction_op(self):
        print("***Building network with CUBE activation***")
        _, word_embeddings, pos_embeddings, dep_embeddings = self.add_embedding()

        with tf.variable_scope("layer_connections"):
            with tf.variable_scope("layer_1"):
                w11 = random_uniform_initializer((self.config.word_features_types * self.config.embedding_dim,
                                                  self.config.l1_hidden_size), "w11",
                                                 0.01, trainable=True)
                w12 = random_uniform_initializer((self.config.pos_features_types * self.config.embedding_dim,
                                                  self.config.l1_hidden_size), "w12",
                                                 0.01, trainable=True)
                w13 = random_uniform_initializer((self.config.dep_features_types * self.config.embedding_dim,
                                                  self.config.l1_hidden_size), "w13",
                                                 0.01, trainable=True)
                b1 = random_uniform_initializer((self.config.l1_hidden_size,), "bias1",
                                                0.01, trainable=True)
                """
                w11 = xavier_initializer((self.config.word_features_types * self.config.embedding_dim,
                                          self.config.l1_hidden_size), "w11")
                w12 = xavier_initializer((self.config.pos_features_types * self.config.embedding_dim,
                                          self.config.l1_hidden_size), "w12")
                w13 = xavier_initializer((self.config.dep_features_types * self.config.embedding_dim,
                                          self.config.l1_hidden_size), "w13")
                b1 = xavier_initializer((self.config.l1_hidden_size,), "bias1")
                """

                # for visualization
                preactivations = tf.pow(tf.add_n([tf.matmul(word_embeddings, w11),
                                                  tf.matmul(pos_embeddings, w12),
                                                  tf.matmul(dep_embeddings, w13)]) + b1, 3, name="preactivations")

                tf.summary.histogram("preactivations", preactivations)

                # non_positive_activation_fraction = tf.reduce_mean(tf.cast(tf.less_equal(preactivations, 0),
                #                                                           tf.float32))
                # tf.summary.scalar("non_positive_activations_fraction", non_positive_activation_fraction)

                h1 = tf.nn.dropout(preactivations,
                                   keep_prob=self.dropout_placeholder,
                                   name="output_activations")

            with tf.variable_scope("layer_2"):
                """
                w2 = xavier_initializer((self.config.l1_hidden_size, self.config.l2_hidden_size), "w2")
                b2 = xavier_initializer((self.config.l2_hidden_size,), "bias2")
                """

                w2 = random_uniform_initializer((self.config.l1_hidden_size, self.config.l2_hidden_size), "w2",
                                                0.01, trainable=True)
                b2 = random_uniform_initializer((self.config.l2_hidden_size,), "bias2",
                                                0.01, trainable=True)
                h2 = tf.nn.relu(tf.add(tf.matmul(h1, w2), b2), name="activations")

            with tf.variable_scope("layer_3"):
                """
                w3 = xavier_initializer((self.config.l2_hidden_size, self.config.num_classes), "w3")
                b3 = xavier_initializer((self.config.num_classes,), "bias3")
                """

                w3 = random_uniform_initializer((self.config.l2_hidden_size, self.config.num_classes), "w3",
                                                0.01, trainable=True)
                b3 = random_uniform_initializer((self.config.num_classes,), "bias3", 0.01, trainable=True)
        with tf.variable_scope("predictions"):
            predictions = tf.add(tf.matmul(h2, w3), b3, name="prediction_logits")

        return predictions


    def add_prediction_op(self):
        print("***Building network with ReLU activation***")
        x = self.add_embedding()

        with tf.variable_scope("layer_connections"):
            with tf.variable_scope("layer_1"):
                w1 = xavier_initializer((self.config.num_features_types * self.config.embedding_dim,
                                         self.config.hidden_size), "w1")
                b1 = xavier_initializer((self.config.hidden_size,), "bias1")

                # for visualization
                preactivations = tf.add(tf.matmul(x, w1), b1, name="preactivations")
                tf.summary.histogram("preactivations", preactivations)

                non_positive_activation_fraction = tf.reduce_mean(tf.cast(tf.less_equal(preactivations, 0),
                                                                          tf.float32))
                tf.summary.scalar("non_negative_activations_fraction", non_positive_activation_fraction)

                h1 = tf.nn.dropout(tf.nn.relu(preactivations),
                                   keep_prob=self.dropout_placeholder,
                                   name="output_activations")

            with tf.variable_scope("layer_2"):
                w2 = xavier_initializer((self.config.hidden_size, self.config.num_classes), "w2")
                b2 = xavier_initializer((self.config.num_classes,), "bias2")
        with tf.variable_scope("predictions"):
            predictions = tf.add(tf.matmul(h1, w2), b2, name="prediction_logits")

        return predictions

    def l2_loss_sum(self, tvars):
        return tf.add_n([tf.nn.l2_loss(t) for t in tvars], "l2_norms_sum")


    def add_loss_op(self, pred):
        tvars = tf.trainable_variables()
        without_bias_tvars = [tvar for tvar in tvars if 'bias' not in tvar.name]

        with tf.variable_scope("loss"):
            cross_entropy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
                labels=self.labels_placeholder, logits=pred), name="batch_xentropy_loss")

            l2_loss = tf.multiply(self.config.reg_val, self.l2_loss_sum(without_bias_tvars), name="l2_loss")
            loss = tf.add(cross_entropy_loss, l2_loss, name="total_batch_loss")

        tf.summary.scalar("batch_loss", loss)

        return loss


    def add_accuracy_op(self, pred):
        with tf.variable_scope("accuracy"):
            accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(pred, axis=1),
                                                       tf.argmax(self.labels_placeholder, axis=1)), dtype=tf.float32),
                                      name="curr_batch_accuracy")
        return accuracy


    def add_training_op(self, loss):
        with tf.variable_scope("optimizer"):
            optimizer = tf.train.AdamOptimizer(learning_rate=self.config.lr, name="adam_optimizer")
            tvars = tf.trainable_variables()
            grad_tvars = optimizer.compute_gradients(loss, tvars)
            self.write_gradient_summaries(grad_tvars)
            train_op = optimizer.apply_gradients(grad_tvars)

        return train_op


    def get_word_pos_inputs(self, inputs_batch):  # inputs_batch : list([list(word_id), list(pos_id)])
        # inputs_batch: [ [[1,2], [3,4], [5,6]], [[7,8], [9,10],[11,12]] ]
        inputs_batch = np.asarray(inputs_batch)
        word_inputs_batch, pos_inputs_batch, dep_inputs_batch = np.split(inputs_batch, 3, 1)
        word_inputs_batch = np.squeeze(word_inputs_batch)  # removes extra dimenstion -> convert 3-d to 2-d matrix
        pos_inputs_batch = np.squeeze(pos_inputs_batch)
        dep_inputs_batch = np.squeeze(dep_inputs_batch)
        return word_inputs_batch, pos_inputs_batch, dep_inputs_batch


    def train_on_batch(self, sess, inputs_batch, labels_batch, merged):
        word_inputs_batch, pos_inputs_batch, dep_inputs_batch = inputs_batch
        feed = self.create_feed_dict([word_inputs_batch, pos_inputs_batch, dep_inputs_batch], labels_batch=labels_batch,
                                     keep_prob=self.config.keep_prob)
        _, summary, loss = sess.run([self.train_op, merged, self.loss], feed_dict=feed)
        return summary, loss


    def compute_dependencies(self, sess, data, dataset):
        sentences = data
        rem_sentences = [sentence for sentence in sentences]
        [sentence.clear_prediction_dependencies() for sentence in sentences]
        [sentence.clear_children_info() for sentence in sentences]

        while len(rem_sentences) != 0:
            curr_batch_size = min(dataset.model_config.batch_size, len(rem_sentences))
            batch_sentences = rem_sentences[:curr_batch_size]

            enable_features = [0 if len(sentence.stack) == 1 and len(sentence.buff) == 0 else 1 for sentence in
                               batch_sentences]
            enable_count = np.count_nonzero(enable_features)

            while enable_count > 0:
                curr_sentences = [sentence for i, sentence in enumerate(batch_sentences) if enable_features[i] == 1]

                # get feature for each sentence
                # call predictions -> argmax
                # store dependency and left/right child
                # update state
                # repeatngpeng

                curr_inputs = [
                    dataset.feature_extractor.extract_for_current_state(sentence, dataset.word2idx, dataset.pos2idx,
                                                                        dataset.dep2idx , dataset.idx2dep) for sentence in curr_sentences]
                word_inputs_batch = [curr_inputs[i][0] for i in range(len(curr_inputs))]
                pos_inputs_batch = [curr_inputs[i][1] for i in range(len(curr_inputs))]
                dep_inputs_batch = [curr_inputs[i][2] for i in range(len(curr_inputs))]

                predictions = sess.run(self.pred,
                                       feed_dict=self.create_feed_dict([word_inputs_batch, pos_inputs_batch,
                                                                        dep_inputs_batch]))
                legal_labels = np.asarray([sentence.get_legal_labels() for sentence in curr_sentences],
                                          dtype=np.float32)
                
                self.legal_transitions = np.argmax(predictions + 1000 * legal_labels, axis=1)

                # update left/right children so can be used for next feature vector
                [sentence.update_child_dependencies(transition) for (sentence, transition) in
                 zip(curr_sentences, self.legal_transitions) if transition != 0]

                # update state
                [sentence.update_state_by_transition(legal_transition, gold=False) for (sentence, legal_transition) in
                 zip(curr_sentences, self.legal_transitions)]

                enable_features = [0 if len(sentence.stack) == 1 and len(sentence.buff) == 0 else 1 for sentence in
                                   batch_sentences]
                enable_count = np.count_nonzero(enable_features)

            # Reset stack and buffer
            [sentence.reset_to_initial_state() for sentence in batch_sentences]
            rem_sentences = rem_sentences[curr_batch_size:]

#    def decode(self, word):
#        list_word = []
#        stack_word = list(word)
#        dict_word = {}
#        for i in range(len(self.legal_transitions)):
#            if self.legal_transitions[i] == 0:
#                list_word.append(stack_word[0])
#                stack_word.pop(0)
#            else if self.legal_transitions[i] >0 and self.legal_transitions[i] <= 72:
#                dict_word[list_word[-2]] = all_dep_label[self.legal_transitions[i] - 1]
#                list_word.pop(-2)
#            else if self.legal_transitions[i] > 72 and self.legal_transitions[i] <= 72*2:
#                dict_word[list_word[-1]] = all_dep_label[self.legal_transitions[i] - 72 -1]
#                list_word.pop(-1)
#        return dict_word



    def get_UAS(self, data):
        correct_tokens = 0
        correct_tokens_dep = 0
        all_tokens = 0
        punc_token_pos = [pos_prefix + each for each in punc_pos]
        token_num = []
        token_dep = []
        for sentence in data:
            # reset each predicted head before evaluation
            [token.reset_predicted_head_id() for token in sentence.tokens]

            head = [-2] * len(sentence.tokens)
            dep_l = [""] * len(sentence.tokens)
            for h, t, k in sentence.predicted_dependencies:
                head[t.token_id] = h.token_id
                dep_l[t.token_id] = k
            token_dep.append(dep_l)

            non_punc_tokens = [token for token in sentence.tokens if token.pos not in punc_token_pos]
            token_num = [head[token.token_id] for (_, token) in enumerate(non_punc_tokens)]
            #string =  [token.dep for  (_, token) in enumerate(non_punc_tokens)]
            correct_tokens += sum([1 if token.head_id == head[token.token_id] else 0 for (_, token) in enumerate(
                non_punc_tokens)])
            correct_tokens_dep += sum([1 if token.dep == dep_l[token.token_id] else 0 for (i, token) in enumerate(non_punc_tokens)])

            # all_tokens += len(sentence.tokens)
            all_tokens += len(non_punc_tokens)

        UAS = correct_tokens / float(all_tokens)
        LAS = correct_tokens_dep / float(all_tokens)
        return UAS, LAS, token_num, token_dep


    def run_epoch(self, sess, config, dataset, train_writer, merged):
        prog = Progbar(target=1 + len(dataset.train_inputs[0]) / config.batch_size)
        for i, (train_x, train_y) in enumerate(get_minibatches([dataset.train_inputs, dataset.train_targets],
                                                               config.batch_size, is_multi_feature_input=True)):

            summary, loss = self.train_on_batch(sess, train_x, train_y, merged)
            prog.update(i + 1, [("train loss", loss)])
            # train_writer.add_summary(summary, global_step=i)
        return summary, loss  # Last batch


    def run_valid_epoch(self, sess, dataset):
        print("Evaluating on dev set\n",
        self.compute_dependencies(sess, dataset.valid_data, dataset))
        valid_UAS, valid_LAS, _, __ = self.get_UAS(dataset.valid_data)
        print("- dev UAS: {:.2f}".format(valid_UAS * 100.0))
        print("- dev LAS: {:.2f}".format(valid_LAS * 100.0))
        return valid_UAS, valid_LAS


    def fit(self, sess, saver, config, dataset, train_writer, valid_writer, merged):
        best_valid_UAS = 0
        best_valid_LAS = 0
        for epoch in range(config.n_epochs):
            print("Epoch {:} out of {:}".format(epoch + 1, self.config.n_epochs))

            summary, loss = self.run_epoch(sess, config, dataset, train_writer, merged)

            if (epoch + 1) % dataset.model_config.run_valid_after_epochs == 0:
                valid_UAS, valid_LAS = self.run_valid_epoch(sess, dataset)
                valid_UAS_summary = tf.summary.scalar("valid_UAS", tf.constant(valid_UAS, dtype=tf.float32))
                valid_LAS_summary = tf.summary.scalar("valid_LAS", tf.constant(valid_LAS, dtype=tf.float32))
                valid_writer.add_summary(sess.run(valid_UAS_summary), epoch + 1)
                valid_writer.add_summary(sess.run(valid_LAS_summary), epoch + 1)
                if valid_UAS > best_valid_UAS or valid_LAS > best_valid_LAS:
                    best_valid_UAS = valid_UAS
                    best_valid_LAS = valid_LAS
                    if saver:
                        print("New best dev UAS or LAS! Saving model..")
                        saver.save(sess, os.path.join(DataConfig.data_dir_path, DataConfig.model_dir,
                                                      DataConfig.model_name))

            # trainable variables summary -> only for training
            if (epoch + 1) % dataset.model_config.write_summary_after_epochs == 0:
                train_writer.add_summary(summary, global_step=epoch + 1)

def highlight_string(temp):
    print(80 * "=")
    print(temp)
    print(80 * "=")


def main(flag, load_existing_dump=True):
    highlight_string("INITIALIZING")
    print("loading data..")
    
    list_word = []
    list_pos = []
    dataset = load_datasets(list_word, list_pos, True, load_existing_dump)
    config = dataset.model_config

    print("word vocab Size: {}".format(len(dataset.word2idx)))
    print("pos vocab Size: {}".format(len(dataset.pos2idx)))
    print("dep vocab Size: {}".format(len(dataset.dep2idx)))
    print("Training Size: {}".format(len(dataset.train_inputs[0])))
    print("valid data Size: {}".format(len(dataset.valid_data)))
    print("test data Size: {}".format(len(dataset.test_data)))

    if not os.path.exists(os.path.join(DataConfig.data_dir_path, DataConfig.model_dir)):
        os.makedirs(os.path.join(DataConfig.data_dir_path, DataConfig.model_dir))

    with tf.Graph().as_default(), tf.Session() as sess:
        print("Building network...",)
        start = time.time()
        with tf.variable_scope("par_model") as model_scope:
            model = ParserModel(config, dataset.word_embedding_matrix, dataset.pos_embedding_matrix,
                                dataset.dep_embedding_matrix)
            saver = tf.train.Saver()
            """
            model_scope.reuse_variables()
                -> no need to call tf.variable_scope(model_scope, reuse = True) again
                -> directly access variables & call functions inside this block itself.
                -> ref: https://www.tensorflow.org/versions/r1.2/api_docs/python/tf/variable_scope
                -> https://stackoverflow.com/questions/35919020/whats-the-difference-of-name-scope-and-a-variable-scope-in-tensorflow
            """

        print("took {:.2f} seconds\n".format(time.time() - start))

        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(os.path.join(DataConfig.data_dir_path, DataConfig.summary_dir,
                                                          DataConfig.train_summ_dir), sess.graph)
        valid_writer = tf.summary.FileWriter(os.path.join(DataConfig.data_dir_path, DataConfig.summary_dir,
                                                          DataConfig.test_summ_dir))

        if flag == Flags.TRAIN:

            # Variable initialization -> not needed for .restore()
            """ The variables to restore do not have to have been initialized,
            as restoring is itself a way to initialize variables. """
            sess.run(tf.global_variables_initializer())
            """ call 'assignment' after 'init' only, else 'assignment' will get reset by 'init' """
            sess.run(tf.assign(model.word_embedding_matrix, model.word_embeddings))
            sess.run(tf.assign(model.pos_embedding_matrix, model.pos_embeddings))
            sess.run(tf.assign(model.dep_embedding_matrix, model.dep_embeddings))

            highlight_string("TRAINING")
            model.print_trainable_varibles()

            model.fit(sess, saver, config, dataset, train_writer, valid_writer, merged)

            # Testing
            highlight_string("Testing")
            print("Restoring best found parameters on dev set")
            saver.restore(sess, os.path.join(DataConfig.data_dir_path, DataConfig.model_dir,
                                             DataConfig.model_name))
            model.compute_dependencies(sess, dataset.test_data, dataset)
            test_UAS, test_LAS, _, _ = model.get_UAS(dataset.test_data)
            print("test UAS: {}".format(test_UAS * 100))
            print("test LAS: {}".format(test_LAS * 100))

            train_writer.close()
            valid_writer.close()

            # visualize trained embeddings after complete training (not after each epoch)
            with tf.variable_scope(model_scope, reuse=True):
                pos_emb = tf.get_variable("feature_lookup/pos_embedding_matrix",
                                          [len(dataset.pos2idx.keys()), dataset.model_config.embedding_dim])
                visualize_sample_embeddings(sess, os.path.join(DataConfig.data_dir_path, DataConfig.model_dir),
                                            dataset.pos2idx.keys(), dataset.pos2idx, pos_emb)
            print("to Visualize Embeddings, run in terminal:")
            print("tensorboard --logdir=" + os.path.abspath(os.path.join(DataConfig.data_dir_path,
                                                                         DataConfig.model_dir)))

        else:
            ckpt_path = tf.train.latest_checkpoint(os.path.join(DataConfig.data_dir_path,
                                                                DataConfig.model_dir))
            if ckpt_path is not None:
                print("Found checkpoint! Restoring variables..")
                saver.restore(sess, ckpt_path)
                highlight_string("Testing")
                model.compute_dependencies(sess, dataset.test_data, dataset)
                test_UAS,test_LAS, _ ,_ = model.get_UAS(dataset.test_data)
                print("test UAS: {}".format(test_UAS * 100))

                highlight_string("Embedding Visualization")
                with tf.variable_scope(model_scope, reuse=True):
                    pos_emb = tf.get_variable("feature_lookup/pos_embedding_matrix",
                                              [len(dataset.pos2idx.keys()), dataset.model_config.embedding_dim])
                    visualize_sample_embeddings(sess, os.path.join(DataConfig.data_dir_path, DataConfig.model_dir),
                                                dataset.pos2idx.keys(), dataset.pos2idx, pos_emb)
                print("to Visualize Embeddings, run in terminal:")
                print("tensorboard --logdir=" + os.path.abspath(os.path.join(DataConfig.data_dir_path,
                                                                             DataConfig.model_dir)))

            else:
                print("No checkpoint found!")


if __name__ == '__main__':
    main(Flags.TRAIN, load_existing_dump=True)
