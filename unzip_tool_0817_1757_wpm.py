# 代码生成时间: 2025-08-17 17:57:23
import zipfile
def unzip_file(file_path, output_path):
    """
    解压zip文件到指定路径。
    :param file_path: 压缩文件的路径。
    :param output_path: 解压后文件的存放路径。
    :return: 解压是否成功。
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
            return True
    except Exception as e:
        # 日志记录错误信息
        print(f"An error occurred: {e}")
        return False

# 示例用法
if __name__ == '__main__':
    file_path = '/path/to/your/zip/file.zip'
    output_path = '/path/to/your/output/directory'
    if unzip_file(file_path, output_path):
        print("File has been successfully unzipped.")
    else:
        print("Failed to unzip the file.")