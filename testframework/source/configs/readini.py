# -*- coding:utf-8 -*-
# 读取 ini 类型的配置文件
import os
import configparser
from testframework.source.utils.logclass.logconfig import Logger

current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(current_path), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ConfigIni:
    """ini config operation"""

    def __init__(self, log_obj):
        self.con = MyConfigParser()
        self.absolute_config_path = os.path.join(current_path, 'absolute.ini')
        self.log = log_obj

    def get_section(self):
        try:
            self.con.read(self.absolute_config_path, encoding='utf-8')
        except Exception as e:
            self.log.exception('config.ini read failed, Error: %s' % str(e))
            return
        sections_list = self.con.sections()
        return self.con, sections_list

    def get_str(self, section, option):
        cf, sections_list = self.get_section()
        try:
            ret = cf.get(section.upper(), option)
            if not ret:
                return None
            else:
                return ret
        except Exception as e:
            self.log.exception(e)
            return

    def get_int(self, section, option):
        cf, sections_list = self.get_section()
        try:
            ret = cf.getint(section, option)
            if str(ret).strip() not in ['', 'None', 'False']:
                return ret
            else:
                return None
        except Exception as e:
            self.log.exception(e)
            return

    def get_float(self, section, option):
        cf, sections_list = self.get_section()
        try:
            ret = cf.getfloat(section, option)
            if str(ret).strip() not in ['', 'None', 'False']:
                return ret
            else:
                return None
        except Exception as e:
            self.log.exception(e)
            return

    def get_bool(self, section, option):
        cf, sections_list = self.get_section()
        try:
            ret = cf.getboolean(section, option)
            return ret
        except Exception as e:
            self.log.exception('bool value only [0, 1, True, False], Error:%s' % str(e))
            return

    def update_data(self, section, option, value):
        cf, sections_list = self.get_section()
        try:
            cf.set(section, option, value)
            cf.write(open(self.absolute_config_path, "w+", encoding='utf-8'))
            return True
        except Exception as e:
            self.log.exception(e)
            return

    def add_data(self, section, option, value):
        cf, sections_list = self.get_section()
        try:
            _section = cf.has_section(section=section)
            if not _section:
                cf.add_section(section)
            cf.set(section, option, value)
            cf.write(open(self.absolute_config_path, "w+"))
            return True
        except Exception as e:
            self.log.exception(e)
            return


if __name__ == '__main__':
    # pass
    ini = ConfigIni(log_obj=source_log_object)
    project_name = 'MTM'
    # _re = ini.get_str(section=project_name, option=project_name.lower())

    # _int = ini.get_int(section='UR', option='_int')
    # _float = ini.get_float(section='UR', option='_float')
    # _bool = ini.get_bool(section='UR', option='_bool')
    # _str = ini.get_str(section='UR', option='_None')

    # ini.update_data(section='XXX', option='BBB', value='1234')
    # ini.add_data(section='CAD', option='aaa', value='xxx')
