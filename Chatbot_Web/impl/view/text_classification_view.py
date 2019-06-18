# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   text_classification_view.py
 
@Time    :   2019-06-18 16:37
 
@Desc    :
 
'''


from django.shortcuts import render

def text_classification_page(request):
    context = {}
    return render(request, 'text_classification/text_classification.html', context)