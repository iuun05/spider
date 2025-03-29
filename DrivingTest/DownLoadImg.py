import os
import time
import threading
import requests
import json

# 共享变量和锁
cnt = 1
PrintLock = threading.Lock()
CntLock = threading.Lock()


def read_json_files_in_directory(dir_path, type):
    global cnt

    if not os.path.exists(dir_path):
        with PrintLock:
            print(f"Directory '{dir_path}' does not exist.")
        return

    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)

        if filename.endswith('.json') and type in filename:
            with PrintLock:
                print(f'reading {filepath}')

            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            for data in json_data:
                img_url = data.get('描述图片', None)

                if img_url:
                    with PrintLock:
                        print(f'request {img_url} \t\t', end='')

                    req = requests.get(img_url)

                    if req.status_code == 200:
                        file_extension = os.path.splitext(img_url)[-1]
                        with PrintLock:
                            print(f'success')

                        with CntLock:
                            ImageName = f'./images/image-{cnt}' + file_extension
                            cnt += 1

                        # 保存图片
                        with open(ImageName, 'wb') as img_file:
                            img_file.write(req.content)

                        data['描述图片'] = ImageName

                        time.sleep(1)

                    else:
                        with PrintLock:
                            print(f'failed !!!')

                        with open('failed.txt', 'a', encoding='utf-8') as failed:
                            failed.write(f"{filename}-{img_url}\n")

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

        else:
            with PrintLock:
                print(f"{filename} is not a json file or type is wrong.")

    with PrintLock:
        print(f'cnt: {cnt}')


if __name__ == '__main__':
    threads = []
    start = time.time()

    # List of paths and types to process
    paths = [
        (r'D:\mywork\Crawlers\DrivingTest\jxbd', 'car'),
        (r'D:\mywork\Crawlers\DrivingTest\jxbd', 'moto'),
        (r'D:\mywork\Crawlers\DrivingTest\jxbd', 'truck'),
        (r'D:\mywork\Crawlers\DrivingTest\jxbd', 'bus'),

        (r'D:\mywork\Crawlers\DrivingTest\jxedt', 'car'),
        (r'D:\mywork\Crawlers\DrivingTest\jxedt', 'moto'),
        (r'D:\mywork\Crawlers\DrivingTest\jxedt', 'truck'),
        (r'D:\mywork\Crawlers\DrivingTest\jxedt', 'bus'),
    ]

    # Creating and starting threads for each path and type
    for path, type_ in paths:  # Unpack the tuple here
        thread = threading.Thread(target=read_json_files_in_directory, args=(path, type_))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    stop = time.time()
    print(f'Cost time: {stop - start}')
    print('End')
