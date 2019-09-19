# -*- coding: utf-8 -*-
# 构造文件目录
import os
import shutil
from testframework.source.configs.readini import ConfigIni
from testframework.source.utils.logclass.logconfig import Logger
from testframework.source.utils.file_operation import FileOperation

current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class ConstructDir:

    def __init__(self, project_name, log_obj):
        self.log = log_obj
        self.create_project_name = project_name
        self.ini = ConfigIni(log_obj=source_log_object)

        self.create_dir = ['%s/case/' % project_name,
                           '%s/case/runcase/' % project_name,
                           '%s/case/testcase/' % project_name,
                           '%s/case/testdata/' % project_name,
                           '%s/images/' % project_name,
                           '%s/images/errorimages/' % project_name,
                           '%s/images/memoryimages/' % project_name,
                           '%s/logs/' % project_name,
                           '%s/report/' % project_name,
                           '%s/src/function/' % project_name]

    def create_apps_dir(self):
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
        project_dir_data = FileOperation().get_return_dirs_dir_or_file(dirs_path=project_dir, return_dir=True)
        if 'apps' not in project_dir_data:
            FileOperation().create_new_dir(project_dir, 'apps')
            apps_path = os.path.join(project_dir, 'apps/')
            for create_dir_item in self.create_dir:
                FileOperation().create_new_dir(apps_path, create_dir_item)
        else:
            apps_path = os.path.join(project_dir, 'apps/')
            apps_path_data = FileOperation().get_return_dirs_dir_or_file(dirs_path=apps_path, return_dir=True)
            for item in apps_path_data:
                if item.lower() == self.create_project_name.lower():
                    self.log.error('Project name already exist')
                    return
            for create_dir_item in self.create_dir:
                FileOperation().create_new_dir(apps_path, create_dir_item)

        init_file = apps_path + '%s/src/function/__init__.py' % self.create_project_name
        if not os.path.exists(init_file):
            file = open(init_file, 'w', encoding='utf8')
            file.close()
        project_function_path = apps_path + '%s/src/function/' % self.create_project_name
        # self.create_file(project_function_path)
        self.write_config_project_name()

    # 构造文件内容
    def create_file(self, project_function_path):
        file_name = self.create_project_name.lower() + '-function.py'
        source_function_path = os.path.join(current_path, 'function/')

        source_path = source_function_path + file_name
        target_path = project_function_path + file_name
        if os.path.isdir(source_path):
            self.log.error("it's a special file: %s" % source_path)
            raise Exception('Copy file to run case failed')
        try:
            shutil.copyfile(source_path, target_path)
        except Exception as e:
            self.log.exception("copyfile: %s --> %s, Failed" % (source_path, target_path))
            raise e

    def write_config_project_name(self):
        section = self.create_project_name.upper()
        option = self.create_project_name.lower()
        value = '^%s-' % self.create_project_name.lower()
        self.ini.add_data(section=section, option=option, value=value)


if __name__ == '__main__':
    project_name = 'UR'
    construct = ConstructDir(project_name=project_name, log_obj=source_log_object)
    construct.create_apps_dir()
