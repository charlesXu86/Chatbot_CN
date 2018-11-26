# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     ie_interface.py
   Description :   信息抽取接口
   Author :       charl
   date：          2018/11/15
-------------------------------------------------
   Change Activity: 2018/11/15:
-------------------------------------------------
"""

from rest_framework.views import APIView
from dss.Serializer import serializer
from django.http import HttpResponse, HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def ner(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })