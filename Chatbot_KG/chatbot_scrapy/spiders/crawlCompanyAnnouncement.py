# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Inverted_index_cn.py
   Description :   爬取新浪财经网股票公司每日公告
   Author :       charl
   date：          2018/9/5
-------------------------------------------------
   Change Activity: 2018/9/5:
-------------------------------------------------
"""


# 爬取新浪财经网股票公司每日公告
# 提供日期即可  eg: 2017-02-21
import os
import math
import time
import datetime
import requests
import threading
from lxml import etree


# 爬取一条公告并保存
def spiderOnePiece(iurl,headers,datetime,filename):
	# 去除文件名中的非法字符
	invaild=['*','\\','/',':','\"','<','>','|','?']
	for c in invaild:
		if c in filename:
			filename=filename.replace(c,'')

	response=requests.get(iurl,headers=headers).content
	page=etree.HTML(response)
	content=page.xpath('//*[@id="content"]/pre')
	if len(content)==0:
		return
	content=content[0].text
	with open(datetime+os.sep+filename,'w') as f:
		f.write(content.encode('utf-8'))

# 爬取一页
def spiderOnePage(url,headers,datetime):
	website='http://vip.stock.finance.sina.com.cn'

	response=requests.get(url,headers=headers).content
	page=etree.HTML(response)
	trList=page.xpath(r'//*[@id="wrap"]/div[@class="Container"]/table/tbody/tr')

	print(len(trList))
	if len(trList)==1:  # 爬取结束  该行（对不起没有相关记录）
		return 0

	if not os.path.exists(datetime):  # 创建日期文件夹
		os.mkdir(datetime)

	for item in trList:
		aUrl=item.xpath('th/a[1]')
		title=aUrl[0].text    # 公告标题
		href=aUrl[0].attrib['href']   # 公告uri
		href=website+href    # 公告url

		atype=item.xpath('td[1]')[0].text # 公告类型

		spiderOnePiece(href,headers,datetime,title+'_'+atype+'.txt')
	return 1

# 爬取一天
def spiderOneDay(url,headers,datetime,log_path='log'):
	url=url.replace('#datetime#',datetime)  # 填充日期
	flag=1   # 爬取成功标志
	index=1  # 起始页
	f=open(log_path+os.sep+datetime+'.txt','a')
	while flag:
		t_url=url+str(index)
		try:
			flag=spiderOnePage(t_url,headers,datetime)
		except Exception as e:
			print('err:',e)
			flag=0
		finally:
			if flag:
				print('%s page_%d load success,continue.' %(datetime,index))
				f.write('%s_page_%d load success.\n' %(datetime,index))
				f.flush()
			else:
				print('%s page_%d load fail,end.' %(datetime,index))
				f.write('%s_page_%d load failed.\n' %(datetime,index))
				f.flush()
			index+=1
	f.close()

# 爬取一组天股票公司的数据
def spiderOneGroupDays(url,headers,date_group,log_path):
	for idate in date_group:
		try:
			spiderOneDay(url,headers,idate,log_path)
			print('%s has load success.over.' %idate)
		except Exception as e:
			print('err:',e)
			continue


# 获取指定起始日期[包含]--结束日期[包含]之间的日期  
def getBetweenDay(begin_date,end_date):
	date_list=[]
	begin_date=datetime.datetime.strptime(begin_date,'%Y-%m-%d')
	# 现在的日期
	now_date=datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())),'%Y-%m-%d')
	end_date=datetime.datetime.strptime(end_date,'%Y-%m-%d')
	# 如果给出的结束日期大于现在的日期  则将今天的日期作为结束日期
	if end_date>now_date:
		end_date=now_date
	while begin_date<=end_date:
		date_str=begin_date.strftime('%Y-%m-%d')
		date_list.append(date_str)
		begin_date+=datetime.timedelta(days=1)
	return date_list

# 将date_list 平均分成threadNum组  最后一组可能较少
def split_date_list(date_list,threadNum):
	# length=(len(date_list)/threadNum if len(date_list)%threadNum==0 else len(date_list)/threadNum+1)
	length=int(math.ceil(len(date_list)*1.0/threadNum))
	return [date_list[m:m+length] for m in range(0,len(date_list),length)]

def main():
	headers = {
		"Accept-Language": "zh-CN,zh;q=0.8", 
		"Accept-Encoding": "gzip, deflate, sdch", 
		"Host": "vip.stock.finance.sina.com.cn", 
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
		"Upgrade-Insecure-Requests": "1", 
		"Connection": "keep-alive", 
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
	}
	url='http://vip.stock.finance.sina.com.cn/corp/view/vCB_BulletinGather.php?gg_date=#datetime#&page='

	log_path='log'
	if not os.path.exists(log_path):
		os.mkdir(log_path)

	# datetime='2017-02-19'
	# spiderOneDay(url,headers,datetime,log_path)

	begin_date='2017-01-01'
	end_date='2017-01-31'
	# begin_date[包含]-->end_date[包含] 之间的所有date
	date_list=getBetweenDay(begin_date,end_date)
	print('%s-%s:%d days.' %(begin_date,end_date,len(date_list)))

	cut_date_list=split_date_list(date_list,4)
	print(cut_date_list)

	threads=[]
	for dgroup in cut_date_list:
		t=threading.Thread(target=spiderOneGroupDays,args=(url,headers,dgroup,log_path,))
		threads.append(t)

	# 开始线程
	for t in threads:
		t.start()

	# 等待所有线程结束  阻塞主线程
	for t in threads:
		t.join()
	print('all load success...')


if __name__ == '__main__':
	main()