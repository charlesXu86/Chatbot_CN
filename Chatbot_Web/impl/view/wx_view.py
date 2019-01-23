# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     wx_view.py
   Description :   接入微信公众号
   Author :       charl
   date：          2019/1/23
-------------------------------------------------
   Change Activity: 2019/1/23:
-------------------------------------------------
"""

import hashlib

from django.http import HttpResponse

def wechat(request):
    '''
    所有的消息都会先进入这个函数进行处理，这个函数包括两个功能：
         1、微信接入验证是GET方法
         2、微信的正常手发消息是POST方法
    :param request:
    :return:
    '''
    WEIXIN_TOKEN = " "
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("error")
