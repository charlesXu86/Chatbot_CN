# ChineseTone （汉字转拼音）

ChineseTone是基于Python实现的拼音转汉字工具，实现了与[jpinyin](https://github.com/stuxuhai/jpinyin)类似的接口，兼容Python2、Python3，支持多音字。


## 安装

方式1：
```
$ python setup.py install --user
```

方式2：
```
$ sudo python setup.py install
```

方式3：
```
$ pip install ChineseTone --user
```

方式4：
```
$ sudo pip install ChineseTone
```


## 使用

#### 基本使用


```python
from ChineseTone import *

print PinyinHelper.convertToPinyinFromSentence('了解了')
# 输出：[u'li\u01ceo', u'ji\u011b', u'le']

print '/'.join(PinyinHelper.convertToPinyinFromSentence('了解了'))
# 输出：liǎo/jiě/le

print PinyinHelper.convertToPinyinFromSentence('了解了', pinyinFormat=PinyinFormat.WITH_TONE_MARK)
# 输出：[u'li\u01ceo', u'ji\u011b', u'le']

print PinyinHelper.convertToPinyinFromSentence('了解了', pinyinFormat=PinyinFormat.WITH_TONE_NUMBER)
# 输出：[u'lia3o', u'jie3', u'le']

print PinyinHelper.convertToPinyinFromSentence('了解了', pinyinFormat=PinyinFormat.WITHOUT_TONE)
# 输出：[u'liao', u'jie', u'le']
```

__第一个参数必须是unicode类型，或者utf-8编码的字符串。__


非中文字符保持不变：

```python
print PinyinHelper.convertToPinyinFromSentence('了解了，Mike', pinyinFormat=PinyinFormat.WITHOUT_TONE)
# 输出：[u'liao', u'jie', u'le', u'\uff0c', u'M', u'i', u'k', u'e']
```

可以用指定的字符作为非中文字符的输出：
```python
print PinyinHelper.convertToPinyinFromSentence('了解了，Mike', pinyinFormat=PinyinFormat.WITHOUT_TONE, replace='%')
# 输出：[u'liao', u'jie', u'le', u'%', u'%', u'%', u'%', u'%']
```

某些情况下，为了保证准确性，可以指定一个分词函数，该函数必须返回一个可迭代对象，例如下面的cut函数：

```python
import jieba

def cut(s):
    return jieba.cut(s, cut_all=False)

for word in cut('我来到北京清华大学,mike'):
    print word

'''输出
我
来到
北京
清华大学
,
mike
'''
```

使用segment参数指定分词函数：

```python
import jieba

def cut(s):
    return jieba.cut(s, cut_all=False)

## 未指定分词函数
print PinyinHelper.convertToPinyinFromSentence('提出了解决方案', pinyinFormat=PinyinFormat.WITHOUT_TONE)
# 输出：[u'ti', u'chu', u'liao', u'jie', u'jue', u'fang', u'an']

## 指定分词函数
print PinyinHelper.convertToPinyinFromSentence('提出了解决方案', pinyinFormat=PinyinFormat.WITHOUT_TONE, segment=cut)
# 输出：[u'ti', u'chu', u'le', u'jie', u'jue', u'fang', u'an']
```

#### 添加自己的词库
```python
from ChineseTone import *

print ','.join(PinyinHelper.convertToPinyinFromSentence('金馆长啊', pinyinFormat=PinyinFormat.WITHOUT_TONE))
# 输出有错： jin,guan,chang,a

# 添加词库
PinyinHelper.addWordPinyin('金馆长', ['jin', 'guan', 'zhang'])  # 建议实际情况下拼音中加入声调
print ','.join(PinyinHelper.convertToPinyinFromSentence('金馆长啊', pinyinFormat=PinyinFormat.WITHOUT_TONE))
# 输出正确： jin,guan,zhang,a

# 也可以自定义某个字符的读音
print ','.join(PinyinHelper.convertToPinyinFromSentence('价值40$', pinyinFormat=PinyinFormat.WITHOUT_TONE))
# 输出： jia,zhi,4,0,$
# 自定义
PinyinHelper.addCharPinyin('4', ['si'])   # 考虑多音字，所以用list
PinyinHelper.addCharPinyin('0', ['ling'])
PinyinHelper.addWordPinyin('$', ['mei', 'yuan'])  # 这个用法奇怪些
print ','.join(PinyinHelper.convertToPinyinFromSentence('价值40$', pinyinFormat=PinyinFormat.WITHOUT_TONE))
# 输出： jia,zhi,si,ling,mei,yuan
```

#### 获取某汉字的所有拼音
```python
print PinyinHelper.convertToPinyinFromChar('了')
# 输出：[u'le', u'li\u01ceo']

print PinyinHelper.convertToPinyinFromChar('了', PinyinFormat.WITH_TONE_MARK)
# 输出：[u'le', u'li\u01ceo']

print PinyinHelper.convertToPinyinFromChar('了', PinyinFormat.WITH_TONE_NUMBER)
# 输出：[u'le', u'lia3o']

print PinyinHelper.convertToPinyinFromChar('了', PinyinFormat.WITHOUT_TONE)
# 输出：[u'le', u'liao']

## 若不是单个汉字，返回原值组成的长度为1的列表
print PinyinHelper.convertToPinyinFromChar('了解')
# 输出：[u'\u4e86\u89e3']  # 即“了解”

print PinyinHelper.convertToPinyinFromChar('12')
# 输出：[u'12']
```

#### 判断是否为多音字

```python
print PinyinHelper.hasMultiPinyin('了')
# 输出：True

print PinyinHelper.hasMultiPinyin('你')
# 输出：False
```

#### 获取拼音的声母部分

```python
print PinyinHelper.getShengmu('ni')
# 输出：n

print PinyinHelper.getShengmu('sheng')
# 输出：sh

print PinyinHelper.getShengmu('en')
# 输出：None
```

#### 是否全部是汉字

```python
print ChineseHelper.isChinese('n')
# 输出：False

print ChineseHelper.isChinese('你好')
# 输出：True

print ChineseHelper.isChinese('hi，小王')
# 输出：False
```

#### 简单的简/繁转换

```python
print ChineseHelper.convertToTraditionalChinese('hi，你好，我来到了北京天安门')
# 输出：hi，你好，我來到了北京天安門

print ChineseHelper.convertToSimplifiedChinese('hi，你好，我來到了北京天安門')
# 输出：hi，你好，我来到了北京天安门
```

## 词库

词库位于`ChineseTone/data`下，可以根据需要添加条目。 

词库来自[jpinyin](https://github.com/stuxuhai/jpinyin)、[pinyin](https://github.com/overtrue/pinyin)、[pinyin](https://github.com/hotoo/pinyin)。 `pinyin.db`中的数据是合成自这三个词库。

更新词库后需要重新安装：

* 如果有`build`目录，则删除；
* [安装](#安装)。


## 原理

[如何实现拼音与汉字的互相转换](http://www.letiantian.me/2016-02-08-pinyin-hanzi/)

## 感谢

* jpinyin: https://github.com/stuxuhai/jpinyin
* pinyin: https://github.com/hotoo/pinyin
* pypinyin: https://github.com/mozillazg/python-pinyin
* pinyin: https://github.com/overtrue/pinyin

## 补充 
@2016-6-12: https://github.com/mozillazg/pinyin-data/ 整理了非常好的拼音数据。

## 协议
WTFPL  && 注明词库来源，即：

* jpinyin: https://github.com/stuxuhai/jpinyin
* pinyin: https://github.com/hotoo/pinyin
* pinyin: https://github.com/overtrue/pinyin