# maoistProject
### 作者
211250128 林峰  
211250129 韩博侨

### 数据
data/weibo中存储微博爬取源数据，以及chatgpt处理后的情绪数据。  
data/output中存储情绪统计生成的饼状图。

### 代码

#### emo.py
负责调用chatgpt api，处理微博源数据，并生成初始情绪数据

#### GPT_DOS.py和sele.py
分别是使用GPT_DOS和selenium访问chatgpt镜像的接口。

#### parse_csv.py
处理chatgpt初始情绪数据，过滤无效数据。

#### calculate_emotion.py
统计情绪分布，制成饼状图。