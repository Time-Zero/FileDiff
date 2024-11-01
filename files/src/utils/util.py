import os

from files.src.file_process.filediff import calculate_similarity
from files.src.file_process.fileread import *

def get_target_files(dirpath):
    """
    获取指定文件夹中的所有的doc,docx,pdf文件路径
    :param dirpath: 文件夹路径
    :return: list：包含所有目标格式的文件的路径
    """

    file_list = []
    target_type = {'.docx','.doc','.pdf'}

    for home, dirs, files in os.walk(dirpath):
        for filename in files:
            file_base_name, file_type = os.path.splitext(filename)
            if file_type in target_type:
                file_list.append(os.path.join(home, filename))
    return file_list

def match_type_and_function(base_file, compare_file):
    """
    得出文件类型，选择对应的读取函数，并且返回匹配结果
    :param base_file: 基准文件
    :param compare_file: 待比较文件
    :return: {base_file, compare_file, similarities}
    """

    file_base_name, file_type = os.path.splitext(base_file)
    base_file_type = file_type
    if base_file_type == '.docx':
        base_file_content = read_docx(base_file)
    else:
        base_file_content = read_pdf(base_file)

    file_base_name, file_type = os.path.splitext(compare_file)
    compare_file_type = file_type
    if compare_file_type == '.docx':
        compare_file_content = read_docx(compare_file)
    else:
        compare_file_content = read_pdf(compare_file)

    similarities = calculate_similarity(base_file_content, compare_file_content)
    return similarities

