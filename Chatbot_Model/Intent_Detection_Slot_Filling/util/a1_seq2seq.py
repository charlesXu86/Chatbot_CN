# -*- coding: utf-8 -*-
import tensorflow as tf

# 【该方法测试的时候使用】返回一个方法。这个方法根据输入的值，得到对应的索引，再得到这个词的embedding.
def extract_argmax_and_embed(embedding, output_projection=None):
    """
    Get a loop_function that extracts the previous symbol and embeds it. Used by decoder.
    :param embedding: embedding tensor for symbol
    :param output_projection: None or a pair (W, B). If provided, each fed previous output will
    first be multiplied by W and added B.
    :return: A loop function
    """
    def loop_function(prev, _):
        if output_projection is not None:
            prev = tf.matmul(prev, output_projection[0]) + output_projection[1]
        prev_symbol = tf.argmax(prev, 1) #得到对应的INDEX
        emb_prev = tf.gather(embedding, prev_symbol) #得到这个INDEX对应的embedding
        return emb_prev
    return loop_function

# version1:attention mechansion based on current time stamp and encode states to get attention vector, then concat attention vector with decode input by using feed forward layer.
# 如果是训练，使用训练数据的输入；如果是test,将t时刻的输出作为t+1时刻的s输入
def rnn_decoder_with_attention(decoder_inputs, initial_state, cell, loop_function,encode_source_states,input_knowledges,hidden_size,scope=None,
                               use_self_attention=False,use_multiplication_attention=False):#3D Tensor [batch_size x attn_length x attn_size]
    """RNN decoder for the sequence-to-sequence model.
    Args:
        decoder_inputs: A list of 2D Tensors [batch_size x input_size].it is decoder input.
        initial_state: 2D Tensor with shape [batch_size x cell.state_size].it is the encoded vector of input sentences, which represent 'thought vector'
        cell: core_rnn_cell.RNNCell defining the cell function and size.
        loop_function: If not None, this function will be applied to the i-th output
            in order to generate the i+1-st input, and decoder_inputs will be ignored,
            except for the first element ("GO" symbol). This can be used for decoding,
            but also for training to emulate http://arxiv.org/abs/1506.03099.
            Signature -- loop_function(prev, i) = next
                * prev is a 2D Tensor of shape [batch_size x output_size],
                * i is an integer, the step number (when advanced control is needed),
                * next is a 2D Tensor of shape [batch_size x input_size].
        encode_source_states: 3D Tensor [batch_size x attn_length x attn_size].it is represent input X.
        input_knowledges:    3D Tensor [batch_size x decoder_sent_length x slots_voc_size].represent knowledge we have. each knowledge is represent by multi-hot.such as [0,1,0,0,1,0,...,0]
        hidden_size: a scalar.
        scope: VariableScope for the created subgraph; defaults to "rnn_decoder".
    Returns:
        A tuple of the form (outputs, state), where:
        outputs: A list of the same length as decoder_inputs of 2D Tensors with
            shape [batch_size x output_size] containing generated outputs.
        state: The state of each cell at the final time-step.
            It is a 2D Tensor of shape [batch_size x cell.state_size].
            (Note that in some cases, like basic RNN cell or GRU cell, outputs and
            states can be the same. They are different for LSTM cells though.)
    """
    with tf.variable_scope(scope or "rnn_decoder"):
        batch_size,sequence_length,_=encode_source_states.get_shape().as_list()
        encode_source_states_=tf.layers.dense(encode_source_states,hidden_size,use_bias=False) #[batch_size, sequence_length,hidden_size]. transform encode source states in advance, only once.
        outputs = []
        prev = None
        current_target_hidden_state = initial_state #shape:[batch_size x state_size]
        previous_target_hidden_state=current_target_hidden_state
        input_knowledge=None
        for i, inp in enumerate(decoder_inputs):#循环解码部分的输入。如sentence_length个[batch_size x input_size].如果是训练，使用训练数据的输入；如果是test, 将t时刻的输出作为t + 1 时刻的s输入
            if loop_function is not None and prev is not None:#测试的时候：如果loop_function不为空且前一个词的值不为空，那么使用前一个的值作为RNN的输入
                with tf.variable_scope("loop_function", reuse=True):
                    inp = loop_function(prev, i)
            if i > 0:
                tf.get_variable_scope().reuse_variables()

            #output,current_target_hidden_state=cell(inp,attention_vector)
            output, current_target_hidden_state = cell(inp, current_target_hidden_state)

            if use_self_attention: #use multi-head attention mechanism: check paper: 'Attention is all you need'
                attention_vector=multi_head_attention(current_target_hidden_state, encode_source_states_, hidden_size)
            #elif use_multiplication_attention:attention_vector = multiplication_attention(current_target_hidden_state, encode_source_states_, hidden_size)
            else:
                if use_multiplication_attention: #use multiplication attention. check paper:'Effective approaches to attention-based neural machine translation'
                    attention_weights=multiplication_attention_get_weights(previous_target_hidden_state,encode_source_states_,hidden_size)#current_target_hidden_state
                else: # additive attention mechansim from 'Learn to alignment for machine translation'. this is a default method.
                #1. the current target hidden state is compared with all source states to derive attention weights
                    attention_weights=score_function(previous_target_hidden_state,encode_source_states_,hidden_size) #[batch_size x sequence_length].current_target_hidden_state
                #2. based on the attention weights we compute a context vector as the weighted average of the source states.
                context_vector=weighted_sum(attention_weights,encode_source_states) #[batch_size x attn_size]
                #3. combine the context vector with the current target hidden state to yield the final attention vector
                # below two lines is for aligned encoder hidden state. for last position of decoder, target will be <END> token, we use zero vector.
                if i!=len(decoder_inputs)-1:
                    aligned_encoder_hiden_state=encode_source_states[:,i,:]
                    input_knowledge=input_knowledges[:,i,:]
                else:
                    aligned_encoder_hiden_state=tf.zeros(encode_source_states[:,0,:].get_shape().as_list())
                    input_knowledge=tf.zeros_like(input_knowledge) #input_knowledges[:,0,:].get_shape().as_list()

                attention_vector=get_attention_vector(context_vector,current_target_hidden_state,aligned_encoder_hiden_state,input_knowledge,hidden_size)
            #4. the attention vector is fed as an input to the next time step (input feeding).
            outputs.append(attention_vector) # 将输出添加到结果列表中

            previous_target_hidden_state=current_target_hidden_state
            if loop_function is not None:
                prev = attention_vector
    return outputs, current_target_hidden_state

