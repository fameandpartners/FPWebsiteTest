# -*- coding: utf-8 -*-
# 参数解析


class ArgumentParser:

    def __init__(self, argv):
        self.argv = argv

    def get_arguments(self, _key):
        for item in range(len(self.argv)):
            if self.argv[item] == _key and item + 1 < len(self.argv):
                return self.argv[item + 1]
        return None

    def get_case_name(self):
        value = self.get_arguments(_key='--test_case_name')
        if value:
            # print(value)
            return value
        else:
            return None

    def get_run_case_path(self):
        value = self.get_arguments(_key='--run_case_path')
        if value:
            # print(value)
            return value
        else:
            return None

    def get_test_case_path(self):
        value = self.get_arguments(_key='--test_case_path')
        if value:
            # print(value)
            return value
        else:
            return None

    def get_test_data_path(self):
        value = self.get_arguments(_key='--test_data_path')
        if value:
            # print(value)
            return value
        else:
            return None

    def get_log_file_name(self):
        value = self.get_arguments(_key='--test_log_file_name')
        # print(value)
        if value:
            # print(value)
            return value
        else:
            return None

    def get_run_by_manager(self):
        value = self.get_arguments(_key='--run_by_manager')
        if value:
            # print(value)
            return value == 'True'
        else:
            return False


if __name__ == '__main__':
    args = ''
    argument = ArgumentParser(args)
    argument.get_case_name()
    argument.get_run_by_manager()
