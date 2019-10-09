# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from testframework.source.configs.readini import ConfigIni
from testframework.source.utils.logclass.logconfig import Logger


current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs')


class Timers():

    def __init__(self):
        self.source_logs_object = Logger(log_path=source_log_path)
        self.ini = ConfigIni(log_obj=self.source_logs_object)
        self.set_time = self.ini.get_int(section='TIMER', option='interval')

    def task(self):
        print("This is task done")
        print('\r\n')

    def start_task(self, func):

        scheduler = BackgroundScheduler()
        # scheduler = BlockingScheduler()
        scheduler.add_job(func, 'interval', seconds=self.set_time, id='task-01')  # 间隔调度
        scheduler.start()


        try:
            while True:
                if scheduler.get_job(job_id='task-01').pending != True:
                    print(scheduler.print_jobs())
                    print(scheduler.get_job(job_id='task-01'))
                    # current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
                    boo = Timers.time_refresh(_stop=True)

        except Exception as e:
            self.source_logs_object.exception(e)
            scheduler.shutdown()

    @staticmethod
    def time_refresh(_stop=None):
        if not _stop:
            while True:
                current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
                print("\r{}".format(current_time), end="", flush=True)
        else:
            print('')


def test():
    print("This is test func")


if __name__ == '__main__':
    ti = Timers()
    ti.start_task(test)
