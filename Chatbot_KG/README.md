# 知识图谱可视化

知识图谱是将复杂的信息通过计算处理成能够结构化表示的知识，所表示的知识可以通过图形绘制而展现出来，为人们的学习提供有价值的参考，为信息的检索提供便利。本文将利用思知知识图谱API接口对知识图谱进行可视化展示。（API请求说明见：https://www.ownthink.com/）

![head](https://pic1.zhimg.com/80/v2-681d10fdf19e3f249b24bdd7805144e6_hd.jpg)

### 环境准备

Python3安装requests库：pip3 install requests



### 数据获取方式

目前知识图谱有许多开放的API接口，为知识图谱可视化提供了大大的便利，这里以思知API接口对知识图谱可视化进行简单示范。

思知请求API：

```shell
https://api.ownthink.com/kg/knowledge?entity=刘德华
```

正确返回的数据格式为：

```shell
{
    "entity": "entity_name",            // 实体名称
    "desc": "entity_desc",              // 实体描述
    "avp": [                            // AVP列表
        [
            "entity_attribute1",        // 属性1
            "entity_value1"             // 值
        ],
        [
            "entity_attribute2",        // 属性2
            "entity_value2"             // 值
        ]
    ],
    "tag": [                            // 标签列表
        "tag1",                         // 标签1
        "tag2"                          // 标签2
    ]
}
```

利用Python请求api接口，获取可视化数据节点：

```python
import os
import sys
import requests

def KG_View(entity):
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
	KG_View('图灵')
```

这里将其保存为kgview.py 并运行

```shell
[Yener@localhost ~]$ python3 kgview.py 
```

打印出来的节点数据：

```python
{type: 'resolved', target: 'Alan Mathison Turing', source: '艾伦·麦席森·图灵', 'rela': '外文名'},
{type: 'resolved', target: '英国', source: '艾伦·麦席森·图灵', 'rela': '国籍'},
{type: 'resolved', target: '英国伦敦', source: '艾伦·麦席森·图灵', 'rela': '出生地'},
{type: 'resolved', target: '1912年6月23日', source: '艾伦·麦席森·图灵', 'rela': '出生日期'},
{type: 'resolved', target: '1954年6月7日', source: '艾伦·麦席森·图灵', 'rela': '逝世日期'},
{type: 'resolved', target: '数学家，逻辑学家，密码学家', source: '艾伦·麦席森·图灵', 'rela': '职业'},
{type: 'resolved', target: '剑桥大学国王学院，普林斯顿大学', source: '艾伦·麦席森·图灵', 'rela': '毕业院校'},
{type: 'resolved', target: '“计算机科学之父”', source: '艾伦·麦席森·图灵', 'rela': '主要成就'},
{type: 'resolved', target: '提出“图灵测试”概念', source: '艾伦·麦席森·图灵', 'rela': '主要成就'},
{type: 'resolved', target: '人工智能', source: '艾伦·麦席森·图灵', 'rela': '主要成就'},
{type: 'resolved', target: '破解德国的著名密码系统Enigma', source: '艾伦·麦席森·图灵', 'rela': '主要成就'},
{type: 'resolved', target: '《论数字计算在决断难题中的应用》', source: '艾伦·麦席森·图灵', 'rela': '代表作品'},
{type: 'resolved', target: '《机器能思考吗？》', source: '艾伦·麦席森·图灵', 'rela': '代表作品'},
```



### 数据可视化

利用d3js实现可视化展示：

将前面打印出来的数据复制到以下的html代码的links中，如下所示。html全部代码见文末GitHub，保存后直接用浏览器打开即可对数据进行可视化绘制。

```html
<!DOCTYPE html>
<meta charset="utf-8">
<style>.link {  fill: none;  stroke: #666;  stroke-width: 1.5px;}#licensing {  fill: green;}.link.licensing {  stroke: green;}.link.resolved {  stroke-dasharray: 0,2 1;}circle {  fill: #ccc;  stroke: #333;  stroke-width: 1.5px;}text {  font: 12px Microsoft YaHei;  pointer-events: none;  text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;}.linetext {    font-size: 12px Microsoft YaHei;}</style>
<body>
<script src="https://d3js.org/d3.v3.min.js"></script>
<script>

var links = 
[
{source: '艾伦·麦席森·图灵', target: 'Alan Mathison Turing', 'rela': '外文名', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '英国', 'rela': '国籍', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '英国伦敦', 'rela': '出生地', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '1912年6月23日', 'rela': '出生日期', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '1954年6月7日', 'rela': '逝世日期', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '数学家，逻辑学家，密码学家', 'rela': '职业', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '剑桥大学国王学院，普林斯顿大学', 'rela': '毕业院校', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '“计算机科学之父”', 'rela': '主要成就', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '提出“图灵测试”概念', 'rela': '主要成就', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '人工智能', 'rela': '主要成就', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '破解德国的著名密码系统Enigma', 'rela': '主要成就', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '《论数字计算在决断难题中的应用》', 'rela': '代表作品', type: 'resolved'},
{source: '艾伦·麦席森·图灵', target: '《机器能思考吗？》', 'rela': '代表作品', type: 'resolved'},
];

var nodes = {};

links.forEach(function(link)
{
  link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
  link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
});

```





GitHub：https://github.com/ownthink/KG-View




