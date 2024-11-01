from threading import Lock, Thread
from PyQt5.QtWidgets import QFileDialog, QMessageBox, \
    QStackedWidget
from src.utils.util import *
from src.qt.boxstyleprogressbar import *
from src.qt.resultshowwindow import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget_2 = None
        self.widget_1 = None
        self.progress_bar = None
        self.stack_widget = None
        self.confirm_pushbutton = None  # 确认操作按钮
        self.select_file_dir_pushbutton = None      # 文件选择按钮
        self.file_path_lineedit = None  # 文件路径显示
        self.file_dir_path = None       # 要进行比对的文件夹路径
        self.compare_result = []      # 比对结果
        self.file_list = None           # 待处理文件列表
        self.task_count = 0             # 任务总数
        self.complete_task_count = 0    # 完成的任务数
        self.file_list_lock = Lock()
        self.compare_result_lock = Lock()
        self.result_show_window = ResultShowWindow(self)        # 结果显示窗口
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FileCompare')
        self.setFixedSize(400,300)

        self.setStyleSheet("QLineEdit {"
                           "background-color: #ffffff;"
                           "border: 1px solid #cccccc;"
                           "border-radius: 4px;"
                           "padding: 4px;"
                           "color: #333333;"
                           "font-size: 14px;"
                           "}"
                           ""
                           "QLineEdit:focus {"
                           "border: 1px solid #007bff;"
                           "background-color: #e9f5ff;"
                           "}"
                           ""
                           "QPushButton {"
                           "background-color: #007bff;"
                           "border: none;"
                           "border-radius: 4px;"
                           "color: #ffffff;"
                           "font-size: 14px;"
                           "padding: 10px 20px;"
                           "}"
                           ""
                           "QPushButton:hover {"
                           "background-color: #0056b3;"
                           "}"
                           ""
                           "QPushButton:pressed {"
                           "background-color: #003d80;"
                           "}")

        # 文件路径栏
        file_path_layout = QVBoxLayout()
        self.file_path_lineedit = QLineEdit()
        self.file_path_lineedit.setText('')
        file_path_layout.addWidget(self.file_path_lineedit)
        file_path_widget = QWidget()
        file_path_widget.setLayout(file_path_layout)

        # 按钮
        self.select_file_dir_pushbutton = QPushButton('选择文件夹')
        self.select_file_dir_pushbutton.clicked.connect(self.get_file_dir_path)
        self.confirm_pushbutton = QPushButton('确认')
        self.confirm_pushbutton.clicked.connect(self.process_file)
        file_func_layout = QHBoxLayout()
        file_func_layout.addWidget(self.select_file_dir_pushbutton)
        file_func_layout.addWidget(self.confirm_pushbutton)
        file_fun_widget = QWidget()
        file_fun_widget.setLayout(file_func_layout)

        # 把上面两个功能区加入main_windows_layout
        main_window_layout = QVBoxLayout()
        main_window_layout.addWidget(file_path_widget)
        main_window_layout.addWidget(file_fun_widget)

        # 创建stack_widget
        self.stack_widget = QStackedWidget()

        # 创建一个widget，把上面的layout放入这个widget
        self.widget_1 = QWidget()
        self.widget_1.setLayout(main_window_layout)
        self.stack_widget.addWidget(self.widget_1)

        # 创建一个新的widget，存放progressbar
        progress_bar_layout = QVBoxLayout()
        self.progress_bar = BoxStyleProgressBar()
        progress_bar_layout.addWidget(self.progress_bar)
        self.widget_2 = QWidget()
        self.widget_2.setLayout(progress_bar_layout)
        self.stack_widget.addWidget(self.widget_2)

        base_widget_layout = QVBoxLayout()
        base_widget_layout.addWidget(self.stack_widget)
        self.setLayout(base_widget_layout)
        self.stack_widget.setCurrentIndex(0)

    def get_file_dir_path(self):
        """
        选择目标文件夹
        :return:
        """
        file_dir_path = QFileDialog.getExistingDirectory(self)
        self.file_path_lineedit.setText(file_dir_path)
        self.file_dir_path = file_dir_path

        # 如果重新选择文件，则将其他部分重置状态
        self.complete_task_count = 0
        self.task_count = 0
        # 排除第一次使用时file_list还是None的情况
        if type(self.file_list) == list :
            self.file_list.clear()
        self.compare_result.clear()

    def compare_file(self):
        while True :
            self.file_list_lock.acquire_lock()

            # 如果文件列表被处理完成，则释放锁并且返回
            if len(self.file_list) == 0:
                self.file_list_lock.release()
                break

            base_file = self.file_list.pop()
            current_file_list = self.file_list.copy()
            self.file_list_lock.release()

            for compare_file in current_file_list:
                result = match_type_and_function(base_file, compare_file)
                self.compare_result_lock.acquire()
                self.complete_task_count += 1
                self.compare_result.append([base_file, compare_file, result])
                self.compare_result_lock.release()
                self.progress_bar.setValue(int((self.complete_task_count / self.task_count) * 100))

    def process_file(self):
        """
        确认按钮的槽函数
        :return:
        """
        if self.file_dir_path is None or len(self.file_dir_path) == 0:
            QMessageBox.critical(self,'Error','文件夹路径不能为空')
            return

        file_list = get_target_files(self.file_dir_path)
        for file in file_list:
            print(file)

        self.file_list = file_list
        file_list_len = len(self.file_list)
        if file_list_len == 0:
            QMessageBox.information(self,'提示','没有文件需要比对')
            return
        else:
            QMessageBox.information(self,'提示',f'共检测到文件{file_list_len}个，点击确认开始检查')
            # Thread(target=lambda : self.stack_widget.setCurrentIndex(1) ).start()
            self.stack_widget.setCurrentIndex(1)
            self.task_count = (file_list_len * (file_list_len - 1)) / 2
            all_task = []

            print("=====start=====")
            for i in range(8):
                thread = Thread(target=self.compare_file)
                thread.start()
                all_task.append(thread)

            for thread in all_task:
                thread.join()
            print("=====end=====")

            # 显示结果窗口
            self.compare_result.sort(key=lambda x: x[2],reverse=True)
            for result in self.compare_result:
                self.result_show_window.add_row(result[0],result[1],result[2])
            self.result_show_window.show()
            self.hide()