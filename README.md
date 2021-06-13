<h1 align="center">Chatbot_CN</h1>

<p align="center">基于深度学习、强化学习、对话引擎的多场景对话机器人</p>

<p align="center">
  <a href="https://github.com/charlesXu86/Chatbot_CN/stargazers">
    <img src="https://img.shields.io/github/stars/charlesXu86/Chatbot_CN.svg?colorA=orange&colorB=orange&logo=github"
         alt="GitHub stars">
  </a>
    
  <a href="https://github.com/charlesXu86/Chatbot_CN/network/members">
      <img src="https://img.shields.io/github/forks/charlesXu86/Chatbot_CN"
           alt="GitHub forks">
    </a>
    
  <a href="https://img.shields.io/github/issues/charlesXu86/Chatbot_CN">
        <img src="https://img.shields.io/github/issues/charlesXu86/Chatbot_CN.svg"
             alt="GitHub issues">
  </a>
  <a href="https://github.com/charlesXu86/Chatbot_CN/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/charlesXu86/Chatbot_CN.svg"
             alt="GitHub license">
  </a>      
</p>

<p align="center">
  <a href="#highlights">项目说明</a> •
  <a href="#what-is-it">项目结构</a> •
  <a href="#install">项目演示</a> •
  <a href="#getting-started">各模块详细介绍</a> •
  <a href="#server-and-client-api">使用说明</a> •
  <a href="#book-tutorial">Update News</a> •
  <a href="#speech_balloon-faq">FAQ</a> •
  <a href="#zap-benchmark">参考</a> •
  <a href="https://hanxiao.github.io/2019/01/02/Serving-Google-BERT-in-Production-using-Tensorflow-and-ZeroMQ/" target="_blank">Blog</a>
  
</p>

<p align="center">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/chatbot.jpg?raw=true" width="300 height=350">
</p>

<h6 align="center">Made by Xu • :globe_with_meridians: <a href="https://www.chatbotcn.com">https://www.chatbotcn.com</a></h6>


<h2 align="center">项目说明</h2>

&ensp; &ensp; **Chatbot_CN** 是一个基于第三代对话系统的多轮对话机器人项目，旨在于开发一个结合规则系统、深度学习、强化学习、知识图谱、多轮对话策略管理的 聊天机器人，目前随着时间的慢慢发展，从最初的一个 Chatbot_CN 项目，发展成了一个 Chatbot_* 的多个项目。目前已经包含了在多轮任务型对话的场景中，基于话术（Story）、知识图谱（K-G）、端到端对话（E2E）。目的是为了实现一个可以快速切换场景、对话灵活的任务型机器人。
同时，**Chatbot_CN** 不仅仅是一个对话系统，而是一套针对客服场景下的完整人工智能解决方案。对话是解决方案的核心和最重要一环，但不仅限于对话，还包括智能决策，智能调度，智能预测，智能推荐等

&ensp; &ensp; 目前**Chatbot_CN** 已经拆分成了13个子项目，涵盖了对话数据收集处理、基本算法模型、对话引擎、对话质量评估，第三方平台快速接入、数据回流、模型优化等等。主要可以分为：

    1、数据层：对话业务数据，开源多轮对话数据等
    
    2、算法层：句法分析、细粒度情感分析、实体抽取、query纠错等
                                                
    3、能力层：自然语言理解、对话管理、对话策略、策略优化、对话工厂
    
    4、应用层：网页端、钉钉群机器人、微信公众号、第三方平台（如拼夕夕）等
    
    5、硬件接入：可接入作为智能语音助手，目前已经加入语音助手模块，可接入树莓派、单片机等硬件
    
项目的大致流程如下图：

<p align="center">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/Chatbot_CN00.png?raw=true" width="600 height=250">
</p>

注：
    
    1、图中的虚线部分为文本机器人部分
    
    2、具体的项目结构请参考项目结构和各模块详细说明。
    
    3、Chatbot_CN 系列项目还存在不少细节问题，正在慢慢完善中。

项目思维导图

<p align="center">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/wechatter_1130.png?raw=true">
</p>


<h2 align="center">项目结构</h2>

#### 1. **Chatbot_CN**整体架构

<p align="center">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/架构.png?raw=true" width="600 height=600">
</p>

#### 2. 各子模块介绍

<summary>当你熟悉了项目的整体架构后，你还需要对其各个子模块进行详细的了解，这样你才能对机器人的机制有一个深刻的理解</summary>


<table>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_CN">Chatbot_CN</a></td><td>总体项目介绍，包含文档（这里不包含代码）</td></tr>
<tr><td><a href="https://github.com/we-chatter/chatbot_kg">chatbot_kg</a></td><td>知识图谱模块、关系网络、实体连接、知识推理等</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_S2S">Chatbot_S2S</a></td><td>训练端到端的对话模型，目前这个模块只为了项目的完整，作用不大，不过这个是一个研究方向</td></tr>
<tr><td><a href="https://github.com/we-chatter/chatbot_utils">chatbot_utils</a></td><td>机器人的基本算法组件，比如query纠错、实体识别等，他是机器人的基础</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_RASA">Chatbot_RASA</a></td><td>机器人的核心对话引擎，基于RASA开源框架</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Doc">Chatbot_Doc</a></td><td>NLP和对话系统的一些文献、收集的文章等等</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Data">Chatbot_Data</a></td><td>机器人的一些语料收集</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Crawler">Chatbot_Crawler</a></td><td>爬虫</td></tr>
<tr><td><a href="https://github.com/we-chatter/chatbot_retrieval">chatbot_retrieval</a></td><td>基于检索的对话模型，他在机器人无法处理用户意图时发挥重要作用</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Evaluate_">Chatbot_Evaluate</a></td><td>对话质量评估、评价、对话诊断、数据回流模块，对话模型优化</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Help">Chatbot_Help</a></td><td>一个将机器人接入第三方平台的工具、如钉钉群、微信公众号等，可快速实现工程化</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Recommendation">Chatbot_Recommendation</a></td><td>对话系统与推荐系统结合，目前正在规划中、暂未开始</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Web">Chatbot_Web</a></td><td>机器人的简单pc端页面交互，可以实现快速体验机器人效果</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Voice">Chatbot_Voice</a></td><td>聊天机器人的语音交互模块</td></tr>
<tr><td><a href="https://github.com/charlesXu86/Chatbot_Analytics">Chatbot_Analytics</a></td><td>聊天机器人的数据分析模块</td></tr>
</table>

