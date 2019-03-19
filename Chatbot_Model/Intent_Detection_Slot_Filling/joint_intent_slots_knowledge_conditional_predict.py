# -*- coding: utf-8 -*-
#prediction using model.process--->1.load data. 2.create session. 3.feed data. 4.predict
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import tensorflow as tf
import numpy as np
import os
from joint_intent_slots_knowledge_conditional_model import joint_knowledge_conditional_model

from a1_data_util import *
import math
import pickle

#configuration
FLAGS=tf.app.flags.FLAGS
tf.app.flags.DEFINE_float("learning_rate",0.001,"learning rate")
tf.app.flags.DEFINE_integer("batch_size", 1, "Batch size for training/evaluating.") #批处理的大小 32-->128
tf.app.flags.DEFINE_integer("decay_steps", 1000, "how many steps before decay learning rate.") #6000批处理的大小 32-->128
tf.app.flags.DEFINE_float("decay_rate", 0.99, "Rate of decay for learning rate.") #0.87一次衰减多少
tf.app.flags.DEFINE_string("ckpt_dir","checkpoint_67800/","checkpoint location for the model")
tf.app.flags.DEFINE_integer("sequence_length",25,"max sentence length") #100
tf.app.flags.DEFINE_integer("embed_size",128,"embedding size")
tf.app.flags.DEFINE_boolean("is_training",False,"is traning.true:tranining,false:testing/inference")
tf.app.flags.DEFINE_integer("num_epochs",10,"number of epochs to run.")
tf.app.flags.DEFINE_integer("validate_step", 1000, "how many step to validate.") #1000做一次检验
tf.app.flags.DEFINE_integer("hidden_size",128,"hidden size")
tf.app.flags.DEFINE_float("l2_lambda", 0.0001, "l2 regularization")

tf.app.flags.DEFINE_boolean("enable_knowledge",True,"whether to use knwoledge or not.")
tf.app.flags.DEFINE_string("knowledge_path","knowledge_67800","file for data source") #skill3_train_20171114.txt
tf.app.flags.DEFINE_string("data_source","knowledge_67800/training_data_1w.txt","file for data source") #knowledge/sht_20171125.txt training_data_38_50w.txt
tf.app.flags.DEFINE_boolean("test_mode",False,"whether use test mode. if true, only use a small amount of data")

tf.app.flags.DEFINE_string("validation_file","wzz_training_data_20171211_20w_validation.txt","validation file")

# create session and load the model from checkpoint
# load vocabulary for intent and slot name
word2id = create_or_load_vocabulary(None,FLAGS.knowledge_path)
id2word = {value: key for key, value in word2id.items()}
word2id_intent = create_or_load_vocabulary_intent(None,FLAGS.knowledge_path)
id2word_intent = {value: key for key, value in word2id_intent.items()}
word2id_domain= create_or_load_vocabulary_domain(None,FLAGS.knowledge_path)
id2word_domain = {value: key for key, value in word2id_domain.items()}
word2id_slotname = create_or_load_vocabulary_slotname_save(None,FLAGS.knowledge_path)
id2word_slotname = {value: key for key, value in word2id_slotname.items()}
knowledge_dict=load_knowledge(FLAGS.knowledge_path)

basic_pair=FLAGS.knowledge_path+'/raw_data.txt'
q2a_dict,a2q_dict,q_list,q_list_index=process_qa(basic_pair,word2id,FLAGS.sequence_length)

intent_num_classes=len(word2id_intent)
domain_num_classes=len(word2id_domain)

vocab_size=len(word2id)
slots_num_classes=len(id2word_slotname)

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
FLAGS.batch_size = 1
sequence_length_batch = [FLAGS.sequence_length] * FLAGS.batch_size

S_Q_len=len(q_list_index)
print("S_Q_len:",S_Q_len)
model = joint_knowledge_conditional_model(intent_num_classes, FLAGS.learning_rate, FLAGS.decay_steps, FLAGS.decay_rate,
                          FLAGS.sequence_length, vocab_size, FLAGS.embed_size, FLAGS.hidden_size,
                          sequence_length_batch, slots_num_classes, FLAGS.is_training,domain_num_classes,S_Q_len=S_Q_len)
