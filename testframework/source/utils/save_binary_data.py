# -*- coding: utf-8 -*-
# 将数据转换成二进制数据
import os
import pickle
current_path = os.path.dirname(__file__)
data_path = current_path + '/data/'


def seva_binary_data(run_compare_data, _test_file_name):
    file_name = data_path + str(_test_file_name) + '.data'
    with open(file_name, 'wb') as f:
        pickle.dump(run_compare_data, f)


def load_compare_data(current_test_point_file_name):
    test_point_path = data_path + str(current_test_point_file_name) + '.data'
    with open(test_point_path, 'rb') as f:
        original_data = pickle.load(f)
    print(original_data)
    print(type(original_data))


if __name__ == '__main__':
    current_test_point_file_name = 'compare_data_1'
    load_compare_data(current_test_point_file_name)
