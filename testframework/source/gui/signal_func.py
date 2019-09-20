# -*- coding: utf-8 -*-
# 界面启动入口
import sys

import time
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QDateTime
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QMainWindow, QPushButton, QLineEdit, QLabel, QHBoxLayout, \
    QWidget, QVBoxLayout


class BackendThread(QObject):

    update_date = pyqtSignal(str)

    def run(self):
        while True:
            current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            self.update_date.emit(str(current_time))
            time.sleep(0.1)


class UIMainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(parent=None, *args, **kwargs)

        self.setWindowTitle('PyQt 5界面实时更新例子')
        self.resize(400, 100)
        self.main_layout = QHBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)

        # button
        self.button_1 = QPushButton('124')
        self.line_edit = QLineEdit()

        QMainWindow.setCentralWidget(self, self.widget)
        self.main_layout.addWidget(self.button_1)
        self.main_layout.addWidget(self.line_edit)

        # 初始化窗口
        self.init_ui()

    def init_ui(self):
        # 线程init
        self.backend_ = BackendThread()
        # 创建信号连接
        self.thread = QThread()
        self.backend_.update_date.connect(self.button_clear_event)
        self.backend_.moveToThread(self.thread)
        # 开始线程
        self.thread.started.connect(self.backend_.run)
        self.thread.start()

    def button_clear_event(self, data):
        self.line_edit.setText(data)


def main():
    app = QApplication(sys.argv)
    qt = UIMainWindow()
    qt.show()
    sys.exit(app.exec_())  # 循环执行窗口触发事件


if __name__ == '__main__':
    main()
