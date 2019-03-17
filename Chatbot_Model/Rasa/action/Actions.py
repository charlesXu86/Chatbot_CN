#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Actions.py 
@desc:
@time: 2019/03/17 
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

import requests

support_search = ['法律咨询', '量化交易']

def extract_item(item):
    if item is None:
        return None
    for name in support_search:
        if name in item:
            return name
    return None

class ActionSearchConsume(Action):
    def name(self):
        return 'action_search_consume'

    def run(self, dispatcher, tracker, domain):
        item = tracker.get_slot("item")
        item = extract_item(item)
        if item is None:
            dispatcher.utter_message("您好，我现在只会查话费和流量")
            dispatcher.utter_message("你可以这样问我：“帮我查话费”")
            return []

        time = tracker.get_slot("time")
        if time is None:
            dispatcher.utter_message("您想查询哪个月的消费？")
            return []
        # query database here using item and time as key. but you may normalize time format first.
        dispatcher.utter_message("好，请稍等")
        if item == "流量":
            dispatcher.utter_message(
                "您好，您{}共使用{}二百八十兆，剩余三十兆。".format(time, item))
        else:
            dispatcher.utter_message("您好，您{}共消费二十八元。".format(time))
        return []

class FetchProfileAction(Action):
    def name(self):
        return "fetch_profile"

    def run(self, dispatcher, tracker, domain):
        url = "http://myprofileurl.com"
        data = requests.get(url).json
        return [SlotSet("account_type", data["account_type"])]