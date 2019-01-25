# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql
from pymysql import connections
from baidu_baike import settings

class BaiduBaikePipeline(object):
    def __init__(self):
        self.article_file = open("articles.txt", "a+")
    def process_item(self, item, spider):
        # process info for actor
        articles = str(item['articles']).decode('utf-8')
        article_id = str(item['article_id']).decode('utf-8')
        self.article_file.write(article_id + "," + articles.replace("\n", " ") + "\n")

    def close_spider(self, spider):
        self.article_file.close()
