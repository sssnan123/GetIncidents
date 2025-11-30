import requests
import base64
import xlwt
import json
import getShiftTime
import os

CONSTANT_PRIORITY = ["-- None --", "1 - Critical", "2 - High", "3 - Moderate", "4 - Low", "5 - Planning"]
CONSTANT_INCIDENT_STATE = {
    1 : "New",
    2 : "In Progress",
    6 : "Resolved",
    7 : "Closed",
    8 : "Canceled",
    20 : "Monitoring"
}

shiftStartTime, shiftEndTime = getShiftTime.getShift()

# 查询参数
sysparm_query = (
    # 分配的组为IRT
    "assignment_group=7c7a30761bd3f3c0cc2da9fbbc4bcbbd"
    "^short_descriptionNOT LIKEecam"
    "^sysparm_fields=number,prioriy,incident_state,assigned_to,short_description,sys_class_name"
    # 创建的起始时间
    "^sys_created_onBETWEENjavascript:gs.dateGenerate(" + shiftStartTime + ")"
    # 创建的结束时间
    "@javascript:gs.dateGenerate(" + shiftEndTime + ")"
)

# service_account
service_account_username = "u_sa_ebay_snow_net"
service_account_password = "Restinpeacetrace2020"
authorization = base64.urlsafe_b64encode((service_account_username + ":" + service_account_password).encode(encoding="utf-8")).decode("utf-8")

# api url
incidentURL = "https://ebayinc.service-now.com/api/now/table/incident"

headers = {
    "Content-Type" : "application/json",
    "Accept" : "application/json",
    "Authorization" : "Basic " + authorization
}

params = {
    "sysparm_query" : sysparm_query
}

response = requests.get(incidentURL, headers = headers, params = params)

IncidentsList = json.loads(response.text)["result"]

# 创建文档Office文档
workbook = xlwt.Workbook(encoding='utf-8')
sheet = workbook.add_sheet("On Shift Ticket", cell_overwrite_ok = True)

# 设置样式
style = xlwt.XFStyle()

# 颜色参考 https://blog.csdn.net/weixin_44065501/article/details/88874643

# 字体
font = xlwt.Font()
font.name = u"Calibri (Body)"
font.height = 20 * 20
font.colour_index = 63
font.bold = True

# 边框
bolders = xlwt.Borders()
bolders.left = 1
bolders.top = 1
bolders.right = 1
bolders.bottom = 1
bolders.bottom_colour = 0x0
bolders.top_colour = 0x0
bolders.left_colour = 0x0
bolders.right_colour = 0x0

# 填充
fill = xlwt.Pattern()
fill.pattern = 0x01
fill.pattern_fore_colour = 1

style.font = font
style.borders = bolders
style.pattern = fill

# 遍历所有ticket信息写入excel
for index, incident in enumerate(IncidentsList):
    number = incident["number"]
    priority = CONSTANT_PRIORITY[int(incident["priority"])]
    state = CONSTANT_INCIDENT_STATE[int(incident["incident_state"])]
    name = ""
    userDict = incident["assigned_to"]
    if isinstance(incident["assigned_to"], dict):
        userURL = userDict["link"]
        usersInfoResponse = requests.get(userURL, headers = headers)
        userInfo = json.loads(usersInfoResponse.text)["result"]
        name = userInfo["name"]
    short_description = incident["short_description"]
    task_type = incident["sys_class_name"]
    # print(number + " " + priority + " " + state + " " + name + " " + short_description + " " + task_type + " Class " + incident_class + " " + created_on)
    sheet.write(index, 0, number, style)
    sheet.write(index, 1, priority, style)
    sheet.write(index, 2, state, style)
    sheet.write(index, 3, name, style)
    sheet.write(index, 4, short_description, style)
    sheet.write(index, 5, task_type, style)

# 设置列宽
sheet.col(0).set_width(240 * 20)
sheet.col(1).set_width(300 * 20)
sheet.col(2).set_width(350 * 20)
sheet.col(3).set_width(600 * 20)
sheet.col(4).set_width(2000 * 20)
sheet.col(5).set_width(200 * 20)
sheet.col(6).set_width(100 * 20)
sheet.col(7).set_width(450 * 20)

# 保存Excel
workbook.save(r"./OnShiftTickets.xls")