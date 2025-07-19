import pdfplumber
import sys
import os

def extract_pdf_content(pdf_path):
    """
    提取PDF文件中的文本内容
    """
    if not os.path.exists(pdf_path):
        print(f"文件 {pdf_path} 不存在")
        return None
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"PDF文件信息:")
            print(f"- 总页数: {len(pdf.pages)}")
            print(f"- 文件路径: {pdf_path}")
            print("-" * 50)
            
            all_text = ""
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\n=== 第 {page_num} 页 ===")
                
                # 提取文本
                text = page.extract_text()
                if text:
                    print(text)
                    all_text += f"\n=== 第 {page_num} 页 ===\n"
                    all_text += text + "\n"
                else:
                    print("(此页无可提取的文本)")
                
                # 提取表格 (如果有)
                tables = page.extract_tables()
                if tables:
                    print(f"\n--- 表格 (共 {len(tables)} 个) ---")
                    for table_num, table in enumerate(tables, 1):
                        print(f"\n表格 {table_num}:")
                        for row in table:
                            if row:  # 跳过空行
                                print(" | ".join([str(cell) if cell else "" for cell in row]))
            
            # 保存提取的内容到文件
            output_file = "extracted_content.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(all_text)
            print(f"\n提取的内容已保存到: {output_file}")
            
            return all_text
            
    except Exception as e:
        print(f"提取PDF内容时出错: {e}")
        return None

def main():
    pdf_file = "Undergraduate_Admission_Statistics.pdf"
    
    # 检查是否安装了pdfplumber
    try:
        import pdfplumber
    except ImportError:
        print("需要安装 pdfplumber 库:")
        print("pip install pdfplumber")
        return
    
    print("开始提取PDF内容...")
    content = extract_pdf_content(pdf_file)
    
    if content:
        print(f"\n✅ 成功提取了 {len(content)} 个字符的内容")
    else:
        print("❌ 提取失败")

if __name__ == "__main__":
    main()
