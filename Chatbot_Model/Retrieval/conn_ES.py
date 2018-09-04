# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     conn_ES.py
   Description :   py连接es
   Author :       charl
   date：          2018/9/4
-------------------------------------------------
   Change Activity: 2018/9/4:
-------------------------------------------------
"""

import sys
import json

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'', 'port':9200}])

