# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     test_interface.py
   Description :   信息抽取接口
   Author :       charl
   date：          2018/11/14
-------------------------------------------------
   Change Activity: 2018/11/14:
-------------------------------------------------
"""
import json

from django.shortcuts import render
from rest_framework.views import APIView
from dss.Serializer import serializer
from django.http import HttpResponse, HttpRequest

# create your views here
def response_as_json(data, foreign_penetrate=False):
    jsonString = serializer(data=data, output_type="json", foreign=foreign_penetrate)
    response = HttpResponse(
        # json.dumps(data, cls=My)
        jsonString,
        content_type="application/json",
    )
    response["Access-Controll-Allow-Origin"] = "*"
    return response

def json_response(data, code=200, foreign_penetrate=False, **kwargs):
    data = {
        "code": code,
        "msg": "成功",
        "data": data,
    }
    return response_as_json(data, foreign_penetrate=foreign_penetrate)

def json_error(error_string="", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)

JsonResponse = json_response
JsonError = json_error
class ReturnJson(APIView):

    def get(self, request, *args, **kwargs):
        return JsonResponse("Hello world!!!!!!!!++++++中文测试")


