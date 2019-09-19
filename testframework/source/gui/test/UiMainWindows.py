# -*- coding: utf-8 -*-
import datetime
import sys
import os
from multiprocessing import Pool, Manager
import threading
import time
from imp import reload
import gc
from importlib import import_module

import multiprocessing
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QDir, QSize
from PyQt5.QtWidgets import QFrame, QPushButton, QLineEdit, QSpacerItem, QSizePolicy, QTabWidget, QTableWidget, \
    QToolButton, QDialogButtonBox, QAction, QFileDialog, QComboBox, QAbstractItemView
from PyQt5.QtGui import QIcon, QBrush, QColor, QIntValidator, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget, QGridLayout, QMessageBox, QMenu, qApp, \
    QTreeWidgetItem, QVBoxLayout, QTreeWidget, QHBoxLayout, QLabel

from TestCaseManager import TestCaseManager
from source.configs.readini import ConfigIni
from source.construct_project.get_project_path import PathExistProject
from source.gui.qss.qss_tools import QssTools
from source.gui.thread_func import ReturnCodeThread
from source.run_testcase.start_project import StartProject
from source.utils.file_operation import FileOperation
from source.utils.logclass.logconfig import Logger

current_path = os.path.dirname(__file__)
images_path = os.path.join(os.path.dirname(current_path), 'ico/')
qss_path = os.path.join(os.path.dirname(current_path), 'qss/')
ico_path = images_path + 'title.png'
style_path = qss_path + 'style.qss'
images_dir = os.path.join(os.path.dirname(current_path), 'images/')

