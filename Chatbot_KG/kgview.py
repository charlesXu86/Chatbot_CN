# -*- coding: utf-8 -*-
'''
 * Name        : kgview.py - 知识图谱api请求
 * Author      : Yener(Zheng Wenyu) <yener@ownthink.com>
 * Version     : 1.0
 * Description : 从OwnThink知识图谱中获取数据，利用D3.js实现知识图谱的可视化。
 	数据获取https://api.ownthink.com/kg/knowledge?entity=刘德华
'''
import os
import sys
import requests

def kg_view(entity):
	url = 'https://api.ownthink.com/kg/knowledge?entity=%s'%entity      # 知识图谱API
	
	sess = requests.get(url) # 请求
	text = sess.text # 获取返回的数据

	response = eval(text) # 转为字典类型
	knowledge = response['data']
	
	nodes = []
	for avp in knowledge['avp']:
		if avp[1] == knowledge['entity']:
			continue
		node = {'source': knowledge['entity'], 'target': avp[1], 'type': "resolved", 'rela':avp[0]}
		nodes.append(node)
		
	for node in nodes:
		node = str(node)
		node = node.replace("'type'", 'type').replace("'source'", 'source').replace("'target'", 'target')
		print(node+',')
	
if __name__=='__main__':
	kg_view('图灵')


