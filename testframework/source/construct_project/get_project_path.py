# -*- coding: utf-8 -*-
import os
from testframework.source.utils.file_operation import FileOperation

current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')


class PathExistProject:

    def __init__(self, project_name, log_obj):
        self.log = log_obj
        self.project_name = project_name
        self.apps_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_path))), 'apps/')
        self.path_data = {}

    def return_path(self):
        dir_list = FileOperation().get_return_dirs_dir_or_file(self.apps_path, return_dir=True)

        # if self.project_name.upper() not in dir_list:
        if self.project_name not in map(lambda x: x, dir_list):
            self.log.error('Project: %s does not exist' % self.project_name)
            return
        project_path = self.apps_path + self.project_name
        projects_list_dir = FileOperation().return_all_name(project_path, is_dir=True)
        if len(projects_list_dir) < 11:
            self.log.error('Project: %s, Missing file directory' % self.project_name)
            self.log.error('Project: %s, Full the file directory: %s' % (self.project_name, projects_list_dir))
            return

        self.path_data["run_case_path"] = os.path.join(project_path, 'case/runcase/')
        self.path_data["test_case_path"] = os.path.join(project_path, 'case/testcase/')
        self.path_data["test_data_path"] = os.path.join(project_path, 'case/testdata/')
        self.path_data["error_images_path"] = os.path.join(project_path, 'images/errorimages/')
        self.path_data["memory_images_path"] = os.path.join(project_path, 'images/memoryimages/')
        self.path_data["logs_path"] = os.path.join(project_path, 'logs/')
        self.path_data["report_path"] = os.path.join(project_path, 'report/')
        self.path_data["function_path"] = os.path.join(project_path, 'src/function')

        for item_key in self.path_data:
            item_key_value = self.path_data[item_key]
            if not os.path.exists(item_key_value):
                self.log.error('project: %s, file path: %s does not exist' % (self.project_name, item_key_value))
                return

        self.path_data["import_module_path"] = "." + self.project_name + ".case.runcase.%s"

        # print(self.path_data["import_module_path"])
        return self.path_data


if __name__ == '__main__':
    project_name = 'MTM'
    from testframework.source.utils.logclass.logconfig import Logger

    logger = Logger(log_path=source_log_path)
    pa = PathExistProject(project_name=project_name, log_obj=logger)
    a = pa.return_path()
    print(a)
