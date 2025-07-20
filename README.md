# 广东省2025年本科普通类（物理）投档情况排行榜

## 排序规则
按照最差的专业组来排名，不算中外合办、医学部、浙大农学之类的比较特殊的专业组

## 仓库结构
- `Undergraduate_Admission_Statistics.pdf`: 下载自官网的原始PDF文件
- `program.py`: 提取数据的脚本
- `extracted_content.txt`: 从PDF中提取的文本内容
- `sort_universities.py`: 排序大学投档数据的脚本
- `sorted_universities.md`: 排序后的文件
- `排序版（至深大）.md`: 截断至深大的排行榜

## 使用方法
~~~zsh
# 提取文本内容
python program.py

# 排序
python sort_universities.py
~~~