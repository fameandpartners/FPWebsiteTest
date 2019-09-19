# -*- coding: utf-8 -*-
# logger 异常信息记录
# 需要传入三个参数
# logger_path ：目标日志的记录位置，为项目内公共日志
# _view：出错视图
# _error：出错的原因
from testframework.source.utils.logclass.logconfig import Logger
from testframework.source.utils.screenshots.get_screenshots import GetScreenshots

project_name = ''


def get_return_code(log_obj, msg='', _code=0, free_shot=False):
    ge = GetScreenshots(project_name)
    if _code != 0:
        if msg:
            try:
                log_obj.exception('  -* ERROR-Code: %s, ERROR-Mess: %s' % (_code, msg))
                ge.get_screenshots(error_code=_code, code_status=False)
            except Exception as e:
                log_obj.exception('  -* %s' % e)
            finally:
                exit(_code)
    else:
        if msg:
            log_obj.info('  -* %s' % msg)
        if free_shot:
            ge.get_screenshots(error_code=200, code_status=True)


# def get_return_code(log_obj, msg, _code=0):
#     if _code != 0:
#         if msg:
#             log_obj.exception('  -* ERROR-Code: %s, ERROR-Mess: %s' % (_code, msg))
#             exit(500)
#     else:
#         if msg:
#             log_obj.info('  -* %s' % msg)


def write_logs(_view, _msg, logger_path=None, logger_obj=None):
    """
    1，记录info信息，打印logs
    # x = sys._getframe().f_code.co_filename
    # xx = sys._getframe().f_code.co_name
    # xxx = sys._getframe().f_lineno
    # msg = 'This is file path: %s, function: %s, location: %s' % (x, xx, xxx)
    :param _view:
    :param _msg:
    :return:
    """
    if logger_path:
        logger = Logger(log_path=logger_path)
    else:
        logger = logger_obj
    logger.info('  *INFO-VIEW - - %s' % _view)
    logger.info('  *INFO-MESS - - %s' % _msg)


def exception_logs(_error, logger_path=None, logger_obj=None):
    """
    1，记录异常信息，打印logs
    :param _error:
    :return:
    """
    if logger_path:
        logger = Logger(log_path=logger_path)
    else:
        logger = logger_obj
    logger.log('--- --- --- --- --- --- --- separator --- --- --- --- --- --- ---')
    logger.exception('  *ERROR-MESS - - \n%s', _error)


# 脚本统一打印信息函数
# def get_return_code(log_obj, msg='', _code=None):
#     if _code != 0:
#         import traceback
#         import sys
#
#         exc = sys.exc_info()[0]
#         stack = traceback.extract_stack()[:-1]
#         if exc:  # i.e. if an exception is present
#             del stack[-1]  # remove call of full_stack, the printed exception
#         trc = '\nTraceback (most recent call last):'
#         stack_str = trc + ''.join(traceback.format_list(stack))
#         stack_str += '' + traceback.format_exc().lstrip(trc)
#         if msg:
#             log_obj.error('  -*ERROR-Mess: %s' % msg + stack_str)
#             exit(500)
#         else:
#             log_obj.error('  -*ERROR-Mess: %s' % exc + stack_str)
#             exit(500)
#     else:
#         if msg:
#             log_obj.info('  -* %s' % msg)
