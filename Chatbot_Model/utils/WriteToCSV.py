# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     WriteToCSV.py
   Description :  将数据写入到excel
   Author :       charles
   date：          2018/12/12
-------------------------------------------------
   Change Activity: 2018/12/12:
-------------------------------------------------
"""

import xlsxwriter
'''
#### 例子  ####
workbook = xlsxwriter.Workbook('./text.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A3',15)
worksheet.write('B3',20)
worksheet.write('C3',44)
worksheet.write('D3',36)

headings = ['a','b','c']
data = [
  [1,2,3,4,5],
  [2,4,6,8,10],
  [3,6,9,12,15],
]
# 按行插入数据
worksheet.write_row('A4',headings)
# 按列插入数据
worksheet.write_column('A5',data[0])
worksheet.write_column('B5',data[1])
worksheet.write_column('C5',data[2])

workbook.close()
'''


def NER2CSV(judgementId, addr, charge, keywords, court, per, loc, org, mon, proponents, opponents, text, timestamp):
    '''
    将NER抽取出来的结果写入csv，以方便入Neo4J
    写入的参数可以自行调整
    :param judgementId:
    :param addr:
    :param charge:
    :param keywords:
    :param court:
    :param per:
    :param loc:
    :param org:
    :param mon:
    :param proponents:
    :param opponents:
    :param text:
    :param timestamp:
    :return:
    '''
    workbook = xlsxwriter.Workbook('./Ner_Result.csv')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'judgementId')
    worksheet.write('B1', 'addr')
    worksheet.write('C1', 'charge')
    worksheet.write('D1', 'keywords')
    worksheet.write('E1', 'court')
    worksheet.write('F1', 'per')
    worksheet.write('G1', 'loc')
    worksheet.write('H1', 'org')
    worksheet.write('I1', 'mon')
    worksheet.write('J1', 'proponents')
    worksheet.write('K1', 'opponents')
    worksheet.write('L1', 'text')
    worksheet.write('M1', 'timestamp')

    # 按行插入数据
    worksheet.write_row(judgementId, addr, charge, keywords, court, per, loc, org, mon, proponents, opponents, text, timestamp)
    workbook.close()

    return workbook