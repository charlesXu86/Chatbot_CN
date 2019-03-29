# 基于TD-IDF的中文关键词提取

## requirements

默认环境python3，需要结巴分词器的支持

```bash
$ pip install jieba
```

## IDF(逆文档频率)生成

用法：

```bash
$ python gen_idf.py -i <inputdir> -o <outputfile>
```

- `-i <inputdir>`   ： 语料库目录，程序会扫描目录下的所有文件
- `-o <outputfile>` ： 保存idf到指定文件

## TF-IDF关键词提取

用法：

```bash
$ python tfidf.py -i <idffile> -d <document> -t <topK>
```
- `-i <idffile>`  ： idf文件路径
- `-d <document>` ： 所需处理文档路径
- `-t <topK>`     ： 返回topK结果

### 示例

```bash
$ python tfidf.py -i idf.txt -d test.txt -t 20
```

返回结果：

```
核
处理器
服务器
系统核心
封装
系列
插槽
核心
主频
产品
伊斯坦布尔
英特尔
功耗
多处理器
低仅
折合
浮点运算
性能
构建
吹起
```

> 注：该repo中提供的idf.txt由清华NLP组的新闻数据集训练获得。
