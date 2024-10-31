from docx import Document
from pdfminer.high_level import extract_text
# import chardet


# def read_common_file(filename):
#     """
#     读取普通文本文件
#     :param filename: 文件名
#     :return: 文件内容
#     """
#     # 读取二进制原始内容
#     file = open(filename, 'rb')
#     raw_content = file.read()
#     file.close()
#
#     # 获取原始内容长度，选择合适的子集大小
#     raw_content_len = len(raw_content)
#     if raw_content_len / 10 > 2048:
#         sub_content_len = 2048
#     else :
#         if raw_content_len < 2048:
#             sub_content_len = raw_content_len
#         else:
#             sub_content_len = raw_content_len / 10
#
#     result = chardet.detect(raw_content[0:sub_content_len])
#
#     try:
#         file = open(filename, 'r', encoding=result['encoding'])
#         content = file.read()
#     except UnicodeDecodeError:
#         file.close()
#         file = open(filename, 'r', encoding='utf-8')
#         content = file.read()
#
#     file.close()
#     return content


def read_docx(filename):
    """
    读取docx文件，返回文件内容
    :param filename: 文件名
    :return: 文件内容
    """
    doc = Document(filename)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return "\n".join(full_text)


def read_pdf(filename):
    """
    读取pdf文件中的文本内容
    :param filename: 文件名
    :return: 文本内容
    """
    pdf = extract_text(filename)
    return pdf

