#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function


from baidu_baike.items import BaiduBaikeItem
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import urlparse

class BaiduBaikeSpider(scrapy.Spider, object):
    name = 'baidu'
    allowed_domains = ["baike.baidu.com"]
    start_urls = ['https://baike.baidu.com/item/%E5%91%A8%E6%98%9F%E9%A9%B0/169917?fr=aladdin']
#    start_urls = ['https://baike.baidu.com/item/%E4%B8%83%E5%B0%8F%E7%A6%8F']
    
    def _get_from_findall(self, tag_list):
        result = []        
                           
        for slist in tag_list:
            tmp = slist.get_text()
            result.append(tmp)
        return result

    def parse(self, response):
        page_category = response.xpath("//dd[@id='open-tag-item']/span[@class='taglist']/text()").extract()
        page_category = [l.strip() for l in page_category]
        item = BaiduBaikeItem()

        # tooooo ugly,,,, but can not use defaultdict
        for sub_item in [ 'actor_bio', 'actor_chName', 'actor_foreName', 'actor_nationality', 'actor_constellation', 'actor_birthPlace', 'actor_birthDay', 'actor_repWorks', 'actor_achiem', 'actor_brokerage','movie_bio', 'movie_chName', 'movie_foreName', 'movie_prodTime', 'movie_prodCompany', 'movie_director', 'movie_screenwriter', 'movie_genre', 'movie_star', 'movie_length', 'movie_rekeaseTime', 'movie_language', 'movie_achiem' ]:
            item[sub_item] = None

        if u'演员' in page_category:
            print("Get a actor page")
            soup = BeautifulSoup(response.text, 'lxml')
            summary_node = soup.find("div", class_ = "lemma-summary")
            item['actor_bio'] = summary_node.get_text().replace("\n"," ")

            all_basicInfo_Item = soup.find_all("dt", class_="basicInfo-item name")
            basic_item = self._get_from_findall(all_basicInfo_Item)
            basic_item = [s.strip() for s in basic_item]
            all_basicInfo_value = soup.find_all("dd", class_ = "basicInfo-item value" )
            basic_value = self._get_from_findall(all_basicInfo_value)
            basic_value = [s.strip() for s in basic_value]
            for i, info in enumerate(basic_item):
                info = info.replace(u"\xa0", "")
                if info == u'中文名':
                    item['actor_chName'] = basic_value[i]
                elif info == u'外文名':
                    item['actor_foreName'] = basic_value[i]
                elif info == u'国籍':
                    item['actor_nationality'] = basic_value[i]
                elif info == u'星座':
                    item['actor_constellation'] = basic_value[i]
                elif info == u'出生地':
                    item['actor_birthPlace'] = basic_value[i]
                elif info == u'出生日期':
                    item['actor_birthDay'] = basic_value[i]
                elif info == u'代表作品':
                    item['actor_repWorks'] = basic_value[i]
                elif info == u'主要成就':
                    item['actor_achiem'] = basic_value[i]
                elif info == u'经纪公司':
                    item['actor_brokerage'] = basic_value[i]
            yield item
        elif u'电影' in page_category:
            print("Get a movie page!!")

            soup = BeautifulSoup(response.text, 'lxml')
            summary_node = soup.find("div", class_ = "lemma-summary")
            item['movie_bio'] = summary_node.get_text().replace("\n"," ")
            all_basicInfo_Item = soup.find_all("dt", class_="basicInfo-item name")
            basic_item = self._get_from_findall(all_basicInfo_Item)
            basic_item = [s.strip() for s in basic_item]
            all_basicInfo_value = soup.find_all("dd", class_ = "basicInfo-item value" )
            basic_value = self._get_from_findall(all_basicInfo_value)
            basic_value = [s.strip() for s in basic_value]
            for i, info in enumerate(basic_item):
                info = info.replace(u"\xa0", "")
                if info == u'中文名':
                    item['movie_chName'] = basic_value[i]
                elif info == u'外文名':
                    item['movie_foreName'] = basic_value[i]
                elif info == u'出品时间':
                    item['movie_prodTime'] = basic_value[i]
                elif info == u'出品公司':
                    item['movie_prodCompany'] = basic_value[i]
                elif info == u'导演':
                    item['movie_director'] = basic_value[i]
                elif info == u'编剧':
                    item['movie_screenwriter'] = basic_value[i]
                elif info == u'类型':
                    item['movie_genre'] = basic_value[i]
                elif info == u'主演':
                    item['movie_star'] = basic_value[i]
                elif info == u'片长':
                    item['movie_length'] = basic_value[i]
                elif info == u'上映时间':
                    item['movie_rekeaseTime'] = basic_value[i]
                elif info == u'对白语言':
                    item['movie_language'] = basic_value[i]
                elif info == u'主要成就':
                    item['movie_achiem'] = basic_value[i]
            yield item

        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link["href"]
            new_full_url = urlparse.urljoin('https://baike.baidu.com/', new_url)
            yield scrapy.Request(new_full_url, callback=self.parse)
