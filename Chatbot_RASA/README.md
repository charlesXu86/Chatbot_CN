# OverView
**一个基于Rasa Stack, 带有WebUI的知识问答机器人**

[后端](https://github.com/bing-zhub/RasaChatBot)   [前端](https://github.com/bing-zhub/RasaChatBot_ui)

## 功能截图
![Demo][1]

## 技术架构
![pipeline][2]
[参考](https://rasa.com/docs/get_started_step1/)

### 模块化
Action - Rasa NLU - Rasa Core - Web Server
### Context保存
将所需要的entities放入不同slot中(通过Rasa-core实现)
### 基于意图(Intent-based)的对话
这是当NLP算法使用intents和entities进行对话时，通过识别用户声明中的名词和动词，然后与它的dictionary交叉引用，让bot可以执行有效的操作。
### ...
## Rasa NLU
使用自然语言理解进行意图识别和实体提取
### Example:
rquest(part)
`"张青红的生日什么时候"`

response
```json
{
  "intent": "view_defendant_data",
  "entities": {
    "defendant" : "张青红",
    "item" : "生日"
  }
}
```
### Pipeline
假设我们在config文件中这样设置pipeline`"pipeline": ["Component A", "Component B", "Last Component"]`
那么其生命周期如下：
![LifeCircle][3]
在`Component A`调用开始之前， rasa nlu会首先根据nlu的训练集创建一个Context(no more than a python dict). Context用于在各个Component之间传递消息。 比如， 我们可以让`Component A`去根据训练集计算特征向量， 训练完成后将结果保存在Context中， 传递到下一个Component。 `Component B` 可以获取这些特征向量， 并根据其做意图分类。在所有Component完成后， 最后的Context中保存这个模型的元数据(metadata). 

``` yaml
language: "zh"

pipeline:
- name: "nlp_mitie"
  model: "data/total_word_feature_extractor_zh.dat"
- name: "tokenizer_jieba" 
- name: "ner_mitie" 
- name: "ner_synonyms"
- name: "intent_entity_featurizer_regex"
- name: "intent_featurizer_mitie"
- name: "intent_classifier_sklearn"
```
MITIE是一个MIT信息提取库，该库使用了最先进的统计机器学习工具构建。它类似于word2vec中的word embedding。MITIE模型，在NLU（自然语言理解）系统中，完成实体识别和意图提示的任务。
”nlp_mitie”初始化MITIE
”tokenizer_jieba”用jieba来做分词
”ner_mitie”和”ner_synonyms”做实体识别
”intent_featurizer_mitie”为意图识别做特征提取”intent_classifier_sklearn”使用sklearn做意图识别的分类。

### Training
我们的训练集`data.json`
``` json
{
  "rasa_nlu_data": {
    "common_examples": [
      {
        "text": "张青红的生日什么时候",
        "intent": "viewDefendantData",
        "entities": [
          {
            "start": 4,
            "end": 6,
            "value": "生日",
            "entity": "item"
          },
          {
            "start": 0,
            "end": 3,
            "value": "张青红",
            "entity": "defendant"
          }
        ]
      }
    ]
  }
}
```
也可以通过[可视化工具(rasa-nlu-trainer)](https://github.com/RasaHQ/rasa-nlu-trainer)进行实体的标注等
![Rasa-nlu-trainer][5]
### Run as a service
``` bash
curl -XPOST localhost:5000/parse -d '{"q":"张青红的生日是什么时候", "project":"CriminalMiner", "model":"nlu"}'
```

## Rasa Core
用于对话管理
### 技术架构
![Core技术架构][6]
1. Rasa_Core首先接收到信息, 将信息传递给`Interpreter`, `Interpreter`将信息打包为一个字典(`dict`), 这个`dict`包括原始信息(`original text`), 意图(`intent`)的找到的所有实体(`entities`)
2. `Tracker`保持对话的状态.
3. `Policy` 接收到当前`Tracker`的状态
4. `Policy`选择执行哪个动作(`Action`)
5. 被选中的`Action`同时被`Tracker`记录
6. `Action`执行后产生回应

### Training
基于对话
```
## story_01
* greet
  - utter_greet
## story_02
* goodbye
  - utter_goodbye
## story_03
* viewCaseDefendantsNum
  - action_view_case_defendants_num
## story_04
* viewCaseDefendants
  - action_view_case_defendants
## story_05
* viewCase
  - utter_ask_case
```
### Interactive Learning

在交互式学习模式下, 我们可以为Bot对话提供反馈. 这是一个非常强有力的方式去检测Bot能做什么, 同时也是修改错误最简单的方式. 基于机器学习的对话的有点就在于当bot不知道如何回答或者回答错误时, 我们可以及时的反馈给bot. 有些人称这种方式为[Software 2.0](https://medium.com/@karpathy/software-2-0-a64152b37c35)

同时在这个训练过程中, 是可视化的, 在我看来, 是个究极阉割版的[TensorBoard](https://www.tensorflow.org/guide/summaries_and_tensorboard)

### Action
进行数据校验, 和数据交互. 
采用Py2Neo与数据库(Neo4j)进行交互. 

  [1]: http://images.zshaopingb.cn/2018/12/3664281616.png
  [2]: http://images.zshaopingb.cn/2018/12/4005670685.png
  [3]: http://images.zshaopingb.cn/2018/12/4136964647.png
  [4]: http://images.zshaopingb.cn/2018/12/923236055.jpg
  [5]: http://images.zshaopingb.cn/2018/12/2537130720.jpg
  [6]: http://images.zshaopingb.cn/2018/12/1133622055.png
