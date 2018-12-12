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
import datetime
import time

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