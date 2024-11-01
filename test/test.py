# import ssdeep
#
#
# # 读取文件内容
# def read_file(file_path):
#     with open(file_path, 'rb') as file:
#         return file.read()
#
#
# # 计算文件的模糊哈希值
# def calculate_fuzzy_hash(file_path):
#     file_content = read_file(file_path)
#     return ssdeep.hash(file_content)
#
#
# # 比较两个模糊哈希值
# def compare_fuzzy_hashes(hash1, hash2):
#     return ssdeep.compare(hash1, hash2)
#
#
# if __name__ == '__main__':
#     # 文件路径
#     file1_path = 'E:\\Code\\Python\\FileDiff\\FileDiff\\test\\test_file\\doc\\file-sample_1MB.doc'
#     file2_path = 'E:\\Code\\Python\\FileDiff\\FileDiff\\test\\test_file\\doc\\file-sample_1MB - 副本.doc'
#
#     # 计算两个文件的模糊哈希值
#     hash1 = calculate_fuzzy_hash(file1_path)
#     hash2 = calculate_fuzzy_hash(file2_path)
#
#     # 比较两个文件的相似度
#     similarity = compare_fuzzy_hashes(hash1, hash2)
#
#     print(f"The similarity between the two files is: {similarity}")