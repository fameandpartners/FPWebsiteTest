# -*- coding: utf-8 -*-
# log 日志处理模块
import re
import time
#import matplotlib.pyplot as plt
from datetime import datetime
import os
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.templates.generate_report import Report
from testframework.source.utils.logclass.logconfig import Logger

current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class LogProcess:

    def __init__(self, project_name, case_log_list):
        pa = PathExistProject(project_name=project_name, log_obj=source_log_object)
        self.path_data = pa.return_path()
        self.source_log = source_log_object

        self.dir_logs_path = self.path_data["logs_path"]
        self.dir_m_image_path = self.path_data["memory_images_path"]
        self.case_log_list = case_log_list
        self.now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.coll_data = {}
        self.start_time = ''

    def hand_out_data(self):

        for case_log_item in self.case_log_list:

            case_data = {}
            _case_name = case_log_item.split('-' + self.now_time)[0].strip()
            self.coll_data[_case_name] = case_data

            open_case_log_item_path = self.dir_logs_path + case_log_item
            with open(open_case_log_item_path, 'r', encoding='utf8') as f:
                original_data = f.readlines()



                # 获取运行时间
                start_time_info, ip = original_data[0].split(' -   *主机IP   - ')
                start_time = start_time_info.split(self.now_time)[1].strip()
                end_time_info, _code = original_data[-1].split('-   *End of the process')
                end_time = end_time_info.split(self.now_time)[1].strip()
                if case_log_item == self.case_log_list[0]:
                    self.start_time = start_time
                s = datetime.strptime('%s %s' % (self.now_time, start_time), "%Y-%m-%d %H:%M:%S,%f")
                start_time = int(time.mktime(s.timetuple()))
                e = datetime.strptime('%s %s' % (self.now_time, end_time), "%Y-%m-%d %H:%M:%S,%f")
                end_time = int(time.mktime(e.timetuple()))
                total_time = end_time - start_time
                case_data["total_time"] = total_time

                # 获取脚本是否运行成功
                return_code = _code.split('Return code:')[1].strip()
                result_data = {}
                memory_data = {}
                memory_data["x_data"] = []
                memory_data["y_data"] = []
                case_data["result"] = result_data
                case_data["memory_data"] = memory_data

                # 内存信息获取
                error_list = []
                result_data["code"] = 0
                original_data_length = len(original_data)
                for index, original_data_item in enumerate(original_data):

                        if re.match(r'^WARNING', original_data_item):
                            _x_time, _y_memory = original_data_item.split(' -   *主机内存 - ')
                            _x_time_data = _x_time.split(self.now_time)[1].strip()
                            _y_memory_data = _y_memory.split('*内存占用 - ')[1].strip()
                            _y_memory_data = _y_memory_data.split('%')[0].strip()
                            memory_data["x_data"].append(_x_time_data)
                            memory_data["y_data"].append(float(_y_memory_data))

                        if re.match('^ERROR -', original_data_item):
                            error_list.append(original_data[index])
                            current_error_index = index
                            while True:
                                current_error_index += 1
                                if current_error_index < original_data_length:
                                    data = original_data[current_error_index]
                                    if not re.match(r'^WARNING -', data) and not re.match(r'^INFO -', data) and not re.match(r'^ERROR -', data):
                                        error_list.append(data)
                                    else:
                                        break
                                else:
                                    break
                            result_data["code"] = 500

                error_msg = ''
                for error_item in error_list:
                    error_msg += error_item
                result_data["error_msg"] = error_msg
                x_data = memory_data["x_data"]
                y_data = memory_data["y_data"]
                # self.get_scatter_diagram(case_log_name=case_log_item, x_data=x_data, y_data=y_data)

        return self.coll_data

    def report_data(self, data):
        r_data = {}
        # data = self.hand_out_data()
        total_time = 0
        pass_num = 0
        fail_num = 0
        all_num = 0
        passing_rate = 0
        pass_item = []
        fail_item = []
        for index_key in data:
            total_time += data[index_key]['total_time']
            code = data[index_key]['result']['code']
            if code == 0:
                pass_num += 1
                pass_item.append({"pass_case_name": index_key,
                                  "p_id": "pt2_%s" % pass_num})
            else:
                fail_num += 1
                fail_item.append({"fail_case_name": index_key,
                                  "f_id": "ft2_%s" % fail_num,
                                  "fail_message": data[index_key]['result']['error_msg']})

        all_num = pass_num + fail_num
        passing_rate = '%.2f%%' % (pass_num * 100 / all_num)
        r_data["total_time"] = '%s' % str('{:.0f}分{:.0f}秒'.format(total_time // 60, total_time % 60))
        r_data["pass_num"] = pass_num
        r_data["fail_num"] = fail_num
        r_data["all_num"] = all_num
        r_data["passing_rate"] = passing_rate
        r_data["pass_item"] = pass_item
        r_data["fail_item"] = fail_item
        r_data["start_time"] = self.start_time

        return r_data

   


if __name__ == '__main__':
    project_name = 'FPWebsite'
    case_log_list = ['fpwebsite-filter-2019-08-15-18-40-50.log']
    l = LogProcess(project_name=project_name, case_log_list=case_log_list)
    data = l.hand_out_data()
    r_data = l.report_data(data=data)

    data = {
        "project_title": "自动化测试",
        "author_name": "XXXXX",
        "start_time": r_data["start_time"],
        "total_time": r_data["total_time"],
        "passing_rate": r_data["passing_rate"],
        "pass_num": r_data["pass_num"],
        "fail_num": r_data["fail_num"],
        "all_num": r_data["all_num"],
        "pass_item": r_data["pass_item"],
        "fail_item": r_data["fail_item"]
    }

    re = Report(l, project_name)
    r_data = ''
    re.save_report(r_data)
