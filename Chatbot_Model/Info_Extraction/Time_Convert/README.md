## 用于句子中时间词的抽取和转换

## 功能说明
用于句子中时间词的抽取和转换  
详情请见test.py

    res = tn.parse(target=u'过十分钟') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'2013年二月二十八日下午四点三十分二十九秒', timeBase='2013-02-28 16:30:29') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'我需要大概33天2分钟四秒', timeBase='2013-02-28 16:30:29') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'今年儿童节晚上九点一刻') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'2个小时以前') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'晚上8点到上午10点之间') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
返回结果：

    {"timedelta": "0 days, 0:10:00", "type": "timedelta"}
    {"timestamp": "2013-02-28 16:30:29", "type": "timestamp"}
    {"type": "timedelta", "timedelta": {"year": 0, "month": 1, "day": 3, "hour": 0, "minute": 2, "second": 4}}
    {"timestamp": "2018-06-01 21:15:00", "type": "timestamp"}
    {"error": "no time pattern could be extracted."}
    {"type": "timespan", "timespan": ["2018-03-16 20:00:00", "2018-03-16 10:00:00"]}
    
## 使用方式 
demo：python3 Test.py

优化说明
    
| 问题          | 以前版本                                     | 现在版本                    |
| ----------- | ---------------------------------------- | ---------------------- |
| 无法解析下下周末     | "timestamp": "2018-04-01 00:00:00"                                    | "timestamp": "2018-04-08 00:00:00"                 |
| 无法解析 3月4         | "2018-03-01"                                   | "2018-03-04"               |
| 无法解析 初一 初二      | cannot parse                                    | "2018-02-16"              |
| 晚上8点到上午10点之间  无法解析上午      | ["2018-03-16 20:00:00", "2018-03-16 22:00:00"] |  ["2018-03-16 20:00:00", "2018-03-16 10:00:00"]|
| 3月21号  错误解析成2019年      | "2019-03-21" | "2018-03-21" |

感谢@[tianyuningmou](https://github.com/tianyuningmou) 目前增加了对24节气的支持


    temp = ['今年春分']
    "timestamp" : "2020-03-20 00:00:00"

## TODO

| 问题          | 现在版本                                     | 正确
| ----------- | ---------------------------------------- | ---------------------- |
| 晚上8点到上午10点之间     |  ["2018-03-16 20:00:00", "2018-03-16 22:00:00"] |  ["2018-03-16 20:00:00", "2018-03-17 10:00:00"]"                                    | "timestamp": "2018-04-08 00:00:00"                 |
