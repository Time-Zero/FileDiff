import os.path
from datasketch import MinHash, MinHashLSH
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

def calculate_similarity(base_file, compare_file):
    """
    输入两个文件，返回这个两个文件的相似度
    :param base_file: 基准文件
    :param compare_file: 要比较的文件
    :return: 两个文件的精准度
    """
    vectorizer = TfidfVectorizer().fit_transform([base_file, compare_file])
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return cosine_similarities * 100


def generate_diff_html_file(base_file_name, compare_file_name, base_file_content, compare_file_content):
    """
    生成两个输入文件的差异文件
    :param base_file_name: 基准文件名
    :param compare_file_name: 待比较文件名
    :param base_file_content: 基准文件内容
    :param compare_file_content: 待比较文件内容
    :return:
    """
    compare = difflib.HtmlDiff()
    res  = compare.make_file(base_file_content,compare_file_content)
    file_1_name = os.path.basename(base_file_name).split('.')[0]
    file_2_name = os.path.basename(compare_file_name).split('.')[0]
    out_file = 'compare_{}_{}.html'.format(file_1_name, file_2_name)
    with open(out_file, 'w') as f:
        f.write(res)


# def calculate_binary_similarity(base_file_content, compare_file_content):
#     seq_matcher = difflib.SequenceMatcher(None, base_file_content, compare_file_content)
#     similarity = seq_matcher.quick_ratio() * 100
#     return similarity