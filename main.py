from filediff import *
from fileread import *

if __name__ == '__main__':
    # base_file = read_docx("files/docx/file_1.docx")
    # compare_file = read_docx("files/docx/file_2.docx")
    base_file = read_pdf("./files/pdf/file_1.pdf")
    compare_file = read_pdf("./files/pdf/file_3.pdf")
    similarities = calculate_similarity(base_file,compare_file)
    print(similarities)