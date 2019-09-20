# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta


def set_time_run_task(func, day=0, hour=0, min=0, second=0):
    """定时函数"""

    now = datetime.now()
    str_now_time = now.strftime('%Y-%m-%d %H:%M:%S')

    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_run_time = period + now
    str_next_run_time = next_run_time.strftime('%Y-%m-%d %H:%M:%S')
    # print(str_next_run_time)

    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(str_next_run_time):
            func()
            # Get next iteration time
            iter_time = iter_now + period
            str_next_run_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')

            continue


if __name__ == '__main__':
    # set_time_run_task()
    pass