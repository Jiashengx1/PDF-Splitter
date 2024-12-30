import os
import argparse
import pikepdf
from io import BytesIO

def get_output_file_name(input_pdf_path, output_dir, suffix):
    """
    生成输出文件的完整路径，格式为 baseName_suffix.pdf
    """
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    return os.path.join(output_dir, f"{base_name}_part_{suffix}.pdf")

def split_pdf_by_pages(input_pdf_path, output_dir, pages_per_split):
    """
    按页数分割PDF，每个输出文件包含指定数量的页面
    """
    with pikepdf.Pdf.open(input_pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        for i in range(0, total_pages, pages_per_split):
            new_pdf = pikepdf.Pdf.new()
            for j in range(i, min(i + pages_per_split, total_pages)):
                new_pdf.pages.append(pdf.pages[j])
            
            output_pdf_path = get_output_file_name(input_pdf_path, output_dir, f"{i // pages_per_split + 1}")
            new_pdf.save(output_pdf_path)
            
            file_size = os.path.getsize(output_pdf_path) / (1024 * 1024)  # 转换为MB
            print(f"生成文件: {output_pdf_path} (大小: {file_size:.2f} MB)")

def split_pdf_by_size(input_pdf_path, output_dir, max_size_mb):
    """
    按文件大小分割PDF，确保每个输出文件大小不超过指定的最大值
    使用二分查找优化性能
    """
    with pikepdf.Pdf.open(input_pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        split_count = 1
        current_page = 0

        while current_page < total_pages:
            low = current_page + 1
            high = total_pages
            best = current_page + 1  # 至少包含一页

            while low <= high:
                mid = (low + high) // 2
                temp_pdf = pikepdf.Pdf.new()
                for page_num in range(current_page, mid):
                    temp_pdf.pages.append(pdf.pages[page_num])
                
                # 使用 BytesIO 作为内存中的临时文件
                temp_buffer = BytesIO()
                temp_pdf.save(temp_buffer)
                current_size = temp_buffer.tell() / (1024 * 1024)  # 转换为MB
                
                if current_size <= max_size_mb:
                    best = mid
                    low = mid + 1
                else:
                    high = mid - 1
            
            # 处理找到的最佳页面范围
            temp_pdf = pikepdf.Pdf.new()
            for page_num in range(current_page, best):
                temp_pdf.pages.append(pdf.pages[page_num])
            
            # 保存最终的分割文件
            output_pdf_path = get_output_file_name(input_pdf_path, output_dir, f"{split_count}")
            temp_pdf.save(output_pdf_path)
            
            file_size = os.path.getsize(output_pdf_path) / (1024 * 1024)  # 转换为MB
            print(f"生成文件: {output_pdf_path} (大小: {file_size:.2f} MB)")
            
            split_count += 1
            current_page = best

def merge_pdfs(input_pdf_paths, output_dir, output_file_name=None):
    """
    合并多个PDF文件为一个
    """
    if not input_pdf_paths:
        print("没有提供要合并的PDF文件。")
        return

    merged_pdf = pikepdf.Pdf.new()

    for pdf_path in input_pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"文件不存在: {pdf_path}")
            return
        with pikepdf.Pdf.open(pdf_path) as pdf:
            merged_pdf.pages.extend(pdf.pages)
    
    if not output_file_name:
        first_base = os.path.splitext(os.path.basename(input_pdf_paths[0]))[0]
        output_file_name = f"{first_base}_merge.pdf"
    
    output_path = os.path.join(output_dir, output_file_name)
    merged_pdf.save(output_path)
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # 转换为MB
    print(f"合并后的文件: {output_path} (大小: {file_size:.2f} MB)")

def main():
    parser = argparse.ArgumentParser(description="PDF分割与合并工具")
    parser.add_argument("input_pdfs", nargs='+', help="输入的PDF文件路径。单个文件用于分割，多个文件用于合并。")
    parser.add_argument("-m", "--merge", action="store_true", help="合并多个PDF文件")
    parser.add_argument("-s", "--size", type=float, help="按大小分割的最大文件大小 (MB)，支持小数")
    parser.add_argument("-p", "--pages", type=int, help="按页数分割的每个文件的页数")
    parser.add_argument("-o", "--output", help="输出目录，默认与输入PDF相同", default=None)
    parser.add_argument("-f", "--filename", help="合并后的输出文件名，仅在合并时使用", default=None)
    
    args = parser.parse_args()
    
    if args.merge:
        # 合并操作
        if len(args.input_pdfs) < 2:
            print("合并操作需要至少两个PDF文件。")
            return
        
        # 如果没有指定输出目录，默认输出到第一个输入PDF文件的目录
        if args.output is None:
            args.output = os.path.dirname(args.input_pdfs[0])
        
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        
        merge_pdfs(args.input_pdfs, args.output, args.filename)
    else:
        # 分割操作
        if len(args.input_pdfs) != 1:
            print("分割操作需要一个输入PDF文件。")
            return
        
        input_pdf = args.input_pdfs[0]
        
        if not os.path.exists(input_pdf):
            print("输入的PDF文件不存在!")
            return
        
        # 如果没有指定输出目录，默认输出到输入PDF文件的目录
        if args.output is None:
            args.output = os.path.dirname(input_pdf)
        
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        
        if args.size:
            split_pdf_by_size(input_pdf, args.output, args.size)
        elif args.pages:
            split_pdf_by_pages(input_pdf, args.output, args.pages)
        else:
            print("请提供分割方式：按页数(-p)或按大小(-s)。")

if __name__ == "__main__":
    main()
