import re
from collections import defaultdict

def parse_extracted_content(file_path):
    """
    解析提取的PDF内容，返回结构化数据
    """
    universities = defaultdict(list)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 匹配数据行的正则表达式
    # 格式：院校代码 院校名称 专业组代码 计划数 投档人数 投档最低分 投档最低排位
    # 例如：10001 北京大学 206 34 35 689 99
    pattern = r'^(\d{5})\s+(.+?)\s+(\d{3})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 跳过页面标题和表头
        if ('广东省2025年本科普通类' in line or 
            '院校代码' in line or 
            '====' in line or
            '页' in line or
            '表格' in line or
            line.startswith('---')):
            continue
        
        match = re.match(pattern, line)
        if match:
            code, name, group_code, plan_num, admit_num, min_score, min_rank = match.groups()
            
            # 清理院校名称，去除可能的特殊字符
            name = name.strip()
            # 去除院校名称末尾可能的特殊字符（如院、试、考、育、教、省、东、广等）
            name = re.sub(r'[院试考育教省东广]$', '', name).strip()
            
            if not name:
                continue
                
            try:
                universities[name].append({
                    'code': code,
                    'group_code': group_code,
                    'plan_num': int(plan_num),
                    'admit_num': int(admit_num),
                    'min_score': int(min_score),
                    'min_rank': int(min_rank)
                })
            except ValueError:
                continue
    
    return universities

def sort_universities(universities):
    """
    按照要求排序大学和专业组
    """
    # 计算每个大学的最低投档最低分
    university_min_scores = {}
    for name, groups in universities.items():
        min_score = min(group['min_score'] for group in groups)
        university_min_scores[name] = min_score
    
    # 按照大学的最低投档最低分从高到低排序
    sorted_universities = sorted(university_min_scores.items(), 
                               key=lambda x: x[1], reverse=True)
    
    # 对每个大学内部的专业组按投档最低分从高到低排序
    result = []
    for name, _ in sorted_universities:
        groups = sorted(universities[name], 
                       key=lambda x: x['min_score'], reverse=True)
        result.append((name, groups))
    
    return result

def generate_markdown_table(sorted_data):
    """
    生成Markdown表格
    """
    # 表头
    markdown = "# 广东省2025年本科普通类（物理）投档情况排序表\n\n"
    markdown += "按照各大学最低投档分排序（从高到低），同一大学内部按专业组投档分排序\n\n"
    markdown += "| 院校名称 | 专业组代码 | 计划数 | 投档人数 | 投档最低分 | 投档最低排位 |\n"
    markdown += "|----------|------------|--------|----------|------------|-------------|\n"
    
    # 数据行
    for university_name, groups in sorted_data:
        for i, group in enumerate(groups):
            # 第一行显示大学名称，后续行留空以避免重复
            name_display = university_name if i == 0 else ""
            
            markdown += f"| {name_display} | {group['group_code']} | {group['plan_num']} | {group['admit_num']} | {group['min_score']} | {group['min_rank']} |\n"
    
    return markdown

def main():
    print("开始处理录取数据...")
    
    # 解析数据
    universities = parse_extracted_content('extracted_content.txt')
    print(f"共解析到 {len(universities)} 所大学的数据")
    
    if len(universities) == 0:
        print("未能解析到任何数据，请检查数据格式")
        return
    
    # 排序
    sorted_data = sort_universities(universities)
    
    # 生成Markdown表格
    markdown_content = generate_markdown_table(sorted_data)
    
    # 保存到文件
    with open('sorted_universities.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("排序完成！结果已保存到 sorted_universities.md")
    
    # 显示前10所大学作为预览
    print("\n=== 前10所大学预览 ===")
    count = 0
    for university_name, groups in sorted_data:
        if count >= 10:
            break
        min_score = min(group['min_score'] for group in groups)
        print(f"\n{count+1}. {university_name} (最低分: {min_score})")
        for group in groups:
            print(f"   专业组{group['group_code']}: {group['min_score']}分 (排位{group['min_rank']})")
        count += 1

if __name__ == "__main__":
    main() 