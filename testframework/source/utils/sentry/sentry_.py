# -*- coding: utf-8 -*-
import time
from raven import Client
import os
from testframework.source.configs.readini import ConfigIni
from testframework.source.utils.logclass.logconfig import Logger


current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'logs')
source_log_object = Logger(log_path=source_log_path)


class Sentry:

    def __init__(self, project_name):
        self.project_name = project_name
        self.logger = source_log_object
        self.ini = ConfigIni(log_obj=source_log_object)


    def sent_sentry(self, r_data):

        all_num = r_data["all_num"]
        passing_rate = r_data["passing_rate"]
        start_time = r_data["start_time"]
        total_time = r_data["total_time"]
        pass_num = r_data["pass_num"]
        fail_num = r_data["fail_num"]
        pass_item = r_data["pass_item"]
        fail_item = r_data["fail_item"]

        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sentry_switch = self.ini.get_bool(section='SENTRY', option='switch')
        if not sentry_switch:
            self.logger.warning("Sentry service has been closed, will not send sentry message")
            return
        sentry_url = self.ini.get_bool(section='SENTRY', option='url')
        client = Client(sentry_url)

        json_data = 'Results for FPWebsite autotest'
        json_data += '\n' + 'current_time: %s,' % time_now
        json_data += '\n' + 'description: %s  - 工程自动化测试,' % self.project_name
        json_data += '\n' + 'test_script_num: %s,' % all_num
        json_data += '\n' + 'passing_rate: %s,' % passing_rate
        json_data += '\n' + 'start_time: %s,' % start_time
        json_data += '\n' + 'total_time: %s,' % total_time
        json_data += '\n' + 'pass_num: %s,' % pass_num
        json_data += '\n' + 'fail_num: %s,' % fail_num
        # json_data += '\n' + 'pass_item: %s,' % pass_item
        # json_data += '\n' + 'fail_item: %s' % fail_item
        msg = json_data
        client.captureMessage(msg)



if __name__ == '__main__':
    project_name = 'FPwebsiteTest'
    sen = Sentry(project_name)
    r_data = ''
    sen.sent_sentry(r_data)
