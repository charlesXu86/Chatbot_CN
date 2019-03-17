#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Ticket_Action.py
@desc: 车票预订
@time: 2019/03/16 
"""

import json
from typing import List

from rasa_core.dispatcher import Dispatcher
from rasa_core.domain import Domain
from rasa_core.events import Event
from rasa_core.trackers import DialogueStateTracker
from rasa_core_sdk.forms import EntityFormField, FormAction

from tools.api import fetch_train_list, city_List


class ActionReportWeather(FormAction):
    RANDOMIZE = True

    @staticmethod
    def required_fields():
        return [
            EntityFormField("origin", "origin"),
            EntityFormField("destination", "destination"),
            EntityFormField("daytime","daytime")
        ]

    def name(self):
        return "action_report_ticket"

    def submit(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        # stories = tracker.export_stories().encode('utf-8').decode('unicode_escape')
        # print(stories)

        origin = tracker.get_slot('origin')
        destination = tracker.get_slot('destination')
        date_time = tracker.get_slot('daytime')
        # return dispatcher.utter_message(date_time+'|'+origin+'|'+destination)
        if '-' not in date_time:
            return dispatcher.utter_message('日期格式不正确,示例：2018-10-01')
        # return dispatcher.utter_message(date_time+'|'+origin+'|'+destination)
        contents = str(fetch_train_list(date_time,origin,destination))
        if 'err_bot' in contents:
            return dispatcher.utter_message("12306服务异常,请检查请求参数")
        if 'html' in contents:
            return dispatcher.utter_message("日期格式或地址无效,示例:2018-10-19上海到南京")
        # return dispatcher.utter_message(contents)
        weather_data = get_text_datas(contents)

        return dispatcher.utter_message(weather_data)


def get_text_datas(contents):
    datas = json.loads(contents)
    lists = datas['data']['result']
    results = ''
    for content in lists:
        result = str(content).split('|')
        if result[3] is None:
            num = ''
        else:
            num = str(result[3])
        if result[6] is None:
            origin = ''
        else:
            origin = str(result[6])
        if result[7] is None:
            to = ''
        else:
            to = str(result[7])
        if result[8] is None:
            start_time = ''
        else:
            start_time = str(result[8])
        if result[9] is None:
            end_time = ''
        else:
            end_time = str(result[9])
        if result[10] is None:
            during = ''
        else:
            during = str(result[10])
        for key in city_List:
            if origin == city_List.get(key):
                w_1 = key
            if to == city_List.get(key):
                w_2 = key
        results = (results +'车次'+num+'|'+w_1+'到'
        +w_2+'|'+start_time+'开车|'+end_time+'抵达|历时'+during+'\n')

    return results