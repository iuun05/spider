import random

import requests
import time
import pandas as pd
import fake_useragent


url = "http://jwc.swjtu.edu.cn/vatuu/ClassroomBorrowInfoAction?setAction=hadLendClassAjax"

# 星期数的编码
weekday = ['0000001', '0000010', '0000100', '0001000', '0010000', '0100000', '1000000']

# 2024周数的编码，这里是18周，19周
week = ['000000000100000000000000000', '000000001000000000000000000']
ua = fake_useragent.UserAgent()

# 把cookies换成自己的
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "120",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "",
    "Host": "jwc.swjtu.edu.cn",
    "Origin": "http://jwc.swjtu.edu.cn",
    "Pragma": "no-cache",
    "Referer": "http://jwc.swjtu.edu.cn/vatuu/ClassroomBorrowInfoAction?setAction=classroomLendList",
    "User-Agent": ua.random,
    "X-Requested-With": "XMLHttpRequest"
}

columns = ['考试周次', '考试星期', '考试节数', '类型', '考试科目', '课程代码', '课程教师', '考试地点']
result = []

print('开始爬取')
index = 0
for week in week:
    index = 0
    for weekday in weekday:

        setAction = {
            "QueryType": "testAndWhere",
            "school_area_code": "2",
            "term_id": "113",
            "IsLesson": "NO",
            "SelectWeek": str(week),
            "WeekDay": str(weekday)
        }
        '''
        borrowWeek:"18"
        borrowDay:"星期一"
        borrowLesson:"1-5节"
        borrowType:"考试"
        reasonMemo:"检测技术与故障诊断"
        reasonType:"ELEC009112"
        reasonUser:"陈健,刘东"
        roomName:"X9541"
        '''
        response = requests.post(url, headers=headers, data=setAction,verify=False)
        json = response.json()
        print(json)
        if 'items' in json:
            for data in json['items']:
                temp = [data['borrowWeek'], data['borrowDay'], data['borrowLesson'], data['borrowType'], data['reasonMemo'],
                        data['reasonType'], data['reasonUser'], data['roomName']]
                # temp = {'borrowWeek': data['borrowWeek'], 'borrowDay': data['borrowDay'],
                #         'borrowLesson': data['borrowLesson'], 'borrowType': data['borrowType'],
                #         'reasonMemo': data['reasonMemo'], 'reasonType': data['reasonType'],
                #         'reasonUser': data['reasonUser'], 'roomName': data['roomName']}

                print(temp)
                result.append(temp)
        else:
            print('items not exist')

        time.sleep(3+random.randint(1,5))

df = pd.DataFrame(result, columns=columns)
df.to_excel('swjtu.xlsx', index=False)