def attention_util(query,sources,hidden_size):
    # 1. the current target hidden state is compared with all source states to derive attention weights
    attention_weights = score_function(query, sources, hidden_size)  # [batch_size x sequence_length].current_target_hidden_state
    # 2. based on the attention weights we compute a context vector as the weighted average of the source states.
    context_vector = weighted_sum(attention_weights, sources)  # [batch_size x attn_size]
    attention_vector = get_attention_vector_simple(context_vector, query, hidden_size)
    return attention_vector

def get_attention_vector_simple(context_vector,current_target_hidden_state,hidden_size):
    """
    get attention vector by concat context vector and current target hidden state, then use feed foward layer.
    attention_vector=tanh(Wc[c;h])
    :param context_vector: [batch_size x attn_size]
    :param current_target_hidden_state: [batch_size x state_size]
    :return get_attention_vector:[batch_size,hidden_size]
    """

    with tf.variable_scope("attention_vector_simple"):
        #if aligned_encoder_hiden_state is not None:
        concat_vector = [context_vector, current_target_hidden_state]
        #else:
        #    concat_vector=[context_vector,current_target_hidden_state]
        attention_vector=tf.layers.dense(tf.concat(concat_vector,-1),hidden_size,activation=tf.nn.tanh,use_bias=False) #[batch_size,hidden_size]
    return attention_vector #[batch_size,hidden_size]

