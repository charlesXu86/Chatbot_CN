<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Sequence-to-Sequence 模型](#sequence-to-sequence-%E6%A8%A1%E5%9E%8B)
    - [模型流程](#%E6%A8%A1%E5%9E%8B%E6%B5%81%E7%A8%8B)
    - [Seq2Seq模型流程伪代码（python）](#seq2seq%E6%A8%A1%E5%9E%8B%E6%B5%81%E7%A8%8B%E4%BC%AA%E4%BB%A3%E7%A0%81python)
    - [预测时](#%E9%A2%84%E6%B5%8B%E6%97%B6)
    - [另一种解释](#%E5%8F%A6%E4%B8%80%E7%A7%8D%E8%A7%A3%E9%87%8A)
- [与神经机器翻译的异同](#%E4%B8%8E%E7%A5%9E%E7%BB%8F%E6%9C%BA%E5%99%A8%E7%BF%BB%E8%AF%91%E7%9A%84%E5%BC%82%E5%90%8C)
    - [embedding不同](#embedding%E4%B8%8D%E5%90%8C)
    - [结果重复性不同](#%E7%BB%93%E6%9E%9C%E9%87%8D%E5%A4%8D%E6%80%A7%E4%B8%8D%E5%90%8C)
    - [对称性不同](#%E5%AF%B9%E7%A7%B0%E6%80%A7%E4%B8%8D%E5%90%8C)
    - [语料不同，与所产生的问题](#%E8%AF%AD%E6%96%99%E4%B8%8D%E5%90%8C%E4%B8%8E%E6%89%80%E4%BA%A7%E7%94%9F%E7%9A%84%E9%97%AE%E9%A2%98)
    - [评价标准问题](#%E8%AF%84%E4%BB%B7%E6%A0%87%E5%87%86%E9%97%AE%E9%A2%98)
- [技巧与提高（trick）](#%E6%8A%80%E5%B7%A7%E4%B8%8E%E6%8F%90%E9%AB%98trick)
    - [抗语言模型与互信息模型](#%E6%8A%97%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E4%B8%8E%E4%BA%92%E4%BF%A1%E6%81%AF%E6%A8%A1%E5%9E%8B)
        - [抗语言(anti-language)损失函数](#%E6%8A%97%E8%AF%AD%E8%A8%80anti-language%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0)
        - [互信息损失函数](#%E4%BA%92%E4%BF%A1%E6%81%AF%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0)
    - [反转技巧](#%E5%8F%8D%E8%BD%AC%E6%8A%80%E5%B7%A7)
    - [强化学习](#%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0)
    - [对抗学习](#%E5%AF%B9%E6%8A%97%E5%AD%A6%E4%B9%A0)
    - [TFIDF技巧](#tfidf%E6%8A%80%E5%B7%A7)
    - [上下文相似技巧](#%E4%B8%8A%E4%B8%8B%E6%96%87%E7%9B%B8%E4%BC%BC%E6%8A%80%E5%B7%A7)
    - [分组技巧（buckets）](#%E5%88%86%E7%BB%84%E6%8A%80%E5%B7%A7buckets)
- [工程级实战参考与提高](#%E5%B7%A5%E7%A8%8B%E7%BA%A7%E5%AE%9E%E6%88%98%E5%8F%82%E8%80%83%E4%B8%8E%E6%8F%90%E9%AB%98)
    - [训练不同情绪的bot](#%E8%AE%AD%E7%BB%83%E4%B8%8D%E5%90%8C%E6%83%85%E7%BB%AA%E7%9A%84bot)
    - [训练不同人格特征的bot](#%E8%AE%AD%E7%BB%83%E4%B8%8D%E5%90%8C%E4%BA%BA%E6%A0%BC%E7%89%B9%E5%BE%81%E7%9A%84bot)
    - [语料处理](#%E8%AF%AD%E6%96%99%E5%A4%84%E7%90%86)
    - [将语料分类，训练多个模型](#%E5%B0%86%E8%AF%AD%E6%96%99%E5%88%86%E7%B1%BB%E8%AE%AD%E7%BB%83%E5%A4%9A%E4%B8%AA%E6%A8%A1%E5%9E%8B)
    - [如果可能的话，避免（现在）使用神经对话模型](#%E5%A6%82%E6%9E%9C%E5%8F%AF%E8%83%BD%E7%9A%84%E8%AF%9D%E9%81%BF%E5%85%8D%E7%8E%B0%E5%9C%A8%E4%BD%BF%E7%94%A8%E7%A5%9E%E7%BB%8F%E5%AF%B9%E8%AF%9D%E6%A8%A1%E5%9E%8B)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# Sequence-to-Sequence 模型

### 模型流程

input_text =>  
encoder =>  
decoder =>  
target_text

### Seq2Seq模型流程伪代码（python）

训练时：

```python

# 这两条是训练数据
input_text = ['A', 'B', 'C']
output_text = ['D', 'E', 'F']

# 计算encoder的状态
encoder_state = encoder(input_text)

output_text_with_start = ['<SOS>'] + output_text
output_text_with_end = output_text + ['<EOS>']

output = []
decoder_state = 0
for decoder_input, decoder_target in zip(
    output_text_with_start, output_text_with_end):
    # decoder_state 相当于每轮都会更新
    # 根据不同策略，最开始可以是 0 (例如是一个全 0 向量的状态)
    # 然后每轮结束后，decoder_state 也会更新
    decoder_output, decoder_state = decoder(
        encoder_state, decoder_state, decoder_input)
    output.append(decoder_output)

    # 收集loss
    loss = loss_function(decoder_output, decoder_target)
    # 第一个 loss 实际上相当于概率 P('D'|'<SOS>') 的损失函数
    # 也就是给decoder输入最开始字符'SOS'，给出句子的第一个词'D'的概率，依次还有：
    # P('E'|'D')
    # P('F'|'E')
    # P('<EOS>'|'F')
    # 也即是我们分别喂给decoder： '<SOS>', 'D', 'E', 'F'
    # 我们希望它的输出是： 'D', 'E', 'F', '<EOS>'

"""
decoder(encoder_state, decoder_state, '<SOS>') -> 'D'
decoder(encoder_state, decoder_state, 'D') -> 'E'
decoder(encoder_state, decoder_state, 'E') -> 'F'
decoder(encoder_state, decoder_state, 'F') -> '<EOS>'
output == ['D', 'E', 'F', '<EOS>']
"""
```

### 预测时

```python

# 这是用户输入数据
input_text = ['床', '前', '明', '月', '光']

# 计算encoder的状态
encoder_state = encoder(input_text)

# 第一个输入到decoder的字，是我们预设的'<SOS>'
# 而后续输入到decoder的字，是上一轮decoder的输出
last_decoder_output = '<SOS>'
output = []
decoder_state = 0
# 如果句子太长了，就是说预测句子结尾可能已经失败了
# 则退出预测
# 也就是循环最长也就是output_length_limit
for _ in range(output_length_limit):
    # decoder_state 相当于每轮都会更新
    decoder_output, decoder_state = decoder(
        encoder_state, decoder_state, last_decoder_output)
    output.append(decoder_output)
    # 更新 last_decoder_output
    last_decoder_output = decoder_output

    # 如果察觉到句子结尾，则直接退出预测
    if decoder_output == '<EOS>':
        break

```

### 另一种解释

`['床', '前', '明', '月', '光']`这个输入，构成了encoder_state，
decoder相当于是构建一个函数关系：

下文`=>`是指左侧到右侧的单向函数映射

encoder(`['床', '前', '明', '月', '光']`) => encoder_state

decoder(encoder_state, `['<SOS>']`) => `'疑'`  
decoder(encoder_state, `['<SOS>', '疑']`) => `'是'`  
decoder(encoder_state, `['<SOS>', '疑', '是']`) => `'地'`  
decoder(encoder_state, `['<SOS>', '疑', '是', '地']`) => `'上'`  
decoder(encoder_state, `['<SOS>', '疑', '是', '地', '上']`) => `'霜'`  
decoder(encoder_state, `['<SOS>', '疑', '是', '地', '上', '霜']`) => `'<EOS>'`  

# 与神经机器翻译的异同

神经对话模型最开始就来源于对神经翻译模型的思考，但是他们有很多不同之处。

### embedding不同

神经翻译模型因为是从一个语种到另一个语种的翻译，
所以encoder和decoder的embedding往往是不同的。

例如翻译数据中，英文我们取10万个词，法文取10万个词，
我们需要建立的是两个10万的embedding，
或者一个20万的embedding。

而神经对话模型里，因为输入和输出都是一个语种，
也就是只有英文到英文、法文到法文，所以encoder和docoder
可以共用一个10万个词的embedding。

### 结果重复性不同

神经机器翻译往往是一对一的映射，一句话对应一句话，例如：

hello <> 你好  
bye <> 再见  

也就是说输入与输出都是唯一对应的输出，或者近似对应的输出，虽然也可能一句话、或者一个词有多个翻译：

hi <> 你好  
hello <> 你好

但是这种情况并不会太多，而对话模型这种问题更普及，例如可以：

你好吗？ > 烦着呢别理我  
今天我们去哪玩？ > 烦着呢别理我  
我们去吃牛排吧 > 烦着呢别理我   
你知道qhduan吗 > 不知道  
你知道qhduan是帅哥吗 > 不知道  
你知道龙傲天吗 > 不知道  

上面的情况实际上在统计意义上是出现的。
这也导致对话模型更容易出现“I don't know”问题，
也就是模型更容易学会更好回答而不犯错的答案，任何问题都回答“我不知道”就行了，或者类似的简单回复。

所以后续的一些文献更看重神经对话模型的diversity，也就是结果多样。

### 对称性不同

神经翻译模型有对称性，例如

en_zh(hello) = 你好

zh_en(你好) = hello

即有：

zh_en(en_zh(hello)) = hello

也就是平行语料之间有对称性，但是聊天的上一句下一句是没有的：

假设我们有：

chat(你是谁) = 我是你哥哥

但我们不能说：

chat(chat(你是谁)) == 你是谁

chat(我是你哥哥) == 你是谁

### 语料不同，与所产生的问题

神经机器翻译依赖平行语聊，即统一意思的一句话。
例如代表某个意思的一句话，有中文表示也有英文表示，那么这两句话的意义是平行的。

神经对话的模型的来源不是平行预料，
早期研究的大部分语料是来自电影字幕。
（例如来自OpenSubtitles）

后续的来源也有：ubuntu系统的系统客服的语料、来自社交媒体的语料，等等。

神经机器翻译的语料，往往可靠性更容易控制，因为一句“hello”，不太可能有多种翻译。而神经对话模型，有人开头一句“你好”之后，很大概率之后的回答，并不是回一句“你好”，因为很正式的回答语料很少。
而社交媒体之类的，更容易产生很发散的语料，这导致神经机器对话的语料质量普遍不高。

另一方面，电影字幕语料有天然的缺陷，
例如不好确定发言人，例如连续两句话很可能是同一人连续说的，因为长度问题分割为两句；
话题转换导致上下文没有相关性；
或者是两个不相干的场景说导致上下文相关性判断错误（即便在时间上接近）。
这些问题同样也导致了语料质量不高的问题。

### 评价标准问题

神经机器翻译的主要评价标准可以分为机器评价和人工评价。
机器评价普遍使用BLEU值进行估算。人工评价则是人工打分。
BLEU是一种自动机器评价算法，一些文献表示，BLEU分数与人类对翻译质量的判断高度相关，即BLEU高，翻译质量越高(在一定统计意义上)。

虽然对于神经机器翻译模型，BLEU也不是一个完美的解决方案，可总体来说效果还是可以接受的。
但是针对神经对话模型，BLEU就更加不是一个好的评价模型了，
后续一些文献反而针对Diversity等其他指标评价模型好坏。

有大量的对话机器人文献，都采用了人工评价，
当然这也显著提高了成本。
很多文献彻底放弃了机器评价。

# 技巧与提高（trick）

一些模型的普遍技巧，例如：
Attention机制，
Residual RNN 机制，
Dropout 机制，
在此不介绍。

### 抗语言模型与互信息模型

在文献
[Li et al., 2015](https://arxiv.org/pdf/1510.03055v3.pdf)
中提到，可以通过加入抗语言信息或者互信息来提高结果的BLEU和Diversity。

假设我们训练语料的第一句话是S，而其他人的回复是T，例如：

S：你今年几岁了？  
T：野原新之助，5岁！  

一般来说我们所训练提高的概率就是P(T|S)，损失函数log(P(T|S))

##### 抗语言(anti-language)损失函数

log(P(T|S)) - log(P(T))

也就是我们在提高P(T|S)的同时，需要抑制P(T)

解释是：如果T是经常出现的句子，例如“我不知道”，
那么P(T)就会很高。
所以我们需要人为降低P(T)出现的概率。

##### 互信息损失函数

log(P(T|S)) + log(P(S|T))

解释是：提高S与T的相关性。如果T是与S完全无关的回复，例如“我不知道”，那么P(S|T)的概率就会很低，即相关性很低。
我们的目的是奖励S与T相关性（互信息高）的训练数据。

BTW：文献中结论为，抗语言模型比互信息模型的diversity高，而互信息模型的BLEU更高。

### 反转技巧

有很多文献指出，把输入语句反转，
可以提高Seq2Seq模型的准确度。

即不再按“床前明月光”这个顺序喂给encoder，
而是按照“光月明前床”这个顺序。

理由一般认为是，一句话的开头的信息量更高，而反向输出会让RNN模型更重视开头。
因为RNN，尤其是门模型，先输入的信息会经过数次遗忘门的迭代，所以越后面的输入反而遗留信息越多。

### 强化学习

我们设计一些特征可以计算出某种Reward，
例如：T与S相似度太高，则Reward低；
T与S的互信息太少，则Reward低。

然后通过log likelihood trick，
使用Reward修正每次更新loss时的权重，
则可以提高模型效果。

也就是高Reward的训练loss更高，让模型更倾向于学习高Reward的训练语料。

参考[Li et al., 2016](https://arxiv.org/abs/1606.01541)

### 对抗学习

假设我们设计一个分类器，可以分出哪些是机器的回复、
哪些是人的回复。
例如分类器学习到，机器更倾向于老回答“我不知道”，
所以会给类似“我不知道”这样的回答以较低概率是人说的。

然后就可以计算出一个对于问句质量的近似打分，
越接近人的回复则Reward越高，越接近机器的回复则Reward越低。
通过log likelihood trick对loss进行修正，
则可以提高训练效果。

参考[Li et al., 2017](https://arxiv.org/abs/1701.06547)

### TFIDF技巧

如果S中TFIDF相对整个batch来说的信息量较低，
则降低这些S的权重

### 上下文相似技巧

降低T与S太相似的训练集权重。

例如我们可以计算embedding之后的T与S的cosine距离。

### 分组技巧（buckets）

把要输入decoder的数据，根据不同长度分组。
例如1~5个字长的一组，6~10长度的一组，11~15长度一组。

这样的好处至少有：
decoder时的RNN解码长度在每个batch中是差不多的，
提高整体运算效率。

decoder的RNN是可以并行运行的，
如果batch数据中的解码长度不一致，
那么解码时间必然以最长的解码长度为准，
batch中长度很短的数据会很快解码完，
但是从系统运行效率上，还是要等待长的数据解码完才能完成整个batch的decoder解码运算，
这样无形的消耗了一定效率。

# 工程级实战参考与提高

### 训练不同情绪的bot

假设我们有了一个语料的情绪分类器（sentiment classifier）

那么我们可以把语料分为不同的情绪，
然后结合一些trick，
例如给训练数据添加一些标签，例如：

S: [happy] 你 好  
T: 你好啊！偶好开心！

S: [sad] 你 好  
T: 哦……你来啦  

S: [angry] 你 好  
T: 你滚啦！  

这样把标签后的数据输入一个模型训练，
使用时只要给用户的输入加入不同的标签，
则可以得到不同情绪的机器返回结果。

当然了，你也可以直接根据不同情感训练多个模型，
具体怎么做好需要实际测试。

### 训练不同人格特征的bot

其实和上面不同情绪的差不多，只是首先你要有不同人格的训练语料。

原文献中的是使用美国电视剧的剧本，已经标清楚了说话人是谁。

参考[Nguyen et al., 2017](http://web.stanford.edu/class/cs224n/reports/2761115.pdf)

### 语料处理

- 去除重复语料
- 去除非目标文字语料
    - 例如中文训练集去掉句子中包含英文的语料
- 去除太短的语料
- 去除太长的语料
- 去除特殊符号太多的语料
- 尝试从更多资源获取语料：电影、小说、社交媒体、剧本，请使用合法来源……嘿嘿
- 去除特定实体太多的语料，例如包含人名的语料可能不适合

### 将语料分类，训练多个模型

把语料根据来源或者语料本身，
使用某种无监督聚类机制来把语料分类。

例如你的语料来自电影字幕，
可以根据这个电影的所有字幕来把语料无监督分类。
如使用简单的TFIDF算法，然后使用K-Means之类算法进行分类。
这样结果就是例如可以分为：动作片字幕、爱情片字幕、动作爱情片字幕……等等不同语料组。

然后用不同语料组内的语料来训练多个模型，
使用前预判哪个模型更优秀，
或者根据不同场景使用不同模型（使用某种Ensemble算法）。

### 如果可能的话，避免（现在）使用神经对话模型

如题 :)

请考虑传统技术，如AIML等技术。
