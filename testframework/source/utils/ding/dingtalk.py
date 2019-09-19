# -*- coding: utf-8 -*-
import requests
import os
import time
from testframework.source.configs.readini import ConfigIni
from testframework.source.utils.logclass.logconfig import Logger


current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class DingTalk:

    def __init__(self, project_name, source_log_object):
        self.project_name = project_name
        self.logger = source_log_object
        self.ini = ConfigIni(log_obj=self.logger)
        self.token = self.ini.get_str(section='DINGTALK', option='token')
        self.ding_url = self.ini.get_str(section='DingTalk', option='dingurl')

    def sent_message(self, r_data):
        all_num = r_data["all_num"]
        passing_rate = r_data["passing_rate"]
        start_time = r_data["start_time"]
        total_time = r_data["total_time"]
        pass_num = r_data["pass_num"]
        fail_num = r_data["fail_num"]
        pass_item = r_data["pass_item"]
        fail_item = r_data["fail_item"]

        ding_switch = self.ini.get_bool(section='DINGTALK', option='switch')
        if not ding_switch:
            self.logger.warning("Ding talk service has been closed, will not send ding message")
            return
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        json_data = 'current_time: %s,' % time_now
        json_data += '\n' + 'description: %s  - 工程自动化测试,' % self.project_name
        json_data += '\n' + 'test_script_num: %s,' % all_num
        json_data += '\n' + 'passing_rate: %s,' % passing_rate
        json_data += '\n' + 'start_time: %s,' % start_time
        json_data += '\n' + 'total_time: %s,' % total_time
        json_data += '\n' + 'pass_num: %s,' % pass_num
        json_data += '\n' + 'fail_num: %s,' % fail_num
        json_data += '\n' + 'pass_item: %s,' % pass_item
        json_data += '\n' + 'fail_item: %s' % fail_item

        msg = json_data
        payload = {'access_token': self.token}
        data = {'msgtype': 'text', 'text': {'content': msg}}
        if self.ding_url and self.token:
            requests.post(self.ding_url, params=payload, json=data)
        else:
            source_log_object.warning('  *Please configure the DINGTALK information first')
            return


if __name__ == '__main__':
    r_data = ''

    ding = DingTalk('FPWebsite', source_log_object)
    ding.sent_message(r_data)
    # pass