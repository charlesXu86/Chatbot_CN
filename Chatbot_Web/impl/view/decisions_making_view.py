#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: decisions_making_view.py 
@desc: 辅助决策视图跳转
@time: 2019/01/26 
"""

from django.shortcuts import render


def decisions_making_page(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'decisions_making.html', context)