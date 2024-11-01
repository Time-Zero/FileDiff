from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

def calculate_similarity(base_file, compare_file):
    """
    输入两个文件内容，返回这个两个文件的相似度
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
    :return: 返回文件差异内容
    """
    compare = difflib.HtmlDiff()
    res  = compare.make_file(base_file_content,compare_file_content)
    return res