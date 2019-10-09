# -*- coding:utf-8 -*-
# UR 主流程测试 - 函数列表
import sys
import time
import struct
import os
import re
import pickle
from source.configs.readini import ConfigIni
from source.construct_project.get_project_path import PathExistProject
from source.utils.logclass.logconfig import Logger
from source.utils.file_operation import FileOperation
from source.utils.argumentparser import ArgumentParser

project_name = 'UR'
current_path = os.path.dirname(__file__)
source_logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path)))), 'source/logs')
source_log_obj = Logger(log_path=source_logs_path)

pa = PathExistProject(project_name=project_name, log_obj=source_log_obj)
path_data = pa.return_path()
dir_test_data_path = path_data["test_data_path"]


ini = ConfigIni(log_obj=source_log_obj)
release_dir_path = ini.get_str(section='UR', option='release')
exe_path = release_dir_path + '/USM2MShell.exe'
sys.path.append(release_dir_path)