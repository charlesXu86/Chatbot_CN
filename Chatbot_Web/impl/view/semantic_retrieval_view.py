# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     semantic_retrieval_view.py
   Description :   语义检索视图跳转
   Author :       charl
   date：          2018/11/7
-------------------------------------------------
   Change Activity: 2018/11/7:
-------------------------------------------------
"""

from django.shortcuts import render

from Chatbot_Model.Retrieval.sematic_retrieval.semantic_retrieval_search import _val_linking, translate_NL2LF, _parse_query

def semantic_retrieval_view(request):
    context = {}
    return render(request, 'retrieval/semantic_retrieval.html', context)

def search(request):
    '''
    前台的query首先进到这个方法。
    query_type: -1: 未识别到实体
                2:
                3:
                4:
    :param request:
    :return:
    '''
    question = request.GET['question']
    val_d = _val_linking(question)
    lf_question = translate_NL2LF(question)
    answer, msg, query_type = _parse_query(lf_question)

    if msg == 'done':
        if query_type == 1:
            return render(request, 'retrieval/entity.html', {"question": question, "ans":answer})
        elif query_type == 4:
            return render(request, 'retrieval/entity_list.html', {"question": question, "ans": answer})
        elif query_type == 3:
            if isinstance(answer, int):
                answer = str(answer)
            return render(request, 'retrieval/message.html', {"question": question, "ans":answer})
        elif msg == 'none':
            return  render(request, 'retrieval/message.html', {"question": question, "ans": "Find Nothing"})
        else:
            return render(request, 'retrieval/message.html', {"question": question, "ans": answer + " " + msg})



