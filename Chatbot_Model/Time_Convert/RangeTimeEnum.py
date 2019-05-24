#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: RangeTimeEnum.py
@desc: 时间段枚举
@time: 2019/05/23
"""



# 范围时间的默认时间点
class RangeTimeEnum():
    day_break = 3  # 黎明
    early_morning = 8  # 早
    morning = 10  # 上午
    noon = 12  # 中午、午间
    afternoon = 15  # 下午、午后
    night = 18  # 晚上、傍晚
    lateNight = 20  # 晚、晚间
    midNight = 23  # 深夜


if __name__ == "__main__":
    print(RangeTimeEnum.afternoon)
