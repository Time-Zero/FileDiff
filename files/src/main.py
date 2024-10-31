import sys

from PyQt5.QtWidgets import QMainWindow

from qt.mainwindow import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())