from threading import Lock

import win32com
from docx import Document
from pdfminer.high_level import extract_text
from win32com.client import Dispatch


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


word = None
doc_read_lock = Lock()
def read_doc(file_path):
    """
    读取doc文件，依赖微软的word，通过Microsoft的Word来打开doc文件并且读取内容
    :param file_path:
    :return:
    """
    global word
    global doc_read_lock
    doc_read_lock.acquire()
    if word is None:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False

    doc = word.Documents.Open(file_path)
    content = doc.Content.Text
    doc.Close()
    doc_read_lock.release()
    return content
