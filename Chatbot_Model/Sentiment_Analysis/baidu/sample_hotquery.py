#!/usr/bin/python
#encoding=utf8
"""
    created by guqi <guqi@baidu.com>
    bce yuqing  tools
"""

import sys
import hashlib
import time
import json
import urllib
import urllib.request as re
import hmac
from baidu import conf


def create_url():
    timestamp = str(int(time.time()))
    token = hmac.new(conf.api_secret, conf.api_key + timestamp, hashlib.sha1).hexdigest()

    auth = {
        'user_key': conf.api_key,
        'token': token,
        'timestamp': timestamp
    }
    params_dict = {
        "province":"广东",
        "city":"深圳",
        "calc_type":"city",
        "time_from":1477238400,
        "time_to":1477321200,
        "top_num":10
        }
    params_dict_str = urllib.quote(json.dumps(params_dict, ensure_ascii=False))
    url_param = urllib.urlencode(auth) + "&params_dict=%s" % params_dict_str
    url = "http://" + conf.host + "/openapi/hotquery?%s" % url_param
    return url

def send(url, method):
    auth = conf.gen_authorization(method, url)
    header = {
        'host': conf.host,
        'content-type': 'application/x-www-form-urlencoded',
        'authorization': auth,
        'accept': '*/*'
    }
    request = re.Request(url, headers=header)
    request.get_method = lambda: method
    response = None
    try:
        response = re.urlopen(request, timeout=60)
        post_res_str = response.read()
        print(post_res_str)
    except re.HTTPError as e:
        print("HTTPError")
        print(e.code, e.reason)
        print(e.read())
    except re.URLError as e:
        print("URLError")
        print(e)

if __name__ == "__main__":
    url = create_url()
    send(url, "GET")





