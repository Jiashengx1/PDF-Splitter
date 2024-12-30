import os
import pikepdf
from io import BytesIO
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def get_output_file_name(input_pdf_path, output_dir, suffix):
    """
    生成输出文件的完整路径，格式为 baseName_suffix.pdf
    """
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    return os.path.join(output_dir, f"{base_name}_part_{suffix}.pdf")

def split_pdf_by_pages(input_pdf_path, output_dir, pages_per_split, progress_callback=None):
    """
    按页数分割PDF，每个输出文件包含指定数量的页面
    """
    try:
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
                
                if progress_callback:
                    progress_callback((i + pages_per_split) / total_pages * 100)
        return True, "PDF 分割成功。"
    except Exception as e:
        return False, f"分割失败: {str(e)}"

def split_pdf_by_size(input_pdf_path, output_dir, max_size_mb, progress_callback=None):
    """
    按文件大小分割PDF，确保每个输出文件大小不超过指定的最大值
    使用二分查找优化性能
    """
    try:
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
                
                if progress_callback:
                    progress_callback(best / total_pages * 100)
                
                split_count += 1
                current_page = best
        return True, "PDF 分割成功。"
    except Exception as e:
        return False, f"分割失败: {str(e)}"

def merge_pdfs(input_pdf_paths, output_dir, output_file_name=None, progress_callback=None):
    """
    合并多个PDF文件为一个
    """
    try:
        if not input_pdf_paths:
            return False, "没有提供要合并的PDF文件。"

        merged_pdf = pikepdf.Pdf.new()

        total_files = len(input_pdf_paths)
        for idx, pdf_path in enumerate(input_pdf_paths):
            if not os.path.exists(pdf_path):
                return False, f"文件不存在: {pdf_path}"
            with pikepdf.Pdf.open(pdf_path) as pdf:
                merged_pdf.pages.extend(pdf.pages)
            
            if progress_callback:
                progress_callback((idx + 1) / total_files * 100)

        if not output_file_name:
            first_base = os.path.splitext(os.path.basename(input_pdf_paths[0]))[0]
            output_file_name = f"{first_base}_merge.pdf"
        
        output_path = os.path.join(output_dir, output_file_name)
        merged_pdf.save(output_path)
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # 转换为MB
        print(f"合并后的文件: {output_path} (大小: {file_size:.2f} MB)")
        
        return True, f"PDF 合并成功。输出文件: {output_path} (大小: {file_size:.2f} MB)"
    except Exception as e:
        return False, f"合并失败: {str(e)}"

class PDFToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 分割与合并工具")
        self.root.geometry("600x600")
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        # 分割标签
        self.split_tab = ttk.Frame(tab_control)
        tab_control.add(self.split_tab, text='分割 PDF')

        # 合并标签
        self.merge_tab = ttk.Frame(tab_control)
        tab_control.add(self.merge_tab, text='合并 PDF')

        tab_control.pack(expand=1, fill="both")

        self.create_split_tab()
        self.create_merge_tab()

    def create_split_tab(self):
        # 输入PDF文件选择
        input_frame = ttk.LabelFrame(self.split_tab, text="输入PDF文件")
        input_frame.pack(fill="x", padx=10, pady=10)

        self.split_input_path = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.split_input_path, width=50)
        input_entry.pack(side="left", padx=5, pady=5)

        browse_button = ttk.Button(input_frame, text="浏览", command=self.browse_split_input)
        browse_button.pack(side="left", padx=5, pady=5)

        # 分割方式选择
        method_frame = ttk.LabelFrame(self.split_tab, text="分割方式")
        method_frame.pack(fill="x", padx=10, pady=10)

        self.split_method = tk.StringVar(value="pages")
        pages_radio = ttk.Radiobutton(method_frame, text="按页数分割", variable=self.split_method, value="pages", command=self.toggle_split_options)
        pages_radio.pack(anchor="w", padx=5, pady=2)

        size_radio = ttk.Radiobutton(method_frame, text="按文件大小分割", variable=self.split_method, value="size", command=self.toggle_split_options)
        size_radio.pack(anchor="w", padx=5, pady=2)

        # 分割参数
        self.split_options_frame = ttk.Frame(self.split_tab)
        self.split_options_frame.pack(fill="x", padx=10, pady=10)

        # 按页数分割选项
        self.pages_label = ttk.Label(self.split_options_frame, text="每个文件的页数:")
        self.pages_entry = ttk.Entry(self.split_options_frame)

        # 按大小分割选项
        self.size_label = ttk.Label(self.split_options_frame, text="最大文件大小 (MB):")
        self.size_entry = ttk.Entry(self.split_options_frame)

        self.toggle_split_options()

        # 输出目录选择
        output_frame = ttk.LabelFrame(self.split_tab, text="输出目录")
        output_frame.pack(fill="x", padx=10, pady=10)

        self.split_output_dir = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.split_output_dir, width=50)
        output_entry.pack(side="left", padx=5, pady=5)

        browse_output_button = ttk.Button(output_frame, text="浏览", command=self.browse_split_output)
        browse_output_button.pack(side="left", padx=5, pady=5)

        # 分割按钮
        split_button = ttk.Button(self.split_tab, text="开始分割", command=self.start_split)
        split_button.pack(pady=10)

        # 进度条
        self.split_progress = ttk.Progressbar(self.split_tab, orient='horizontal', mode='determinate', length=580)
        self.split_progress.pack(padx=10, pady=10)

        # 状态信息
        self.split_status = tk.StringVar()
        split_status_label = ttk.Label(self.split_tab, textvariable=self.split_status, foreground="blue")
        split_status_label.pack(padx=10, pady=5)

    def create_merge_tab(self):
        # 输入PDF文件选择
        input_frame = ttk.LabelFrame(self.merge_tab, text="输入PDF文件")
        input_frame.pack(fill="both", padx=10, pady=10, expand=True)

        self.merge_input_paths = tk.Variable(value=[])
        self.merge_listbox = tk.Listbox(input_frame, listvariable=self.merge_input_paths, selectmode='multiple', width=50, height=10)
        self.merge_listbox.pack(side="left", padx=5, pady=5, expand=True, fill="both")

        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=self.merge_listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.merge_listbox.config(yscrollcommand=scrollbar.set)

        add_button = ttk.Button(input_frame, text="添加文件", command=self.add_merge_files)
        add_button.pack(side="left", padx=5, pady=5)

        remove_button = ttk.Button(input_frame, text="移除选中", command=self.remove_merge_files)
        remove_button.pack(side="left", padx=5, pady=5)

        # 输出文件名
        filename_frame = ttk.LabelFrame(self.merge_tab, text="输出文件名 (可选)")
        filename_frame.pack(fill="x", padx=10, pady=10)

        self.merge_output_filename = tk.StringVar()
        filename_entry = ttk.Entry(filename_frame, textvariable=self.merge_output_filename, width=50)
        filename_entry.pack(side="left", padx=5, pady=5)

        # 输出目录选择
        output_frame = ttk.LabelFrame(self.merge_tab, text="输出目录")
        output_frame.pack(fill="x", padx=10, pady=10)

        self.merge_output_dir = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.merge_output_dir, width=50)
        output_entry.pack(side="left", padx=5, pady=5)

        browse_output_button = ttk.Button(output_frame, text="浏览", command=self.browse_merge_output)
        browse_output_button.pack(side="left", padx=5, pady=5)

        # 合并按钮
        merge_button = ttk.Button(self.merge_tab, text="开始合并", command=self.start_merge)
        merge_button.pack(pady=10)

        # 进度条
        self.merge_progress = ttk.Progressbar(self.merge_tab, orient='horizontal', mode='determinate', length=580)
        self.merge_progress.pack(padx=10, pady=10)

        # 状态信息
        self.merge_status = tk.StringVar()
        merge_status_label = ttk.Label(self.merge_tab, textvariable=self.merge_status, foreground="blue")
        merge_status_label.pack(padx=10, pady=5)

    def browse_split_input(self):
        file_path = filedialog.askopenfilename(title="选择PDF文件", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.split_input_path.set(file_path)

    def browse_split_output(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.split_output_dir.set(directory)

    def browse_merge_output(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.merge_output_dir.set(directory)

    def add_merge_files(self):
        files = filedialog.askopenfilenames(title="选择PDF文件", filetypes=[("PDF Files", "*.pdf")])
        current_files = list(self.merge_listbox.get(0, tk.END))
        for file in files:
            if file not in current_files:
                self.merge_listbox.insert(tk.END, file)

    def remove_merge_files(self):
        selected_indices = self.merge_listbox.curselection()
        for index in reversed(selected_indices):
            self.merge_listbox.delete(index)

    def toggle_split_options(self):
        for widget in self.split_options_frame.winfo_children():
            widget.pack_forget()

        if self.split_method.get() == "pages":
            self.pages_label.pack(anchor="w", padx=5, pady=2)
            self.pages_entry.pack(anchor="w", padx=5, pady=2)
        else:
            self.size_label.pack(anchor="w", padx=5, pady=2)
            self.size_entry.pack(anchor="w", padx=5, pady=2)

    def start_split(self):
        input_pdf = self.split_input_path.get()
        output_dir = self.split_output_dir.get()

        if not input_pdf:
            messagebox.showwarning("输入文件缺失", "请选择要分割的PDF文件。")
            return
        if not os.path.exists(input_pdf):
            messagebox.showerror("文件不存在", "选择的PDF文件不存在。")
            return
        if not output_dir:
            messagebox.showwarning("输出目录缺失", "请选择输出目录。")
            return
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        method = self.split_method.get()
        if method == "pages":
            try:
                pages = int(self.pages_entry.get())
                if pages <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("无效输入", "每个文件的页数必须是一个正整数。")
                return
            split_func = split_pdf_by_pages
            split_args = (input_pdf, output_dir, pages)
        else:
            try:
                size = float(self.size_entry.get())
                if size <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("无效输入", "最大文件大小必须是一个正数。")
                return
            split_func = split_pdf_by_size
            split_args = (input_pdf, output_dir, size)

        # 重置进度条和状态
        self.split_progress['value'] = 0
        self.split_status.set("正在分割...")

        # 执行分割
        success, message = split_func(*split_args, progress_callback=self.update_split_progress)
        if success:
            self.split_status.set(message)
            messagebox.showinfo("成功", message)
            self.reset_split_fields()
        else:
            self.split_status.set(message)
            messagebox.showerror("失败", message)

    def update_split_progress(self, percent):
        self.split_progress['value'] = percent
        self.root.update_idletasks()

    def reset_split_fields(self):
        """
        重置分割标签页的输入字段和进度条
        """
        # 清除输入PDF路径
        self.split_input_path.set("")
        # 清除分割参数
        if self.split_method.get() == "pages":
            self.pages_entry.delete(0, tk.END)
        else:
            self.size_entry.delete(0, tk.END)
        # 重置进度条
        self.split_progress['value'] = 0
        # 清除状态信息
        self.split_status.set("")

    def start_merge(self):
        input_pdfs = list(self.merge_listbox.get(0, tk.END))
        output_dir = self.merge_output_dir.get()
        output_file_name = self.merge_output_filename.get()

        if not input_pdfs:
            messagebox.showwarning("输入文件缺失", "请添加要合并的PDF文件。")
            return
        if not output_dir:
            messagebox.showwarning("输出目录缺失", "请选择输出目录。")
            return
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        merge_func = merge_pdfs
        merge_args = (input_pdfs, output_dir, output_file_name if output_file_name else None)

        # 重置进度条和状态
        self.merge_progress['value'] = 0
        self.merge_status.set("正在合并...")

        # 执行合并
        success, message = merge_func(*merge_args, progress_callback=self.update_merge_progress)
        if success:
            self.merge_status.set(message)
            messagebox.showinfo("成功", message)
            self.reset_merge_fields()
        else:
            self.merge_status.set(message)
            messagebox.showerror("失败", message)

    def update_merge_progress(self, percent):
        self.merge_progress['value'] = percent
        self.root.update_idletasks()

    def reset_merge_fields(self):
        """
        重置合并标签页的输入字段和进度条
        """
        # 清除输出文件名
        self.merge_output_filename.set("")
        # 重置进度条
        self.merge_progress['value'] = 0
        # 清除状态信息
        self.merge_status.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolGUI(root)
    root.mainloop()
