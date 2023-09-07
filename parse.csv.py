import re
import csv
import pandas as pd
def parse(str):
    strcpy = str
    # 去除所有空白符
    str = ''.join(str.split())

    # 尝试匹配 pattern1
    pattern1 = r"\([a-zA-Z]+,\d+\.\d+\)(,\([a-zA-Z]+,\d+\.\d+\))*"
    match1 = re.findall(pattern1, str)
    if match1:
        # 转换为 pattern1 格式
        result = ','.join([f"{x}" for x in re.findall(r"\([a-zA-Z]+,\d+\.\d+\)", str)])
        return result

    # 尝试匹配 pattern2
    pattern2 = r"\{[a-zA-Z]+,\d+\.\d+\}(,\{[a-zA-Z]+,\d+\.\d+\})*"
    match2 = re.findall(pattern2, str)
    if match2:
        # 转换为 pattern1 格式
        result = ','.join([f"({x[1:-1]})" for x in re.findall(r"\{[a-zA-Z]+,\d+\.\d+\}", str)])
        return result

    # 尝试匹配 pattern3
    pattern3 = r"\({[a-zA-Z]+},{\d+\.\d+\}\)(,\{[a-zA-Z]+},{\d+\.\d+\})*"
    match3 = re.findall(pattern3, str)
    if match3:
        # 转换为 pattern1 格式
        result = ','.join([f"({x[1:-1].replace('{', '').replace('}', '')})" for x in re.findall(r"\({[a-zA-Z]+},{\d+\.\d+\}\)", str)])
        return result

    pattern4 = r""

    # 所有匹配失败
    return ""

def parse_csv(old_csv_path, new_csv_path):
    with open(old_csv_path, "r", encoding="utf-8") as old_csv, open(new_csv_path, "w", encoding="utf-8",
                                                                    newline="") as new_csv:
        csv_reader = pd.read_csv(old_csv)
        csv_writer = csv.writer(new_csv)



        # 写入新csv文件的表头
        new_header = ["id", "微博正文", "发布时间", "情绪"]
        # csv_writer.writerow(new_header)

        # 遍历旧csv每一行，生成新csv的每一行
        i = 0
        success = 0

        csv_reader["情绪"] = csv_reader["情绪"].apply(parse)
        csv_reader.to_csv(new_csv_path)

        # for row in csv_reader["情绪"]:
        #     row = str(row)
        #     row = ''.join(row.split())
        #     print(str(i)+" "+ row)
        #
        #     parsed, flag = parse(row)
        #     print("     "+ parsed)
        #     if(flag == 1):
        #         success +=1
        #
        #
        #
        #
        #
        #     # 写入新csv文件的一行数据
        #     # new_row = [id_col, text_col, time_col, emotion_col]
        #
        #     # csv_writer.writerow(new_row)
        #
        #     i +=1
        # print(success)


if __name__ == '__main__':
    parse_csv("newData/weibo/就业/就业新.csv", "newData/weibo/就业/就业新1.csv")