# initialize Saver
saver = tf.train.Saver()
print('restoring Variables from Checkpoint!')
saver.restore(sess, tf.train.latest_checkpoint(FLAGS.ckpt_dir))


slot_values_file = FLAGS.knowledge_path+'/slot_values.txt'
jieba.load_userdict(slot_values_file)

def main(_):
    sentence=u'开灯' #u'帮我打开厕所的灯'
    #indices=[240, 277, 104, 274, 344, 259, 19, 372, 235, 338, 338, 338, 338, 338, 338] #[283, 180, 362, 277, 99, 338, 338, 338, 338, 338, 338, 338, 338, 338, 338] #u'帮我把客厅的灯打开'
    intent,intent_logits, slots,slot_list,similiarity_list_result,domain,domain_score=predict(sentence)
    print(sentence)
    print('intent:{},intent_logits:{},domain:{}'.format(intent, intent_logits,domain))
    for slot_name,slot_value in slots.items():
        print('slots.slot_name:{},slot_value:{}'.format(slot_name, slot_value))
    for i,element in enumerate(slot_list):
        slot_name,slot_value=element
        print('slot_list.slot_name:{},slot_value:{}'.format(slot_name, slot_value))

    #accuracy_similiarity, accuracy_classification=accuarcy_for_similiarity_validation_set()
    #print("accuracy_similiarity:",accuracy_similiarity,";accuracy_classification:",accuracy_classification)

    predict_interactive()

def predict_joint(context_list,query):
    """
    :param context_list: a list of string
    :param query: a string
    :return:
        predicted_intent: string
        score: a string
        slots: a dict
    """
    intent, intent_logits, slots, slot_list, similiarity_list_result, domain,domain_logits = predict(query)
    return intent,intent_logits,slots

def predict_with_one_single_question_add_scores(context_list,query):
    """
    :param context_list: a list of string
    :param query: a string
    :return:
        predicted_intent: string
        score: a string
        slots: a dict
    """
    intent, intent_logits, slots, slot_list, similiarity_list_result, domain,domain_logits = predict(query)
    return intent,intent_logits

def predict_slots(context_list,current_intent):
    """
    :param context_list: a list of string
    :param query: a string
    :return:
        predicted_intent: string
        score: a string
        slots: a dict
    """
    query=context_list[-1]
    intent, intent_logits, slots, slot_list, similiarity_list_result, domain,domain_score = predict(query)
    return slots

def accuarcy_for_similiarity_validation_set():#read validation data from outside file, and compute accuarcy for classification model and similiarity model
    #1.get validation set
    source_file_name=FLAGS.knowledge_path+"/" +FLAGS.validation_file
    dict_pair=generate_raw_data(source_file_name, test_mode=False, knowledge_path=FLAGS.knowledge_path, target_file=source_file_name+'_raw_data')
    #2.loop each data
    count_similiarity_right=0
    count_classification_right=0
    len_validation=len(dict_pair)

    i=0
    for sentence,value in dict_pair.items():
        #3.call predict
        intent, intent_logits, slots, slot_list, similiarity_list_result,domain,domain_score = predict(sentence)
        y_intent_target=value['intent']
        similiar_intent=similiarity_list_result[0]
        if similiar_intent ==y_intent_target:
            count_similiarity_right+=1
        if intent==y_intent_target:
            count_classification_right+=1
        if i%10==0:
            print(i,"count_similiarity_right%:",str(float(count_similiarity_right)/float(i+1)),";count_classification_right%:",str(float(count_classification_right)/float(i+1)))
            print('sentence:{},y_intent_target:{},intent_classification:{},intent_similiar:{}'.format(sentence,y_intent_target,intent,similiar_intent))
        i=i+1
    #4.get accuracy
    accuracy_similiarity=float(count_similiarity_right)/float(len_validation)
    accuracy_classification = float(count_classification_right) / float(len_validation)

    return accuracy_similiarity,accuracy_classification

