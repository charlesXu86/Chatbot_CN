# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   text_classification.py
 
@Time    :   2019-06-18 16:45
 
@Desc    :    文本分类前后端交互
 
'''


from django.shortcuts import render

from Chatbot_Model.Text_Classification.Fasttext.predict import Predict


def text_cls_post(request):
    '''
    对前端传过来的query进行实体抽取
    :param request: 前端传过来的query
    :return:
    '''
    ctx = {}
    if request.POST:
        sentence = request.POST['cls_text']

        fc = Predict()
        res = fc.fc_predicts(sentence)
        cls_result = res    # 这里调用

        ctx['cls_result'] = cls_result

    return render(request, "text_classification/text_classification.html", ctx)