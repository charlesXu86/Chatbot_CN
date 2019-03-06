在学习过程中看了很多paper或教程，都存到了自己的文件夹里，但放久了自己都忘了哪篇对应哪个算法了。因此整理起来放到这里。这个列表会随着我的学习不断更新。

[Pelhans/paper_list](https://github.com/Pelhans/paper_list/tree/master/knowledge_graph)

## 知识图谱介绍

* [知识图谱入门笔记](https://zhuanlan.zhihu.com/c_211846834)    
* [从零开始构建知识图谱](https://zhuanlan.zhihu.com/c_1018901137012928512)    
* [徐增林_知识图谱技术综述](https://www.jianguoyun.com/p/DafFvLcQq_6CBxi-6XM)    
* [知识图谱构建技术综述](https://www.jianguoyun.com/p/Da-sCUcQq_6CBxjB6XM)

## RDF 语法

* JSON-LD[A JSON-based Serialization for Linked Data](https://json-ld.org/)    
* Turtle [ RDF 1.1 Turtle Terse RDF Triple Language](https://www.w3.org/TR/turtle/)    
* Turtle中文翻译(自己翻译的，仅供参考)[RDF 1.1 Turtle 中文翻译](https://zhuanlan.zhihu.com/p/44381615)

## 结构化数据的知识抽取
从结构化数据如MYSQL等数据库获取知识得到三元组。

* 直接映射，W3C的[ A Direct Mapping of Relational Data to RDF  ](https://www.w3.org/TR/rdb-direct-mapping/)    
* R2RML[R2RML: RDB to RDF Mapping Language](https://www.w3.org/TR/r2rml/)    
* D2RQ [D2RQ Accessing Relational Databases as Virtual RDF Graphs](http://d2rq.org/)

## 半结构化文本的知识抽取

* [面向半结构化文本的知识抽取研究](https://www.jianguoyun.com/p/DaJwJnsQq_6CBxiy6XM)    
* [抽取 Web 信息的包装器归纳学习构造](https://www.jianguoyun.com/p/DfkkQ3QQq_6CBxiz6XM)    
* 中文百科类知识图谱的构建 zhishi.me [Zhishi.me - Weaving Chinese Linking Open Data](https://www.jianguoyun.com/p/DbFQAPoQq_6CBxi06XM)    
* [Wikipedia Mining Wikipedia as a Corpus for Knowledge Extraction](https://www.jianguoyun.com/p/DUUsSxoQq_6CBxi26XM)    
* [Mining Type Information from Chinese Online Encyclopedias](https://www.jianguoyun.com/p/DcSjsMYQq_6CBxi36XM)    
* Depedia 的构建 [DBpedia A Nucleus for a Web of Open Data](https://www.jianguoyun.com/p/DZYAPMIQq_6CBxi46XM)    
* [DBpedia A Multilingual Cross-Domain Knowledge Base](https://www.jianguoyun.com/p/DZm_Ym8Qq_6CBxi56XM)    
* [DBpedia - A crystallization point for the Web of Data ](https://www.jianguoyun.com/p/DROkjWoQq_6CBxi66XM)    
* [DBpedia - A Large-scale, MultilingualKnowledge Base Extracted from Wikipedia](https://www.jianguoyun.com/p/DRS78wIQq_6CBxi86XM)

## 非结构化文本知识抽取

### 命名实体识别

* [CRF++的使用](https://taku910.github.io/crfpp/#download)    
* [使用CRF++做词性标注等序列化任务](https://github.com/Pelhans/ZNLP/tree/master/lexical_analysis/crfpos%2B%2B)    
* 使用深度学习做命名实体识别[Neural Architectures for Named Entity Recognition](https://www.jianguoyun.com/p/Df6Up8kQq_6CBxi663M)    
* [Bidirectional LSTM-CRF Models for Sequence Tagging](https://www.jianguoyun.com/p/DVPq0SgQq_6CBxi563M)    

### 关系抽取

#### 关系抽取工具

* DeepDive 官网介绍 http://deepdive.stanford.edu/    
* DeepDive 开发者毕业论文 [DeepDive: A Data Management System for Automatic Knowledge Base Construction](https://www.jianguoyun.com/p/DS_fpSEQq_6CBxi76YIB)
* [支持中文的 DeepDive ](http://www.openkg.cn/dataset/cn-deepdive) 并附有股权交易示例    
* [Deepdive实战 抽取演员-电影间关系](https://zhuanlan.zhihu.com/p/46560845)    
* [开放领域关系抽取 OpenIE ](http://knowitall.github.io/openie/) 包含 TextRunner等    
* [ TextRunner 论文 ](https://www.researchgate.net/publication/220816876_TextRunner_Open_Information_Extraction_on_the_Web)    

#### 无监督方法

* 基于模板类的实体关系抽取，最简单的是[基于触发词的匹配](http://pelhans.com/2018/03/19/xiaoxiangkg-note3/#%E5%9F%BA%E4%BA%8E%E8%A7%A6%E5%8F%91%E8%AF%8D%E7%9A%84pattern)   
* 复杂一点的如基于依存句法匹配的,该方法对输入的单据进行依存分析，通过依存分析输出的依存弧判断单句是否为动词谓语句，如果是则结合中文语法启发式规则抽取关系表述。根据距离确定论元位置，对三元组进行评估，输出符合条件的三元组  [基于依存分析的开放式中文实体关系抽取方法](https://www.jianguoyun.com/p/DcmCTjAQq_6CBxjS63M)    
* 基于核的方法典型的为编辑距离核、字符串核、卷积树核等。基于卷积树核的方法以最短路径包含树作为关系实例的结构化表示形式，以卷积树核作为树相似度的计算方法，采用分层聚类方法进行无监督中文实体关系抽取。[基于卷积树核的无指导中文实体关系抽取研究](https://www.jianguoyun.com/p/DWHoHEgQq_6CBxjU63M)    
* 基于聚类的方法，如对共现的实体及它们的上下文进行聚类，最后标记每一个类簇，以核心词汇作为关系表述。如[无监督关系抽取方法研究](http://xueshu.baidu.com/s?wd=paperuri%3A%2838e36a4d56216693db5923975f0b36e4%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Fwww.doc88.com%2Fp-1177286175360.html&ie=utf-8&sc_us=11379075570837652647)    

####  半监督方法

* 标签传播算法[标签传播算法理论及其应用研究综述](https://www.jianguoyun.com/p/DZWOPZIQq_6CBxie7HM)    
* 标签传播算法论文[Relation Extraction Using Label Propagation Based Semi-supervisedLearning](https://www.jianguoyun.com/p/DT1Rn2QQq_6CBxig7HM)    
* 协同训练[基于弱监督学习的海量网络数据关系抽取](https://www.jianguoyun.com/p/DXGXUkUQq_6CBxim7HM)    
* Boot Strapping 算法[基于Boot Strapping的中文实体关系自动生成](https://www.jianguoyun.com/p/DRbjl-gQq_6CBxip7HM)    
* 远程监督 [Distant supervision for relation extraction without labeled data](https://www.jianguoyun.com/p/DbBDsOkQq_6CBxis7HM)   

#### 监督学习

* pipeline方法。采用Classification by Ranking CNN(CR-CNN)模型，可以学习深度学习在关系抽取中的应用方式，如position embeding 这种。[Classifying Relations by Ranking with Convolutional Neural Networks](https://www.jianguoyun.com/p/DeKJe7IQq_6CBxjQyHQ)    
* 关系抽取中的特征介绍，包含三大类(contextual and lexical features、 nominal rol affiliation、pre-existion relation features)八小类(lexical features、hypernyms from wordNet、dependency parse、PropBank parse、FrameNet parse、nominalization、predicates from TextRunner、nominal similarity derived from the Google N-Gram data set)特征：[UTD Classifying Semantic Relations by CombiningLexical and Semantic Resources](https://www.jianguoyun.com/p/DWX0NyMQq_6CBxjwyHQ)    
* Pipeline 方法，基于Attention CNN模型 [Relation Classification via Multi-Level Attention CNNs](https://www.jianguoyun.com/p/DbmG2l8Qq_6CBxiDyXQ)    
* Pipeline 方法，基于Attention-BLSTM模型 [Attention-Based Bidirectional Long Short-Term Memory Networks forRelation Classification](https://www.jianguoyun.com/p/DXJaqLAQq_6CBxiNyXQ)    
* Joint 方法，基于 LSTM-RNN模型 [End-to-End Relation Extraction using LSTMson Sequences and Tree Structures](https://www.jianguoyun.com/p/DWT-a9YQq_6CBxiQyXQ)    
* 远程监督与深度学习结合，采用注意力机制取筛选有效实例[Distant Supervision for Relation Extraction with Sentence-level Attention andEntity Descriptions](https://www.jianguoyun.com/p/DYMywjYQq_6CBxiUyXQ)

#### 事件抽取

* 对时间抽取做了一个综合的介绍，将其分为元事件抽取和主题事件抽取。其中元事件表示一个动作的发生或状态的变化。主题事件包括一类核心事件或活动以及所有与之直接相关的事件和活动，可以由多个元事件组成。对于元事件抽取包含基于模式匹配的元事件抽取和基于机器学习的元事件抽取。对于主题事件抽取，包含基于事件框架的主题事件抽取和基于本体的主题事件抽取两种。它的这个分类和我之前接触到的不大一样，仅供参考。[事件抽取技术研究综述 2013 年](https://www.jianguoyun.com/p/DZPjG50Qq_6CBxjttnU)    
* 介绍神经网络在事件抽取方便的综述文章。同时对事件抽取的定义和ACE任务做了简单介绍。其中事件抽取的子任务包含触发词识别、事件类型分类、论元识别、角色分类。而触发词识别和事件类型分类又可以归结为事件识别。论元角色识别和角色分类可归为论元角色分类。根据学习方式的不同，可以将事件抽取分为基于流水线模型(先事件识别，后论元角色识别,论元角色分类的输入是上一步识别出的触发词和所有候选实体)的事件抽取和基于联合模型的事件抽取。而后，对于ACE任务，事件识别变为基于词的34类多元分类任务，角色分类变为基于词的36类多元分类任务。[神经网络事件抽取技术综述](https://www.jianguoyun.com/p/DVY3Kj8Qq_6CBxjstnUi)    
* [The stages of event extraction](https://www.jianguoyun.com/p/DbktYawQq_6CBxiXuXU)    
* [Refining Event Extraction through Cross-document Inference](https://www.jianguoyun.com/p/DVPwJs8Qq_6CBxiauXU)    
* [Joint Event Extraction via Structured Prediction with Global Features](https://www.jianguoyun.com/p/DbxjxvYQq_6CBxibuXU)    
* [Incremental Joint Extraction of Entity Mentions and Relations](https://www.jianguoyun.com/p/DdNlTPIQq_6CBxiguXU)    
* [Event Extraction via Dynamic Multi-Pooling Convolutional NeuralNetworks](https://www.jianguoyun.com/p/De8bVRMQq_6CBxiiuXU)    
* [Leveraging FrameNet to Improve Automatic Event Detection](https://www.jianguoyun.com/p/DWoQMAIQq_6CBximuXU)    
* [Improving Information Extraction by Acquiring External Evidence withReinforcement Learning](https://www.jianguoyun.com/p/DapzVB0Qq_6CBxisuXU)    

## 知识挖掘

### 实体消岐与链接

* [Entity Linking with a Knowledge Base Issues, Techniques and Solutions](https://www.jianguoyun.com/p/DQCU3uYQq_6CBxij44IB)    
* [A Generative Entity-Mention Model for Linking Entities with Knowledge Base](https://www.jianguoyun.com/p/DU97ifkQq_6CBxiV44IB)    
* [Graph Ranking for Collective Named Entity Disambiguation](https://www.jianguoyun.com/p/DUWnQ8wQq_6CBxiZ44IB)    
* [Large-Scale Named Entity Disambiguation Based on Wikipedia Data](https://www.jianguoyun.com/p/DceRQiwQq_6CBxio44IB)    
* [Learning Entity Representation for Entity Disambiguation](https://www.jianguoyun.com/p/DYyDuwYQq_6CBxis44IB)    
* [Learning to Link Entities with Knowledge Base](https://www.jianguoyun.com/p/DVjbGp8Qq_6CBxiy44IB)    
* [Leveraging Deep Neural Networks and Knowledge Graphs for Entity Disambiguation](https://www.jianguoyun.com/p/DdZG--EQq_6CBxi044IB)    
* [Using TF-IDF to Determine Word Relevance in Document Queries](https://www.jianguoyun.com/p/DT5RToAQq_6CBxi444IB)

### 知识规则挖掘

* [关联规则挖掘综述 ](https://www.ixueshu.com/document/01650259a49c1f7a.html)    
* [Random walk inference and learning in a large scale knowledge base](https://www.jianguoyun.com/p/DUs_NpoQq_6CBxiu5YIB)    
* [Variational Knowledge Graph Reasoning](https://www.jianguoyun.com/p/Dca7zYcQq_6CBxi75YIB)    

### 知识图谱表示学习

* [Collaborative Knowledge Base Embedding for Recommender Systems](https://www.jianguoyun.com/p/DbqefYEQq_6CBxjP5oIB)    
* [Improving Learning and Inference in a Large Knowledge-base using Latent Syntactic Cues](https://www.jianguoyun.com/p/Ddicc8wQq_6CBxiS6IIB)    
* [Jointly Embedding Knowledge Graphs and Logical Rules](https://www.jianguoyun.com/p/DaKzj6UQq_6CBxiU6IIB)    
* [Knowledge Graph Embedding by Translating on Hyperplanes](https://www.jianguoyun.com/p/DV4ATSsQq_6CBxiZ6IIB)    
* [Knowledge Graph Representation with Jointly Structural and Textual Encoding](https://www.jianguoyun.com/p/DXGe4NMQq_6CBxia6IIB)    
* [Knowledge Representation Learning with Entities, Attributes and Relations](https://www.jianguoyun.com/p/Dcc4fEYQq_6CBxic6IIB)    
* [Learning Entity and Relation Embeddings for Knowledge Graph Completion](https://www.jianguoyun.com/p/DdWCXEUQq_6CBxif6IIB)    
* [Translating Embeddings for Modeling Multi-relational Data](https://www.jianguoyun.com/p/DdJ3k9cQq_6CBxih6IIB)    

## 知识存储

* [图数据库 中文第二版](https://www.jianguoyun.com/p/DYGrTMAQq_6CBxih6YIB)    
* [Neo4j权威指南](https://www.jianguoyun.com/p/DVVfZcsQq_6CBxil6YIB)    
* [实战 将数据存进Neo4j](https://zhuanlan.zhihu.com/p/48708750)    