def accuarcy_for_similiarity_validation_setX(): #read cached validation data
    #1.get validation set
    traing_data, valid_data, test_data, vocab_size, intent_num_classes, slots_num_classes = generate_training_data(FLAGS.data_source,FLAGS.knowledge_path,FLAGS.test_mode,sequence_length=FLAGS.sequence_length)
    x_valid, y_intent_valid, y_slots_valid = valid_data
    #2.loop each data
    count_similiarity_right=0
    count_classification_right=0
    len_validation=len(x_valid)
    for i, x_indices in enumerate(x_valid):
        y_intent=y_intent_valid[i]
        sentence=get_sentence_from_index(x_indices)
        #3.call predict
        intent, intent_logits, slots, slot_list, similiarity_list_result,model = predict(sentence)
        y_intent_target=id2word_intent[y_intent]
        similiar_intent=similiarity_list_result[0]
        if similiar_intent ==y_intent_target:
            count_similiarity_right+=1
        if intent==y_intent_target:
            count_classification_right+=1
        if i%10==0:
            print(i,"count_similiarity_right%:",str(float(count_similiarity_right)/float(i+1)),";count_classification_right%:",str(float(count_classification_right)/float(i+1)))
            print('sentence:{},y_intent_target:{},intent_classification:{},intent_similiar:{}'.format(sentence,y_intent_target,intent,similiar_intent))
    #4.get accuracy
    accuracy_similiarity=float(count_similiarity_right)/float(len_validation)
    accuracy_classification = float(count_classification_right) / float(len_validation)

    return accuracy_similiarity,accuracy_classification

def get_sentence_from_index(x_indices):
    sentence=[ id2word.get(index,UNK) for index in x_indices]
    sentence="".join(sentence)
    return sentence

def predict(sentence,enable_knowledge=1):
    """
    :param sentence: a sentence.
    :return: intent and slots
    """
    #print("FLAGS.knowledge_path====>:",FLAGS.knowledge_path)
    sentence_indices=index_sentence_with_vocabulary(sentence,word2id,FLAGS.sequence_length,knowledge_path=FLAGS.knowledge_path)
    y_slots= get_y_slots_by_knowledge(sentence,FLAGS.sequence_length,enable_knowledge=enable_knowledge,knowledge_path=FLAGS.knowledge_path)
    #print("predict.y_slots:",y_slots)
    qa_list_length=len(q_list_index)
    feed_dict = {model.x: np.reshape(sentence_indices,(1,FLAGS.sequence_length)),
                 model.y_slots:np.reshape(y_slots,(1,FLAGS.sequence_length)),
                 model.S_Q:np.reshape(q_list_index,(qa_list_length,FLAGS.sequence_length)), #should be:[self.S_Q_len, self.sentence_len]
                 model.dropout_keep_prob:1.0}
    logits_intent,logits_slots,similiarity_list,logits_domain = sess.run([model.intent_scores,model.logits_slots,model.similiarity_list,model.domain_scores], feed_dict) #similiarity_list:[1,None]
    intent,intent_logits,slots,slot_list,similiarity_list_result,domain,domain_logits=get_result(logits_intent,logits_slots,sentence_indices,similiarity_list,logits_domain)
    return intent,intent_logits,slots,slot_list,similiarity_list_result,domain,domain_logits

def get_y_slots_by_knowledge(sentence,sequence_length,enable_knowledge=1,knowledge_path=None):
    """get y_slots using dictt.e.g. dictt={'slots': {'全部范围': '全', '房间': '储藏室', '设备名': '四开开关'}, 'user': '替我把储藏室四开开关全关闭一下', 'intent': '关设备<房间><全部范围><设备名>'}"""
    #knowledge_dict=#{'储藏室': '房间', '全': '全部范围', '四开开关': '设备名'}
    user_speech_tokenized=tokenize_sentence(sentence,knowledge_path=knowledge_path) #['替', '我', '把', '储藏室', '四开', '开关', '全', '关闭', '一下']
    result=[word2id_slotname[O]]*sequence_length
    if enable_knowledge=='1' or enable_knowledge==1:
        for i,word in enumerate(user_speech_tokenized):
            slot_name=knowledge_dict.get(word,None)
            #print('i:{},word_index:{},word:{},slot_name:{}'.format(i,word,id2word.get(word,UNK),slot_name))
            if slot_name is not None:
                try:
                    result[i]=word2id_slotname[slot_name]
                except:
                    pass
    return result

