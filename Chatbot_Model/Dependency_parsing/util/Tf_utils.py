import os
import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector
from feature_extraction import DataConfig
import numpy as np


def visualize_sample_embeddings(sess, log_dir, words, word2idx, embeddings):  # embedding -> tf.get_variable()
    list_idx = map(lambda word: word2idx[word], words)
    # sample_embeddings = tf.gather(embeddings, list_idx, name="my_embeddings")
    # sample_embeddings = embeddings[list_idx]

    config = projector.ProjectorConfig()
    embedding_conf = config.embeddings.add()

    metadata_path = os.path.join(log_dir, 'metadata.tsv')
    with open(metadata_path, "w") as f:
        [f.write(word + "\n") for word in words]

    embedding_conf.tensor_name = embeddings.name  # embeddings.name
    embedding_conf.metadata_path = os.path.join(log_dir, 'metadata.tsv')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    summary_writer = tf.summary.FileWriter(log_dir, graph=sess.graph)
    projector.visualize_embeddings(summary_writer, config)
    # summary_writer.close()


def write_gradient_summaries(grad_tvars):
    train_variables_summaries = []
    with tf.name_scope("gradient_summaries"):
        for (grad, tvar) in grad_tvars:
            mean = tf.reduce_mean(grad)
            stddev = tf.sqrt(tf.reduce_mean(tf.square(grad - mean)))
            histogram_summary = tf.summary.histogram("{}/hist".format(tvar.name), grad)
            mean_summary = tf.summary.scalar("{}/mean".format(tvar.name), mean)
            std_dev_summary = tf.summary.scalar("{}/stddev".format(tvar.name), stddev)
            sparse_summary = tf.summary.scalar("{}/sparsity".format(tvar.name), tf.nn.zero_fraction(grad))

            # train_variables_summaries.append(histogram_summary)
            # train_variables_summaries.append(mean_summary)
            # train_variables_summaries.append(std_dev_summary)
            # train_variables_summaries.append(sparse_summary)
            # grad_summaries_merged = tf.summary.merge(train_variables_summaries)
            #
            # return grad_summaries_merged
