# SMP2018
> 通过SMP2018，展现处理中文文本分类的一般方法。特别是 [Keras 和中文分词工具 jieba 的联合使用](SMP2018_EDA_and_Baseline_Model(Keras).ipynb)

  SMP2018中文人机对话技术评测由中国中文信息学会社会媒体处理专委会主办，哈尔滨工业大学、科大讯飞股份有限公司承办，讯飞公司提供数据，华为公司提供奖金。旨在促进中文人机对话系统相关研究的发展，为人机对话技术相关的学术研究人员和产业界从业人员提供一个良好的沟通平台。在此，评测会务组诚邀各个单位参加本次人机对话技术评测活动！
  
# 用户意图领域分类   

在人机对话系统的应用过程中，用户可能会有多种意图，相应地会触发人机对话系统中的多个领域（domain） ，其中包括任务型垂直领域（如查询机票、酒店、公交车等）、知识型问答以及闲聊等。因而，人机对话系统的一个关键任务就是正确地将用户的输入分类到相应的领域（domain）中，从而才能返回正确的回复结果。

**例如**

1）  你好啊，很高兴见到你！ — 闲聊类

2）  我想订一张去北京的机票。 — 任务型垂类（订机票）

3）  我想找一家五道口附近便宜干净的快捷酒店 — 任务型垂类（订酒店）

## 相关资源

|标题|说明|
|-|-|
|[CodaLab评测主页](https://worksheets.codalab.org/worksheets/0x27203f932f8341b79841d50ce0fd684f/)|[数据下载](https://worksheets.codalab.org/worksheets/0x27203f932f8341b79841d50ce0fd684f/#)|
|[CodaLab 评测教程](https://worksheets.codalab.org/worksheets/0x1a7d7d33243c476984ff3d151c4977d4/)||20181010|
|[评测排行榜](https://smp2018ecdt.github.io/Leader-board/)||
|[SMP2018-ECDT评测主页](http://smp2018.cips-smp.org/ecdt_index.html)||
|[SMP2018-ECDT评测成绩公告链接](https://mp.weixin.qq.com/s/_VHEuXzR7oXRTo5loqJp8A)||


# [SMP2018中文人机对话技术评测（ECDT）](http://smp2018.cips-smp.org/ecdt_index.html)

1. 本资源是一个完整的针对 [SMP2018中文人机对话技术评测（ECDT）](http://smp2018.cips-smp.org/ecdt_index.html) 的实验，由该实验训练的基线模型能达到评测排行榜的前三的水平。
2. 通过本实验，可以掌握处理自然语言文本数据的一般方法。
3. 推荐自己修改此文件，达到更好的实验效果，比如改变以下几个超参数

```python
# 词嵌入的维度
embedding_word_dims = 32
# 批次大小
batch_size = 30
# 周期
epochs = 20
```

## 本实验还可以改进的地方举例

1. 预处理阶段使用其它的分词工具
2. 采用字符向量和词向量结合的方式
3. 使用预先训练好的词向量
4. 改变模型结构
5. 改变模型超参数

## 资源说明

+ [SMP2018_EDA_and_Baseline_Model.ipynb](SMP2018_EDA_and_Baseline_Model.ipynb) 是完整的数据分析和模型构建过程的代码
+ [app.py](用户意图分类APP/app.py) 是根据训练的模型构建的 用户意图分类应用
+ 其它资源见名知意
