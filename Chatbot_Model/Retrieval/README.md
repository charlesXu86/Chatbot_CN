# Chatbot_CN检索模块

核心的代码在4个python文件中，其它的文件都是网站代码，或者数据文件，可以忽视

### preprocess.py
将实验的数据集转换为json格式，同时做一些预处理。处理后，一个实体及其所关联的所有属性和属性值存储为一个json对象，作为将导入elasticsearch的一个文档

### build_dict.py
构建数据集中属性名字典和实体名字典，用于在解析查询时判断查询语句是否包含知识库中的属性或实体。在数据集较小的时候可以这样做，在数据集较大的时候可以通过检索elasticsearch来判断

### insert.py
将处理好的数据导入elasticsearch, 需为elasticsearch新建index和type（这个没有写成代码，在命令行完成)

### search/views.py
核心代码，包括用户查询解析，elasticsearch查询构造。
