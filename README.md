# FileDiff——一个文档对比工具
## 简介
本项目为合肥工业大学领域综合设计课程设计，旨在设计一个可以实现对doc文档进行对比并输出相似度的带有GUI的程序

在此基础上，本项目基于TD-IDF算法实现了对doc、docx、pdf进行对比，并且输出相似度的功能，并且使用Qt设计了一个较为简单的操作页面

## 详细描述
1. 在文档对比方面，使用多线程，实现了同时多文件的对比，但是由于Python的GIL的存在，所以效率并不是很高
2. 使用PyQt设计的GUI页面，简化了用户操作
3. 基于Microsoft Document的doc文件读取功能，**_所以需要借助Office中的Word工具，使用前请先确认你是否有Office_**

## 如何运行
1. 在conda或者其他虚拟环境中运行`pip install -r requirements.txt`安装依赖
2. 运行`/src/main.py`
推荐使用Pycharm打开项目，防止出现路径问题
