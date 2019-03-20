# Neural_dependency_parsing

## 项目介绍 
基于[Chen and Manning](https://cs.stanford.edu/%7Edanqi/papers/emnlp2014.pdf) 论文的一个神经网络依存句法分析工具。框架使用tensorflow。<br>
项目参考自 [akjindal53244/dependency_parsing_tf](https://github.com/akjindal53244/dependency_parsing_tf) 。感谢原作者<br>
原项目是用于英文的，这里将其修改为中文的分析器, 同时添加了LAS的计算。<br>
<br>
## 依赖
tensorflow_gpu = 1.9, #更低的应该也可以<br>
<br>

## 数据集说明
![image]()
第一列是单词在句子中的序号，第二列是单词，第五列是POS tags，第七列是所依赖的序号，第八列是依赖关系也是arc labels。

## 实现说明
   1、分词
   2、依赖词性标注(pos-tagging)
   3、句法解析树的构造
   4、歧义问题处理
   
   分词和词性标注这里没有自己实现，调用的第三方接口(thulac，初步感觉效果还不错，具体安装和使用方法请自行百度)。(有空的时候会自己实现)
   
## 模型结构
![image](Chatbot_Model/Dependency_parsing/img/architecture.png)
![image]()

## 测试结果
现在为初始版本，使用THU语义依存语料库，输出格式为conll格式。<br>
test UAS: 79.3430018128<br>
test LAS: 72.7448896668<br>
<br>
测试输出：<br>
1 世界 世界 n n _ 5 限定<br>
2 第 第 m m _ 5 限定<br>
3 八 八 m m _ 2 连接依存<br>
4 大 大 a a _ 5 限定<br>
5 奇迹 奇迹 n n _ 6 经验者<br>
6 出现 出现 v v _ 0 核心成分<br>
<br>
Gold原文：<br>
1   世界    世界    n   n   _   5   限定    <br>
2   第  第  m   m   _   4   限定    <br>
3   八  八  m   m   _   2   连接依存    <br>
4   大  大  a   a   _   5   限定    <br>
5   奇迹    奇迹    n   n   _   6   存现体  <br>
6   出现    出现    v   v   _   0   核心成分<br>
可改进的地方为模型参数（未细调)/embeding（在该语料库上训练的)等处<br>
<br>

## 运行
训练模型： python parser_model.py<br>
测试模型： python parser_test.py<br>

## 其他
