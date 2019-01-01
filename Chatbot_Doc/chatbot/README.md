<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Conversational Robot](#conversational-robot)
- [名词解释（非专业，非官方，非权威）](#%E5%90%8D%E8%AF%8D%E8%A7%A3%E9%87%8A%E9%9D%9E%E4%B8%93%E4%B8%9A%E9%9D%9E%E5%AE%98%E6%96%B9%E9%9D%9E%E6%9D%83%E5%A8%81)
  - [对话系统(dialogue system / dialog system)](#%E5%AF%B9%E8%AF%9D%E7%B3%BB%E7%BB%9Fdialogue-system--dialog-system)
  - [问答系统(question answering system)](#%E9%97%AE%E7%AD%94%E7%B3%BB%E7%BB%9Fquestion-answering-system)
    - [问答对(QA pairs)](#%E9%97%AE%E7%AD%94%E5%AF%B9qa-pairs)
    - [基于知识的问答(knowledge based QA)](#%E5%9F%BA%E4%BA%8E%E7%9F%A5%E8%AF%86%E7%9A%84%E9%97%AE%E7%AD%94knowledge-based-qa)
    - [基于检索的问答（Retrival-based QA）](#%E5%9F%BA%E4%BA%8E%E6%A3%80%E7%B4%A2%E7%9A%84%E9%97%AE%E7%AD%94retrival-based-qa)
      - [一个简单搜索回答的流程](#%E4%B8%80%E4%B8%AA%E7%AE%80%E5%8D%95%E6%90%9C%E7%B4%A2%E5%9B%9E%E7%AD%94%E7%9A%84%E6%B5%81%E7%A8%8B)
    - [其他类型问答](#%E5%85%B6%E4%BB%96%E7%B1%BB%E5%9E%8B%E9%97%AE%E7%AD%94)
  - [聊天机器人（chatbot）](#%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BAchatbot)
  - [DeepQA](#deepqa)
  - [人工智能标记语言，AIML](#%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E6%A0%87%E8%AE%B0%E8%AF%AD%E8%A8%80aiml)
    - [基于深度学习Sequence to Sequence的聊天机器人](#%E5%9F%BA%E4%BA%8E%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0sequence-to-sequence%E7%9A%84%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA)
- [一个完整的Conversational UI（平台）需要的东西](#%E4%B8%80%E4%B8%AA%E5%AE%8C%E6%95%B4%E7%9A%84conversational-ui%E5%B9%B3%E5%8F%B0%E9%9C%80%E8%A6%81%E7%9A%84%E4%B8%9C%E8%A5%BF)
- [Dialogue System / Conversational UI 可能的资料](#dialogue-system--conversational-ui-%E5%8F%AF%E8%83%BD%E7%9A%84%E8%B5%84%E6%96%99)
  - [平台](#%E5%B9%B3%E5%8F%B0)
    - [国外](#%E5%9B%BD%E5%A4%96)
    - [国内](#%E5%9B%BD%E5%86%85)
    - [开源实现（机器人相关）：](#%E5%BC%80%E6%BA%90%E5%AE%9E%E7%8E%B0%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%9B%B8%E5%85%B3)
  - [厂家](#%E5%8E%82%E5%AE%B6)
    - [微软](#%E5%BE%AE%E8%BD%AF)
    - [亚马逊](#%E4%BA%9A%E9%A9%AC%E9%80%8A)
    - [剑桥大学](#%E5%89%91%E6%A1%A5%E5%A4%A7%E5%AD%A6)
    - [脸书](#%E8%84%B8%E4%B9%A6)
    - [Linkdin](#linkdin)
    - [作者的其他相关链接](#%E4%BD%9C%E8%80%85%E7%9A%84%E5%85%B6%E4%BB%96%E7%9B%B8%E5%85%B3%E9%93%BE%E6%8E%A5)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# Conversational Robot

作者不保证任何此repo内容的权威性，
对权威性又苛求，又对内容抱有兴趣的人，
您可以先参考斯坦福的[这本书 28~30章](http://web.stanford.edu/~jurafsky/slp3/)

这个repo会记录我对 Conversational Robot 的理解、学习、研究、设计、实现的相关内容

如果有疑问、质疑、讨论需求：

mail (a) qhduan.com

微信 longinusd

文章列表：

[对话机器人技术简介：问答系统、对话系统与聊天机器人](/对话机器人技术简介：问答系统、对话系统与聊天机器人)

[聊天机器人：神经对话模型的实现与技巧](/聊天机器人：神经对话模型的实现与技巧)

施工中，有生之年系列：

对话系统：~~自然~~语言理解

对话系统：对话策略管理

对话系统：自然语言生成

对话系统：完整对话系统构建

聊天机器人：模板模型与AIML简介

问答系统：文本检索模型

问答系统：知识模型

完整机器人实现

# 名词解释（非专业，非官方，非权威）

## 对话系统(dialogue system / dialog system)

特指 Task-oriented dialogue system ，也就是为了完成一种任务而发明的系统。
这种任务的特征往往有：

- 结果唯一，例如买一张机票，订一场电影，买一杯咖啡
- 任务需要多项要素，例如机票需要时间、起始地、到达地；电影需要名称、电影院、场次时间；咖啡需要时间、大杯小杯、口味
- 任务需要通过多轮对话、多轮反复确认达成，例如：你要大杯的咖啡还是小杯的？你需要几点送？你确定要9点送？

主流对话系统研究集中在 GUS-style frame-based 类型的对话系统

    GUS对话系统，是 Genial Understander System 的缩写，可以追溯到1977年的论文(Daniel G. Bobrow, GUS, A Frame-Driven Dialog System, 1977)

## 问答系统(question answering system)

### 问答对(QA pairs)

也就是问题是一句话，回答是确定的一个词、一句话。

训练数据是纯粹的一问一答，类似各种FAQ。

此类也被称为 Answer selection，Answer ranking，Answer sentence selection

这种绝对不叫做“Knowledge based QA”，因为一问一答的数据，
不构成知识，知识必须是有结构的、有属性的、互相有关联的数据。

    Answer sentence selection is the task of identifying sentences that contain the answer to a given question. This is an important problem in its own right as well as in the larger context of open domain question answering.(Lei Yu, Deep Learning for Answer Sentence Selection, 2014)

    We present a question answering (QA) system which learns how to detect and rank answer passages by analyzing questions and their answers (QA pairs) provided as training data.(Ganesh Ramakrishnan, Is Question Answering an Acquired Skill?, 2004)

### 基于知识的问答(knowledge based QA)

学术上基本不区分基于知识的，还是基于知识图谱的（knowledge graph），因为知识图谱是谷歌提出的一个较商业概念。知识在传统上就是三元组，或类似的图结构，而知识图谱也是如此。

这种方式，需要你提供一个知识库，例如一堆有关联的三元组（Triples），它们可以存储于普通数据库或者专门的图数据库（graph database），或者语义网相关的 RDF 数据库。
[Wikipedia Triplestore](https://en.wikipedia.org/wiki/Triplestore)

输入是自然语言，上下文是知识库，结果往往是知识库中的一个关系或者一个实体。

例如有知识库（三元组）：

(中国，有首都，北京)  
(北京，是某国的首都，中国)  

三元组的结构是（主，谓，宾），
实际上是（实体，属性，属性值），
或者（实体，关系，实体）结构。
代表了一种两个节点，一个有属性的边的有向图结构。

那么就可以解答用户输入“中国的首都是哪”，“北京是哪个国家的首都”，“中国与北京的关系”，这样的问题。
这三个问题分别相当于查询(中国，有首都，？)，(北京，是某国首都，？)，(中国，？，北京)，
其中问号“？”代指一种我们暂时不知道的变量，这种查询思想就是SPARQL的思想之一。

为什么这是图结构，例如：

(何云伟，师傅，郭德纲)  
(曹云金，师傅，郭德纲)  
(何云伟，师兄弟，曹云金)  

（师傅代表“有师傅”，或者has 师傅，师兄弟类似）

上面三个实体，2种关系，构成了一个三角形的图。
所以这并不是简单的二维表模式（关系数据库模式），
也不是树模式，因为兄弟节点有连接。

（严格来说应该是有向图模式；图模式依然可以用传统数据库，如SQL、KV数据库来保存）

### 基于检索的问答（Retrival-based QA）

也可以说是 Text-based 的

问答输入是用户的一个问题，而上下文是一个或多个文字信息碎片。

例如我们有百度百科关于“北京”的文章，假设我们并没有将这个文章知识化（三元组化），
但是我们可以通过用户提问的关键字，预测用户可能期望的结果，从这个文章中找到答案。

#### 一个简单搜索回答的流程

假设用户问“北京的面积”。

首先我们把这个问题进行一定变形，例如重点词是“北京”和“面积”。
我们也可以对词进行同义词扩展，例如扩展成：北京，中国首都，面积，大小

然后我们推理结果是，用户所需的回答类型应该是某个数字（代表面积的数字）。

之后我们可以检索已有数据中和“北京”、“面积”相关的文章（这部分也可以利用搜索引擎，或者百科类网站）。

有了这个文章作为上下文，我们就从文章中找到最接近问题的段落，
并在段落中根据语义、答案类型等信息，提取出真正的答案，可能是一个实体、一个属性、或者一个短句。

### 其他类型问答

例如输入一个图片，一个用户问题，用户询问“图上有什么”，“图里有谁”，“图里有苹果吗”。
也就是系统要根据图片内容和用户提问，做出一定程度的描述或推理。

例如输入一段文章，一个用户问题，就好像做语文、英语的阅读理解那样的问答，
用户的问题就好像是阅读理解的选择题或者填空题。
这也算是机器阅读理解的课题。

学术上，问答也可以分为 Factoid QA 和 Non-factoid QA。
Factoid就是答案往往是某个事实实体、简单的属性、关系的。
例如地球到月亮有多远，中国有大面积，美国有多少人口这样。

Non-factoid 可以包含 Factoid 问题，答案可以更发散。
例如描述下这辆车，计算这道数学题，给我你针对这件事儿的见解，给我提意见等等，
这样答案并不明确或者并不是一个明确事实实体、关系的问答。

一般基于知识（库）的问答都是说 Factoid QA。

## 聊天机器人（chatbot）

也可以被成为 Non-task-oriented dialogue system，或者 General dialogue system。

此类系统不需要完成一个明确任务（和上面的对话系统相反），它的存在目的往往只是为了尽可能的延长对话，并且完成一些的模糊的目标。例如排解用户无聊，打发时间，一些隐含的心理状况分析，鼓励用户，讨好用户。

著名的Alice机器人中的一个模板，很好的描述了它的设计目的（bot.aiml)：

问："what do you need"  
答："I would like to have a longer conversation with you."  

翻译（东北）：

问：你要干哈啊？  
答：我想跟你多唠会儿磕。  

## DeepQA

DeepQA一般指IBM开发的问答系统，它跟deep learning半分钱关系都没有。如果你觉得它跟deep learning有关系，可以想想 deep blue，就是那个IBM造出来下国际象棋的那个。

既然是QA系统，也就是说它既不能帮你买咖啡也不能帮你订机票，它就只是一个问答系统。

它应用了很多问答系统的技术、技巧、工程方法，和海量的数据，DeepQA并不是一个你能简单用得到的系统，它既不免费，也不开源。

## 人工智能标记语言，AIML

它的最简单的例子是这样的：

```xml
<category>
  <pattern>YOU CAN DO BETTER</pattern>  
  <template>Ok, I will try.</template>  
</category>  
```

问题是“you can do better”，机器人会回答“ok, i will try”。

当然实际上这个模板语言可以完成很多复杂的功能，包括而不限于：计算（例如1+1=？），数据库查询（通过调用其他接口），一些简单的嵌套等等。

我可以很明确的说，这套系统基本上没什么用处，因为书写成本高，语法复杂，XML并不人类可读，优化少，相关资源很少，几乎很少的工业界支援，几乎已经被学术界放弃。

注意我说的是AIML没用，没说模板方法没用，模板方法依然是现在构建一切bot最重要最重要最重要没有之一的手段。

这里列出几个你应该看看的AIML的代替品：

[Rive Script](https://www.rivescript.com/)

[Super Script](https://github.com/superscriptjs/superscript)

[Chat Script](https://github.com/bwilcox-1234/ChatScript)

### 基于深度学习Sequence to Sequence的聊天机器人

它本质是脱胎于神经机器翻译技术（Neural Machine Translation），也就是说本质是把机器翻译的一种语言的一句话到另一种语言的一句话的生成，改为聊天中上一句话到下一句话的生成。

它几乎没什么用，甚至说都建议你先去看AIML是什么，都比在这耽误时间可能来的要好。

因为它：结果不可靠、质量不可控，高质量数据集少，trick多，对系统能补足的程度小，工程时间成本高，太过独立很难与其他部分契合，人格不一致，结果发散性低……

并不是嘛玩意儿沾点深度学习就是好。


# 一个完整的Conversational UI（平台）需要的东西

非官方、非权威、非专业！！！

- ！ 易用、易学的QA Pairs管理与查询引擎
  - 用于机器人管理者简单定义类似FAQ的问答，例如“怎么退货”这种有一个固定回答问题
- ！ 易用、易学的对话模板生成管理方法（用于生成可能的用户说的话）
  - 机器人管理者用于生成针对对话系统（任务）的对话
- ！ 足够使用的NLU部件
  - 内部需要包括其他各种基本组件，例如intent classification，entity recognization
- ！ 当机器人不准确、失效时，人工代替解决方案
  - 最好能即时接入人工，给用户接入人工的手段，即时评价当前对话质量，最低要求是提供其他人工渠道：电话、邮箱、IM
- 足够使用的对话状态跟踪部件与对话策略部件
  - dialogue state tracker & dialogue policy
- 易用、易学的自然语言生成模板方法（用于生成机器人的回复）
  - 根据当前状态，生成对应回复所需要的模板系统
- 用户行为模拟程序与系统评价程序
  - 行为模拟可以用于强化学习，就算不用强化学习，这套系统也是一套标准的集成测试系统
- 良好的自动用户反馈、评价机制
  - 用户评价机器人好坏、反馈结果、与用户沟通联系
- 一个良好的、易懂的面向开发人员文档
  - 用于帮助专业人员构建更详细、自定义的机器人
- 一个良好的、易懂的面向非专业人员培训文档
  - 用户普及知识，做简单的非专业训练，让他能够很好的管理基本问答、知识库
- ～ 基于某种UI（例如web）的高级图形管理界面
  - 方便非专业人员使用
- ～ 自动的训练程序，例如基于强化学习的
  - 未测试
- ～ 足够覆盖基本问答的chatbot引擎
  - 回答一些非常基本机器人，你是谁，你从哪来，你到哪去，用于最基本的调戏、使用帮助目的
- ～ 高效的Knowledge-based QA问答引擎
  - 用于更方便的回答例如，这个东西保修几年，这双鞋有多大码的，这种更细节的知识问题
- ～ 一个简易的知识库构建与对接系统（如果需要Knowledge-based QA问答引擎的话）
- ～ 较准确的Retrival-based QA问答引擎
  - 例如用于一些百科知识问答，某些特定领域的文档问答
- ～～ 人类情绪分析部件（NLU中）
- ～～ 一个基于Seq2Seq的chatbot引擎
- ～～ 语音识别
- ～～ 人工语言合成

！：必须  
～：部分场景可有可无  
～～：可能需要忽略的

# Dialogue System / Conversational UI 可能的资料

下列**不完全**

## 平台

### 国外

- wit.ai
- api.ai
- luis.ai
- [国外客服](https://ada.support/)

### 国内

- yige.ai
- ruyi.ai
- UNIT
- dueros
- 思必驰dui开放平台

### 开源实现（机器人相关）：

- 剑桥的开源DS [PyDial](http://www.camdial.org/pydial/)
- 一个开源的DS [deepmipt/DeepPavlov](https://github.com/deepmipt/DeepPavlov)
- 一个商业但开源的DS [Rasa Core](https://rasa.com)
- 比较简单的机器人[ChatterBot](https://github.com/gunthercox/ChatterBot)
- 一个开源的QA系统，里面那个论文列表不错 [castorini/BuboQA](https://github.com/castorini/BuboQA)
- AIML的公司 [pandorabots](https://home.pandorabots.com/en/)

## 厂家

### 微软

微软的cortana应该使用了很多相关技术

比较新的论文如

(Xiujun Li, End-to-End Task-Completion Neural Dialogue Systems, 2018)

(Jason D. Williams, Hybrid Code Networks: practical and efficient end-to-end dialog control
with supervised and reinforcement learning, 2017)

还有数据和比赛：

[https://github.com/xiul-msr/e2e_dialog_challenge](https://github.com/xiul-msr/e2e_dialog_challenge)
[https://www.microsoft.com/en-us/research/event/dialog-state-tracking-challenge/](https://www.microsoft.com/en-us/research/event/dialog-state-tracking-challenge/)

### 亚马逊

Alexa Prize 相关的有一堆论文，例如下面这篇

亚马逊的这些，我觉得更偏从QA角度设计DS

(Huiting Liu, RubyStar: A Non-Task-Oriented Mixture Model Dialog System, 2017)

### 剑桥大学

剑桥大学有一个 [Dialogue Systems Group](http://dialogue.mi.eng.cam.ac.uk/) ，里面包括一些这个组发的会议论文

他们还有一个项目叫 [PyDial](http://www.camdial.org/pydial/)  2017下半年的产物

[还有这些课件](http://mi.eng.cam.ac.uk/~mg436/LectureSlides/)

### 脸书

[BABI数据集，很多论文使用](https://research.fb.com/downloads/babi/)

### Linkdin

[Linkdin在KDD2018上做的tutorial是我认为现在对话系统、QA最好的一个tutorial、简单survey，没有之一（截止18年）](https://weibo.com/1402400261/Gw5DIykjj?type=repost#_rnd1535135595967)

### 作者的其他相关链接

[Sequence-to-Sequence模型的一个实现](https://github.com/qhduan/just_another_seq2seq)

---

graphml与一些图片文件是使用[yEd Live](https://www.yworks.com/yed-live/)制作
