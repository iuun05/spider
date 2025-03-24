import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

dirver = webdriver.Edge()
dirver.get("https://www.jiakaobaodian.com/mnks/kemu1/car-chengdu.html")
time.sleep(60)
dictCookies = dirver.get_cookies()  # 获得所有cookie信息(返回是字典)
print(dictCookies)
print(type(dictCookies))
jsonCookies = json.dumps(dictCookies)  # dumps是将dict转化成str格式
print(jsonCookies)
print(type(jsonCookies))
# 登录完成后,将cookies保存到本地文件
with open("cookie_jx.json", "w") as fp:
    fp.write(jsonCookies)