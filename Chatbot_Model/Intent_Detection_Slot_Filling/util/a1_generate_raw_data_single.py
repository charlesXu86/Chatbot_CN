# -*- coding: utf-8 -*-
import json

def generate_raw_data_singel(sline):
    try:
        myjson=json.loads(sline)
    except:
        print(sline)
        return None
    result={}
    elements=myjson['actions']
    for i,element in enumerate(elements):
        target=element['target']
        actor = element['actor']
        intent = element['intent']
        if 'speech' in element: speech=element['speech']
        slots = element['slots']

        if actor=='u' and target=='a':
            result['user']=speech
        if actor=='a' and target=='s':
            result['intent']=intent
            #print("slots:",slots)
            slot_dict={}
            for i,element in enumerate(slots):
                slot_dict[element['name']]=element['value']
            result['slots']=slot_dict
    return result



#sline='{"dialog_template_id": "关设备_范围_成功__2c9081a45ff32c08015ff339cfe10045", "actions": [{"speech": "帮忙关闭一下一同的彩色灯泡吧", "actor": "u", "intent": "用户关设备<全部范围><设备名>", "target": "a", "slots": [{"name": "全部范围", "svd_name": "shared/全部范围", "value": "一同", "start": 6}, {"name": "设备名", "svd_name": "shared/设备名", "value": "彩色灯泡", "start": 9}]}, {"actor": "a", "intent": "关设备<全部范围><设备名>", "target": "s", "slots": [{"name": "全部范围", "value": "一同"}, {"name": "设备名", "value": "彩色灯泡"}]}, {"actor": "s", "intent": "关设备<全部范围><设备名>的应答", "target": "a", "slots": [{"name": "状态", "svd_name": "状态1", "value": "成功"}]}, {"speech": "控制成功", "actor": "a", "intent": "控制成功确认", "target": "u", "slots": []}]}'
#result=generate_raw_data_singel(sline)
#print(result)
