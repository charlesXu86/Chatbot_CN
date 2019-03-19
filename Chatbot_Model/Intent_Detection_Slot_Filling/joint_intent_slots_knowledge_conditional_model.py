# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# seq2seq_attention: 1.word embedding 2.encoder 3.decoder(optional with attention). for more detail, please check:Neural Machine Translation By Jointly Learning to Align And Translate
import tensorflow as tf
import numpy as np
import tensorflow.contrib as tf_contrib
import random
import copy
import os

class joint_knowledge_conditional_model:
    def __init__(self, intent_num_classes, learning_rate, decay_steps, decay_rate, sequence_length,
                 vocab_size, embed_size,hidden_size, sequence_length_batch,slots_num_classes,is_training,domain_num_classes,
                 initializer=tf.random_normal_initializer(stddev=0.1),clip_gradients=3.0,l2_lambda=0.0001,use_hidden_states_slots=True,
                 filter_sizes=[1,2,3],num_filters=64,S_Q_len=1):
        """init all hyperparameter here"""
        # set hyperparamter
        self.intent_num_classes = intent_num_classes
        self.domain_num_classes=domain_num_classes
        self.sequence_length = sequence_length
        self.vocab_size = vocab_size
        self.embed_size = embed_size
        self.is_training = is_training
        self.learning_rate = tf.Variable(learning_rate, trainable=False, name="learning_rate")
        self.learning_rate_decay_half_op = tf.assign(self.learning_rate, self.learning_rate * 0.80) #0.5
        self.initializer = initializer
        self.hidden_size = hidden_size
        self.clip_gradients=clip_gradients
        self.l2_lambda=l2_lambda
        self.sequence_length_batch=sequence_length_batch
        self.slots_num_classes=slots_num_classes
        self.use_hidden_states_slots=use_hidden_states_slots
        #below is for TextCNN
        self.filter_sizes=filter_sizes
        self.num_filters=num_filters
        self.num_filters_total = self.num_filters * len(filter_sizes)
        self.S_Q_len = S_Q_len

        self.x = tf.placeholder(tf.int32, [None, self.sequence_length], name="x")
        self.y_slots = tf.placeholder(tf.int32, [None, self.sequence_length],name="y_slots")
        self.y_intent = tf.placeholder(tf.int32, [None],name="y_intent")
        self.y_domain = tf.placeholder(tf.int32, [None], name="y_domain")
        self.input_knowledges = tf.placeholder(tf.int32, [None, self.sequence_length],name="input_knowledges")  #nput_knowledges

        if self.S_Q_len>1:
            self.S_Q = tf.placeholder(tf.int32, [self.S_Q_len, self.sequence_length], name="Standard_Queries") #标准问题的集合

        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
        self.global_step = tf.Variable(0, trainable=False, name="Global_Step")
        self.epoch_step = tf.Variable(0, trainable=False, name="Epoch_Step")
        self.epoch_increment = tf.assign(self.epoch_step, tf.add(self.epoch_step, tf.constant(1)))
        self.decay_steps, self.decay_rate = decay_steps, decay_rate

        self.instantiate_weights()
        self.encoder_bi_directional_alime()

        self.logits_domain = self.inference_domain() #[none,domain_num_classes]
        logits_domian_max=tf.reduce_max(self.logits_domain, axis=-1, keep_dims=True) #[none,domain_num_classes]
        logits_domain_smooth = self.logits_domain - logits_domian_max
        self.domain_scores=tf.nn.softmax(logits_domain_smooth)

        self.logits_intent = self.inference_intent() #[none,intent_num_classes]

        logits_intent_max = tf.reduce_max(self.logits_intent, axis=-1, keep_dims=True)
        logits_intent_smooth = self.logits_intent - logits_intent_max
        self.intent_scores = tf.nn.softmax(logits_intent_smooth)

        self.logits_slots = self.inference_slot() #[none,sequence_length,slots_num_classes]


        self.predictions_intent = tf.argmax(self.logits_intent, axis=1,name="predictions_intent")  # [batch_size]
        correct_prediction_intent = tf.equal(tf.cast(self.predictions_intent, tf.int32),self.y_intent)  # [batch_size]
        self.accuracy_intent = tf.reduce_mean(tf.cast(correct_prediction_intent, tf.float32), name="accuracy_intent")  # shape=()

        self.predictions_domain = tf.argmax(self.logits_domain, axis=1, name="predictions_domain")  # [batch_size]
        correct_prediction_domain = tf.equal(tf.cast(self.predictions_domain, tf.int32), self.y_domain)  # [batch_size]
        self.accuracy_domain = tf.reduce_mean(tf.cast(correct_prediction_domain, tf.float32),name="accuracy_domain")  # shape=()

        self.predictions_slots = tf.argmax(self.logits_slots, axis=2, name="predictions_slots") #[batch_size,slots_num_classes]
        correct_prediction_slot = tf.equal(tf.cast(self.predictions_slots, tf.int32),self.y_slots)  #[batch_size, self.sequence_length]
        self.accuracy_slot = tf.reduce_mean(tf.cast(correct_prediction_slot, tf.float32), name="accuracy_slot") # shape=()
        if not is_training:
            if self.S_Q_len > 1:
                self.similiarity_module()
            return
        self.loss_val = self.loss_seq2seq()
        self.train_op = self.train()

    def encoder_bi_directional_alime(self):
        """1.word vector+symbol vector 2.context window 3.nolinear projection 4.bi-directional lstm """
        # 1.word vector+symbol vector
        embedded_words = tf.nn.embedding_lookup(self.Embedding,self.x)  # [None, self.sequence_length, self.embed_size]
        self.embedded_words=embedded_words
        input_knowledges_embedding = tf.nn.embedding_lookup(self.Embedding_slot_label,self.y_slots) #[batch_size,sequence_length,hidden_size]
        inputs_concat=tf.concat([embedded_words,input_knowledges_embedding],axis=2) #[batch_size,sequence_length,hidden_size*2]
        self.inputs_concat=inputs_concat #for intent and domain
        batch_size,_,last_dimension_size=inputs_concat.get_shape().as_list()
        feature_left=inputs_concat[:, 0, :] #tf.ones((batch_size,last_dimension_size))
        feature_right =inputs_concat[:, self.sequence_length-1, :] # tf.ones((batch_size, last_dimension_size))
        inputs_list=[] #a list.each element is:[batch_size,hidden_size]
        for i in range(self.sequence_length):
            #2.context window
            feature = inputs_concat[:, i, :] #[batch_size,hidden_size*2]
            if i>0:
                feature_left=inputs_concat[:, i-1, :]
            if i!=self.sequence_length-1:
                feature_right=inputs_concat[:, i+1, :]
            context=tf.concat([feature_left,feature,feature_right],axis=1) #[batch_size,hidden_size*6]
            #3.nolinear projection
            representation = tf.layers.dense(context, self.hidden_size, activation=tf.nn.tanh) #[batch_size,hidden_size]. learn sailent featue, ad feature reduction.
            inputs_list.append(representation)
        inputs=tf.stack(inputs_list,axis=1) #[batch_size,sequence_length,hidden_size]

        # 2.encode with bi-directional GRU
        self.fw_cell =tf.nn.rnn_cell.BasicLSTMCell(self.hidden_size, state_is_tuple=True) #rnn_cell.LSTMCell
        self.bw_cell =tf.nn.rnn_cell.BasicLSTMCell(self.hidden_size, state_is_tuple=True)
        #fw_cell = tf.contrib.rnn.DropoutWrapper(fw_cell, output_keep_prob=self.dropout_keep_prob);bw_cell = tf.contrib.rnn.DropoutWrapper(bw_cell, output_keep_prob=self.dropout_keep_prob)
        bi_outputs, self.bi_state = tf.nn.bidirectional_dynamic_rnn(self.fw_cell, self.bw_cell, inputs, dtype=tf.float32,#sequence_length: size `[batch_size]`,containing the actual lengths for each of the sequences in the batch
                                                          sequence_length=self.sequence_length_batch, time_major=False, swap_memory=True)
        self.inputs_representation=tf.concat([bi_outputs[0],bi_outputs[1]],-1) #should be:[none, self.sequence_length,self.hidden_size*2]

    def inference_domain(self): #domain
        with tf.variable_scope("hidden_layer_domain"): #some inference structure with intent, but parameters is not the same.
            hidden_states=self.conv_layer() #[None,num_filters_total]
        self.domain_hidden_states=hidden_states
        logits_domain = tf.matmul(hidden_states, self.W_projection_domain) + self.b_projection_domain #[none,domain_num_classes]
        return logits_domain

    def inference_intent(self): #intent
        with tf.variable_scope("hidden_layer_intent"):
            hidden_states=self.conv_layer() #[None,num_filters_total]
        self.intent_hidden_states=hidden_states
        hidden_states_concat=tf.concat([hidden_states,self.domain_hidden_states],axis=1) #[None,num_filters_total*2]
        hidden_states_concat=tf.layers.dense(hidden_states_concat,self.num_filters_total,activation=tf.nn.tanh)
        logits = tf.matmul(hidden_states_concat, self.W_projection_intent) + self.b_projection_intent #[none,intent_num_classes]
        return logits

    def inference_slot(self): #slot
        logits = [] #self.inputs_representation：[none, self.sequence_length,self.hidden_size*2]
        hidden_states_list=[]
        for i in range(self.sequence_length):
            feature=self.inputs_representation[:,i,:] #[none,self.hidden_size*2]
            feature=tf.concat([feature,self.intent_hidden_states],axis=1) #ADD.201712.20.slot contional on intent#[none,self.hidden_size*2+self.num_filters_total*2]
            hidden_states = tf.layers.dense(feature, self.hidden_size, activation=tf.nn.tanh) #[none,hidden_size]
            output=tf.matmul(hidden_states, self.W_projection_slot) + self.b_projection_slot #[none,slots_num_classes]
            logits.append(output)
            hidden_states_list.append(hidden_states)
        #logits is a list. each element is:[none,slots_num_classes]
        logits=tf.stack(logits,axis=1) #[none,sequence_length,slots_num_classes]
        self.hidden_states_slots=tf.stack(hidden_states_list,axis=1) #[none,sequence_length,hidden_size]
        return logits

    def similiarity_module_bi_directional(self):
        print("going thought similiarity module,%d" % self.S_Q_len)
        query_standard_embedding = tf.nn.embedding_lookup(self.Embedding, self.S_Q)  # Shape:[None,sequence_length,embed_sz]

        # 2.encode with bi-directional GRU
        with tf.variable_scope("similiarity_module"):
            #fw_cell =tf.nn.rnn_cell.BasicLSTMCell(self.hidden_size, state_is_tuple=True) #rnn_cell.LSTMCell
            #bw_cell =tf.nn.rnn_cell.BasicLSTMCell(self.hidden_size, state_is_tuple=True)
            #fw_cell = tf.contrib.rnn.DropoutWrapper(fw_cell, output_keep_prob=self.dropout_keep_prob);bw_cell = tf.contrib.rnn.DropoutWrapper(bw_cell, output_keep_prob=self.dropout_keep_prob)
            bi_outputs, bi_state = tf.nn.bidirectional_dynamic_rnn(self.fw_cell, self.bw_cell, query_standard_embedding, dtype=tf.float32,#sequence_length: size `[batch_size]`,containing the actual lengths for each of the sequences in the batch
                                                              time_major=False, swap_memory=True)
        query_representation=tf.concat([bi_outputs[0],bi_outputs[1]],-1) #should be:[none, self.sequence_length,self.hidden_size*2]
        query_representation=tf.reduce_max(query_representation,axis=1) #[none,self.hidden_size*2]
        inputs_representation=tf.reduce_max(self.inputs_representation,axis=1) #[none,self.hidden_size*2]
        self.similiarity_list = self.cos_similiarity_vectorized(inputs_representation, query_representation) ##[1,None]

    def similiarity_module(self):
        print("going thought similiarity module,%d" % self.S_Q_len)
        query_standard_embedded = tf.nn.embedding_lookup(self.Embedding, self.S_Q)  # Shape:[None,sequence_length,embed_sz]

        # 2.encode with positional bag of words
        query_representation=tf.reduce_sum(query_standard_embedded,axis=1) #[none,self.embed_sz]
        inputs_representation=tf.reduce_sum(self.embedded_words,axis=1) #[none,self.embed_sz]
        self.similiarity_list = self.cos_similiarity_vectorized(inputs_representation, query_representation) #[1,None]

    def similiarity_module_postional_bow(self):
        print("going thought similiarity module,%d" % self.S_Q_len)
        query_standard_embedding = tf.nn.embedding_lookup(self.Embedding, self.S_Q)  # Shape:[None,sequence_length,embed_sz]

        # 2.encode with positional bag of words
        query_representation= tf.multiply(query_standard_embedding, self.x_mask) #[None, self.sequence_length, self.embed_size]
        query_representation=tf.reduce_sum(query_representation,axis=1) #[none,self.hidden_size*2]
        inputs_representation=tf.reduce_sum(self.inputs_representation,axis=1) #[none,self.hidden_size*2]
        self.similiarity_list = self.cos_similiarity_vectorized(inputs_representation, query_representation) ##[1,None]

    def cos_similiarity_vectorized(self,v,V):
        """
        cosine similiarity vectorized
        v:[1,embed_sz],
        V:[None,embed_sz]
        """
        print("cos_similiarity_vectorized.started.v:",v,";V:",V)
        dot_product=tf.reduce_sum(tf.multiply(v, V),axis=1) #[1,None]
        v1_norm=tf.sqrt(tf.reduce_sum(tf.pow(v,tf.constant(2.0)))) #scalar
        v2_norm=tf.sqrt(tf.reduce_sum(tf.pow(V,tf.constant(2.0)),axis=1)) #[1,None]
        v1_v2=tf.multiply(v1_norm,v2_norm) #[1,None]
        cos=tf.divide(dot_product,v1_v2) #[1,None]
        print("cos_similiarity_vectorized.ended.result:",cos)
        return cos

    def conv_layer(self):
        dimension=self.inputs_concat.get_shape().as_list()[-1]
        self.inputs_representation_expanded = tf.expand_dims(self.inputs_concat,-1)  # [None,sentence_length,hidden_size*2,1]. expand dimension so meet input requirement of 2d-conv

        # 2.=====>loop each filter size. for each filter, do:convolution-pooling layer(a.create filters,b.conv,c.apply nolinearity,d.max-pooling)--->
        # you can use:tf.nn.conv2d;tf.nn.relu;tf.nn.max_pool; feature shape is 4-d. feature is a new variable
        pooled_outputs = []
        for i, filter_size in enumerate(self.filter_sizes):
            with tf.variable_scope("convolution-pooling-%s" % filter_size):
                # ====>a.create filter
                filter = tf.get_variable("filter-%s" % filter_size,[filter_size, dimension, 1, self.num_filters],initializer=self.initializer)
                # ====>b.conv operation: conv2d===>computes a 2-D convolution given 4-D `input` and `filter` tensors.
                # Conv.Input: given an input tensor of shape `[batch, in_height, in_width, in_channels]` and a filter / kernel tensor of shape `[filter_height, filter_width, in_channels, out_channels]`
                # Conv.Returns: A `Tensor`. Has the same type as `input`.
                #         A 4-D tensor. The dimension order is determined by the value of `data_format`, see below for details.
                # 1)each filter with conv2d's output a shape:[1,sequence_length-filter_size+1,1,1];2)*num_filters--->[1,sequence_length-filter_size+1,1,num_filters];3)*batch_size--->[batch_size,sequence_length-filter_size+1,1,num_filters]
                # input data format:NHWC:[batch, height, width, channels];output:4-D
                conv = tf.nn.conv2d(self.inputs_representation_expanded, filter, strides=[1, 1, 1, 1],padding="VALID",name="conv")  # shape:[batch_size,sequence_length - filter_size + 1,1,num_filters]
                # ====>c. apply nolinearity
                b = tf.get_variable("b-%s" % filter_size, [self.num_filters])  #bias.
                h = tf.nn.relu(tf.nn.bias_add(conv, b),"relu")  # shape:[batch_size,sequence_length - filter_size + 1,1,num_filters]. tf.nn.bias_add:adds `bias` to `value`
                # ====>. max-pooling.  value: A 4-D `Tensor` with shape `[batch, height, width, channels]
                #                  ksize: A list of ints that has length >= 4.  The size of the window for each dimension of the input tensor.
                #                  strides: A list of ints that has length >= 4.  The stride of the sliding window for each dimension of the input tensor.
                pooled = tf.nn.max_pool(h, ksize=[1, self.sequence_length - filter_size + 1, 1, 1],strides=[1, 1, 1, 1], padding='VALID',name="pool")  # shape:[batch_size, 1, 1, num_filters].max_pool:performs the max pooling on the input.
                pooled_outputs.append(pooled)
        # 3.=====>combine all pooled features, and flatten the feature.output' shape is a [1,None]
        # e.g. >>> x1=tf.ones([3,3]);x2=tf.ones([3,3]);x=[x1,x2]
        #         x12_0=tf.concat(x,0)---->x12_0' shape:[6,3]
        #         x12_1=tf.concat(x,1)---->x12_1' shape;[3,6]
        self.h_pool = tf.concat(pooled_outputs,-1)  # shape:[batch_size, 1, 1, num_filters_total]. tf.concat=>concatenates tensors along one dimension.where num_filters_total=num_filters_1+num_filters_2+num_filters_3
        self.h_pool_flat = tf.reshape(self.h_pool, [-1,self.num_filters_total])  # shape should be:[None,num_filters_total]. here this operation has some result as tf.sequeeze().e.g. x's shape:[3,3];tf.reshape(-1,x) & (3, 3)---->(1,9)

        # 4.=====>add dropout: use tf.nn.dropout
        with tf.name_scope("dropout"):
            cnn_feature = tf.nn.dropout(self.h_pool_flat,keep_prob=self.dropout_keep_prob)  # [None,num_filters_total]

        return cnn_feature

    def loss_seq2seq(self):
        with tf.name_scope("loss"):
            #input: `logits` and `labels` must have the same shape `[batch_size, intent_num_classes]`
            #output: A 1-D `Tensor` of length `batch_size` of the same type as `logits` with the softmax cross entropy loss.
            loss_slot = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.y_slots, logits=(self.logits_slots+self.epsilon()))  #[none, self.sequence_length]. A `Tensor` of the same shape as `labels`
            loss_slot=tf.reduce_sum(loss_slot,axis=1)/self.sequence_length #loss_batch:[batch_size]
            loss_slot=tf.reduce_mean(loss_slot) #scalar

            loss_intent= tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.y_intent, logits=(self.logits_intent+self.epsilon())) #[batch_size].#A `Tensor` of the same shape as `labels`
            loss_intent=tf.reduce_mean(loss_intent) #scalar

            loss_domain= tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.y_domain, logits=(self.logits_domain+self.epsilon())) #[batch_size].#A `Tensor` of the same shape as `labels`
            loss_domain=tf.reduce_mean(loss_domain) #scalar

            l2_losses = tf.add_n([tf.nn.l2_loss(v) for v in tf.trainable_variables() if 'bias' not in v.name]) * self.l2_lambda
            weights_intent=tf.nn.sigmoid(tf.cast(self.global_step/1000,dtype=tf.float32))/4        #0-0.25
            weights_domain = tf.nn.sigmoid(tf.cast(self.global_step / 1000, dtype=tf.float32)) / 4 #0-0.25
            weights=weights_intent+weights_domain
            loss = (1.0-weights)*loss_slot+weights_intent*loss_intent+ weights_domain*loss_domain+ l2_losses #loss = (1.0-weights)*loss_slot+weights*loss_intent + l2_losses
            return loss

    def epsilon(self,dtype=tf.float32):
        if dtype is tf.float16:
            return 1e-7
        else:
            return 1e-10

    def train(self):
        """based on the loss, use SGD to update parameter"""
        learning_rate = tf.train.exponential_decay(self.learning_rate, self.global_step, self.decay_steps,self.decay_rate, staircase=True)
        self.learning_rate_=learning_rate
        train_op = tf_contrib.layers.optimize_loss(self.loss_val, global_step=self.global_step,
                                                   learning_rate=learning_rate, optimizer="Adam",clip_gradients=self.clip_gradients)
        return train_op

    def instantiate_weights(self):
        """define all weights here"""
        with tf.name_scope("embedding"):
            self.Embedding = tf.get_variable("Embedding", shape=[self.vocab_size, self.embed_size],initializer=self.initializer)  # [vocab_size,embed_size] tf.random_uniform([self.vocab_size, self.embed_size],-1.0,1.0)
            self.Embedding_slot_label = tf.get_variable("Embedding_slot_label", shape=[self.slots_num_classes, self.embed_size],dtype=tf.float32) #,initializer=self.initializer
        with tf.name_scope("projection"):  # embedding matrix
            # w projection slot is used for slot. slots_num_classes means how many slots name totally.
            self.W_projection_slot = tf.get_variable("W_projection_slot", shape=[self.hidden_size, self.slots_num_classes],initializer=self.initializer)  # [embed_size,label_size]
            self.b_projection_slot = tf.get_variable("b_projection_slot", shape=[self.slots_num_classes])

            # w projection is used for intent. intent_num_classes mean target side classes.
            self.W_projection_intent = tf.get_variable("W_projection_intent", shape=[self.num_filters_total, self.intent_num_classes],initializer=self.initializer)  #[self.hidden_size,self.intent_num_classes]
            self.b_projection_intent = tf.get_variable("b_projection_intent", shape=[self.intent_num_classes])

            # w projection is used for domain. domain_num_classes mean target side classes.
            self.W_projection_domain = tf.get_variable("W_projection_domain",shape=[self.num_filters_total, self.domain_num_classes],initializer=self.initializer)  # [self.hidden_size,self.domain_num_classes]
            self.b_projection_domain = tf.get_variable("b_projection_domain", shape=[self.domain_num_classes])