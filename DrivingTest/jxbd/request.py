import time

import requests
import json
import fake_useragent

# 目录
catalogue = {
    0: "判断题",
    1: "选择题",
    2: "多选题",
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
                  'YaBrowser/19.7.0.1635 Yowser/2.5 Safari/537.36',
}


def get_data(CarType, Course, kemuStyle):
    url = f"https://api2.jiakaobaodian.com/api/web/sync/question-last-status.htm?_r=17492846048929949110&authToken" \
          f"=f58ceb1bd864fba3f560ebb2d809fbb16bc15015&carStyle={CarType}&carType={CarType}&cityCode=510100&c" \
          f"ourse={Course}&kemuStyle={kemuStyle}&scene=101"

    req = requests.get(url, headers=headers)

    print(req.text)

    data = json.loads(req.text)

    ids = data['data']['allList']
    id_length = len(ids)

    result = []

    for i in range(0, id_length, 10):

        other_id = "%2C".join([f"{id}" for id in ids[i:i + 10]])

        # answers_url = f"https://jk-tiku.kakamobi.cn/api/web/practise/question-list.htm?_r=11936917007555568093&carType" \
        #               f"=car&course=kemu1&questionIds=" + other_id

        answers_url = f"https://jk-tiku.kakamobi.cn/api/web/practise/question-list.htm?_r=11959500185615553084&carType" \
                      f"={CarType}&course={Course}&questionIds=" + other_id

        answers_req = requests.get(answers_url)

        if answers_req.status_code != 200:
            print(CarType, Course, kemuStyle, "请求失败!!!!")
            return

        answers_data = json.loads(answers_req.text)


        for answer_data in answers_data['data']:
            question, optionType = answer_data['question'], answer_data['optionType']
            optionA, optionB, optionC, optionD = answer_data['optionA'], answer_data['optionB'], answer_data['optionC'], \
            answer_data['optionD']
            img = answer_data['mediaContent']
            explain = answer_data['explain']

            content = {
                "问题描述": question,
                "问题类型": catalogue[optionType],
                "描述图片": img,
                "选项A": optionA,
                "选项B": optionB,
                "选项C": optionC,
                "选项D": optionD,
                "答案详解": explain,
            }

            result.append(content)

        if i % 100 == 0 or i == id_length - 1:
            print(f"已获取{i} / {id_length}条数据")

        time.sleep(2)

    with open("jxbd" + CarType + kemuStyle + ".json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
        result.clear()

if __name__ == '__main__':
    # car
    get_data(CarType="car", Course="kemu1", kemuStyle="kemu1")
    get_data(CarType="car", Course="kemu3", kemuStyle="kemu4")

    # bus
    get_data(CarType="bus", Course="kemu1", kemuStyle="kemu1")
    get_data(CarType="bus", Course="kemu3", kemuStyle="kemu4")

    # truck
    get_data(CarType="truck", Course="kemu1", kemuStyle="kemu1")
    get_data(CarType="truck", Course="kemu3", kemuStyle="kemu4")

    # moto
    get_data(CarType="moto", Course="kemu1", kemuStyle="kemu1")
    get_data(CarType="moto", Course="kemu3", kemuStyle="kemu4")




