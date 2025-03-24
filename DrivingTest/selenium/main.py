import json
import time
from selenium.common.exceptions import NoSuchElementException
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.jiakaobaodian.com/mnks/kemu1/car-chengdu.html"
kemu1_url = "https://www.jiakaobaodian.com/mnks/exercise/6-car-kemu1-chengdu.html?id=800500"
kemu4_url = "https://www.jiakaobaodian.com/mnks/exercise/6-car-kemu4-chengdu.html?id=881600"

driver = webdriver.Edge()

# 读取cookie
driver.get(url=url)
time.sleep(2)
driver.delete_all_cookies()
print("cookie删除成功")
with open("cookie_jx.json", "r", encoding='utf-8') as f:
    listCookies = json.loads(f.read())

for cookie in listCookies:
    # print(cookie)
    driver.add_cookie(cookie)

print("cookie加载成功")

# 重新访问
driver.get(url=url)
time.sleep(2)


# 结果
def get_data(url, FileName):
    kemuData = []
    with open(FileName, "w", encoding='utf-8') as f:
        print(f"开始爬取科目一，url为{kemu1_url}")
        driver.get(url=url)
        time.sleep(10)

        # 关闭初始对话框
        wait = WebDriverWait(driver, 10)
        dialog = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'com-appdown-dialog')))
        close_button = dialog.find_element(By.CLASS_NAME, 'btn-dialog-close')
        close_button.click()
        time.sleep(2)

        # 点击答案详解
        Answers_button = driver.find_element(by=By.CSS_SELECTOR, value="[ref=xiangqing]")
        Answers_button.click()
        time.sleep(2)
        print("点击答案详解")

        pre_url = ""
        cur_url = driver.current_url
        cnt = 0

        while pre_url != cur_url:
            # 获取题目类型
            ProblemType = driver.find_element(by=By.CLASS_NAME, value="option-type-msg").text.split("，")[0]

            # 获取题目
            Problem = driver.find_element(by=By.CLASS_NAME, value="timu-text").text

            # 获取选项
            Choices = driver.find_elements(by=By.CSS_SELECTOR, value="[ref=answerclick]")
            choice = []
            for c in Choices:
                choice.append(c.text)

            # 获取图片
            try:
                image_element = driver.find_element(by=By.CSS_SELECTOR, value="img[ref='bigImg']")
                if image_element.is_displayed():
                    # 元素存在且可见
                    image_url = image_element.get_attribute('src')
                    # 进行下载操作
                else:
                    # 元素存在但不可见
                    image_element = None
                    image_url = ""
            except NoSuchElementException:
                # 元素不存在
                image_element = None
                image_url = ""

            # 获取答案详解
            ProblemLevel = driver.find_element(by=By.CLASS_NAME, value="bfb").get_attribute('style')
            Answers = driver.find_element(by=By.CLASS_NAME, value="xiangjie").find_element(by=By.CLASS_NAME,
                                                                                           value="content").text

            OneOfData = {
                "题目类型": ProblemType,
                "问题描述": Problem,
                "图片": image_url,
                "选项": choice,
                "答案": Answers,
                "难度": ProblemLevel[-4:-1]
            }
            # 添加到结果
            kemuData.append(OneOfData)
            print(OneOfData)

            # 更新当前url
            pre_url = cur_url
            cur_url = driver.current_url
            cnt += 1

            # 写入文件
            if cnt % 100 == 0:
                print(cnt)
                json.dump(kemuData, f, indent=4, ensure_ascii=False)
                kemuData.clear()

            # 点击下一题
            next = driver.find_element(by=By.CSS_SELECTOR, value="[ref=next]")
            next.click()
            time.sleep(3)

        json.dump(kemuData, f, indent=4, ensure_ascii=False)


get_data(kemu1_url, "kemu1.json")

get_data(kemu4_url, "kemu4.json")

print("爬取完成")
driver.quit()
