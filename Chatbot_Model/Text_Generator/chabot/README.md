
# Chatbot测试

## 1、准备数据
这里的数据用的是小黄鸡对话数据：包括30W条对话（分词后）



## 2、下载训练好的fasttext的embedding

https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md

注意是文本格式的

```
wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.zh.vec
```

得到 `wiki.zh.vec` 文件

## 3、改变embedding格式

运行

```
python read_vector.py
```

得到 `word_vec.pkl`文件在目录下

## 4、预处理数据（前面两步embedding部分必须执行完）

```
python extract_conv.py
```

输出：`chatbot.pkl`

## 5、训练数据

运行 `python train.py` 训练（默认到`./s2ss_chatbot.ckpt`）

或者！

运行 `python train_anti.py` 训练抗语言模型（默认到`./s2ss_chatbot_anti.ckpt`）

## 6、测试数据（测试对话）

运行 `python test.py` 查看测试结果，需要提前训练普通模型

或者！

运行 `python test_anti.py` 查看抗语言模型的测试结果，需要提前训练抗语言模型

或者！

运行 `python3 test_compare.py` 查看普通模型和抗语言模型的对比测试结果，
需要提前训练两个模型
