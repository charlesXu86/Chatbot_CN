import numpy as np
import pandas as pd
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
import jieba
import pickle

# 加载 pickle 对象的函数
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
# 输入模型的最终单句长度
max_cut_query_lenth = 26

# 加载查询词汇和对应 ID 的字典
word_2_index_dict = load_obj('word_2_index_dict')
# 加载模型输出 ID 和对应标签（种类）的字典
index_2_label_dict = load_obj('index_2_label_dict')
# 加载模型结构
model_structure_json = load_obj('model_structure_json')
model = model_from_json(model_structure_json)
# 加载模型权重
model.load_weights('SMP2018_GlobalAveragePooling1D_model(F1_86).h5')

def query_2_label(query_sentence):
    '''
    input query: "从中山到西安的汽车。"
    return label: "bus"
    '''
    x_input = []
    # 分词 ['从', '中山', '到', '西安', '的', '汽车', '。']
    query_sentence_list = list(jieba.cut(query_sentence))
    # 序列化 [54, 717, 0, 8, 0, 0, 1, 0, 183, 2]
    x = [word_2_index_dict.get(w, 0) for w in query_sentence]
    # 填充  array([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    #      0,   0,   0,  54, 717,   0,   8,   0,   0,   1,   0, 183,   2]], dtype=int32)
    x_input.append(x)
    x_input = pad_sequences(x_input, maxlen=max_cut_query_lenth)
    # 预测
    y_hat = model.predict(x_input)
    # 取最大值所在的序号 11
    pred_y_index = np.argmax(y_hat)
    # 查找序号所对应标签（类别）
    label = index_2_label_dict[pred_y_index]
    return label

if __name__=="__main__":
    query_sentence = '狐臭怎么治？'
    print(query_2_label(query_sentence))