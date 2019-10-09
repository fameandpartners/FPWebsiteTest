# -*- coding: UTF-8 -*-
# 生成 HTML 报告类
import os
import pystache
import time

from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.logclass.logconfig import Logger
import datetime

current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')
logger = Logger(log_path=source_log_path)


class Report:

    def __init__(self, logger_obj, project_name):
        self.mustache = ''
        self.logger = logger_obj
        self.project_name = project_name

        self.ini = ConfigIni(log_obj=source_log_path)

        self.pe = PathExistProject(project_name, logger_obj)
        self.path_data = self.pe.return_path()
        self.save_report_path = self.path_data["report_path"]


    def data_parser(self, r_data):

        author_name = self.ini.get_str(section='REPORT', option='_The_operator')

        mustache = {
            "project_title": "自动化测试",
            "author_name": author_name,
            "start_time": r_data["start_time"],
            "total_time": r_data["total_time"],
            "passing_rate": r_data["passing_rate"],
            "pass_num": r_data["pass_num"],
            "fail_num": r_data["fail_num"],
            "all_num": r_data["all_num"],
            "pass_item": r_data["pass_item"],
            "fail_item": r_data["fail_item"]
        }

        return mustache

    def save_report(self, r_data):

        mustache_data = self.data_parser(r_data)

        _path = self.save_report_path
        report_name = time.strftime("-%Y-%m-%d-%H-%M-%S.html", time.localtime(time.time()))
        save_path = _path + self.project_name.lower() + report_name

        base_path = os.path.join(current_path, 'report.html')
        t = open(base_path, "r", encoding="utf-8")
        file_content = pystache.render(t.read(), mustache_data)
        t.close()
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write(file_content)

    def get_new_file(self):
        dir_path = self.save_report_path
        in_dir_list = os.listdir(dir_path)
        if not in_dir_list:
            self.logger.error("  *当前时间：%s, 目录文件为空" % time.strftime("-%Y-%m-%d-%H-%M-%S.html", time.localtime(time.time())))

        # 对文件修改时间进行升序排列
        in_dir_list.sort(key=lambda _file: os.path.getmtime(dir_path + _file))
        filetime = datetime.datetime.fromtimestamp(os.path.getmtime(dir_path + in_dir_list[-1]))
        file_path = os.path.join(dir_path, in_dir_list[-1])
        file_name = in_dir_list[-1]
        self.logger.log("  *最新修改的文件(夹)：" + in_dir_list[-1])
        self.logger.log("  *文件生成时间：" + filetime.strftime('%Y-%m-%d %H:%M:%S'))

        return file_path, file_name


if __name__ == '__main__':
    pass
    project_name = 'MTM'
    data = ''
    re = Report(logger, project_name)
    re.get_new_file()
