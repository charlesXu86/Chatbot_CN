# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     forms.py
   Description :
   Author :       charl
   date：          2018/11/9
-------------------------------------------------
   Change Activity: 2018/11/9:
-------------------------------------------------
"""

from django.contrib.auth.forms import UserCreationForm

from Chatbot_Web.authdata.models import User
# from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
