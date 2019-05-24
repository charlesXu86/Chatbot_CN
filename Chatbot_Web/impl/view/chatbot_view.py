# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     chatbot_view.py
   Description :   人机对话页面视图
   Author :       charl
   date：          2019/1/25
-------------------------------------------------
   Change Activity: 2019/1/25:
-------------------------------------------------
"""

import queue,json,time

from django.shortcuts import render,HttpResponse

GLOBAL_MSG_QUEUES = {

}

def chatbot_page(request):
    context = {}
    return render(request, 'dialogue/dialogue_v2.html', context)

def send_msg(request):
    '''
    接受消息函数
    :param request:
    :return:
    '''
    # 接受关于data的数据
    msg_data = request.POST.get('data')
    # 判断是否正确
    if msg_data:
        msg_data = json.loads(msg_data)
        msg_data['timestamp'] = time.time()
        if msg_data['type'] == 'single':
            if not GLOBAL_MSG_QUEUES.get(int(msg_data['to'])):
                GLOBAL_MSG_QUEUES[int(msg_data["to"])] = queue.Queue()
            GLOBAL_MSG_QUEUES[int(msg_data["to"])].put(msg_data)
        # else:  # group
        #     group_obj = models.ChatGroup.objects.get(id=msg_data['to'])
        #     for member in group_obj.members.select_related():
        #         if not GLOBAL_MSG_QUEUES.get(member.id):  # 如果字典里不存在这个用户的queue
        #             GLOBAL_MSG_QUEUES[member.id] = queue.Queue()
        #         if member.id != request.user.userprofile.id:
        #             GLOBAL_MSG_QUEUES[member.id].put(msg_data)
    return HttpResponse('---发送后端成功---')

def get_new_msgs(request):
    if request.user.userprofile.id not in GLOBAL_MSG_QUEUES:
        print("不存在[%s]" %request.user.userprofile.id,request.user)
        GLOBAL_MSG_QUEUES[request.user.userprofile.id] = queue.Queue()
    msg_count = GLOBAL_MSG_QUEUES[request.user.userprofile.id].qsize()
    q_obj = GLOBAL_MSG_QUEUES[request.user.userprofile.id]
    msg_list = []
    print(msg_list)
    if msg_count >0:
        for msg in range(msg_count):
            msg_list.append(q_obj.get())
        print("new msgs:",msg_list)
    else:#没消息,要挂起
        print("no new msg for ",request.user,request.user.userprofile.id)
        #print(GLOBAL_MSG_QUEUES)
        try:
            msg_list.append(q_obj.get(timeout=60))
        except queue.Empty:
            print("\033[41;1mno msg for [%s][%s] ,timeout\033[0m" %(request.user.userprofile.id,request.user))
    return HttpResponse(json.dumps(msg_list))
