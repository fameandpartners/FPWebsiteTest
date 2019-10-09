# -*- coding: UTF-8 -*-
import os
import time
from raven import Client
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.create_case_demo import CreateCaseDemo
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.run_testcase.start_project import StartProject
from testframework.source.templates.generate_report import Report
from testframework.source.utils.addtestcase import AddTestCase
from testframework.source.utils.ding.dingtalk import DingTalk
from testframework.source.utils.email.Smtp import Email
from testframework.source.utils.file_operation import FileOperation
from testframework.source.utils.logclass.log_process import LogProcess
from testframework.source.utils.logclass.logconfig import Logger
from testframework.source.construct_project.construct_dir import ConstructDir
from testframework.source.utils.sentry.sentry_ import Sentry
from testframework.source.utils.timer import Timers
from testframework.source.utils.verifycase import VerifyTestCase

current_path = os.path.dirname(__file__)
source_logs_path = os.path.join(current_path, 'source/logs/')
source_logs_object = Logger(log_path=source_logs_path)


class TestCaseManager:

    def __init__(self, project_name):
        self.project_name = project_name
        self.apps_path = os.path.join(current_path, 'apps/')

        self.ph = PathExistProject(project_name=project_name, log_obj=source_logs_object)
        self.path_data = self.ph.return_path()
        self.run_case_path = self.path_data["run_case_path"]
        self.log = Logger(log_path=self.path_data["logs_path"])

        self.ad = AddTestCase(self.project_name)

        self.ini = ConfigIni(log_obj=source_logs_path)

    # 创建工程
    @staticmethod
    def create_new_project(create_name):
        construct = ConstructDir(project_name=create_name, log_obj=source_logs_object)
        construct.create_apps_dir()

    def return_exist_project(self):
        if os.path.exists(self.apps_path):
            exist_project = FileOperation.get_return_dirs_dir_or_file(dirs_path=self.apps_path, return_dir=True)
            return exist_project

    def generate_test_case_file(self):
        pass

    @staticmethod
    def create_new_case(project_name, save_case_name, description, author, max_running_time, modules, screenshots):
        cr = CreateCaseDemo(project_name)
        save_case_name = save_case_name
        description = description
        author = author
        max_running_time = max_running_time
        modules = modules
        screenshots = screenshots
        cr.create_test_case(save_case_name, description, author, max_running_time, modules, screenshots)

    def add_case(self, file_path):
        self.ad.add_case(file_path)

    def del_case(self, rm_path, file_name_list):
        self.ad.del_file(rm_path, file_name_list)

    def verify_case(self, case_list):

        exist_project = self.return_exist_project()
        if '__pycache__' in exist_project:
            exist_project.remove('__pycache__')
        if self.project_name not in exist_project:
            source_logs_object.error('Select Project Error')
            return
        try:
            ver = VerifyTestCase(self.project_name, case_list)
            verify_result = ver.verify_case_()
        except Exception as e:
            raise e

        return verify_result

    def run_case(self, case_item=None, case_list=None):

        if case_item:
            pass
        case_name_list = self.ad.get_run_case()
        if case_list:
            case_name_list = case_list
        st = StartProject(self.project_name, case_name_list)
        run_log_name, _ret = st.run_case()
        for index, item in enumerate(run_log_name):
            _path, _file_name = os.path.split(item)
            run_log_name[index] = _file_name
        self.process_log(run_log_name)

    def start_(self, case_item=None, case_list=None):
        start_timer = self.ini.get_bool(section='TIMER', option='switch')

        if start_timer:
            _te = TestCaseManager(self.project_name)
            ti = Timers()
            ti.start_task(_te.run_case)
        else:
            self.run_case(case_item=case_item, case_list=case_list)

    def process_log(self, case_log_name_list):

        case_log_list = case_log_name_list
        l = LogProcess(project_name=self.project_name, case_log_list=case_log_list)
        data = l.hand_out_data()
        r_data = l.report_data(data=data)

        re = Report(source_logs_object, self.project_name)
        re.save_report(r_data)

        self.send_ding_talk(r_data)
        self.send_email()
        self.send_sentry_slack(r_data)

    def send_email(self):
        em = Email(self.project_name)
        em.send_email()

    def send_ding_talk(self, r_data):

        ding = DingTalk(self.project_name, source_logs_object)
        ding.sent_message(r_data)

    def send_sentry_slack(self, r_data):

        sen = Sentry(self.project_name)
        sen.sent_sentry(r_data)


if __name__ == '__main__':
    project_name = 'FPwebsiteTest'
    te = TestCaseManager(project_name)
    case_list = ['fpwebsite-filter.py', 'fpwebsite-Homepage_qa4.py', 'fpwebsite-search.py', 'fpwebsite-menuclassify.py']
    # case_list = ['fpwebsite-Homepage.py', 'fpwebsite-filter.py', 'fpwebsite-menuclassify.py', 'fpwebsite-ordering.py',
    #                 'fpwebsite-search.py', 'fpwebsite-shoppingbag.py', 'fpwebsite-productdetails.py']
    te.start_(case_list=case_list)