def get_attention_vector(context_vector,current_target_hidden_state,aligned_encoder_hiden_state,input_knowledge,hidden_size):
    """
    get attention vector by concat context vector and current target hidden state, then use feed foward layer.
    attention_vector=tanh(Wc[c;h])
    :param context_vector: [batch_size x attn_size]
    :param current_target_hidden_state: [batch_size x state_size]
    :param aligned_encoder_hiden_state:[batch_size x hidden_size]
    :return get_attention_vector:[batch_size,hidden_size]
    """

    with tf.variable_scope("attention_vector"):
        #if aligned_encoder_hiden_state is not None:
        concat_vector = [context_vector, current_target_hidden_state, aligned_encoder_hiden_state,input_knowledge]
        #else:
        #    concat_vector=[context_vector,current_target_hidden_state]
        attention_vector=tf.layers.dense(tf.concat(concat_vector,-1),hidden_size,activation=tf.nn.tanh,use_bias=False) #[batch_size,hidden_size]
    return attention_vector #[batch_size,hidden_size]

def score_function(current_target_hidden_state,encode_source_states,hidden_size):
    """
    the current target hidden state is compared with all source states to derive attention weights. score=V_a.tanh(W1*h_t + W2_H_s)
    :param current_target_hidden_state: [batch_size x hidden_size]
    :param encode_source_states: [batch_size x sequence_length x hidden_size]
    :return: attention_weights: [batch_size x sequence_length]
    """
    with tf.variable_scope("score_function"):
        _, sequence_length, _=encode_source_states.get_shape().as_list()
        v= tf.get_variable("v_a", shape=[hidden_size,1],initializer=tf.random_normal_initializer(stddev=0.1))
        g=tf.get_variable("attention_g",initializer=tf.sqrt(1.0/hidden_size))
        b = tf.get_variable("bias", shape=[hidden_size], initializer=tf.zeros_initializer)

        # get part1: transformed current target hidden state
        current_target_hidden_state=tf.expand_dims(current_target_hidden_state,axis=1) #[batch_size,1,hidden_size]
        part1=tf.layers.dense(current_target_hidden_state, hidden_size,use_bias=False) #[batch_size,1,hidden_size]
        # additive and activated
        attention_logits=tf.nn.tanh(part1+encode_source_states+b) #[batch_size, sequence_length,hidden_size]
        # transform
        attention_logits=tf.reshape(attention_logits,(-1,hidden_size)) #[batch_size*sequence_length,hidden_size]
        normed_v=g*v*tf.rsqrt(tf.reduce_sum(tf.square(v))) #"Weight Normalization: A Simple Reparameterization to Accelerate Training of Deep Neural Networks."normed_v=g*v/||v||,
        attention_weights=tf.reshape(tf.matmul(attention_logits,normed_v),(-1,sequence_length)) #[batch_size,sequence_length]
        # normalized
        attention_weights_max=tf.reduce_max(attention_weights,axis=1,keep_dims=True) #[batch_size,1]
        attention_weights=tf.nn.softmax(attention_weights-attention_weights_max) #[batch_size,sequence_length]
    return attention_weights #[batch_size x sequence_length]

def multiplication_attention_get_weights(current_target_hidden_state,encode_source_states_,hidden_size):
    """
    the current target hidden state is compared with all source states to derive attention weights. score=qWc*normalized
    :param current_target_hidden_state: [batch_size x hidden_size]
    :param encode_source_states: [batch_size x sequence_length x hidden_size]
    :return: attention_weights: [batch_size x sequence_length]
    """
    _,sequence_length,_=encode_source_states_.get_shape().as_list()
    with tf.variable_scope("multiplication_attention"):
        w = tf.get_variable("w", shape=[hidden_size, sequence_length*sequence_length], initializer=tf.random_normal_initializer(stddev=0.1))
        v= tf.get_variable("v_a", shape=[hidden_size,1],initializer=tf.random_normal_initializer(stddev=0.1))
        g=tf.get_variable("attention_g",initializer=tf.sqrt(1.0/hidden_size))
        #0.transform
        current_target_hidden_state=tf.layers.dense(current_target_hidden_state,units=hidden_size)
        #1.m=qW
        m=tf.matmul(current_target_hidden_state,w) #[batch_size,sequence_length*sequence_length]
        m=tf.reshape(m,(-1,sequence_length,sequence_length))
        #2.attention_logits=(qW)*c=m*c
        attention_logits=tf.reshape(tf.matmul(m,encode_source_states_),(-1,hidden_size))
        #3.normalized
        normed_v=g*v*tf.rsqrt(tf.reduce_sum(tf.square(v))) #"Weight Normalization: A Simple Reparameterization to Accelerate Training of Deep Neural Networks."normed_v=g*v/||v||,
        attention_logits=tf.matmul(attention_logits,normed_v) #[batch_size x sequence_length] # [1,5,1000], [1000,1].
        #4.compute weights by using softmax
        attention_logits_max=tf.reduce_max(attention_logits,axis=1,keep_dims=True) #[batch_size,sequence_length]
        attention_weights=tf.nn.softmax(attention_logits-attention_logits_max) ##[batch_size,sequence_length]
        attention_weights=tf.transpose(attention_weights,perm=(1,0))
    return attention_weights #[batch_size x sequence_length]

