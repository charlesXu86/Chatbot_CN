from py2neo import Graph, NodeMatcher
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from socketIO_client import SocketIO, LoggingNamespace
import requests
import json

graph = Graph("http://neo4j:admin@localhost:7474")
selector = NodeMatcher(graph)

# MATCH path = (n)-[r]->(m) where n.案件号 =~ '.*浙1125刑初148号.*' RETURN path
def retrieveDataFromNeo4j(cyber):
    url = 'http://neo4j:admin@localhost:7474/db/data/transaction/commit'
    body = {"statements":[{ "statement":cyber, "resultDataContents":["graph"]}]}
    headers = {'content-type': "application/json"}
    response = requests.post(url, data = json.dumps(body), headers = headers)
    return response.text


class ViewCaseDefendants(Action):
    def name(self):
        return 'action_view_case_defendants'

    def run(self, dispatcher, tracker, domain):
        case = tracker.get_slot('case')
        if(case==None):
            dispatcher.utter_message("服务器开小差了")
            return []
        all_defendants = ""
        a = list(selector.match("被告人", 案件号__contains=case))
        for _ in a:
            if (a[a.__len__() - 1] == _):
                all_defendants = all_defendants + _['name'] + "."
            else:
                all_defendants = all_defendants + _['name'] + ','
        response = "{}案件, 有涉案人员:{}".format(case, all_defendants)
        dispatcher.utter_message(response)
        return [SlotSet('case', case)]


class ViewCaseDefendantsNum(Action):
    def name(self):
        return 'action_view_case_defendants_num'

    def run(self, dispatcher, tracker, domain):
        case = tracker.get_slot('case')
        if(case==None):
            dispatcher.utter_message("服务器开小差了")
            return []
        n = list(selector.match("被告人", 案件号__contains=case)).__len__()

        if(n == 0):
            response = "没有这个案件, 查证后再说吧~"
        else:
            response = "{}案件共有{}个涉案人员".format(case, n)
        graph_data = retrieveDataFromNeo4j("MATCH path = (n)-[r]->(m) where n.案件号 =~ '.*{}.*' RETURN path".format(case))
        with SocketIO('localhost', 8080) as socketIO:
            socketIO.emit('data', graph_data)
        dispatcher.utter_message(response)
        return [SlotSet('case', case)]


class ViewDefendantData(Action):
    def name(self):
        return 'action_view_defendant_data'

    def run(self, dispatcher, tracker, domain):
        defendant = tracker.get_slot('defendant')
        item = tracker.get_slot('item')
        person = graph.nodes.match("被告人", name=defendant).first()
        response = "这个系统还够完善, 没有找到{}关于'{}'的信息, 抱歉哦..".format(defendant, item)
        if(item==None or defendant==None):
            dispatcher.utter_message("服务器开小差了")
            return []

        # < id >: 0
        # name: 张青红出生地: 浙江省云和县出生日期: 1979
        # 年8月14日性别: 女户籍所在地: 云和县凤凰山街道上前溪100号文化程度: 初中文化案件号: （2017）浙1125刑初148号毒品数量: 31.3
        # 克民族: 汉族现住址: 丽水市莲都区水阁工业区齐垵村20号2楼职业: 务工
        if item.find("个人资料") != -1:
            response = "{},{},{}生,户籍所在:{}, {}程度, 现住{}, 贩毒{}".format(defendant, person['性别'],person['出生日期'], person['户籍所在地'], person['文化程度'], person['现住址'],person['毒品数量'])
        elif item.find("出生地") != -1:
            response = "{}的出生地是{}".format(defendant, person['出生地'])
        elif item.find("生日") != -1:
            response = "{}的生日是{}".format(defendant, person['出生日期'])
        elif item.find("性别") != -1:
            response = "{}的性别是:{}".format(defendant, person['性别'])
        elif item.find("户籍所在地") != -1:
            response = "{}的户籍所在地是:{}".format(defendant, person['户籍所在地'])
        elif item.find("文化程度") != -1:
            response = "{}的文化程度是:{}".format(defendant, person['文化程度'])
        elif item.find("贩毒量") != -1:
            response = "{}的贩毒量是:{}".format(defendant, person['毒品数量'])
        elif item.find("民族") != -1:
            response = "{}的民族是:{}".format(defendant, person['民族'])
        elif item.find("现住址") != -1:
            response = "{}的现住址是:{}".format(defendant, person['现住址'])
        elif item.find("职业") != -1:
            response = "{}的职业是:{}".format(defendant, person['职业'])

        graph_data = retrieveDataFromNeo4j("MATCH path = (n)-[r]->(m) where n.name =~ '.*{}.*' RETURN path".format(defendant))
        with SocketIO('localhost', 8080) as socketIO:
            socketIO.emit('data', graph_data)
        dispatcher.utter_message(response)
        return [SlotSet('defendant', defendant)]


class ViewCaseDetail(Action):
    def name(self):
        return 'action_view_case_detail'

    def run(self, dispatcher, tracker, domain):
        case = tracker.get_slot('case')
        if(case==None):
            dispatcher.utter_message("服务器开小差了")
            return []
        found = graph.nodes.match("被告人", 案件号__contains=case)
        n = list(found).__len__()
        if(n==0):
            response = "没有找到这个案件, 是不是案件号错了"
        else:
            graph_data = retrieveDataFromNeo4j("MATCH path = (n)-[r]->(m) where n.案件号 =~ '.*{}.*' RETURN path".format(case))
            with SocketIO('localhost', 8080) as socketIO:
                socketIO.emit('data', graph_data)
            response = "需要我做点什么?"
            
        dispatcher.utter_message(response)
        return [SlotSet('case',case)]

if __name__ == '__main__':
    # data = graph.match("购买人")
    # for rel in data:
    selector = NodeMatcher(graph)
    all_defendants = ""
    a = list(selector.match("被告人", 案件号__endswith="浙1125刑初148号"))
    for _ in a:
        if(a[a.__len__()-1] == _):
            all_defendants = all_defendants + _['name'] + "."
        else:
            all_defendants = all_defendants + _['name'] + ','

    print(all_defendants)
