import re

from django import forms
from django.http import request, response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import User

# Create your views here.


#用户信息form类
class UserForm(forms.Form):
    name = forms.CharField(label='用户名', max_length=10, error_messages={'required': '用户名不能为空', 'invalid': "用户名不能超过10位字符"})
    pwd = forms.CharField(label='密  码', widget=forms.PasswordInput, max_length=15, error_messages={'required': '密码不能为空', 'invalid': '密码不能超过15字符'})


def regist(request):
    Method = request.method
    if Method=='POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['name']
            password = uf.cleaned_data['pwd']
            pattern = re.compile(r'\\w')
            if not re.match(pattern, username):
                return render(request, 'regist.html', {'uf': uf, 'registError': "用户名只能是字母,数字,或者下划线组成"})

            try:
                registJudge = User.objects.filter(name=username).get()
                return render(request, 'regist.html', {'registJudge': registJudge})
            except :
                registAdd = User.objects.create(name=username, pwd=password)
                return render(request, 'regist.html', {'registAdd': registAdd, 'name': username})
    else:
        uf = UserForm()
        return render(request, 'regist.html', {'uf': uf, 'Method': Method})

def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['name']
            password = uf.cleaned_data['pwd']
            #对比输入的用户名和密码和数据库中是否一致
            userPassJudge = User.objects.filter(name=username, pwd=password)

            if userPassJudge:
                response = HttpResponseRedirect('homepage/')
                response.set_cookie('cookie_username', username, 300)
                return response
            else:
                return render(request, 'login.html', {'uf': uf, 'error': "用户名或密码错误"})
    else:
        uf = UserForm()
        return render(request, 'login.html', {'uf': uf})


def index(request):
    username = request.COOKIES.get('cookie_username', '')
    return render(request, 'index.html', {'username': username})

def logout(request):
    response = HttpResponseRedirect('/index/')
    response.delete_cookie('cookie_username')
    return response