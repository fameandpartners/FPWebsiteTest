# -*- coding: utf-8 -*-
# 样式加载


class QssTools:

    @classmethod
    def set_qss_to_object(cls, file_path, obj):
        with open(file_path, 'r') as f:
            obj.setStyleSheet(f.read())


if __name__ == '__main__':
    pass

