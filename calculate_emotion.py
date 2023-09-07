import pandas as pd

def calculate_emotion(input_path, output_path, year=""):
    emotion_dict = {}
    df = pd.read_csv(input_path)


    if year != "":
        df = df[df['发布时间'].str.startswith(str(year))]
        print(df)

    cnt = 0
    for s in df["情绪"]:
        s = str(s)
        if s!="nan":
            cnt+=1
            list = s.replace("(","").replace(")","").split(",")
            # print(list)

            i = 0
            while i<len(list):
                key = list[i]
                val = list[i+1]
                i+=2

                if key in emotion_dict:
                    emotion_dict[key] = float(emotion_dict[key]) + float(val)
                else:
                    emotion_dict[key] = val

    sorted_dict = dict(sorted(emotion_dict.items(), key=lambda item: float(item[1]), reverse=True))
    print(sorted_dict)

    ans = 0.0
    values = sorted_dict.values()
    for value in values:
        ans += float(value)
    print(ans)

    percentage_dict = {}


    for key, value in sorted_dict.items():
        value = float(value)/ans
        percentage_dict[key] = value
        print("{}, {:.2%}".format(key,value))

    print(percentage_dict)

    import pygal

    # 创建饼状图实例
    pie_chart = pygal.Pie()

    # 添加数据
    for item, percentage in percentage_dict.items():
        pie_chart.add(item, percentage)

    # 渲染到SVG文件
    pie_chart.render_to_file(output_path)


if __name__ == '__main__':  
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/总.svg')
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2015.svg', 2015)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2016.svg', 2016)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2017.svg', 2017)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2018.svg', 2018)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2019.svg',2019)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2020.svg',2020)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2021.svg',2021)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2022.svg',2022)
    calculate_emotion("data/weibo/民企/民企新1.csv",'data/output/民企/2023.svg',2023)

