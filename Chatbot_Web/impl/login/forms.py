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

from .models import Users


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ("username", "email")
