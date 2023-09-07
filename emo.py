# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
#
# chat_model = ChatOpenAI(openai_api_key="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")
#
# print(chat_model.predict("hi!"))

import os
from langchain.vectorstores import Milvus
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from  sele import  Sele
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
import time

os.environ["OPENAI_API_KEY"] = "None"
os.environ["OPENAI_API_BASE"] = "http://172.29.7.155:8000/v1"

llm = ChatOpenAI(temperature=0.7, model_name="CodeLlama-34b-")
sele = Sele()
# llm = ChatOpenAI(temperature=0.7, openai_api_key="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")


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

    return llm.predict(question)

import re

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


def emo(old_csv_path, new_csv_path):
    import csv

    # 打开旧csv文件和新csv文件
    with open(old_csv_path, "r", encoding="utf-8") as old_csv, open(new_csv_path, "w", encoding="utf-8",
                                                                    newline="") as new_csv:
        csv_reader = csv.reader(old_csv)
        csv_writer = csv.writer(new_csv)

        # 写入新csv文件的表头
        new_header = ["id", "微博正文", "发布时间", "情绪"]
        csv_writer.writerow(new_header)

        # 遍历旧csv每一行，生成新csv的每一行
        for row in csv_reader:
            id_col = row[0]
            text_col = row[4]
            time_col = row[12]

            temp = text_col
            if len(text_col) > 1500:
                temp = text_col[0:1500]
            # 调用getEmo函数获取情绪
            emotion_col = getEmo(temp)
            emotion_col = parse(emotion_col)

            # 写入新csv文件的一行数据
            new_row = [id_col, text_col, time_col, emotion_col]
            print(new_row)
            csv_writer.writerow(new_row)

    print("新csv文件生成完成。")


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
                emotion_col = sele.getEmoFromSele(temp)
                emotion_col = parse(emotion_col)
            except Exception as e:
                print("error")





            # 写入新csv文件的一行数据
            new_row = [id_col, text_col, time_col, emotion_col]
            print(i, new_row)
            i+=1
            csv_writer.writerow(new_row)


            # 延时，控制循环频率
            time.sleep(loop_delay)

        print("新csv文件生成完成。")


def emo_with_sele(old_csv_path, new_csv_path):
    import csv
    # 打开旧csv文件和新csv文件
    with open(old_csv_path, "r", encoding="utf-8") as old_csv, open(new_csv_path, "w", encoding="utf-8",
                                                                    newline="") as new_csv:
        csv_reader = csv.reader(old_csv)
        csv_writer = csv.writer(new_csv)

        # 写入新csv文件的表头
        new_header = ["id", "微博正文", "发布时间", "情绪"]
        csv_writer.writerow(new_header)

        # 遍历旧csv每一行，生成新csv的每一行
        for row in csv_reader:
            id_col = row[0]
            text_col = row[4]
            time_col = row[12]

            temp = text_col
            if len(text_col) > 1500:
                temp = text_col[:1500]

            # 调用getEmo函数获取情绪
            emotion_col = temp
            try:
                emotion_col = sele.getEmoFromSele(temp)
                emotion_col = parse(emotion_col)
            except Exception as e:
                print("error")






            # 写入新csv文件的一行数据
            new_row = [id_col, text_col, time_col, emotion_col]
            print(new_row)
            csv_writer.writerow(new_row)

        print("新csv文件生成完成。")



def sampling(input_csv_path, output_csv_path):
    import pandas as pd
    import random

    # 读取原始CSV文件
    data = pd.read_csv(input_csv_path, encoding="utf-8")

    # 获取发布时间的年份
    data["发布时间"] = pd.to_datetime(data["发布时间"])
    data["年份"] = data["发布时间"].dt.year

    # 初始化一个空的DataFrame用于存放抽样数据
    sampled_data = pd.DataFrame(columns=data.columns)

    # 每年抽样200条数据
    for year in range(2015, 2024):
        year_data = data[data["年份"] == year]
        if len(year_data) > 200:
            sampled_data = sampled_data._append(year_data.sample(n=200, random_state=42))
        else:
            sampled_data = sampled_data._append(year_data)

    # 重置索引
    sampled_data.reset_index(drop=True, inplace=True)

    # 生成新的CSV文件
    sampled_data.to_csv(output_csv_path, index=False, encoding="utf-8")

    print("抽样数据生成完成。")


def main():
    # sampling("newData/weibo/企业/企业.csv", "newData/weibo/企业/抽样数据.csv")
    # sampling("newData/weibo/民企/民企.csv", "newData/weibo/民企/抽样数据.csv")
    # sampling("data/weibo/企业/企业.csv", "data/weibo/企业/抽样数据.csv")
    # sampling("data/weibo/失业/失业.csv", "data/weibo/失业/抽样数据.csv")
    # sampling("data/weibo/资本/资本.csv", "data/weibo/资本/抽样数据.csv")




    # emo_with_sele("newData/weibo/民企/抽样数据.csv", "newData/weibo/民企/民企新.csv")
    # emo("data/weibo/民企/抽样数据.csv", "data/weibo/民企/民企新.csv")
    # emo("data/weibo/企业/抽样数据.csv", "data/weibo/企业/企业新.csv")
    # emo("data/weibo/失业/抽样数据.csv", "data/weibo/失业/失业新.csv")
    emo_with_filter("newData/weibo/失业/失业新 - 副本.csv", "newData/weibo/失业/失业新新 - 副本.csv")
    # print(getEmo("说调整状态可能不太会像之前一样住在微博里，最近一直在忙着生活，换一种平静的方式去爱他，想    变成更好的人，想要为他做点什么的时候能有一定的资本，喜欢他不能只是靠在网络上嚷嚷的那几句话，以后有空闲时间会帮忙做些能做的事，rest也确实是从赛时加入打投起就生活作息乱七八糟，需要去花点时间平衡生活与追星，也需要去调整自己身体的状态，会努力变得更好，一直在陪他前行"))


if __name__ == '__main__':
    main()
    # print(llm.predict("who are you?"))






