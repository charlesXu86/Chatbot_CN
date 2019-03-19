# -*- coding: utf-8 -*-
import json
import codecs
from  a1_generate_raw_data_single import generate_raw_data_singel

test_mode=True
def generate_raw_data(source_file_name):
    #1.read file
    source_file_object=codecs.open(source_file_name,'r','utf-8')
    lines=source_file_object.readlines()
    #2.loop each line, and add data to list.
    result_dict={}
    for i,line in enumerate(lines):
        sub_dict=generate_raw_data_singel(line)
        if sub_dict is not None and sub_dict['user'] is not None:
            result_dict[sub_dict['user']]=sub_dict

    # print to have a look
    print("length of result list:",len(result_dict))
    i=0
    return result_dict

#source_file_name='knowledge/sht_20171125.txt'
#generate_raw_data(source_file_name)