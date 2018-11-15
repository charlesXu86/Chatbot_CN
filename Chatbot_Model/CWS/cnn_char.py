from __future__ import print_function
from __future__ import division
import tensorflow as tf
import tf_utils

class CNNChar(object):

    """
    A CNN for embedding tokens.
    """
    def __init__(self, char_domain_size, char_embedding_dim, hidden_dim, filter_width, embeddings=None):

        self.char_domain_size = char_domain_size
        self.embedding_size = char_embedding_dim
        self.hidden_dim = hidden_dim
        self.filter_width = filter_width

        # char embedding input
        self.input_chars = tf.placeholder(tf.int64, [None, None], name="input_chars")

        # padding mask
        # self.input_mask = tf.placeholder(tf.float32, [None, None], name="input_mask")

        self.batch_size = tf.placeholder(tf.int32, None, name="batch_size")

        self.max_seq_len = tf.placeholder(tf.int32, None, name="max_seq_len")

        self.max_tok_len = tf.placeholder(tf.int32, None, name="max_tok_len")

        self.input_dropout_keep_prob = tf.placeholder_with_default(1.0, [], name="input_dropout_keep_prob")

        # sequence lengths
        self.sequence_lengths = tf.placeholder(tf.int32, [None, None], name="sequence_lengths")
        self.token_lengths = tf.placeholder(tf.int32, [None, None], name="tok_lengths")

        print("CNN char embedding model:")
        print("embedding dim: ", self.embedding_size)
        print("out dim: ", self.hidden_dim)

        char_embeddings_shape = (self.char_domain_size-1, self.embedding_size)
        self.char_embeddings = tf_utils.initialize_embeddings(char_embeddings_shape, name="char_embeddings", pretrained=embeddings)

        self.outputs = self.forward(self.input_chars, self.input_dropout_keep_prob, reuse=False)

    def forward(self, input_x1, input_dropout_keep_prob, reuse=True):
        with tf.variable_scope("char-forward", reuse=reuse):

            char_embeddings_lookup = tf.nn.embedding_lookup(self.char_embeddings, input_x1)
            print(char_embeddings_lookup.get_shape())

            char_embeddings_flat = tf.reshape(char_embeddings_lookup, tf.stack([self.batch_size*self.max_seq_len, self.max_tok_len, self.embedding_size]))
            print(char_embeddings_flat.get_shape())
            tok_lens_flat = tf.reshape(self.token_lengths, [self.batch_size*self.max_seq_len])
            print(tok_lens_flat.get_shape())

            input_feats_expanded = tf.expand_dims(char_embeddings_flat, 1)
            input_feats_expanded_drop = tf.nn.dropout(input_feats_expanded, input_dropout_keep_prob)


            with tf.name_scope("char-cnn"):
                filter_shape = [1, self.filter_width, self.embedding_size, self.hidden_dim]
                w = tf_utils.initialize_weights(filter_shape, "conv0_w", init_type='xavier',  gain='relu')
                b = tf.get_variable("conv0_b", initializer=tf.constant(0.01, shape=[self.hidden_dim]))
                conv0 = tf.nn.conv2d(input_feats_expanded_drop, w, strides=[1, 1, 1, 1], padding="SAME", name="conv0")
                print("conv0", conv0.get_shape())
                h_squeeze = tf.squeeze(conv0, [1])
                print("squeeze", h_squeeze.get_shape())
                hidden_outputs = tf.reduce_max(h_squeeze, 1)
                print("max", hidden_outputs.get_shape())
                hidden_outputs_unflat = tf.reshape(hidden_outputs, tf.stack([self.batch_size, self.max_seq_len, self.hidden_dim]))

        return hidden_outputs_unflat
