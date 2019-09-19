# -*- coding: utf-8 -*-
# 启动
import importlib
import os
import sys
import threading
from subprocess import call, TimeoutExpired
import time
from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.localinfo import LocalInfo
from testframework.source.utils.logclass.logconfig import Logger
from testframework.source.utils.file_operation import FileOperation
from testframework.source.utils.stop_thread import stop_thread
from testframework.source.utils.time_decorator import set_time_run_task
current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class StartProject:

    def __init__(self, project_name, case_name_list):
        self.project_name = project_name
        self.case_name_list = case_name_list

        self.pt = PathExistProject(project_name, source_log_object)
        self.project_path = self.pt.return_path()

        self.logger = Logger(log_path=self.project_path["logs_path"])

        ini = ConfigIni(log_obj=source_log_object)
        self.exe_path = ini.get_str(section=self.project_name.upper(), option='shellexe')
        # self.exe_path = ini.get_str(section=self.project_name, option='release') + '/USM2MShell.exe'

        # collect log
        self.run_log_name = []

    def run_case(self, return_list=None):
        ret = 0
        dir_path = self.project_path["import_module_path"]
        run_case_path = self.project_path["run_case_path"]
        test_case_path = self.project_path["test_case_path"]
        test_data_path = self.project_path["test_data_path"]

        for case_item in self.case_name_list:

            case_name = FileOperation.get_file_name_and_suffix(case_item)[0]
            current_case_path = run_case_path + case_item

            # create log object
            logger_path = self.project_path["logs_path"]
            current_time = time.strftime("-%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
            current_log_name = self.project_path["logs_path"] + case_name + current_time + '.log'
            log_path = logger_path + current_log_name
            current_log_object = Logger(log_path=logger_path, log_name=current_log_name)

            self.run_log_name.append(current_log_name)

            lo = LocalInfo(log_obj=current_log_object)
            lo.main()

            # t1 = threading.Thread(target=set_time_run_task, args=(run_get_memory(current_log_object), 0, 0, 0, 5), )
            # t1.setDaemon(True)
            # t1.start()
            try:

                case_module = importlib.import_module(dir_path % case_name, package='apps')
                # case_module = importlib.import_module(".FPwebsiteTest.case.runcase.fpwebsite-Homepage", package='apps')
            except Exception as e:
                self.logger.exception(e)
                return

            if case_module.screenshots == 'False':
                current_log_object.info('  -*Case name: %s, screenshots = False' % case_item)

            # args = self.exe_path + ' --script_file ' + current_case_path
            args = self.exe_path + ' ' + current_case_path
            args += ' --test_log_file_name ' + current_log_name
            args += ' --test_case_name ' + case_item
            args += ' --test_case_path ' + test_case_path
            args += ' --run_case_path ' + run_case_path
            args += ' --test_data_path ' + test_data_path
            args += ' --run_by_manager ' + 'True'
            # args = [self.exe_path, current_case_path, ' --test_log_file_name ', current_log_name, ' --test_case_name ', case_item, ' --test_case_path ', test_case_path]
            # args.split()
            # print('This is argv %s' % args)
            # print(args)
            args = args.split()

            try:
                ret = call(args=args, timeout=int(case_module.max_running_time))

            except TimeoutExpired as e:
                current_log_object.error('  *测试超时')
                current_log_object.exception(e)
                ret = 500
                current_log_object.error('  *End of the process, Test Failed. Return code: %s' % ret)
                # if return_list:
                #     return_list.append([self.run_log_name, ret])
                return self.run_log_name, ret
                # return return_list
            except Exception as e:
                # stop_thread(t1)
                current_log_object.exception(e)
                ret = 500
                current_log_object.error('  *End of the process, Test Failed. Return code: %s' % ret)
                # if return_list:
                #     return_list.append([self.run_log_name, ret])
                return self.run_log_name, ret
                # return return_list

            if ret == 0:
                # stop_thread(t1)
                current_log_object.info('  *End of the process, software opens successfully. Return code: %s' % ret)
            else:
                # stop_thread(t1)
                current_log_object.error('  *End of the process, Test Failed. Return code: %s' % ret)

            # if return_list:
            #     return_list.append([self.run_log_name, ret])

        return self.run_log_name, ret
        # return return_list


if __name__ == '__main__':
    pass
    # project_name = 'MTM'
    # # case_name_list = ['mtm-base.py']
    # case_name_list = ['mtm-base.py', 'mtm-base_test.py']
    # st = StartProject(project_name, case_name_list)
    # run_log_name = st.run_case()
    # print(run_log_name)