import json
import time
import random

import requests
from bs4 import BeautifulSoup

# 目录映射
CatalogueType = {
    "1": "判断题",
    "2": "选择题",
    "3": "多选题",
}

CatalogueAnswer = {
    "1": "A",
    "2": "B",
    "3": "C",
    "4": "D",
    "5": "E",
    "6": "F",
    "7": "G",
}

CatalogueCar = {
    "a": "bus",
    "b": "truck",
    "c": "car",
    "e": "moto",
}

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://mnks.jxedt.com/",  # 添加 Referer
    "Accept": "application/json, text/javascript, */*; q=0.01",  # 确保接收 JSON
}

# 创建 Session 复用连接
session = requests.Session()


def get_data(CarType, Course):
    # 获取题目 ID 列表
    # url = 'https://mnks.jxedt.com/ckm4/sxlx/'
    print(f"正在获取 {CarType} {Course} 题目 ID 列表...")

    url = f'https://mnks.jxedt.com/{CarType}{Course}/sxlx/'

    id_response = session.get(url, headers=headers, timeout=10)

    id_list = []
    result = []

    if id_response.status_code == 200:
        soup = BeautifulSoup(id_response.text, 'html.parser')

        for li in soup.find_all('li'):
            question_id = li.get('data-id')
            if question_id:
                id_list.append(question_id)

        print(f"获取到 {len(id_list)} 道题目 ID")
    else:
        print(f"请求失败, 状态码: {id_response.status_code}")
        exit(-1)

    # 获取题目信息
    cnt = 1
    for question_id in id_list:
        url = f'https://mnks.jxedt.com/get_question?index={question_id}'

        try:
            response = session.get(url, headers=headers, timeout=10)

            # 检查响应状态码
            if response.status_code != 200:
                print(f'请求失败, 状态码: {response.status_code}, URL: {url}')
                continue

            # 检查 Content-Type 是否为 JSON
            content_type = response.headers.get('Content-Type', '').lower()
            if "text/html" in content_type:
                print(f"警告：服务器返回的是 HTML，不是 JSON。可能触发了反爬机制。\n内容: {response.text}")
                time.sleep(5)
                continue

            # 解析 JSON
            answer_data = response.json()

            question, optionType = answer_data.get('question'), answer_data.get('type')

            optionA, optionB, optionC, optionD = answer_data.get('a', ""), answer_data.get('b', ""), answer_data.get('c',
                                                                                                                     ""), answer_data.get(
                'd', "")

            img = answer_data.get('imageurl', "")

            answer = answer_data.get('right', "")

            # 多选题
            if optionType == '3':
                endAnswer = ""
                for ans in answer:
                    endAnswer += CatalogueAnswer[ans]
                explain = answer_data.get('bestanswer', "") + f"。因此答案选择 {endAnswer}"
            else:
                explain = answer_data.get('bestanswer', "") + f"。因此答案选择 {CatalogueAnswer.get(answer, '未知')}"


            content = {
                "问题描述": question,
                "问题类型": CatalogueType.get(optionType, "未知"),
                "描述图片": img,
                "选项A": optionA,
                "选项B": optionB,
                "选项C": optionC,
                "选项D": optionD,
                "答案详解": explain,
            }

            result.append(content)
            print(f'已获取 {cnt} 条数据: {content["问题描述"]}...')

            cnt += 1
            time.sleep(random.uniform(1, 2))

        except requests.exceptions.RequestException as e:
            print(f"请求 {url}, {CarType, Course} 失败: {e}")
            time.sleep(5)
            continue

    # 保存数据
    with open('jxedt' + f"{CatalogueCar[CarType]}{Course}Data" + '.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f'数据保存成功，共获取到 {len(result)} 条数据')

if __name__ == '__main__':
    # 客车
    # get_data('a', 'km1')
    get_data('a', 'km4')

    # 货车
    get_data('b', 'km1')
    get_data('b', 'km4')

    # 小车
    # get_data('c', 'km1')
    # get_data('c', 'km4')

    # 摩托车
    # get_data('e', 'km1')
    # get_data('e', 'km4')