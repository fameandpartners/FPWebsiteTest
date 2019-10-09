# -*- coding: UTF-8 -*-
# logger 类
# 初始化 logger 对象 需要传入 日志路径， 日志名不传默认为时间戳
import logging.config
import logging
import time
import os

current_path = os.path.dirname(__file__)


class Logger:

    def __init__(self, log_path, use_console=True, log_name=None):
        # self.log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        # self.log_format = '%(levelname)s - %(message)s- %(asctime)s'
        self.log_format = '%(levelname)s - %(asctime)s - %(message)s'
        self.logger = logging.getLogger(__name__)

        # 设置日志存放路径
        self.__log_path = log_path

        # 获取日志的文件名，默认为当前日期
        if not log_name:
            self.__log_name = time.strftime("%Y-%m-%d.log", time.localtime())
        else:
            # self.__log_name = time.strftime(log_name + "-%Y-%m-%d.log", time.localtime())
            (_name, _name_suffix) = os.path.splitext(log_name)
            self.__log_name = _name + '.log'

        self.log_file_path = os.path.join(self.__log_path, self.__log_name)

        # 清空当前文件的logging
        logging.Logger.manager.loggerDict.pop(__name__)
        self.logger.handlers = []  # 清空当前文件的handlers
        self.logger.removeHandler(self.logger.handlers)  # 再次移除当前文件logging配置

        # 如果logger.handlers列表为空，则添加，否则，直接写日志
        if not self.logger.handlers:
            self.handler = logging.FileHandler(self.log_file_path, encoding='utf8')
            self.logger.setLevel(logging.INFO)  # DEBUG
            formatter = logging.Formatter(self.log_format)
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)

            if use_console:  # 控制台打印日志
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter(self.log_format))
                self.logger.addHandler(console_handler)

    # 重写方法 并且每次记录后清除logger
    def debug(self, message=None):
        # self.__init__()
        self.logger.debug(message)
        self.logger.removeHandler(self.logger.handlers)

    def warning(self, message=None):
        # self.__init__()
        self.logger.warning(message)
        self.logger.removeHandler(self.logger.handlers)

    def info(self, message=None):
        # self.__init__()
        self.logger.info(message)
        self.logger.removeHandler(self.logger.handlers)

    def error(self, message=None):
        # self.__init__()
        self.logger.error(message)
        self.logger.removeHandler(self.logger.handlers)

    def exception(self, message=None, exc_info=True, *args, **kwargs):
        # self.__init__()
        # self.logger.error(message)
        self.logger.error(message, *args, exc_info=exc_info, **kwargs)
        self.logger.removeHandler(self.logger.handlers)

    def critical(self, message=None):
        # self.__init__()
        self.logger.critical(message)
        self.logger.removeHandler(self.logger.handlers)

    # 打印全局日志
    def log(self, message=None):
        # self.__init__()
        self.logger.info(message)
        self.logger.removeHandler(self.logger.handlers)


if __name__ == '__main__':
    # logger = Logger()
    pass
