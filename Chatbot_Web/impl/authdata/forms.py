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

from Chatbot_Web.impl.authdata.models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
