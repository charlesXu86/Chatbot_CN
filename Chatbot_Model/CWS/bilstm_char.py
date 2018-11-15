from __future__ import print_function
from __future__ import division
import tensorflow as tf
import numpy as np
import tf_utils

class BiLSTMChar(object):

    """
    A bidirectional LSTM for embedding tokens.
    """
    def __init__(self, char_domain_size, char_embedding_dim, hidden_dim, embeddings=None):

        self.char_domain_size = char_domain_size
        self.embedding_size = char_embedding_dim
        self.hidden_dim = hidden_dim

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

        self.output_size = 2*self.hidden_dim

        print("LSTM char embedding model")
        print("embedding dim: ", self.embedding_size)
        print("out dim: ", self.output_size)

        # set the pad token to a constant 0 vector
        # self.char_zero_pad = tf.constant(0.0, dtype=tf.float32, shape=[1, self.embedding_size])

        # Embedding layer
        shape = (char_domain_size-1, self.embedding_size)
        self.char_embeddings = tf_utils.initialize_embeddings(shape, name="char_embeddings", pretrained=embeddings)

        self.outputs = self.forward(self.input_chars, self.input_dropout_keep_prob, reuse=False)

    def forward(self, input_x1, input_dropout_keep_prob, reuse=True):
        with tf.variable_scope("char-forward", reuse=reuse):

            char_embeddings_lookup = tf.nn.embedding_lookup(self.char_embeddings, input_x1)
            char_embeddings_flat = tf.reshape(char_embeddings_lookup, tf.stack([self.batch_size*self.max_seq_len, self.max_tok_len, self.embedding_size]))
            tok_lens_flat = tf.reshape(self.token_lengths, [self.batch_size*self.max_seq_len])

            #
            # input_list = [char_embeddings_lookup]
            # # input_size = self.embedding_size
            #
            # input_feats = tf.concat(2, input_list)

            input_feats_drop = tf.nn.dropout(char_embeddings_flat, input_dropout_keep_prob)

            # total_output_width = 2*self.hidden_dim

            with tf.name_scope("char-bilstm"):
                # selected_col_embeddings = tf.nn.embedding_lookup(token_embeddings, self.token_batch)
                fwd_cell = tf.nn.rnn_cell.BasicLSTMCell(self.hidden_dim, state_is_tuple=True)
                bwd_cell = tf.nn.rnn_cell.BasicLSTMCell(self.hidden_dim, state_is_tuple=True)
                lstm_outputs, _ = tf.nn.bidirectional_dynamic_rnn(cell_fw=fwd_cell, cell_bw=bwd_cell, dtype=tf.float32,
                                                                 inputs=input_feats_drop,
                                                                 parallel_iterations=32, swap_memory=False,
                                                                 sequence_length=tok_lens_flat)
                outputs_fw = lstm_outputs[0]
                outputs_bw = lstm_outputs[1]

                # this is batch*output_size (flat)
                fw_output = tf_utils.last_relevant(outputs_fw, tok_lens_flat)
                # this is batch * max_seq_len * output_size
                bw_output = outputs_bw[:, 0, :]
                hidden_outputs = tf.concat(axis=1, values=[fw_output, bw_output])
                # hidden_outputs = tf.concat(2, lstm_outputs)
                # hidden_outputs = tf.Print(hidden_outputs, [tf.shape(hidden_outputs)], message='hidden outputs:')
                hidden_outputs_unflat = tf.reshape(hidden_outputs, tf.stack([self.batch_size, self.max_seq_len, self.output_size]))

        return hidden_outputs_unflat
