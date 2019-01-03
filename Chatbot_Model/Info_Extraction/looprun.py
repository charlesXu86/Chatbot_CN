#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: looprun.py
@desc: 循环执行脚本
@time: 2019/01/03
"""
import os
import time

'''
#run a program again and again 
#try run a program 
#parameter：
    strCmd      program cmd line
    intTimes    run how many times, "-1" means not stop,default is -1,
    intDelay    delay seconds
#return：
#
'''
def loopurn (strCmd, intTimes = -1, intDelay = 5):
    try:
        while intTimes:
            if intTimes>0:
                print("[remain %d times] " %(intTimes),end = "")
                intTimes -= 1
            print ("after %d seconds to run program:[%s] " % (intDelay , strCmd) )
            time.sleep(intDelay)
            os.system(strCmd) 
            
    except Exception as e :
        print (e)      


if __name__ == '__main__':

    loopurn ("python D:\project\Chatbot_CN\Chatbot_Model\Info_Extraction\Info_Ext_main.py --mode=demo")
    
