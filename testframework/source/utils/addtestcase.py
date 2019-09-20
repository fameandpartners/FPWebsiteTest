# -*- coding: utf-8 -*-
# 传入测试脚本目录路径 显示已存在的测试脚本
import os
import shutil
from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.logclass.logconfig import Logger
import re

current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class AddTestCase:

    def __init__(self, project_name):
        self.project_name = project_name

        self.ini = ConfigIni(log_obj=source_log_object)

        self.pat = PathExistProject(project_name, source_log_object)
        self.project_path = self.pat.return_path()
        self.logger = Logger(log_path=self.project_path["logs_path"])

    def get_test_case(self, _suffix=True):
        _dir_path = self.project_path["test_case_path"]
        case_list = os.listdir(_dir_path)

        rm_list = ['__pycache__']
        if set(rm_list) <= set(case_list):
            for i in rm_list:
                case_list.remove(i)

        for item in case_list:
            (_name, _name_suffix) = os.path.splitext(item)
            if _name_suffix != '.py':
                case_list.remove(item)
            _re = r'%s' % self.ini.get_str(section=self.project_name, option=self.project_name.lower())
            if not re.match(_re, item):
                case_list.remove(item)

        if not _suffix:
            for index, item in enumerate(case_list):
                (_name, _name_suffix) = os.path.splitext(item)
                case_list[index] = _name
            return case_list

        return case_list

    def get_run_case(self, _suffix=True):
        _dir_path = self.project_path["run_case_path"]
        case_list = os.listdir(_dir_path)

        rm_list = ['__pycache__']
        if set(rm_list) <= set(case_list):
            for i in rm_list:
                case_list.remove(i)

        for item in case_list:
            _re = r'%s' % self.ini.get_str(section=self.project_name, option=self.project_name.lower())
            (_name, _name_suffix) = os.path.splitext(item)
            if _name_suffix != '.py':
                case_list.remove(item)

            if not re.match(_re, item):
                case_list.remove(item)

        if not _suffix:
            for index, item in enumerate(case_list):
                (_name, _name_suffix) = os.path.splitext(item)
                case_list[index] = _name
            return case_list

        return case_list

    def add_case(self, src_path):

        if os.path.isfile(src_path):
            (_dir_path, _path_file_name) = os.path.split(src_path)
            (_name, _name_suffix) = os.path.splitext(_path_file_name)

            # 验证文件命名规范
            _re = r'%s' % self.ini.get_str(section=self.project_name, option=self.project_name.lower())
            if not re.match(_re, _path_file_name):
                self.logger.error('Please confirm the file name: %s, For example: %s-example.py' % (_path_file_name, self.project_name.lower()))
                return
            if _name_suffix != '.py':
                self.logger.error('Please confirm the suffix: %s' % _name_suffix)
                return

            try:
                shutil.copyfile(src_path, self.project_path["test_case_path"] + _path_file_name)
            except Exception as e:
                self.logger.exception(e)
                return
            self.logger.info("Add file: %s to dir: %s successfully" % (src_path, self.project_path["test_case_path"]))
        else:
            self.logger.error("it's a special file: %s" % src_path)
            return

    def del_file(self, rm_path, file_name_list):

        if set(file_name_list) <= set(os.listdir(rm_path)):

            for item in file_name_list:
                remove_file_path = rm_path + item
                try:
                    os.remove(remove_file_path)
                except Exception as e:
                    self.logger.exception(e)
                    return
                self.logger.info("Delete file: %s successfully" % item)


if __name__ == '__main__':
    project_name = 'MTM'
    ad = AddTestCase(project_name=project_name)
    # print(ad.get_test_case())
    # print(ad.get_run_case())
    src_path = ''
    ad.add_case(src_path=src_path)