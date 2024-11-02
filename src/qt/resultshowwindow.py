from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QHeaderView


class ResultShowWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.html_show_base_widget = None
        self.html_func_widget = None
        self.html_func_layout = None
        self.html_save_place_lineedit = None
        self.html_save_confirm_button = None
        self.html_save_place_select_button = None
        self.html_show_layout = None
        self.html_show_widget = None
        self.result_show_window_layout = None
        self.result_table_base_widget = None
        self.result_table_layout = None
        self.result_table_widget = None
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('文档对比结果')
        self.initUI()
        self.hide()

    def initUI(self):
        # 用于显示结果的table
        self.result_table_widget = QTableWidget(self)         # filename1, filename2, similarities
        self.result_table_widget.setColumnCount(3)
        self.result_table_widget.setHorizontalHeaderLabels(['文件1', '文件2', '相似度%'])       # 设置表头
        self.result_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.result_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        # 示例数据
        # self.add_row('file1.doc','file2.doc',30)

        # 用户包含显示结果table的layout
        self.result_table_layout = QVBoxLayout()
        # 把显示结果的table插入layout
        self.result_table_layout.addWidget(self.result_table_widget)
        # 声明一个base_widget用于存放显示结果的layout
        self.result_table_base_widget = QWidget()
        # 设置这个base_widget的layout为显示结果的layout
        self.result_table_base_widget.setLayout(self.result_table_layout)

        self.result_show_window_layout = QHBoxLayout()
        self.result_show_window_layout.addWidget(self.result_table_base_widget)
        # self.result_show_window_layout.addWidget(self.html_show_base_widget)
        self.setLayout(self.result_show_window_layout)

    def add_row(self,file_name_1, file_name_2, similarities):
        # 获取行数
        row_count = self.result_table_widget.rowCount()
        #插入一行
        self.result_table_widget.insertRow(row_count)

        # 设置新插入行的每列数据
        self.result_table_widget.setItem(row_count, 0, QTableWidgetItem(file_name_1))
        self.result_table_widget.setItem(row_count, 1, QTableWidgetItem(file_name_2))
        self.result_table_widget.setItem(row_count, 2, QTableWidgetItem(format(similarities,'.2f')))

