import datetime
from datetime import datetime, timedelta
import sys
import re

# 是否为冬令时
isWinterTime = input("Is Winter Time? (Please input 1 or 0, 1 = true, 0 = false)\n")
pattern = "^[0, 1]$"
if re.match(pattern, isWinterTime) is None:
    sys.exit()

# 定义时差，shift开始时间，shift结束时间
hourDelta = 0
shiftStartTime = ""
shiftEndTime = ""

# 冬令时
if isWinterTime == "1":
    hourDelta = 8
    shiftStartTime = "18:00:00"
    shiftEndTime = "06:00:00"

# 夏令时
if isWinterTime == "0":
    hourDelta = 7
    shiftStartTime = "19:00:00"
    shiftEndTime = "07:00:00"

# 获取当前美国时间
now = datetime.utcnow() - timedelta(hours = hourDelta)
now_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
now_date = now.strftime("%Y-%m-%d")
print("Current america time: " + now_datetime)

# 参考时间用于判断是否为工作时间
morning_begin = datetime.fromisoformat(now_date + " 00:00:00")
morning_end = datetime.fromisoformat(now_date + " " + shiftEndTime)
night_begin = datetime.fromisoformat(now_date + " " + shiftStartTime)
night_end = datetime.fromisoformat(now_date + " 23:59:59")

# 获取Shift时间
def getShift():
    begin_date = ""
    end_date = ""

    # 非工作时间 --- 获取前一个Shift的列表
    if morning_end <= now < night_begin:
        print("Non-Working time")
        begin_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")

    # 上班时间 --- 获取当前Shift的列表
    else:
        print("Working time")
        # 如果当前时间在00:00:00-06:59:59
        if morning_begin <= now < morning_end:
            begin_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
            end_date = now.strftime("%Y-%m-%d")

        # 如果当前时间在19:00:00-23:59:59
        if night_begin <= now <= night_end:
            begin_date = now.strftime("%Y-%m-%d")
            end_date = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    print("On shift: " + begin_date + " " + shiftStartTime + " --- " + end_date + " " + shiftEndTime)

    return ("'" + begin_date + "','" + shiftStartTime + "'", "'" + end_date + "','" + shiftEndTime + "'")