def multiplication_attention(current_target_hidden_state,encode_source_states_,hidden_size):
    """
    the current target hidden state is compared with all source states to derive attention weights. score=qWc
    :param current_target_hidden_state: [batch_size x hidden_size]
    :param encode_source_states: [batch_size x sequence_length x hidden_size]
    :return: attention_weights: [batch_size x hidden_size]
    """
    _,sequence_length,_=encode_source_states_.get_shape().as_list()
    with tf.variable_scope("multiplication_attention"):
        W=tf.get_variable("w", shape=[hidden_size*2,sequence_length],initializer=tf.random_normal_initializer(stddev=0.1))
        #1. m=qW: shape should be:[batch_size,hidden_size*sequence_length]
        m=tf.matmul(current_target_hidden_state,W) #[batch_size,sequence_length]<-----tf.matmul((b,h),(h,L))
        #2. mc
        result=tf.squeeze(tf.matmul(tf.expand_dims(m,axis=1),encode_source_states_),axis=1)#[batch_size,hidden_size]<---[batch_size,1,hidden_size]<--tf.matmul((b,1,L),(b,L,h))
        #3. normalized
    return result


def multi_head_attention(current_target_hidden_state,encode_source_states_,hidden_size,h=10): #d_k=hidden_size/h.e.g.10.
    """
    the current target hidden state is compared with all source states to derive attention weights. score=V_a.tanh(W1*h_t + W2_H_s)
    :param current_target_hidden_state: [batch_size x hidden_size]
    :param encode_source_states: [batch_size x sequence_length x hidden_size]
    :return: attention_weights: [batch_size x hidden_size]
    """
    d_k = hidden_size / h
    with tf.variable_scope("self_attention"):
        #1.project current_target_hidden_state,encode_source_states_
        current_target_hidden_state=tf.layers.dense(current_target_hidden_state,hidden_size) #[batch_size,hidden_size]
        #2.split current_target_hidden_state and encode_source_states_ to a higher demension
        current_target_hidden_state = tf.stack(tf.split(current_target_hidden_state, h, axis=1), axis=1)  #[batch_size,h,d_k]
        batch_size,sequence_length,_=encode_source_states_.get_shape().as_list()
        encode_source_states_=tf.stack(tf.split(encode_source_states_, h, axis=2), axis=1)                #[batch_size,h,sequence_length,d_k]
        #3.matmul
        current_target_hidden_state=tf.expand_dims(current_target_hidden_state,axis=2) #[batch_size,h,1,d_k]
        encode_source_states_=tf.reshape(encode_source_states_,(batch_size,h,d_k,sequence_length)) #[batch_size,h,d_k,sequence_length]
        result=tf.matmul(current_target_hidden_state,encode_source_states_) #[batch_size,h,1,sequence_length]<------tf.matmul([batch_size,h,1,d_k],[batch_size,h,d_k,sequence_length])
        result = result * (1.0 / tf.sqrt(tf.cast(hidden_size, tf.float32))) #scaled
        result=tf.reshape(result,(batch_size,-1))
        #4.project back to required shape #[batch_size,hidden_size]
        result=tf.layers.dense(result,hidden_size)
    return result

def weighted_sum(attention_weights,encode_source_states):
    """
    weighted sum
    :param attention_weights:[batch_size x sequence_length]
    :param encode_source_states:[batch_size x sequence_length x attn_size]
    :return: weighted_sum: [batch_size, attn_size]
    """
    attention_weights=tf.expand_dims(attention_weights,axis=-1)      #[batch_size x sequence_length x 1]
    weighted_sum=tf.multiply(attention_weights,encode_source_states) #[batch_size x sequence_length x attn_size]
    weighted_sum=tf.reduce_sum(weighted_sum,axis=-1)                 #[batch_size x attn_size]
    return weighted_sum                                              #[batch_size x attn_size]



