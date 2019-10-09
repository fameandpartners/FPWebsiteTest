# -*- coding: utf-8 -*-
# 传入测试用例路径，测试用例名称，对测试用例进行校验
import os
import shutil
import simplejson as simplejson
import importlib
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.file_operation import FileOperation
from testframework.source.utils.logclass.logconfig import Logger


current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')
source_log_object = Logger(log_path=source_log_path)


def read_file(dir_path, case_name):
    case_module = importlib.import_module(dir_path % case_name, package='apps')

    return case_module, case_name


class VerifyTestCase:
    """
    self.error_data = {"mtm-base": }

    """

    def __init__(self, project_name, case_list):

        self.pa = PathExistProject(project_name, source_log_object)
        self.project_path = self.pa.return_path()
        self.logger = source_log_object
        # self.logger = Logger(log_path=self.project_path["logs_path"])

        self.case_list = case_list

        # 需要校验的参数
        self.ver_max_running_time = None  # 用例超时时间
        self.ver_author = None  # 用例作者
        self.ver_date = None  # 用例时间
        self.ver_description = None  # 用例描述
        self.ver_screenshots = None  # 是否开启出错截图
        self.ver_modules = None  # 脚本归属模块

        self.error_bool = False

    def verify_case_max_running_time(self, case_name, case_module):
        try:
            self.ver_max_running_time = case_module.max_running_time
            if not self.ver_max_running_time:
                # self.error_data["max_running_time"] = ''
                self.logger.error('Case name: %s, max_running_time = None' % case_name)
                self.error_bool = True
        except AttributeError as e:
            self.logger.error('Case name: %s, max_running_time = None' % case_name)
            self.error_bool = True

    def verify_case_author(self, case_name, case_module):
        try:
            self.ver_author = case_module.author
            if not self.ver_author:
                self.logger.error('Case name: %s, author = None' % case_name)
                self.error_bool = True
        except AttributeError as e:
            self.logger.error('Case name: %s, author = None' % case_name)
            self.error_bool = True

    def verify_case_date(self, case_name, case_module):
        try:
            self.ver_date = case_module.date
            if not self.ver_date:
                self.logger.error('Case name: %s, date = None' % case_name)
                self.error_bool = True
        except AttributeError as e:
            self.logger.error('Case name: %s, date = None' % case_name)
            self.error_bool = True

    def verify_case_description(self, case_name, case_module):
        try:
            self.ver_description = case_module.description
            if not self.ver_description:
                self.logger.error('Case name: %s, description = None' % case_name)
                self.error_bool = True
        except AttributeError as e:
            self.logger.error('Case name: %s, description = None' % case_name)
            self.error_bool = True

    def verify_case_modules(self, case_name, case_module):
        try:
            self.ver_modules = case_module.modules
            if not self.ver_modules:
                self.logger.error('Case name: %s, modules = None' % case_name)
                self.error_bool = True
        except AttributeError as e:
            self.logger.error('Case name: %s, modules = None' % case_name)
            self.error_bool = True

    def verify_case_screenshots(self, case_name, case_module):
        try:
            self.ver_screenshots = case_module.screenshots
            if not self.ver_screenshots:
                self.logger.error('Case name: %s, screenshots = None' % case_name)
                self.error_bool = True
        except AttributeError as e:
            self.logger.error('Case name: %s, screenshots = None' % case_name)
            self.error_bool = True

    def verify_case_(self):

        case_info_dict = []
        for case_item in self.case_list:
            case_item_name = FileOperation.get_file_name_and_suffix(case_item)[0]
            import_module_path = self.project_path["import_module_path"] % case_item_name
            case_module = importlib.import_module(import_module_path, package='apps')

            self.verify_case_max_running_time(case_name=case_item_name, case_module=case_module)
            self.verify_case_author(case_name=case_item_name, case_module=case_module)
            self.verify_case_date(case_name=case_item_name, case_module=case_module)
            self.verify_case_description(case_name=case_item_name, case_module=case_module)
            self.verify_case_screenshots(case_name=case_item_name, case_module=case_module)
            self.verify_case_modules(case_name=case_item_name, case_module=case_module)

            if not self.error_bool:
                # src_path = self.project_path["test_case_path"] + case_item
                # _path = self.project_path["run_case_path"]
                # VerifyTestCase.move_file_to_run_case(src_path, _path)
                self.logger.info('Case name: %s, verify successfully' % case_item)

                self.error_bool = False
                item_info = [case_item, '校验通过']
                case_info_dict.append(item_info)
            else:
                item_info = [case_item, '脚本错误']
                case_info_dict.append(item_info)

        return case_info_dict

    @staticmethod
    def move_file_to_run_case(src_path, _path):

        # 验证传入的参数为目标路径
        dir_path = src_path
        target_path = _path + '/' + FileOperation.get_file_path_and_name(dir_path)[1]
        if os.path.isdir(dir_path):
            source_log_object.error("it's a special file: %s" % dir_path)
            raise Exception('Copy file to run case failed')
        try:
            shutil.copyfile(src_path, target_path)
        except Exception as e:
            source_log_object.exception("copyfile: %s --> %s, Failed" % (src_path, target_path))
            raise e


if __name__ == '__main__':
    project_name = 'MTM'
    # case_list = ['mtm-base.py', 'mtm-base_test.py']
    case_list = ['mtm-source.py']
    ver = VerifyTestCase(project_name, case_list)
    ver.verify_case_()

