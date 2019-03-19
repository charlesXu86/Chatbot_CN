# -*- coding: utf-8 -*-
#1.read a line
#2.get 1)user_speech, 2)intent, 3)slots, 4)get knowledges for the slots
import json
import codecs
import os
import random
slot_values_file='slot_values.txt'
slot_value_name_pair_file='slot_pairs.txt'
slot_names_file='slot_names.txt'
splitter='|&|'
splitter_slot_names='||'

def get_knowledge(data_source_file,knowledge_path,test_mode=False):
    #if target file not exist, create; otherwise return
    slot_value_name_pair_filee=knowledge_path+"/"+slot_value_name_pair_file
    slot_values_filee=knowledge_path + "/" + slot_values_file
    slot_names_filee=knowledge_path + "/" + slot_names_file
    if  os.path.exists(slot_value_name_pair_filee) and os.path.exists(slot_values_filee) and os.path.exists(slot_names_filee):
        print("knowledge exists. will not generate it.")
        return
    else:
        print("knowledge not exists. will start to generate it.")

    file_object=codecs.open(data_source_file,'r','utf8')
    lines=file_object.readlines()
    random.shuffle(lines)
    if test_mode:
        lines=lines[0:20000]
    print("get_knowledge.length of lines:",len(lines))
    knowledge_dict = {}
    slot_name_set=set()
    for i,line in enumerate(lines):
        if len(line.strip())<2:
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
                    if sett is None:  # slot_value is not exists===>create a list.
                        sett = set()
                        sett.add(slot_name)
                        knowledge_dict[slot_value] = sett
                    else:  # slot_value is exists===>append to exist list.
                        sett.add(slot_name)
                        knowledge_dict[slot_value] = sett

    #print
    #1.write slot_value to file system
    #2.write slot_value-slot_name pair to file system
    #3.write total slot name to file systm
    #ii = 0
    slot_values_file_object = codecs.open(slot_values_filee, 'w', 'utf-8')
    slot_value_name_pair_file_object=codecs.open(slot_value_name_pair_filee,'w','utf-8')
    slot_names_file_object=codecs.open(slot_names_filee,'w','utf-8')

    #if not os.path.exists(slot_value_name_pair_file) and not os.path.exists(slot_values_file) :
    for k, v in knowledge_dict.items():
        if len(k)<=6: #only save short context
            slot_value_name_pair_file_object.write(k+splitter+splitter_slot_names.join(list(v))+"\n")
            seg_value=str(100000) if len(k)==1 else str(2000)
            slot_values_file_object.write(k+" "+seg_value+"\n")
        #ii = ii + 1

    slot_values_file_object.close()
    slot_value_name_pair_file_object.close()

    print("slot_name_set:",slot_name_set)
    #if not os.path.exists(slot_names_file):
    for element in slot_name_set:
        slot_names_file_object.write(element+"\n")
    slot_names_file_object.close()

    return #knowledge_dict

    #print("knowledge_dict:",knowledge_dict)

data_source='knowledge/sht_20171125.txt'
knowledge_path='skill3'
#get_knowledge(data_source,knowledge_path)