def predict_interactive():
    sys.stdout.write("Please Input Story.>")
    sys.stdout.flush()
    question = sys.stdin.readline()
    enable_knowledge=1
    while question:
        if question.find("disable_knowledge")>=0:
            enable_knowledge=0
            print("knowledge disabled")
            print("Please Input Story>")
            sys.stdout.flush()
            question = sys.stdin.readline()
        elif question.find("enable_knowledge")>=0:
            enable_knowledge=1
            #3.read new input
            print("knowledge enabled")
            print("Please Input Story>")
            sys.stdout.flush()
            question = sys.stdin.readline()

        #1.predict using quesiton
        intent, intent_logits,slots,slot_list,similiarity_list,domain,domain_score=predict(question,enable_knowledge=enable_knowledge)
        #2.print
        print('技能:{},置信度:{}'.format(domain,domain_score))
        print('意图:{},置信度:{}'.format(intent, intent_logits))
        for slot_name, slot_value in slots.items():
            print('slot_name:{}-->slot_value:{}'.format(slot_name, slot_value))
        score, is_noise=compute_score_noise(domain_score,intent_logits,slots)
        print('噪声输入：{},综合分数:{}'.format("是" if is_noise==True else "否",score)) #1 if 5>3 else 0
        #3.read new input
        print("Please Input Story>")
        sys.stdout.flush()
        question = sys.stdin.readline()

def compute_score_noise(domain_score,intent_logits,slots,domain_weight=0.4,intent_weight=0.4,slots_weight=0.2):
    """
    compute whether it is a noise or not.今天
    :param domain_score:
    :param intent_logits:
    :param slots:
    :return:
    """
    score=0.0
    is_noise=False
    slots_score=min(1.0,float(len(slots))/2.0)
    score=domain_weight*domain_score+intent_logits*intent_weight+slots_weight*slots_score
    if score>=0.5:
        is_noise=False
    else:
        is_noise=True
    return score,is_noise
    pass

def get_result(logits_intent,logits_slots,sentence_indices,similiarity_list,logits_domain,top_number=3):
    index_intent= np.argmax(logits_intent[0]) #index of intent
    intent_logits=logits_intent[0][index_intent]
    #print("intent_logits:",index_intent)
    intent=id2word_intent[index_intent]

    index_domain=np.argmax(logits_domain[0]) #index of domain
    domain=id2word_domain[index_domain]
    domain_score=logits_domain[0][index_domain]

    slots=[]
    indices_slots=np.argmax(logits_slots[0],axis=1) #[sequence_length]
    for i,index in enumerate(indices_slots):
        slots.append(id2word_slotname[index])
    slots_dict={}
    slot_list=[]
    for i,slot in enumerate(slots):
        word=id2word[sentence_indices[i]]
        #print(i,"slot:",slot,";word:",word)
        if slot!=O and word!=PAD and word!=UNK:
            slots_dict[slot]=word
            slot_list.append((slot,word))

    #get top answer for the similiarity list.
    similiarity_list_top = np.argsort(similiarity_list)[-top_number:]
    similiarity_list_top = similiarity_list_top[::-1]
    similiarity_list_result=[]
    print('最相关问题')
    for k,index in enumerate(similiarity_list_top):
        question=q_list[index]
        answer=q2a_dict[question]
        similiarity_list_result.append(answer)
        print('问题{}：{}, action:{}'.format(k,question, answer))
    return intent,intent_logits,slots_dict,slot_list,similiarity_list_result,domain,domain_score

if __name__ == "__main__":
    tf.app.run()