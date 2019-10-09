# -*- coding: utf-8 -*-
# 生成测试用例样例模板
import os
import time
import re

from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.file_operation import FileOperation
from testframework.source.utils.logclass.logconfig import Logger

current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')
source_log_obj = Logger(log_path=source_log_path)


class CreateCaseDemo:

    def __init__(self, project_name):
        self.log = source_log_obj
        self.project_name = project_name
        self.ini = ConfigIni(log_obj=source_log_obj)

        self.pa = PathExistProject(project_name=project_name, log_obj=source_log_obj)
        self.path_data = self.pa.return_path()
        self.save_case_dir = self.path_data["test_case_path"]

        # 替代数据
        self.description = None
        self.author = None
        self.max_running_time = None
        self.modules = None
        self.screenshots = None


    def verify_save_case_name(self, input_case_name):

        _re = r'%s' % self.ini.get_str(section=self.project_name, option=self.project_name.lower())
        if not re.match(_re, input_case_name):
            self.log.error('Please confirm the file name, For example: %s-example.py' % self.project_name.lower())
            return
        _file_suffix = FileOperation.get_file_name_and_suffix(input_case_name)[1]
        if not _file_suffix:
            input_case_name = input_case_name + '.py'
        else:
            if _file_suffix != '.py':
                self.log.error('Please confirm the suffix: %s' % _file_suffix)
                return
        return input_case_name

    def create_test_case(self, save_case_name, description, author, max_running_time, modules, screenshots):
        # verify save_case_name
        case_name = self.verify_save_case_name(save_case_name)
        if not case_name:
            return
        save_case_path = self.save_case_dir + case_name

        self.description = description
        self.author = author
        self.max_running_time = int(max_running_time)
        self.modules = modules
        self.screenshots = bool(screenshots)
        self.current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        # 脚本头文件信息列表
        tc_list_msg = ['# -*- coding:utf-8 -*-',
                       '# /*',
                       '# * 公司：Hangzhou Graphic China Technology Co.,Ltd',
                       '# * 版权信息：图华所有',
                       '# * 任务：脚本系统',
                       '# * 描述：%s' % self.description,
                       '# * 作者：%s' % self.author,
                       '# * 日期：%s' % self.current_time,
                       '# */',
                       'import sys',
                       '\n',
                       'max_running_time = %s' % self.max_running_time,
                       'author = "%s"' % str(self.author),
                       'date = "%s"' % str(self.current_time),
                       'description = "%s"' % str(self.description),
                       'modules = "%s"' % str(self.modules),
                       'screenshots = %s' % self.screenshots,
                       '\n',
                       'def main(argv):',
                       '    pass',
                       '\n',
                       'if __name__ == "__main__":',
                       '    main(sys.argv)',
                       '\n']

        with open(save_case_path, 'w', encoding='utf-8') as f:
            str_n = '\n'
            msg = str_n.join(tc_list_msg)
            f.write(msg)


if __name__ == '__main__':
    project_name = 'MTM'
    log_obj = source_log_obj
    cr = CreateCaseDemo(project_name)

    save_case_name = 'mtm-test'
    description = 'This is main flow test'
    author = '小明'
    max_running_time = 500
    modules = '主流程'
    screenshots = False
    cr.create_test_case(save_case_name, description, author, max_running_time, modules, screenshots)
