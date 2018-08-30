import re

from django import forms
from django.http import request, response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth

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
                return render(request, 'regist.templates', {'uf': uf, 'registError': "用户名只能是字母,数字,或者下划线组成"})

            try:
                registJudge = User.objects.filter(name=username).get()
                return render(request, 'regist.templates', {'registJudge': registJudge})
            except :
                registAdd = User.objects.create(name=username, pwd=password)
                return render(request, 'regist.templates', {'registAdd': registAdd, 'name': username})
    else:
        uf = UserForm()
        return render(request, 'regist.templates', {'uf': uf, 'Method': Method})

# regist 方法
def register2(request):
    errors = []
    account = None
    password = None

    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('用户名不能为空')
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors.append('密码不能为空')
        else:
            password = request.POST.get('password')

        if account is not None and password is not None :
            user = User.objects.create_user(account,password)
            user.save()

            userlogin = auth.authenticate(username = account,password = password)
            auth.login(request,userlogin)
            return HttpResponseRedirect('/')

    return render(request,'regist.templates', {'errors': errors})

def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['name']
            password = uf.cleaned_data['pwd']
            #对比输入的用户名和密码和数据库中是否一致
            userPassJudge = User.objects.filter(name=username, pwd=password)

            if userPassJudge:
                response = HttpResponseRedirect('/')
                response.set_cookie('cookie_username', username, 300)
                return response
            else:
                return render(request, 'login.templates', {'uf': uf, 'error': "用户名或密码错误"})
    else:
        uf = UserForm()
        return render(request, 'login.templates', {'uf': uf})


def index(request):
    username = request.COOKIES.get('cookie_username', '')
    return render(request, 'homepage.html', {'username': username})

def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('cookie_username')
    return response