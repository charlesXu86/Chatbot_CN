#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: entity_extraction_remote.py 
@desc: 调用tensorflow server端返回的数据
@time: 2019/05/16 
"""

import  tensorflow as tf

from tensorflow_serving.apis import classification_pb2
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from grpc.beta import implementations



'''
生辰客户端请求




'''




def get_model_response(text):
    '''
    获取模型返回的结果
    :param text: 前端传过来的经过预处理（strip等）的query数据。
    :return: 返回的是tensorflow server端处理的结果，数据结构为json格式。
    '''

    # 创建一个RPC stub，这个stub允许我们调用远程服务器的方法
    channel = implementations.insecure_channel('127.0.0.1', 9000)   # 创建一个通道
    stub = prediction_service_pb2.beta_create_PredictionService_stub()