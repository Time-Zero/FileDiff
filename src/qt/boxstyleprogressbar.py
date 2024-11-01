from PyQt5.QtWidgets import QProgressBar

class BoxStyleProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setRange(0, 100)
        self.setValue(0)
        self.setStyleSheet("""
                QProgressBar {
                    border: 2px solid white;
                    background-color: black;
                    padding-left: 2px;
                    padding-right: 2px;
                    text-align: center;
                }

                QProgressBar::chunk {
                    background-color: white;
                    margin-top: 2px;
                    margin-bottom: 2px;
                }
                """)