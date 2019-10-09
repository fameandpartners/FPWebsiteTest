# -*- coding: utf-8 -*-
# 获取 return code
from threading import Thread
from multiprocessing import Pool, Manager, Process


def test(begin, end):
    i = 0
    for item in range(begin, end):
        i += 1

    return i


class ReturnCodeThread(Thread):

    def __init__(self, func, args):
        super().__init__()
        self.args = args
        self.func = func
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            raise e


def main():
    p = Pool()
    result = p.apply_async(test, args=(1, 6))
    p.close()
    p.join()
    a = result.get()
    print(a)


import multiprocessing
from multiprocessing import Manager


def worker(return_dict):
    num = 6
    num2 = 7
    return_dict.append(num)
    return_dict.append(num2)


if __name__ == '__main__':
    manager = Manager()
    return_list = manager.list()
    p = multiprocessing.Process(target=worker, args=(return_list,))
    p.start()
    p.join()
    print(return_list)


# if __name__ == '__main__':
#     # t1 = ReturnCodeThread(test, args=(1, 6))
#     # t1.start()
#     # t1.join()
#     main()
