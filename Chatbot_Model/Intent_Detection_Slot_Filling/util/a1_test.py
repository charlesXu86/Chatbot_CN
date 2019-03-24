# -*- coding: utf-8 -*-
import jieba
import codecs
from Data_util import generate_raw_data

slot_values_file='knowledge_all/slot_values.txt'

#jieba.load_userdict(slot_values_file)
def test_jieba(string):
    result=jieba.lcut(string)
    return result

string='帮我打个从梦想小镇出发到青山湖的快车' #'帮忙关一下主卧所有的挂烫机' #'主卧机顶盒和玄关吸尘器为我关个' #我要关闭壁橱灯''替我关闭一下车库全部的自定义面板' #'帮忙关闭一下一同的彩色灯泡空气炸锅吧'
result=test_jieba(string) #替', '我', '关闭', '一下', '车库', '全部', '的', '自定义面板'
print("result:",result)



def tokenize_sentence(sentence):
    """tokenize sentence"""
    #sentence=sentence.strip()
    result_list=None
    try:
        result_list=jieba.lcut(sentence)
    except:
        print("tokenize_sentence.error:",sentence)
    return result_list

def average_length_user_speech(file):
    #file_object=codecs.open(file,'r','utf-8')
    #lines=file_object.readlines()
    #data_source = 'knowledge/sht_20171125.txt'
    data_dict = generate_raw_data(file)
    sentence_user_speech_list = list(data_dict.keys())
    dict_length={5:0,10:0,15:0,20:0,25:0}
    sum_length=0
    number_line=len(sentence_user_speech_list)
    for i,line in enumerate(sentence_user_speech_list):
        listt=tokenize_sentence(line.strip())
        listt_length=len(listt)
        sum_length+=listt_length
        if listt_length<=5:
            dict_length[5]=dict_length[5]+1
        elif listt_length<=10:
            dict_length[10] = dict_length[10] + 1
        elif listt_length<=15:
            dict_length[15] = dict_length[15] + 1
        elif listt_length<=20:
            dict_length[20] = dict_length[20] + 1
        else:
            dict_length[25] = dict_length[25] + 1
    print("dict_length:",dict_length,";average_length:",float(sum_length)/float(number_line))
    #file_object.close()


#file='knowledge/sht_20171125.txt'
#file='knowledge_skill3/skill3_train_20171114.txt' #('dict_length:', {25: 4614, 10: 178096, 20: 21270, 5: 41632, 15: 48436}, ';average_length:', 8.973320682337578)
#average_length_user_speech(file) #{25: 0, 10: 37632, 20: 50, 5: 16872, 15: 2755}-->{ 10: 37632, 5: 16872, 15: 2755}--->avg:6.6438081278682235


import time
def sayhello(str):
    print("Hello ",str)
    time.sleep(2)

#name_list =['xiaozi','aa','bb','cc']
#start_time = time.time()
#for i in range(len(name_list)):
#    sayhello(name_list[i])
#print ('%d second'% (time.time()-start_time))


import threadpool
def sayhello(str):
    print ("Hello ",str)
    time.sleep(2)

#name_list =['xiaozi','aa','bb','cc'] #start_time = time.time()
#pool = threadpool.ThreadPool(10)
#requests = threadpool.makeRequests(sayhello, name_list)
#[pool.putRequest(req) for req in requests]
#pool.wait() #print ('%d second'% (time.time()-start_time))
