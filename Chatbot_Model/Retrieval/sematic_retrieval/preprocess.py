# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     preprocess.py
   Description :   将数据转换为json格式。处理后，一个实体及其所关联的所有属性和属性值存储为一个json对象，作为将导入elasticsearch的一个文档
   Author :       charl
   date：          2018/11/6
-------------------------------------------------
   Change Activity: 2018/11/6:
-------------------------------------------------
"""

import os
import re
import json

from collections import defaultdict

def transform_triple2json(input_file):
    '''
    将一个三元组转化成json，并且记录entity列表和attribute列表
    一个三元组对应一个文档
    :param input_file:
    :return:
    '''
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    out_name = basename[:basename.rfind(".")]

    f_input = open(input_file)
    f_ent = open(dirname + "/" + out_name + "_entity.txt", "w")
    f_attr = open(dirname + "/" + out_name + "_attr.txt", "w")
    f_json = open(dirname + "/" + out_name + ".json", "w")

    attr_dict = dict()
    entity_dict = dict()
    cnt = 0
    for line in f_input:
        parts = line.strip().split(" ")
        entity = parts[0]
        attr = parts[1]
        attr_vals = " ".join(parts[2:])

        entity_dict[entity] = 1
        attr_dict[attr] = 1

        # for val in attr_vals:
        new_doc = dict()
        new_doc['subj'] = entity
        new_doc['pred'] = attr
        new_doc['obj'] = attr_vals

        new_doc_j = json.dumps(new_doc)
        f_json.write(new_doc_j + "\n")

        cnt += 1
        if not (cnt % 10000):
            print(cnt)

    for en in entity_dict:
        f_ent.write(en + "\n")
    for at in attr_dict:
        f_attr.write(at + "\n")

def transform_entity2json(input_file):
    '''
    一个entity的所有属性为一个文档
    height和weight由于要支持range搜索，需要另存为int类型，要单独考虑
    :param input_file:
    :return:
    '''
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    out_name = basename[:basename.rfind(".")]

    f_input = open(input_file, 'rb')
    f_json = open(dirname + "/" + out_name + ".json", "w")
    f_val = open(dirname + "/" + out_name + "_val.txt", "w")

    val_attr_map = defaultdict(dict)

    last = None
    new_ent = {'po': []}
    for line in f_input:
        line = str(line,encoding="utf-8")
        parts = line.strip().split(" ")
        entity = parts[0]
        attr = parts[1]
        attr_vals = " ".join(parts[2:])
        if last is None:
            last = entity

        if last is not None and entity != last:
            new_ent['subj'] = last
            new_ent_j = json.dumps(new_ent)
            f_json.write(new_ent_j + "\n")
            last = entity
            new_ent = {}
            new_ent['po'] = []

        if attr == 'height':
            v = clean_height(attr_vals)
            if v is not None:
                new_ent['height'] = v
        elif attr == 'weight':
            v = clean_weight(attr_vals)
            if v is not None:
                new_ent['weight'] = v
        elif attr != 'description':
            v = clean_normal(attr_vals)
            for vv in v:
                new_ent['po'].append({'pred': attr, 'obj': vv})
            if attr not in ['height', 'weight', 'description', 'birthDate', '年龄']:
                for vv in v:
                    if attr in val_attr_map[vv]:
                        val_attr_map[vv][attr] += 1
                    else:
                        val_attr_map[vv][attr] = 1
        else:
            new_ent['po'].append({'pred': "description", "obj": attr_vals})

    new_ent['subj'] = last
    new_ent_j = json.dumps(new_ent)
    f_json.write(new_ent_j + "\n")

    for v in val_attr_map:
        val_attr_map[v] = sorted(val_attr_map[v].items(), key=lambda x: x[1], reverse=True)

    for v in val_attr_map:
        f_val.write(v)
        for attr in val_attr_map[v]:
            f_val.write(" " + attr[0])
        f_val.write("\n")
    print('====',dirname)
    print('Done')

def clean_weight(h):
    cm = re.findall('\d{3}', h)
    if len(cm):
        return int(cm[0])
    m = re.findall('\d\.\d{2,3}', h)
    if len(m):
        return int(float(m[0]) * 100)
    return None


def clean_height(w):
    w = w.replace(" ", "")
    kg = re.findall('\d{2,3}\.?\d?', w)
    if len(kg):
        return int(float(kg[0]))
    return None


def clean_normal(attr_vals):
    v = []
    a = re.split(" |,|，|、|\|/|#|;|；", attr_vals)
    for aa in a:
        if aa:
            v.append(aa)
    return v

if __name__ == '__main__':
    # transform_triple2json("../data/Person.txt")
    # transform_triple2json("../data/Org.txt")
    # transform_triple2json("../data/Place.txt")

    transform_entity2json("D:\dataset\Person.txt")