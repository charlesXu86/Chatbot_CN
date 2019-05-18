#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Generate_knowledges.py 
@desc:
@time: 2019/05/09 
"""

import json
import random
import os
import codecs

slot_values_file='slot_values.txt'
slot_value_name_pair_file='slot_pairs.txt'
slot_names_file='slot_names.txt'
splitter='|&|'
splitter_slot_names='||'


def get_knowledge(data_source_file, knowledge_path, test_mode=False):
    '''

    :param data_source_file:
    :param knowldge_path:
    :param test_mode:
    :return:
    '''
    slot_value_name_pair_files = knowledge_path + "/" + slot_value_name_pair_file
    slot_values_files = knowledge_path + "/" + slot_values_file
    slot_names_files = knowledge_path + "/" + slot_names_file

    if os.path.exists(slot_value_name_pair_files) and os.path.exists(slot_values_files) and os.path.exists(slot_names_files):
        print("knowledge exists, will not generate it.")
        return
    else:
        print("Knowledge exists, will start to generate it.")

    file_object = codecs.open(data_source_file, 'r', 'utf-8')
    lines = file_object.readlines()
    random.shuffle(lines)     # 打乱数据
    if test_mode:
        lines = lines[0:200000]
    print("get_knowledge.length of lines:", len(lines))
    knowledge_dict = {}
    slot_name_set = set()
    for i, line in enumerate(lines):
        if len(line.strip()) < 2:
            continue
        try:
            myjson = json.loads(line)
        except:
            continue
        elements = myjson['actions']
        for i, element in enumerate(elements):
            target = element['target']
            actor = element['actor']
            slots = element['slots']
            if actor == 'a' and target == 's':
                for i, element in enumerate(slots):
                    slot_name = element['name']
                    slot_value = element['value']
                    slot_name_set.add(slot_name)
                    sett = knowledge_dict.get(slot_value, None)
                    if sett is None:  # 如果slot_value不存在，则生成
                        sett = set()
                        sett.add(slot_name)
                        knowledge_dict[slot_value] = sett


    #####============
    # 1、写入 slot_value
    # 2、写入 slot_name-slot_value对
    # 3、写入总的slot_name
    slot_values_file_object = codecs.open(slot_values_file, 'w', 'utf-8')
    slot_value_name_pair_file_object = codecs.open(slot_value_name_pair_files, 'w', 'utf-8')
    slot_names_file_object = codecs.open(slot_names_files, 'w', 'utf-8')

    for k, v in knowledge_dict.items():
        if len(k) < 6:     # 只保存短文本，此处可以设置
            slot_value_name_pair_file_object.write(k + splitter + splitter_slot_names.join(list(v)) + "\n")
            seg_value = str(100000) if len(k) == 1 else str(2000)
            slot_values_file_object.write(k + " " + seg_value + "\n")   # 拼接


    slot_values_file_object.close()
    slot_value_name_pair_file_object.close()

    print("slot_name_set:", slot_name_set)
    for element in slot_name_set:
        slot_names_file_object.write(element + "\n")
    slot_names_file_object.close()

    return

data_source='knowledge/sht_20171125.txt'
knowledge_path='skill3'