如果想了解更多详细的细节说明，请参考以下网站(详细文档)：

<p align="center"><a href="www.chatbotcn.top">www.chatbotcn.top</a></p>

<h2 align="center">项目演示</h2>

<p align="left">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/演示1.png?raw=true" width="160 height=340">
</p>

<p align="left">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/演示2.png?raw=true" width="160 height=340">
</p>

<p align="left">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/演示3.png?raw=true" width="160 height=340">
</p>

<h2 align="center">各模块介绍</h2>

##### **1、chatbot_utils**

&ensp; &ensp; 该模块为基本算法组件，同时也提供了restful API接口，其中包括的功能有：

    1、文本纠错，可以纠正用户query的错别字等，同时还可以纠正部分由于ASR和OCR识别出的错误，用到的主要技术为：字音字形特征提取、微调bert mlm
    
    2、实体识别，可以识别出用户query中提及的实体信息，如：人名、机构名、快递公司、时间、地址等等
    
    3、句法分析，基于转移的句法分析
    
    4、指代消解。
    
    5、其他功能后续继续更新
    

##### **2、chatbot_retrieval**

&ensp; &ensp; 检索式单论对话问答（FAQ），主要用到的技术为词权重、倒排索引、bert finetune。实现原理为Q-Q相似度匹配。该模块主要可以解决两类问题：

    1、FAQ
    
    2、在多轮对话过程中，意图未匹配情况下检索出最佳答案
    

##### **3、Chatbot_Skills**

&ensp; &ensp; 任务型多轮对话的技能管理模块，当我们的机器人"学习"到了多种技能的时候，在对话的过程中可能会出现技能的交叉，即在任务A还没完成的时候跳转到任务B。

**Chatbot_Skills**旨在完成多种任务的平滑切换和机器人的技能初始化配置。


##### **4、Chatbot_Recommendation**

&ensp; &ensp; 将推荐系统和任务型对话结合


<h2 align="center">使用说明</h2>

#### Start

在启动服务之前，你需要比较熟悉整个项目的架构，项目的各模块依赖关系如下图：

<p align="center">
    <img src="https://github.com/charlesXu86/Chatbot_CN/blob/master/image/Chatbot_CN01.png?raw=true" width="600 height=600">
</p>

<h2 align="center">Update News</h2>

    *  2019.10    添加 Chatbot_RASA 子项目
    *  2019.10    添加 Chatbot_NLU 子项目
    *  2019.10    添加 Chatbot_DM 子项目
    *  2019.11    添加 Chatbot_Retrieval 子项目
    *  2019.12    添加 Chatbot_Utils 子项目
    *  2019.12    添加 Chatbot_Help 子项目
    *  2020.1     移除项目里的Chatbot_Web模块，添加 Chatbot_Web 子项目，从2020.1.20日开始， Chatbot_CN 不再做工程项目使用，只是该项目的说明
    *  2020.1     将机器人接入钉钉群，实现用户交互
    *  2020.3     添加对话技能管理模块
    *  2020.4     添加爬虫模块（基于scrapy框架）
    *  2020.5     添加语音助手模块 Chatbot_Voice
    *  2020.5     在对话模型中加入 【AutoDL + 模型压缩 + MLflow】技术
    *  2020.6     引入Botfront，此项目可以代替以前的Chatbot_Web项目，同时Botfront还可以对模型、意图等进行管理
    *  2020.6     开始制定对RASA整体进行二次开发（DeepChatbot），DeepChatbot在rasa的基础上引入更多内容，包括集成AutoDL、模型加速（教师-学生模型等）、
                  增加了机器人训练数据的读取方式、DST优化、更加丰富的接口等等  
    *  2020.7     增加了机器人分析模块
    *  2020.4     增加呼叫中心模块

<h2 align="center">FAQ</h2>

    1、目前这个工程比较完备了，但是很多细节需要完善，也正在积极开发维护，如果你有什么新的idea，欢迎联系我： 997562867

    2、如果你也是一个NLPER，或者对对话系统的开发感兴趣，欢迎加入群聊 聊天机器人开发实战，一起讨论技术： 群号： 718607564

    3、欢迎关注知乎专栏`聊天机器人开发实战`
    
    4、有不少人反应整个系统的代码不能启动、Chatbot_CN怎么没有代码，我还是希望读者可以把上述文档好好看一下，对整个机器人的运行流程有个整体的
    思路。
    
    5、目前正在做产品级重构
    

<h2 align="center">参考</h2>
    
    1、RASA demo
    2、bert as service
    3、Botfront
    4、RasaTalk
    5、Dashbot
