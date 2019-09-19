# -*- coding: utf-8 -*-
# 开启程序出错截图
from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.logclass.logconfig import Logger
import time
import sys
import os
import difflib


current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class GetScreenshots:

    def __init__(self, project_name):

        self.project_name = project_name
        self.ini = ConfigIni(log_obj=source_log_object)

        self.pa = PathExistProject(project_name=project_name, log_obj=source_log_object)
        self.path_data = self.pa.return_path()
        self.hwnd_title = dict()
        self.save_images_path = self.path_data["error_images_path"]

    def get_project_title(self):
        title_list = self.get_handle_title()
        cutoff = self.ini.get_float(section='CONFIG', option='cutoff')
        if not cutoff:
            cutoff = 0.6
        # original_title_name = self.ini.get_str(section=self.project_name.upper(), option='title_name')
        original_title_name = "| Fame & Partners - Google Chrome"
        title_name = difflib.get_close_matches(original_title_name, title_list, 1, cutoff=cutoff)
        print(title_name)
        return title_name

    def get_all_handle(self, hwnd, test):
        import win32gui
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
            # print(self.hwnd_title)

    def get_handle_title(self):
        import win32gui
        title_list = []
        win32gui.EnumWindows(self.get_all_handle, 0)
        for handle, title in self.hwnd_title.items():
            title_list.append(title)
            if title is '':
                title_list.remove(title)
        print(title_list)
        return title_list

    def get_screenshots(self, error_code, code_status=False):
        import win32gui
        if error_code not in [0, None, True, False]:
            class_name = None
            title_name = self.get_project_title()

            if not title_name:
                msg = 'Title name does not exist, please adjust the value of cutoff(0 - 1), example:0.6'
                source_log_object.info(msg)
                return

            hwnd = win32gui.FindWindow(class_name, title_name[0])

            # 设置为最前窗口
            win32gui.SetForegroundWindow(hwnd)
            # 获取最前窗口句柄
            hwnd = win32gui.GetForegroundWindow()
            from PyQt5.QtWidgets import QApplication
            qapp = QApplication(sys.argv)
            screen = QApplication.primaryScreen()
            img = screen.grabWindow(hwnd).toImage()
            current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
            images_name = 'ERROR-' + current_time + '.png'
            if code_status:
                images_name = 'INFO-' + current_time + '.png'
            img.save(self.save_images_path + images_name)


if __name__ == '__main__':
    project_name = 'FPWebsite'
    ge = GetScreenshots(project_name)
    # ge.get_handle_title()
    error_code = 500
    ge.get_screenshots(error_code=error_code)
    a = "Custom Clothing | Made-to-order | Less-waste | Fame & Partners - Internet Explorer"
    b = "Custom Clothing | Made-to-order | Less-waste | Fame & Partners - Google Chrome"
