# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     welcome_view.py
   Description :   欢迎页视图跳转
   Author :       charl
   date：          2018/11/9
-------------------------------------------------
   Change Activity: 2018/11/9:
-------------------------------------------------
"""

from django.shortcuts import render,redirect
from Chatbot_Web.authdata.forms import RegisterForm
from django import forms
from django.contrib.auth import authenticate,login

# from Chatbot_Web.impl.login.models import User

def welcome_views(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'welcome.html', context)

def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'login/register.html', context={'form': form, 'next': redirect_to})

# def login(request):
#     if request.method == "POST":
#         uf = UserFormLogin(request.POST)
#         if uf.is_valid():
#             # 获取表单信息
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             userResult = Users.objects.filter(username=username, password=password)
#             if (len(userResult)>0):
#                 return render('success.html', {'operation':"登录"})
#             else:
#                 return HttpResponse("该用户不存在")
#     else:
#         uf = UserFormLogin()
#     return render('login/login.html', {'uf': uf})

def do_login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'base.html')
    else:
        return render(request, 'login/login.html', {
            'username': username,
            'password': password
        })

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())