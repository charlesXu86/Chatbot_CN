#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: word2vec_api.py
@desc: 词向量页面跳转
@time: 2019/05/13 
"""

from django.shortcuts import render

def word2vec_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'word2vec/word2vec.html', context)