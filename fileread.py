from docx import Document
from pdfminer.high_level import extract_text


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

def read_common_file(filename):
    """
    读取普通文本文件
    :param filename: 文件名
    :return: 文件内容
    """
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text