##BELOW METHOD CAN BE DELETED#########################################################################################################################################################
# RNN的解码部分。
# version2: get attention vector using attention mechanism, invoke rnn together with decode input as final outupt.
# 如果是训练，使用训练数据的输入；如果是test,将t时刻的输出作为t+1时刻的s输入
def rnn_decoder_with_attention_TRAIL(decoder_inputs, initial_state, cell, loop_function,encode_source_states,hidden_size,scope=None):#3D Tensor [batch_size x attn_length x attn_size]
    """RNN decoder for the sequence-to-sequence model.
    Args:
        decoder_inputs: A list of 2D Tensors [batch_size x input_size].it is decoder input.
        initial_state: 2D Tensor with shape [batch_size x cell.state_size].it is the encoded vector of input sentences, which represent 'thought vector'
        cell: core_rnn_cell.RNNCell defining the cell function and size.
        loop_function: If not None, this function will be applied to the i-th output
            in order to generate the i+1-st input, and decoder_inputs will be ignored,
            except for the first element ("GO" symbol). This can be used for decoding,
            but also for training to emulate http://arxiv.org/abs/1506.03099.
            Signature -- loop_function(prev, i) = next
                * prev is a 2D Tensor of shape [batch_size x output_size],
                * i is an integer, the step number (when advanced control is needed),
                * next is a 2D Tensor of shape [batch_size x input_size].
        encode_source_states: 3D Tensor [batch_size x attn_length x attn_size].it is represent input X.
        hidden_size: a scalar.
        scope: VariableScope for the created subgraph; defaults to "rnn_decoder".
    Returns:
        A tuple of the form (outputs, state), where:
        outputs: A list of the same length as decoder_inputs of 2D Tensors with
            shape [batch_size x output_size] containing generated outputs.
        state: The state of each cell at the final time-step.
            It is a 2D Tensor of shape [batch_size x cell.state_size].
            (Note that in some cases, like basic RNN cell or GRU cell, outputs and
            states can be the same. They are different for LSTM cells though.)
    """
    with tf.variable_scope(scope or "rnn_decoder"):
        batch_size,sequence_length,_=encode_source_states.get_shape().as_list()
        encode_source_states_=tf.layers.dense(encode_source_states,hidden_size,use_bias=False) #[batch_size, sequence_length,hidden_size]. transform encode source states in advance, only once.
        outputs = []
        prev = None
        current_target_hidden_state = initial_state #shape:[batch_size x state_size]
        for i, inp in enumerate(decoder_inputs):#循环解码部分的输入。如sentence_length个[batch_size x input_size].如果是训练，使用训练数据的输入；如果是test, 将t时刻的输出作为t + 1 时刻的s输入
            if loop_function is not None and prev is not None:#测试的时候：如果loop_function不为空且前一个词的值不为空，那么使用前一个的值作为RNN的输入
                with tf.variable_scope("loop_function", reuse=True):
                    inp = loop_function(prev, i)
            if i > 0:
                tf.get_variable_scope().reuse_variables()
            #1. the current target hidden state is compared with all source states to derive attention weights
            attention_weights=score_function(current_target_hidden_state,encode_source_states_,hidden_size) #[batch_size x sequence_length]
            #2. based on the attention weights we compute a context vector as the weighted average of the source states.
            context_vector=weighted_sum(attention_weights,encode_source_states) #[batch_size x attn_size]
            #3. combine the context vector with the current target hidden state to yield the final attention vector
            attention_vector=get_attention_vector(context_vector,current_target_hidden_state,hidden_size)
            #4. the attention vector is fed as an input to the next time step (input feeding).
            print("inp:",inp,";attention_vector:",attention_vector) #('inp:', shape=(?, 2000) dtype=float32>, ';attention_vector:', shape=(1, 1000) dtype=float32>)
            output,current_target_hidden_state=cell(inp,attention_vector)
            outputs.append(output) # 将输出添加到结果列表中
            if loop_function is not None:
                prev = output
    return outputs, current_target_hidden_state