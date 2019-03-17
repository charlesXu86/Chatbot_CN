#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Chatbot_CN_story.py 
@desc:
@time: 2019/03/17 
"""

import codecs
import os
import re


rtitle = re.compile(r'(##\sGenerated\sStory\s)(.*)')
rootpath = os.getcwd() + os.sep + ".." + os.sep

readpath = os.path.join(rootpath + "data" + os.sep, "mobile_story.md")
writepath = os.path.join(rootpath + "data" + os.sep, "mobile_edit_story.md")

count = 0
with codecs.open(readpath, 'r', 'utf-8') as f, codecs.open(writepath, 'w', 'utf-8') as f2:
    for line in f:
        if rtitle.match(line):
            count += 1
            flag = 'No' + str(count)
            line = re.sub(rtitle, '\\1' + flag, line)

        f2.write(line)