source_log_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class UiMainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(parent=None, *args, **kwargs)

        self.log = source_log_object
        self.config_ini = ConfigIni(log_obj=self.log)

        self.ico_path = ico_path
        self.style_path = style_path
        self.current_project = None
        self.current_project_name = ''

        self.verify_case_list = []
        self.run_case_list = []

        # select project widget
        self.select_project_widget = QWidget(self)
        # 设置横向布局
        # 1, 横向布局里面添加 子 widget， 第一个子widget 里面包含一个button，图标加号， 导入新项目
        # 2，点击button， 出发点击事件 添加子widget， 包含{1，左上图标， 文件名， 2, 项目简述，3, 路径:C:/user/}

        # add case widget
        self.add_case_widget = QWidget(self)
        self.case_name = QLabel('脚本名称: ')
        self.case_name_edit = QLineEdit()
        self.case_name_edit.setPlaceholderText('请输入脚本名称')
        self.case_description = QLabel('脚本描述: ')
        self.case_description_edit = QLineEdit()
        self.case_description_edit.setPlaceholderText('请输入脚本描述信息')
        self.case_author = QLabel('编写作者: ')
        self.case_author_edit = QLineEdit()
        self.case_author_edit.setPlaceholderText('请输入脚本作者')
        self.max_running_time = QLabel('运行时间: ')
        self.max_running_time_edit = QLineEdit()
        self.max_running_time_edit.setPlaceholderText('请输入脚本最大运行时间')
        self.max_running_time_edit.setValidator(QIntValidator())
        self.case_modules = QLabel('所属模块: ')
        # self.case_modules_edit = QLineEdit()
        self.case_modules_edit = QComboBox()
        self.case_modules_edit.addItem('滤镜包')
        self.case_modules_edit.addItem('主流程')
        self.case_modules_edit.addItem('单模块')

        self.case_date = QLabel('创建日期: ')
        self.current_time = time.localtime(time.time())
        self.case_date_edit = QLabel(time.strftime('%Y-%m-%d-%H-%M-%S', self.current_time))
        self.screenshots_button = QtWidgets.QRadioButton(self.add_case_widget)  # centralwidget
        self.screenshots_button.setText('开启出错截图')
        self.create_and_cancel_button = QtWidgets.QDialogButtonBox(self.add_case_widget)
        self.create_and_cancel_button.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.create_and_cancel_button.button(QtWidgets.QDialogButtonBox.Ok).setText("创建")
        self.create_and_cancel_button.button(QtWidgets.QDialogButtonBox.Cancel).setText("取消")
        self.create_and_cancel_button.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.create_add_case_event)
        self.create_and_cancel_button.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel_create_add_case_event)

        # select_path widget
        self.select_path_widget = QWidget(self)
        self.project_path_ = QLabel('项目路径: ')
        self.project_path_edit = QLineEdit()
        self.project_path_edit.setPlaceholderText('请选择 SHELL EXE 路径')
        self.project_path_edit.setReadOnly(True)
        self.project_path_button = QPushButton('更改')
        self.project_path_button.clicked.connect(self.set_exe_path_event)
        self.case_log_path_ = QLabel('日志文件存放路径: ')
        self.case_log_path_edit = QLineEdit()
        self.case_log_path_edit.setReadOnly(True)
        self.case_log_path_button = QPushButton('更改')
        self.select_case_data_read_path_ = QLabel('选择数据读取路径: ')
        self.select_case_data_read_path_edit = QLineEdit()
        self.select_case_data_read_path_edit.setReadOnly(True)
        self.select_case_data_read_path_button = QPushButton('更改')
        self.test_version_images_path_ = QLabel('测试版本出图路径: ')
        self.test_version_images_path_edit = QLineEdit()
        self.test_version_images_path_edit.setReadOnly(True)
        self.test_version_images_path_button = QPushButton('更改')
        self.save_images_path_ = QLabel('标志图片存放路径: ')
        self.save_images_path_edit = QLineEdit()
        self.save_images_path_edit.setReadOnly(True)
        self.save_images_path_button = QPushButton('更改')
        self.finish_button = QPushButton('完成')
        self.finish_button.clicked.connect(self.verify_and_save_path_line_edit_event)

        # open project button ,add project, delete project, switch project
        self.open_project_button = QToolButton(self)
        self.open_project_button.setMaximumWidth(50)
        self.open_project_button.setMinimumHeight(50)
        self.open_project_button.setIconSize(QSize(40, 40))
        self.open_project_button.setIcon(QIcon(images_dir + 'setup.png'))
        self.open_project_button.setObjectName('open_project_button')

        self.add_project_button = QToolButton(self)
        self.add_project_button.setMinimumWidth(298)
        self.add_project_button.setMinimumHeight(108)
        self.add_project_button.setIconSize(QSize(188, 108))
        self.add_project_button.setIcon(QIcon(images_dir + 'add.png'))
        self.add_project_button.setObjectName('add_project_button')
        self.add_project_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.add_project_button.setText('导入新项目')
        self.add_project_button_hidden_bool = True
        self.open_project_button.clicked.connect(self.open_project_button_event)
        self.add_project_button.clicked.connect(self.add_project_button_event)

        self._case_manage = QLabel('用例管理')
        self._case_manage.setObjectName('case_manage')

        # spacer item
        self.spacer_item = QSpacerItem(400, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Expanding

        # search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('用例检索')
        self.search_edit.setObjectName('search_edit')
        self.search_edit.setMinimumWidth(150)
        self.search_edit.setMinimumHeight(32)
        self.search_button = QToolButton(self)
        self.search_button.setObjectName('search_button')
        self.search_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.search_button.setText('搜索')
        self.search_button.clicked.connect(self.search_case_event)

        # case verify
        self.verify_case_button = QToolButton(self)
        self.verify_case_button.setEnabled(False)
        self.verify_case_button.setMaximumWidth(50)
        self.verify_case_button.setObjectName('verify_case_button')
        self.verify_case_button.setIconSize(QSize(36, 36))
        self.verify_case_button.setIcon(QIcon(images_dir + 'verify.png'))
        self.verify_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.verify_case_button.setText('脚本校验')
        self.verify_case_button.clicked.connect(self.verify_case_event)

        # start test
        self.run_case_button = QToolButton(self)
        self.run_case_button.setEnabled(False)
        self.run_case_button.setMaximumWidth(50)
        self.run_case_button.setObjectName('run_case_button')
        self.run_case_button.setIconSize(QSize(36, 36))
        self.run_case_button.setIcon(QIcon(images_dir + 'verify.png'))
        self.run_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.run_case_button.setText('开始测试')
        self.run_case_button.clicked.connect(self.run_case_event)

        # show
        self.show_case_button = QToolButton(self)
        self.show_case_menu = QMenu(self.show_case_button)
        self.show_select_case = QAction('显示选中脚本', self, checkable=True)
        self.show_case_menu.addAction(self.show_select_case)
        self.show_error_case = QAction('显示错误脚本', self, checkable=True)
        self.show_case_menu.addAction(self.show_error_case)
        self.show_verify_pass_case = QAction('显示校验通过脚本', self, checkable=True)
        self.show_case_menu.addAction(self.show_verify_pass_case)
        self.show_case_button.setObjectName('show_case_button')
        self.show_case_button.setIconSize(QSize(36, 36))
        self.show_case_button.setIcon(QIcon(images_dir + 'show.png'))
        self.show_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.show_case_button.setText('显示')
        self.show_case_button.setMenu(self.show_case_menu)
        self.show_case_button.setPopupMode(QToolButton.InstantPopup)

        # hide
        self.hide_case_button = QToolButton(self)
        self.hide_case_menu = QMenu(self.hide_case_button)
        self.hide_select_case = QAction('隐藏选中脚本', self, checkable=True)
        # self.hide_select_case.setChecked(True)
        self.hide_case_menu.addAction(self.hide_select_case)
        self.hide_error_case = QAction('隐藏错误脚本', self, checkable=True)
        self.hide_case_menu.addAction(self.hide_error_case)
        self.hide_verify_pass_case = QAction('隐藏校验通过脚本', self, checkable=True)
        self.hide_case_menu.addAction(self.hide_verify_pass_case)
        self.hide_case_button.setObjectName('hide_case_button')
        self.hide_case_button.setIconSize(QSize(36, 36))
        self.hide_case_button.setIcon(QIcon(images_dir + 'hide.png'))
        self.hide_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.hide_case_button.setText('隐藏')
        self.hide_case_button.setMenu(self.hide_case_menu)
        self.hide_case_button.setPopupMode(QToolButton.InstantPopup)

        # add new case
        self.add_case_button = QToolButton(self)
        self.add_case_button.setEnabled(False)
        self.add_case_button.setObjectName('add_case')
        self.add_case_button.setMaximumWidth(50)
        self.add_case_button.setIconSize(QSize(36, 36))
        self.add_case_button.setIcon(QIcon(images_dir + 'add.png'))
        self.add_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.add_case_button.setText('新增脚本')
        self.add_case_hidden_bool = True
        self.add_case_button.clicked.connect(self.add_case_button_event)

        # refresh
        self.refresh_case_button = QToolButton(self)
        self.refresh_case_button.setEnabled(False)
        self.refresh_case_button.setObjectName('refresh_case_button')
        self.refresh_case_button.setIconSize(QSize(36, 36))
        self.refresh_case_button.setIcon(QIcon(images_dir + 'refresh.png'))
        self.refresh_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.refresh_case_button.setText('刷新')
        self.refresh_case_button.clicked.connect(self.refresh_gui_event)

        # path
        self.path_button = QToolButton(self)
        self.path_button.setEnabled(False)
        self.path_button.setObjectName('path_button')
        self.path_button.setIconSize(QSize(36, 36))
        self.path_button.setIcon(QIcon(images_dir + 'file.png'))
        self.path_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.path_button.setText('路径')
        self.select_path_hidden_bool = True
        self.path_button.clicked.connect(self.path_button_event)
        # self.path_button.clicked.connect(lambda: self.which_btn(self.path_button))

        # main layout
        self.main_layout = QVBoxLayout(self)
        self.top_layout = QHBoxLayout(self)  # 顶层 layout
        self.select_project_layout = QHBoxLayout(self)
        self.add_case_layout = QGridLayout(self)
        self.select_path_layout = QGridLayout(self)
        self.center_layout = QHBoxLayout(self)
        self.case_tree = QTreeWidget(self)
        self.case_tree.header().setStretchLastSection(True)  # 表格宽度自适应
        self.bottom_layout = QHBoxLayout(self)

        # line
        self.top_center_line_1 = QFrame(self)
        self.top_center_line_1.setFrameShape(QFrame.VLine)
        self.top_center_line_1.setFrameShadow(QFrame.Raised)
        self.top_center_line_1.setMaximumHeight(32)
        self.top_center_line_2 = QFrame(self)
        self.top_center_line_2.setFrameShape(QFrame.VLine)
        self.top_center_line_2.setFrameShadow(QFrame.Raised)
        self.top_center_line_2.setMaximumHeight(35)
        self.top_center_line_3 = QFrame(self)
        self.top_center_line_3.setFrameShape(QFrame.VLine)
        self.top_center_line_3.setFrameShadow(QFrame.Raised)
        self.top_center_line_3.setMaximumHeight(35)
        self.top_center_line_4 = QFrame(self)
        self.top_center_line_4.setFrameShape(QFrame.VLine)
        self.top_center_line_4.setFrameShadow(QFrame.Raised)
        self.top_center_line_4.setMaximumHeight(35)
        self.top_center_line_5 = QFrame(self)
        self.top_center_line_5.setFrameShape(QFrame.VLine)
        self.top_center_line_5.setFrameShadow(QFrame.Raised)
        self.top_center_line_5.setMaximumHeight(35)
        self.top_center_line_6 = QFrame(self)
        self.top_center_line_6.setFrameShape(QFrame.VLine)
        self.top_center_line_6.setFrameShadow(QFrame.Raised)
        self.top_center_line_6.setMaximumHeight(35)
        self.top_center_line_7 = QFrame(self)
        self.top_center_line_7.setFrameShape(QFrame.VLine)
        self.top_center_line_7.setFrameShadow(QFrame.Raised)
        self.top_center_line_7.setMaximumHeight(35)
        self.top_center_line_8 = QFrame(self)
        self.top_center_line_8.setFrameShape(QFrame.VLine)
        self.top_center_line_8.setFrameShadow(QFrame.Raised)
        self.top_center_line_8.setMaximumHeight(35)
        self.bottom_center_line = QFrame(self)
        self.setup_ui()
        self.a = self.startTimer(int(100))

    def setup_ui(self):
        # main window set
        qr = QMainWindow.frameGeometry(self)
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        QMainWindow.move(self, qr.topLeft())
        QMainWindow.setWindowTitle(self, '自动化测试')
        QMainWindow.setWindowIcon(self, QIcon(self.ico_path))
        # menu bar
        _menu = QMainWindow.menuBar(self)
        _file = _menu.addMenu('&文件')
        _edit = _menu.addMenu('&编辑')

        # status bar
        _status = QMainWindow.statusBar(self)

        # case_tree
        self.case_tree.setColumnCount(8)
        self.case_tree.setColumnWidth(1, 200)
        self.case_tree.setColumnWidth(3, 250)
        self.case_tree.setColumnWidth(6, 150)
        self.case_tree.setHeaderLabels(["序号", "脚本名称", "校验结果", "脚本描述", "所属模块", "编写作者", "修改时间", "操作"])
        self.case_tree.setObjectName('case_tree')
        self.case_tree.header().setStretchLastSection(True)

        # main layout
        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        QMainWindow.setCentralWidget(self, self.widget)

        # style
        QssTools.set_qss_to_object(self.style_path, self)

        # function
        self.top_()
        self.add_project_widget_func()
        self.add_case_widget_func()
        self.select_path_widget_func()
        self.center_()
        self.bottom_()

    def top_(self):
        # select button
        self.top_layout.addWidget(self.open_project_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_1, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self._case_manage, 0.1, Qt.AlignLeft)
        self.top_layout.addItem(self.spacer_item)
        self.top_layout.addWidget(self.search_edit, 0.5, Qt.AlignLeft)
        self.top_layout.addWidget(self.search_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_2, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.verify_case_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_3, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.run_case_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_4, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.show_case_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.hide_case_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_5, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.add_case_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_6, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.refresh_case_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_7, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.path_button, 0.1, Qt.AlignLeft)
        self.top_layout.addWidget(self.top_center_line_8, 0, Qt.AlignLeft)

        self.main_layout.addLayout(self.top_layout)

    def add_project_widget_func(self):
        self.select_project_widget.setMaximumHeight(108)
        self.select_project_widget.setMinimumHeight(108)
        self.select_project_widget.setLayout(self.select_project_layout)  # 添加横向布局
        self.select_project_layout.addWidget(self.add_project_button, 0.1, Qt.AlignLeft | Qt.AlignVCenter)

        # 2，点击button， 出发点击事件 添加子widget， 包含{1，左上图标， 文件名， 2, 项目简述，3, 路径:C:/user/}

        self.main_layout.addWidget(self.select_project_widget)
        self.select_project_widget.setHidden(self.add_project_button_hidden_bool)

    def add_case_widget_func(self):

        self.add_case_widget.setLayout(self.add_case_layout)
        self.add_case_layout.addWidget(self.case_name, 0, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_name_edit, 0, 1, Qt.AlignLeft | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_description, 1, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_description_edit, 1, 1, Qt.AlignLeft | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_author, 2, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_author_edit, 2, 1, Qt.AlignLeft | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.max_running_time, 0, 2, Qt.AlignRight | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.max_running_time_edit, 0, 3, Qt.AlignLeft | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_modules, 1, 2, Qt.AlignRight | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_modules_edit, 1, 3, Qt.AlignLeft | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_date, 2, 2, Qt.AlignRight | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.case_date_edit, 2, 3, Qt.AlignLeft | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.screenshots_button, 0, 4, Qt.AlignLeft | Qt.AlignVCenter)
        self.add_case_layout.addWidget(self.create_and_cancel_button, 2, 4, Qt.AlignLeft | Qt.AlignVCenter)
        self.main_layout.addWidget(self.add_case_widget)
        self.add_case_widget.setHidden(self.add_case_hidden_bool)

    # 路径框
    def select_path_widget_func(self):
        self.select_path_widget.setLayout(self.select_path_layout)

        self.select_path_layout.addWidget(self.project_path_, 0, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.project_path_edit, 0, 1, Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.project_path_button, 0, 2, Qt.AlignLeft | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.case_log_path_, 1, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.case_log_path_edit, 1, 1, Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.case_log_path_button, 1, 2, Qt.AlignLeft | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.select_case_data_read_path_, 2, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.select_case_data_read_path_edit, 2, 1, Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.select_case_data_read_path_button, 2, 2, Qt.AlignLeft | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.test_version_images_path_, 0, 3, Qt.AlignRight | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.test_version_images_path_edit, 0, 4, Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.test_version_images_path_button, 0, 5, Qt.AlignLeft | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.save_images_path_, 1, 3, Qt.AlignRight | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.save_images_path_edit, 1, 4, Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.save_images_path_button, 1, 5, Qt.AlignLeft | Qt.AlignVCenter)
        self.select_path_layout.addWidget(self.finish_button, 2, 5, Qt.AlignRight | Qt.AlignVCenter)

        # set enable
        self.case_log_path_button.setEnabled(False)
        self.select_case_data_read_path_button.setEnabled(False)
        self.test_version_images_path_button.setEnabled(False)
        self.save_images_path_button.setEnabled(False)

        self.main_layout.addWidget(self.select_path_widget)
        self.select_path_widget.setHidden(self.select_path_hidden_bool)  # bool hidden

    def center_(self):
        self.center_layout.addWidget(self.case_tree)
        self.main_layout.addLayout(self.center_layout)

    def get_case_tree_info(self, current_dir_path):
        self.case_tree.clear()
        sys.path.append(current_dir_path)
        test_case_dir = QDir(current_dir_path)
        test_case_dir.setFilter(QDir.Files | QDir.Hidden | QDir.NoSymLinks)
        test_case_dir.setNameFilters(["*.py", ])
        case_file_list = test_case_dir.entryInfoList()
        import importlib
        for case_file in case_file_list:
            case_module = importlib.reload(import_module(case_file.fileName()[0:-3]))
            # 获取信息
            max_running_time = getattr(case_module, 'max_running_time', '')
            author = getattr(case_module, 'author', '')
            date = getattr(case_module, 'date', '')
            try:
                case_update_time = os.path.getmtime(current_dir_path + case_file.fileName())
                filetime = datetime.datetime.fromtimestamp(case_update_time)
                case_update_time = filetime.strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                raise e
            description = getattr(case_module, 'description', '')
            screenshots = getattr(case_module, 'screenshots', '')
            modules = getattr(case_module, 'modules', '')
            print(modules)
            if not all([max_running_time, author, case_update_time, description, modules]):
                case_item_result = '脚本错误'
                case_item = QTreeWidgetItem(self.case_tree,
                                            ['', case_file.fileName(), case_item_result, description, modules, author,
                                             case_update_time, ''])
                case_item.setFlags(case_item.flags() & ~Qt.ItemIsEnabled)
            else:
                case_item_result = '校验通过'
                case_item = QTreeWidgetItem(self.case_tree,
                                            ['', case_file.fileName(), case_item_result, description, modules, author,
                                             case_update_time, ''])

            # 设置勾选框
            case_item.setFlags(case_item.flags() | Qt.ItemIsUserCheckable)
            case_item.setCheckState(0, Qt.Unchecked)
            # case_item.setSelected(True)  # 设置复选框选中状态

            self.case_tree.addTopLevelItem(case_item)

            self.case_tree.updatesEnabled()

    def bottom_(self):
        # left
        left_msg = '已选择%s 条' % None
        left_label = QLabel(left_msg)
        self.bottom_layout.addWidget(left_label, 0, Qt.AlignLeft | Qt.AlignVCenter)

        # left_label.setText("<html><head/><body><p><span style=\" font-family:'\345\276\256\350\275\257\351\233\205\351\273\221 Bold,\345\276\256\350\275\257\351\233\205\351\273\221 Regular,\345\276\256\350\275\257\351\233\205\351\273\221'; font-size:18px; font-weight:696; color:#00c7e6; background-color:#f7f8fa;\">\346\265\213\350\257\225\345\256\214\346\210\220</span><span style=\" font-family:'\345\276\256\350\275\257\351\233\205\351\273\221'; font-size:14px; color:#333333; background-color:#f7f8fa;\">\347\224\250\346\227\266\357\274\23230</span></p></body></html>")
        # left_label.setText('已选择0条，预计测试总时长N')
        # 分割线  StyledPanel 依据当前GUI类型，画一个矩形面板，可以凸起或下沉
        # NoFrame 无边框, Box 矩形框, Panel 凸起或凹陷的面板, HLine 水平线(用作分隔符), VLine 垂直线(用作分隔符)
        self.bottom_center_line.setFrameShape(QFrame.VLine)
        self.bottom_center_line.setFrameShadow(QFrame.Plain)  # Plain 无阴影, Raised 面板凸起, Sunken 面板下沉
        self.bottom_center_line.setObjectName("bottom_center_line")
        self.bottom_layout.addWidget(self.bottom_center_line)

        # right
        right_msg = '预计测试总时长%s ' % None
        right_label = QLabel(right_msg)
        self.bottom_layout.addWidget(right_label, 1, Qt.AlignLeft | Qt.AlignVCenter)

        self.main_layout.addLayout(self.bottom_layout)

    def open_project_button_event(self):
        if self.add_project_button_hidden_bool:
            # set others bool hidden
            self.select_path_hidden_bool = True
            self.path_button.setIcon(QIcon(images_dir + 'file.png'))
            self.select_path_widget.setHidden(self.select_path_hidden_bool)
            self.add_case_hidden_bool = True
            self.add_case_button.setIcon(QIcon(images_dir + 'add.png'))
            self.add_case_widget.setHidden(self.add_case_hidden_bool)

            self.add_project_button_hidden_bool = False
            self.select_project_widget.setHidden(self.add_project_button_hidden_bool)
        else:
            self.select_project_widget.setHidden(True)
            self.add_project_button_hidden_bool = True

    def add_project_button_event(self):
        apps_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'apps/')
        current_dir = QFileDialog.getExistingDirectory(self, '选择文件夹', apps_path)
        current_select_dir = FileOperation.get_file_path_and_name(current_dir)[1]
        if len(current_select_dir) > 0:
            sections_list = self.config_ini.get_section()[1]
            _time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            self.log.info('current open dir %s, button: open_project_button, time: %s' % (current_select_dir, _time))
            if current_select_dir.upper() not in sections_list:
                self.log.error('current open dir %s, but open dir not in sections list' % current_select_dir)
                return
            self.current_project = current_select_dir
            pa = PathExistProject(project_name=self.current_project, log_obj=self.log)
            all_project_path = pa.return_path()
            test_case_path = all_project_path.get('test_case_path')

            self.get_case_tree_info(test_case_path)

            # 执行点击事件
            self.path_button.setEnabled(True)
            self.path_button.click()

        if self.current_project:
            self.current_project_name = self.current_project
            self.refresh_case_button.setEnabled(True)
            self.add_case_button.setEnabled(True)
            self.verify_case_button.setEnabled(True)
            self.run_case_button.setEnabled(True)

    def search_case_event(self):
        txt = self.search_edit.text()
        for i in range(self.case_tree.topLevelItemCount()):
            case_item = self.case_tree.topLevelItem(i)
            case_item.setSelected(False)
            if txt == case_item.text(1):
                case_item.setSelected(True)  # 设置复选框选中状态

    def verify_case_event(self):
        self.verify_case_list.clear()
        verify_o = TestCaseManager(project_name=self.current_project_name)
        for i in range(self.case_tree.topLevelItemCount()):
            case_item = self.case_tree.topLevelItem(i)
            case_check_state = case_item.checkState(0)
            if case_check_state:
                self.verify_case_list.append(case_item.text(1))
                result_list = verify_o.verify_case([case_item.text(1)])
                if len(result_list) > 0:
                    for item in result_list:
                        if item[0] == case_item.text(1):
                            if item[1] == '校验通过':
                                case_item.setText(2, '校验通过')
                            else:
                                case_item.setText(2, '脚本错误')
                                case_item.setFlags(case_item.flags() & ~Qt.ItemIsEnabled)

            if not case_check_state == Qt.Checked:
                continue
        self.case_tree.updatesEnabled()

    def run_case_event(self):
        # 置灰button
        self.case_log_path_button.setEnabled(False)
        self.select_case_data_read_path_button.setEnabled(False)
        self.test_version_images_path_button.setEnabled(False)
        self.save_images_path_button.setEnabled(False)
        self.widget.updatesEnabled()

        for i in range(self.case_tree.topLevelItemCount()):
            case_item = self.case_tree.topLevelItem(i)
            case_check_state = case_item.checkState(0)
            if case_check_state:
                st = StartProject(self.current_project_name, [case_item.text(1)])
                case_item.setText(2, '测试中....')
                qApp.processEvents()
                run_log_name, ret = st.run_case()
                if ret == 0:
                    case_item.setText(2, '测试通过')
                    qApp.processEvents()
                elif ret == 404:
                    case_item.setText(2, '测试异常(超时)')
                    qApp.processEvents()
                elif ret == 500:
                    case_item.setText(2, '测试异常')
                    qApp.processEvents()

    def add_case_button_event(self):
        if self.add_case_hidden_bool:
            # set others bool hidden
            self.add_project_button_hidden_bool = True
            self.select_project_widget.setHidden(self.add_project_button_hidden_bool)

            self.select_path_hidden_bool = True
            self.path_button.setIcon(QIcon(images_dir + 'file.png'))
            self.select_path_widget.setHidden(self.select_path_hidden_bool)

            self.add_case_hidden_bool = False
            self.add_case_button.setIcon(QIcon(images_dir + 'add_blue.png'))
            self.add_case_widget.setHidden(self.add_case_hidden_bool)
        else:
            self.add_case_widget.setHidden(True)
            self.add_case_button.setIcon(QIcon(images_dir + 'add.png'))
            self.add_case_hidden_bool = True

    def refresh_gui_event(self):
        pa = PathExistProject(project_name=self.current_project, log_obj=self.log)
        all_project_path = pa.return_path()
        test_case_path = all_project_path.get('test_case_path')
        self.get_case_tree_info(current_dir_path=test_case_path)
        QApplication.processEvents()

    def create_add_case_event(self):
        # get save path
        pa_object = PathExistProject(project_name=self.current_project_name, log_obj=self.log)
        _all_project_path = pa_object.return_path()
        test_case_path = _all_project_path.get('test_case_path')
        # get save data
        case_name = self.case_name_edit.text()
        case_description = self.case_description_edit.text()
        case_author = self.case_author_edit.text()
        max_running_time = self.max_running_time_edit.text()
        case_modules = self.case_modules_edit.currentText()
        case_date = self.case_date_edit.text()
        screenshots = bool(self.screenshots_button.isChecked())

        if not all([case_name, case_description, case_author, case_modules, max_running_time, case_date]):
            self.log.error('does not get value, Function: create add case event')
            return
        TestCaseManager.create_new_case(self.current_project_name, case_name, case_description, case_author, int(max_running_time), case_modules, screenshots)

        self.add_case_button.click()

    def cancel_create_add_case_event(self):
        # reset QLineEdit data
        self.case_name_edit.setText('')
        self.case_description_edit.setText('')
        self.case_author_edit.setText('')
        self.max_running_time_edit.setText('')
        # self.case_modules_edit.setText('')
        self.screenshots_button.setChecked(False)
        QApplication.processEvents()

    def path_button_event(self):
        if self.select_path_hidden_bool:
            # set others bool hidden
            self.add_project_button_hidden_bool = True
            self.select_project_widget.setHidden(self.add_project_button_hidden_bool)

            self.add_case_hidden_bool = True
            self.add_case_button.setIcon(QIcon(images_dir + 'add.png'))
            self.add_case_widget.setHidden(self.add_case_hidden_bool)

            self.select_path_hidden_bool = False
            self.path_button.setIcon(QIcon(images_dir + 'file_blue.png'))
            self.select_path_widget.setHidden(self.select_path_hidden_bool)
        else:
            self.select_path_widget.setHidden(True)
            self.path_button.setIcon(QIcon(images_dir + 'file.png'))
            self.select_path_hidden_bool = True

    # set QLine Edit self.project_path_edit -- > self.project_path_button
    def set_exe_path_event(self):
        select_exe_path = QFileDialog.getOpenFileName(self, 'select exe path', '.', 'exe file(*.exe)')[0]
        self.project_path_edit.setText(select_exe_path)

    # verify path_button all button status -- > self.finish_button
    def verify_and_save_path_line_edit_event(self):
        # verify get input value
        shell_exe_path = self.project_path_edit.text()
        if not shell_exe_path:
            return
        release_path = FileOperation.get_file_path_and_name(shell_exe_path)[0]
        self.config_ini.update_data(self.current_project, 'release', release_path)
        self.path_button.click()

    def timerEvent(self, event):
        QApplication.processEvents()
        self.case_tree.updatesEnabled()
        self.current_time = time.localtime(time.time())
        self.case_date_edit.setText(time.strftime('%Y-%m-%d-%H-%M-%S', self.current_time))

    def closeEvent(self, event):
        tip = "Are you sure to quit?"
        reply = QMessageBox.question(self, 'Message', tip, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            QMainWindow.statusBar(self).showMessage('关闭软件')
        else:
            event.ignore()
            QMainWindow.statusBar(self).showMessage('撤销关闭')

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        quit_action = menu.addAction('quit')
        action = menu.exec_(QMainWindow.mapToGlobal(self, event.pos()))

        if action == quit_action:
            qApp.quit()

    def focusOutEvent(self, even):
        pass


def main():
    app = QApplication(sys.argv)
    qt = UiMainWindow()
    qt.show()
    sys.exit(app.exec_())  # 循环执行窗口触发事件


if __name__ == '__main__':
    p = multiprocessing.Process(target=main, args=())
    p.start()
    p.join()
