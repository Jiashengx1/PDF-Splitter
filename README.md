# PDF 分割与合并工具

这是一个使用 `pikepdf` 库编写的 PDF 分割与合并工具，支持根据指定的页数或文件大小对 PDF 文件进行分割，并且可以合并多个 PDF 文件为一个。工具通过命令行参数灵活配置，适用于需要将大文件拆分为多个较小文件，或将多个文件合并成一个文件的场景。

## 功能特性

1. **按页数分割**：根据指定的页数，将 PDF 文件分割成多个小文件，每个文件包含指定数量的页面。
2. **按文件大小分割**：根据指定的最大文件大小（以 MB 为单位），分割 PDF 文件。分割时确保每个文件的大小不超过指定的最大值，使用二分查找优化性能，减少不必要的临时文件生成。
3. **合并 PDF 文件**：将多个 PDF 文件合并为一个文件。用户可以指定输出文件名，如果未指定，则默认使用第一个 PDF 文件的名称加上 `_merge` 后缀。

## 安装依赖

确保你已经安装了 `pikepdf`，它是一个强大的 Python PDF 库。你可以通过以下命令安装：

```bash
pip install pikepdf
```

## 使用方法

### 基本命令

```bash
python pdf_splitter.py <输入PDF文件路径> [-m] [-s <最大文件大小(MB)> | -p <每个文件的页数>] [-o <输出目录>] [-f <合并输出文件名>]
```

### 参数说明

- `input_pdfs`：输入的 PDF 文件路径（分割时为一个文件，合并时为多个文件）。
- `-m`, `--merge`：启用合并模式，合并多个 PDF 文件为一个。
- `-s`, `--size`：按大小分割的最大文件大小（MB），支持小数。
- `-p`, `--pages`：按页数分割的每个文件的页数。
- `-o`, `--output`：输出目录，默认为输入 PDF 所在的目录。如果指定，文件将被保存到该目录。
- `-f`, `--filename`：合并输出的文件名。如果未指定，默认使用第一个输入文件的名称加上 `_merge` 后缀。

### 示例

#### 分割 PDF 文件

1. **按大小分割 PDF 文件**：每个文件最大为 20MB。

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

#### 合并 PDF 文件

1. **合并多个 PDF 文件**：合并 `file1.pdf`、`file2.pdf` 和 `file3.pdf`，并输出为 `merged_output.pdf`。

    ```bash
    python pdf_splitter.py file1.pdf file2.pdf file3.pdf -m -o output_directory -f merged_output.pdf
    ```

2. **合并多个 PDF 文件**：合并 `file1.pdf`、`file2.pdf` 和 `file3.pdf`，输出文件名为默认的 `file1_merge.pdf`。

    ```bash
    python pdf_splitter.py file1.pdf file2.pdf file3.pdf -m -o output_directory
    ```



# PDF Split and Merge Tool

This is a PDF splitting and merging tool written in Python using the `pikepdf` library. It supports splitting PDF files by specified page count or file size, and can also merge multiple PDF files into one. The tool is configurable via command-line arguments and is suitable for situations where you need to split large files into smaller ones or merge multiple files into one.

## Features

1. **Split by Page Count**: Splits a PDF file into multiple smaller files, each containing a specified number of pages.
2. **Split by File Size**: Splits a PDF file by the specified maximum file size (in MB), ensuring that each file does not exceed the specified size limit. Binary search is used to optimize performance and minimize unnecessary temporary file creation.
3. **Merge PDF Files**: Merges multiple PDF files into one. You can specify the output file name; if not specified, the output file name will default to the first input PDF file’s name with a `_merge` suffix.

## Install Dependencies

Make sure you have installed `pikepdf`, a powerful Python library for working with PDFs. You can install it using the following command:

```bash
pip install pikepdf
```

## Usage

### Basic Command

```bash
python pdf_splitter.py <input_pdf_file_paths> [-m] [-s <max_size_in_MB> | -p <pages_per_file>] [-o <output_directory>] [-f <merged_output_filename>]
```

### Arguments

- `input_pdfs`: Input PDF file paths (one file for splitting, multiple files for merging).
- `-m`, `--merge`: Enable merge mode to merge multiple PDF files into one.
- `-s`, `--size`: Maximum file size (in MB) for splitting by size. Supports decimal values.
- `-p`, `--pages`: Number of pages per split file when splitting by page count.
- `-o`, `--output`: Output directory. By default, the output will be saved in the directory of the input PDF file. If specified, the file will be saved to that directory.
- `-f`, `--filename`: The output filename for the merged PDF. If not specified, the output will default to the first input PDF's name with a `_merge` suffix.

### Examples

#### Split PDF File

1. **Split by Size**: Split a PDF into files no larger than 20 MB each.

    ```bash
    python pdf_splitter.py input.pdf -s 20 -o output_directory
    ```

2. **Split by Page Count**: Split a PDF so that each file contains 10 pages.

    ```bash
    python pdf_splitter.py input.pdf -p 10 -o output_directory
    ```

3. **Custom Output Directory**: Specify a custom output directory.

    ```bash
    python pdf_splitter.py input.pdf -s 10 -o custom_output_directory
    ```

#### Merge PDF Files

1. **Merge Multiple PDF Files**: Merge `file1.pdf`, `file2.pdf`, and `file3.pdf` into a single file called `merged_output.pdf`.

    ```bash
    python pdf_splitter.py file1.pdf file2.pdf file3.pdf -m -o output_directory -f merged_output.pdf
    ```

2. **Merge Multiple PDF Files**: Merge `file1.pdf`, `file2.pdf`, and `file3.pdf`, and the output file will be named `file1_merge.pdf` by default.

    ```bash
    python pdf_splitter.py file1.pdf file2.pdf file3.pdf -m -o output_directory
    ```
