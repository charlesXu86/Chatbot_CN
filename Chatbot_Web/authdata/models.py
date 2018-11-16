# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models.py
   Description :  自定义用户类
   Author :       charl
   date：          2018/11/9
-------------------------------------------------
   Change Activity: 2018/11/9:
-------------------------------------------------
"""

from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    '''
    用户信息表
    '''
    usernames = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()




