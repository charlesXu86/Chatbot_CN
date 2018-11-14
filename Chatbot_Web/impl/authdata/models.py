# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models.py
   Description :
   Author :       charl
   date：          2018/11/9
-------------------------------------------------
   Change Activity: 2018/11/9:
-------------------------------------------------
"""

from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
#     nickname = models.CharField(max_length=50, blank=True)
#     event = models.ForeignKey(on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()




