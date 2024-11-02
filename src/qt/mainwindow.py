from threading import Thread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox, \
    QStackedWidget
from src.utils.util import *
from src.qt.boxstyleprogressbar import *
from src.qt.resultshowwindow import *
from src.file_process.fileread import *

file_list = []              # 待处理的文件列表
result_list = []
file_list_lock = Lock()     # 多线程锁,防止文件列表这里不同步
result_list_lock = Lock()
all_task_count = 0          # 总共要处理的任务列表 (n * (n-1)) / 2 个
complete_task_count = 0

class MainWindow(QWidget):
    process_end_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widget_2 = None
        self.widget_1 = None
        self.progress_bar = None
        self.stack_widget = None
        self.confirm_pushbutton = None                   # 确认操作按钮
        self.select_file_dir_pushbutton = None           # 文件选择按钮
        self.file_path_lineedit = None                  # 文件路径显示
        self.result_show_window = ResultShowWindow()        # 结果显示窗口
        self.init_ui()
        self.process_end_signal.connect(self.show_result)

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
        self.select_file_dir_pushbutton.clicked.connect(self.select_file_dir_pushbutton_slot)
        self.confirm_pushbutton = QPushButton('确认')
        self.confirm_pushbutton.clicked.connect(self.confirm_pushbutton_slot)
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


    def select_file_dir_pushbutton_slot(self):
        """
        文件夹选择按钮槽函数
        :return:
        """

        dir_path = QFileDialog.getExistingDirectory()
        self.file_path_lineedit.setText(dir_path)



    def confirm_pushbutton_slot(self):
        """
        confirm_pushbutton的槽函数
        :return:
        """
        dir_path = self.file_path_lineedit.text()
        # 如果路径为空
        if len(dir_path) == 0:
            QMessageBox.critical(self, 'Error', '文件夹路径不能为空')
            return

        # 获取待处理文件列表
        global file_list
        file_list = get_target_files(dir_path)

        # 如果待处理文件数量是0
        file_list_len = len(file_list)
        if file_list_len == 0:
            QMessageBox.information(self,'提示','没有检测到目标文件')
            return

        QMessageBox.information(self,'提示',f'检测到{file_list_len}个文件，点击确认开始比对')
        global all_task_count
        all_task_count = (file_list_len * (file_list_len - 1)) / 2

        # 切换到进度条页面
        self.stack_widget.setCurrentIndex(1)

        # 起多个线程,并且采用分离线程
        for i in range(6):
            thread = Thread(target = self.process_action)
            thread.daemon = True
            thread.start()

    def process_action(self):
        """
        多线程中的任务
        :return:
        """
        global file_list_lock
        global complete_task_count
        global result_list_lock
        global result_list
        global file_list_lock

        while True:
            file_list_lock.acquire()

            # 如果所有文件已经处理完成
            if len(file_list) == 0:
                file_list_lock.release()
                break

            file_1 = file_list.pop()
            compare_files = file_list.copy()
            file_list_lock.release()

            for file_2 in compare_files:
                result = match_type_and_function(file_1, file_2)
                result_list_lock.acquire()
                result_list.append([file_1, file_2, result])
                complete_task_count += 1
                self.progress_bar.setValue(int(complete_task_count / all_task_count * 100))
                result_list_lock.release()

        # 最后一个处理完成并退出的线程先把数据排一下序，然后发送任务完成信号
        if complete_task_count == all_task_count:
            result_list.sort(key= lambda x : x[2], reverse=True)
            self.process_end_signal.emit()

    def show_result(self):
        # 显示结果窗口
        global result_list
        for result in result_list:
            self.result_show_window.add_row(result[0], result[1], result[2])
        self.result_show_window.show()
        self.hide()