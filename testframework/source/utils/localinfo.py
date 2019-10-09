# -*- coding: UTF-8 -*-
from datetime import datetime
import socket
import getpass
#import wmi
import os
#import psutil
#from pynvml import *

# c = wmi.WMI()
current_path = os.path.dirname(__file__)
source_logs_path = os.path.join(os.path.dirname(current_path), 'logs/')


class LocalInfo:

    def __init__(self, log_obj):
        self.log = log_obj
        self.current_time = datetime.now().strftime("%c")

    def get_host_ip(self):

        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            self.log.exception(e)
            return
        finally:
            s.close()

        ip = "  *主机IP   - " + ip
        self.log.info(ip)
        return ip

    def get_host_name(self):

        try:
            hostname = socket.gethostname()
            user_name = getpass.getuser()
        except Exception as e:
            self.log.exception(e)
            return

        _name = "  *主机Name - " + hostname + "  *主机User - " + user_name
        self.log.info(_name)
        return _name

    # def get_cpu(self):
    #
    #     cpu_list = []
    #     try:
    #         for cpu in c.Win32_Processor():
    #             cpu_list.append(cpu.Name)  # CpuType
    #             cpu_list.append(cpu.DataWidth)  # DataWidth
    #     except Exception as e:
    #         self.log.exception(e)
    #         return
    #
    #     cpu = "  *主机CPU  - " + cpu_list[0]
    #     self.log.info(cpu)
    #     return cpu
    #
    # # function of Get CPU State;
    # def get_process_info(self):
    #
    #     self.log.info("----------------------进程信息----------------------")
    #     plist = psutil.pids()
    #     self.log.info('进程名  |   进程bin路径  |   进程状态  |   进程开启的线程数')
    #     for p in plist:
    #         ps = psutil.Process(p)
    #         if ps.name() == 'pycharm64.exe':
    #             self.log.info(ps.name() + '  |  ' + ps.exe() + '  |  ' + ps.status() + '  |  ' + str(ps.num_threads()))
    #
    # def get_disk(self):
    #
    #     disk_list = []
    #     try:
    #         for index, disk in enumerate(c.Win32_DiskDrive()):
    #             index_item = "  *主机disk - " + disk.Caption
    #             disk_list.append(index_item)  # 硬盘驱动
    #     except Exception as e:
    #         self.log.exception(e)
    #         return
    #
    #     for item in disk_list:
    #         self.log.info(item)
    #     return disk_list

    # def get_memory(self):
    #
    #     try:
    #         phymem = psutil.virtual_memory()
    #         total = str(int(phymem.total / 1024 / 1024)) + "M"
    #         used = str(int(phymem.used / 1024 / 1024)) + "M"
    #         free = str(int(phymem.free / 1024 / 1024)) + "M"
    #         sum_mem = str(int(phymem.used / 1024 / 1024) / int(phymem.total / 1024 / 1024) * 100)
    #         sum_mem = sum_mem[0:5] + "%"
    #     except Exception as e:
    #         self.log.exception(e)
    #         return
    #
    #     memory = "  *主机内存 - " + total + "  *内存占用 - " + sum_mem
    #     # self.log.info(memory)
    #     return memory

    # def get_gpu(self):
    #
    #     try:
    #         nvmlInit()
    #         device_count = nvmlDeviceGetCount()  # 显卡数量
    #     except Exception as e:
    #         self.log.exception(e)
    #         return
    #     i = None
    #     nvm_name = None
    #     for i in range(device_count):
    #         handle = nvmlDeviceGetHandleByIndex(i)
    #         nvm_name = nvmlDeviceGetName(handle).decode()
    #         nvmlShutdown()
    #
    #     gpu = "  *主机GPU  - " + "Device: " + str(i) + ",  " + nvm_name
    #     self.log.info(gpu)
    #     return gpu

    # def get_cpu_state(self):
    #
    #     try:
    #         interval = 1
    #         cpu_state = "  *CPU使用率:" + str(psutil.cpu_percent(interval)) + "%"
    #     except Exception as e:
    #         self.log.exception(e)
    #         return
    #
    #     self.log.info(cpu_state)
    #     return cpu_state

    def main(self):
        self.get_host_ip()
        # self.get_host_name()
        # self.get_cpu()
        # self.get_disk()
        # self.get_gpu()
        # self.get_cpu_state()


# 定时器调用函数-获取内存信息，传入对应的 测试用例 logger 对象
def run_get_memory(logger_obj):
    def func():
        a = LocalInfo(log_obj=logger_obj)
        memory = a.get_memory()
        logger_obj.warning(memory)

    return func


if __name__ == '__main__':
    from testframework.source.utils.logclass.logconfig import Logger
    logger = Logger(log_path=source_logs_path)
    lo = LocalInfo(log_obj=logger)
    lo.main()
