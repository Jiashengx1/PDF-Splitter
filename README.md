# PDF 分割工具

这是一个使用 `pikepdf` 库编写的 PDF 分割工具，支持根据指定的页数或文件大小对 PDF 文件进行分割。工具通过命令行参数灵活配置，适用于需要将大文件拆分为多个较小文件的场景。

## 功能特性

1. **按页数分割**：根据指定的页数，将 PDF 文件分割成多个小文件，每个文件包含指定数量的页面。
2. **按文件大小分割**：根据指定的最大文件大小（以 MB 为单位），分割 PDF 文件。分割时确保每个文件的大小不超过指定的最大值，使用二分查找优化性能，减少不必要的临时文件生成。

## 安装依赖

确保你已经安装了 `pikepdf`，它是一个强大的 Python PDF 库。你可以通过以下命令安装：

```bash
pip install pikepdf
```

## 使用方法

### 基本命令

```bash
python pdf_splitter.py <输入PDF文件路径> [-s <最大文件大小(MB)> | -p <每个文件的页数>] [-o <输出目录>]
```

### 参数说明

- `input_pdf`：输入的 PDF 文件路径。
- `-s`, `--size`：按大小分割的最大文件大小（MB），支持小数。
- `-p`, `--pages`：按页数分割的每个文件的页数。
- `-o`, `--output`：输出目录，默认为输入 PDF 所在的目录。如果指定，文件将被保存到该目录。

### 示例

1. **按大小分割 PDF 文件**：每个文件大小最大为 20MB。

    ```bash
    python pdf_splitter.py input.pdf -s 20 -o output_directory
    ```

2. **按页数分割 PDF 文件**：每个文件包含 10 页。

    ```bash
    python pdf_splitter.py input.pdf -p 10 -o output_directory
    ```

3. **自定义输出目录**：

    ```bash
    python pdf_splitter.py input.pdf -s 10 -o custom_output_directory
    ```

# PDF Splitter Tool

This is a PDF splitter tool written using the `pikepdf` library, which supports splitting PDF files based on specified page numbers or file sizes. The tool is configured via command-line arguments, making it flexible and suitable for scenarios where large files need to be split into multiple smaller files.

## Features

1. **Split by Page Count**: Split the PDF file into multiple smaller files based on a specified number of pages per file.
2. **Split by File Size**: Split the PDF file based on a maximum file size (in MB). The tool ensures that each output file does not exceed the specified size. It uses binary search to optimize performance and reduce unnecessary temporary file generation.

## Dependencies

Make sure you have `pikepdf` installed, which is a powerful Python PDF library. You can install it using the following command:

```bash
pip install pikepdf
```

## Usage

### Basic Command

```bash
python pdf_splitter.py <input_pdf_path> [-s <max_file_size(MB)> | -p <pages_per_file>] [-o <output_directory>]
```

### Parameter Descriptions

- `input_pdf`: The path to the input PDF file.
- `-s`, `--size`: The maximum file size (in MB) for splitting, supports decimal values.
- `-p`, `--pages`: The number of pages per file when splitting by page count.
- `-o`, `--output`: The output directory. If not specified, the output files will be saved in the same directory as the input PDF.

### Examples

1. **Split PDF by File Size**: Split the file into chunks with a maximum size of 20MB each.

    ```bash
    python pdf_splitter.py input.pdf -s 20 -o output_directory
    ```

2. **Split PDF by Page Count**: Split the file into chunks, each containing 10 pages.

    ```bash
    python pdf_splitter.py input.pdf -p 10 -o output_directory
    ```

3. **Custom Output Directory**:

    ```bash
    python pdf_splitter.py input.pdf -s 10 -o custom_output_directory
    ```