# -*- coding: utf-8 -*-
import os


class FileOperation:

    def __init__(self):
        self.list_dir = []
        self.file_name = []

    def return_all_name(self, path, is_dir=False):
        for filename in os.listdir(path):
            _path = os.path.join(path, filename)
            if os.path.isfile(_path):
                self.file_name.append(filename)
            if os.path.isdir(_path):
                self.list_dir.append(filename)
                self.return_all_name(_path)

        if not is_dir:
            return self.file_name
        return self.list_dir

    @staticmethod
    def verify_file_exist(file_path):
        pass

    @staticmethod
    def get_return_dirs_dir_or_file(dirs_path, return_dir=False):
        file_data = []
        dir_data = []
        _list = os.listdir(dirs_path)
        for file_list_item in _list:
            file_list_item_path = os.path.join(dirs_path, file_list_item)
            if os.path.isfile(file_list_item_path):
                file_data.append(file_list_item)
            if os.path.isdir(file_list_item_path):
                dir_data.append(file_list_item)
        if not return_dir:
            return file_data
        else:
            return dir_data

    @staticmethod
    def del_file_in_target_path(file_path, target_path):
        return_code = FileOperation.confirm_path_is_dir_or_file(target_path)
        if return_code[0] == 1:
            if str(file_path) in os.listdir(target_path):
                del_file_path = file_path
                if os.path.isfile(del_file_path):
                    try:
                        os.remove(del_file_path)
                    except Exception as e:
                        raise e

    @staticmethod
    def confirm_path_is_dir_or_file(_path):
        if os.path.isfile(_path):
            return [0, _path]
        elif os.path.isdir(_path):
            return [1, _path]
        else:
            return [500]

    @staticmethod
    def create_new_dir(_dir, create_dir_name):
        if os.path.isdir(_dir):
            return_data = FileOperation.get_file_name_and_suffix(create_dir_name)
            _dir = _dir + return_data[0]
        if not os.path.exists(_dir):
            try:
                # shutil.rmtree(_dir)
                # os.mkdir(_dir)
                os.makedirs(_dir)
            except Exception as e:
                raise e

    @staticmethod
    def get_file_path_and_name(full_path):
        _file_path, _file_name = os.path.split(full_path)
        return [_file_path, _file_name]

    @staticmethod
    def get_file_name_and_suffix(file_name):
        _file_name_with_no_suffix, _file_suffix = os.path.splitext(file_name)
        return [_file_name_with_no_suffix, _file_suffix]


if __name__ == '__main__':
    # f = FileOperation()
    # _dir = ''
    # return_data = f.get_return_dirs_dir_or_file(dirs_path=_dir, return_dir=False)
    # print(return_data)
    save_case_name = 'mtm-base'
    _file_name_with_no_suffix = FileOperation.get_file_name_and_suffix(save_case_name)[1]
