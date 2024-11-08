import sys

from PyQt5.QtWidgets import QApplication

from qt.mainwindow import *

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(myapp.exec_())