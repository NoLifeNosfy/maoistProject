# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import time
import re


def getRequest(str):
    url = "https://api.gptdos.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-gptqbwrb5aXElymMConiW9LtiM0GLQRIJ9ZYFPjSLv71i0Hf"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": str
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # print("请求成功")
        # print("返回数据:")
        strs = response.text.split('data:')
        ans = ''
        for str in strs:
            str = str.replace('\r', '').replace('\n', '').replace(' ', '')
            if str != "data:" and str != "[DONE]" and str != '':
                # print(str)
                json_data = json.loads(str)
                # print(json_data['choices'])
                json_choices = json_data['choices'][0]
                if (json_choices['finish_reason'] is None):
                    ans += (json_choices['delta']['content'])

        return ans
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

def getEmo(str):
    question = """Given a raw Chinese text input, Judge the emotions contained in this text. Your output should follow the following format: "({1}, {2}), ({3}, {4})..."
    {1} represent for the first emotion. {2} represent for the weight value of emotion1.
    {3} represent for the second emotion. {4} represent for the weight value of emotion2.
    and then other emotions.
Don't output any other words.

here's 2 examples:
example 1
<<input>>:
你好，我今天很开心。
<<output>>:
(happiness, 0.6), (glad, 0.3), (welcome, 0.1)

example 2
<<input>>:
对生活感到很失望，感觉前途很迷茫。
<<output>>:
(disappointed, 0.5), (confused, 0.3), (sad, 0.1)



now judge the emotions of the following input. Output the emotions according to the example output format. Don't output extra information. Don't output reasoning. Don't output introduction. Don't output such words like "the emotions are".
<<input>>:
""" + str + "\n<<<output>>>:\n"

    return getRequest(question)

def parse(str):
    strcpy = str
    # 去除所有空白符
    str = ''.join(str.split())

    # 尝试匹配 pattern1
    pattern1 = r"\([a-zA-Z]+,\d+\.\d+\)(,\([a-zA-Z]+,\d+\.\d+\))*"
    match1 = re.match(pattern1, str)
    if match1:
        # 转换为 pattern1 格式
        result = ','.join([f"({x})" for x in re.findall(r"\([a-zA-Z]+,\d+\.\d+\)", str)])
        return result

    # 尝试匹配 pattern2
    pattern2 = r"\{[a-zA-Z]+,\d+\.\d+\}(,\{[a-zA-Z]+,\d+\.\d+\})*"
    match2 = re.match(pattern2, str)
    if match2:
        # 转换为 pattern1 格式
        result = ','.join([f"({x[1:-1]})" for x in re.findall(r"\{[a-zA-Z]+,\d+\.\d+\}", str)])
        return result

    # 尝试匹配 pattern3
    pattern3 = r"\({[a-zA-Z]+},{\d+\.\d+\}\)(,\{[a-zA-Z]+},{\d+\.\d+\})*"
    match3 = re.match(pattern3, str)
    if match3:
        # 转换为 pattern1 格式
        result = ','.join([f"({x[1:-1].replace('{', '').replace('}', '')})" for x in re.findall(r"\({[a-zA-Z]+},{\d+\.\d+\}\)", str)])
        return result

    # 所有匹配失败
    return strcpy

def emo_with_filter(old_csv_path, new_csv_path):
    import csv
    # 打开旧csv文件和新csv文件
    with open(old_csv_path, "r", encoding="utf-8") as old_csv, open(new_csv_path, "w", encoding="utf-8",
                                                                    newline="") as new_csv:
        csv_reader = csv.reader(old_csv)
        csv_writer = csv.writer(new_csv)

        # 写入新csv文件的表头
        new_header = ["id", "微博正文", "发布时间", "情绪"]
        csv_writer.writerow(new_header)

        # 设置循环频率
        loop_frequency = 3  # 一分钟执行3次
        loop_delay = 60 / loop_frequency  # 每次循环的延时时间

        i=1
        # 遍历旧csv每一行，生成新csv的每一行
        for row in csv_reader:
            id_col = row[0]
            text_col = row[1]
            time_col = row[2]
            emo_col = row[3]

            pattern1 = r"\(\([a-zA-Z]+,\d+\.\d+\)\)(,\(\([a-zA-Z]+,\d+\.\d+\)\))*"
            match1 = re.match(pattern1, emo_col)
            if match1:
                new_row = [id_col, text_col, time_col, emo_col]
                print(i, "nothing to update")
                i+=1
                csv_writer.writerow(new_row)
                continue

            temp = text_col
            if len(text_col) > 1500:
                temp = text_col[:1500]

                # 调用getEmo函数获取情绪
            emotion_col = temp
            try:
                emotion_col = getEmo(temp)
                emotion_col = parse(emotion_col)
            except Exception as e:
                print("error")





            # 写入新csv文件的一行数据
            new_row = [id_col, text_col, time_col, emotion_col]
            print(i, new_row)
            i+=1
            csv_writer.writerow(new_row)


            # 延时，控制循环频率
            # time.sleep(loop_delay)

        print("新csv文件生成完成。")





# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    emo_with_filter("newData/weibo/失业/失业新 - 副本.csv", "newData/weibo/失业/失业新新 - 副本.csv")
