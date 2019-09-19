import sys
import time
import os
import re
import requests
from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.logclass.logconfig import Logger
from testframework.source.utils.argumentparser import ArgumentParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from testframework.source.utils.screenshots.get_screenshots import GetScreenshots
import warnings
warnings.filterwarnings("ignore")

project_name = 'FPwebsiteTest'
current_path = os.path.dirname(__file__)
source_logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path)))), 'testframework/source/logs')
source_log_obj = Logger(log_path=source_logs_path)

pa = PathExistProject(project_name=project_name, log_obj=source_log_obj)
path_data = pa.return_path()

ini = ConfigIni(log_obj=source_log_obj)

# '''True->制作流程; False->测试流程'''
# _is_test_creating_ = False

'''True->界面执行; False->脚本执行'''
_is_UI_running_ = True

'''True->错误后交给用户操作; False->不'''
_is_user_op_after_fail = False

'''实际打开的产品路径'''
_product_path_ = "."

'''测试数据TestData的路径'''
_test_data_path_ = ""

_gui_application_ = None

current_time = str(int(time.time()))

# 日志打印
# def get_return_code(log_obj, msg, _code=0):
#     if _code != 0:
#         if msg:
#             log_obj.exception('  -* ERROR-Code: %s, ERROR-Mess: %s' % (_code, msg))
#             ge = GetScreenshots(project_name)
#             ge.get_screenshots(error_code=_code)
#             # exit(_code)
#     else:
#         if msg:
#             log_obj.info('  -* %s' % msg)
# 日志打印
def get_return_code(log_obj, msg, _code=0, free_shot=False):
    ge = GetScreenshots(project_name)
    if _code != 0:
        if msg:
            try:
                log_obj.exception('  -* ERROR-Code: %s, ERROR-Mess: %s' % (_code, msg))
                # ge.get_screenshots(error_code=_code)
            except Exception as e:
                log_obj.exception('  -* %s' % e)
            # finally:
            #     exit(_code)
    else:
        if msg:
            log_obj.info('  -* %s' % msg)
        if free_shot:
            ge.get_screenshots(error_code=200, code_status=True)

# 初始化信息获取
def init_fp(argv):
    # print("init_fp %s" % argv)
    argument = ArgumentParser(argv)
    log_path = argument.get_log_file_name()
    run_case_name = argument.get_case_name()
    file_path, file_name_with_suffix = os.path.split(log_path)
    _file_name = os.path.splitext(file_name_with_suffix)[0]
    log = Logger(log_path=file_path, log_name=_file_name, use_console=True)
    get_return_code(log_obj=log, msg='The main process test begins')
    url = ini.get_str(section='FPWEBSITETEST', option='url')
    return log, run_case_name, url

#打开浏览器
def start_driver(way, _log, browser='Firefox'):
    # 方式1：有界面浏览器启动，使用的是Chrome浏览器，之后需要别的浏览器再加
    # 方式3：无界面浏览器
    if way == 1:
        driver = eval(('webdriver.' + browser))()
        get_return_code(log_obj=_log, msg='Start by webdriver')
    elif way == 2:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        driver = webdriver.PhantomJS(executable_path=current_path +'/phantomjs')
        get_return_code(log_obj=_log, msg='Start by PhantomJs')
    return driver

# 定位元素，定位元素后不做任何操作
def find_element(driver, element, method,_log):
    try:
        ele = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
            lambda driver: eval('driver.find_element_by_' + method)(element))
    except TimeoutException:
        _msg = "Find element [%s] timeout" %element
        get_return_code(log_obj=_log, msg=_msg,_code=500)
        return 0
    else:
        if len(ele.text) == 0:
            _mess = "Find element [%s] successfully." % element
        else:
            _mess = "Find element [%s] successfully." % ele.text
        get_return_code(log_obj=_log, msg=_mess)
        return ele

# 定位多个元素，定位元素后不做任何操作
def find_elements(driver, element, method,_log):
    try:
        ele = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
            lambda driver: eval('driver.find_elements_by_' + method)(element))
    except TimeoutException:
        _msg = "Find elements [%s] timeout" %element
        get_return_code(log_obj=_log, msg=_msg,_code=500)
        return 0
    else:
        if len(ele.text) ==0 :
            _mess = "Find elements [%s] successfully." % element
        else:
            _mess = "Find elements [%s] successfully." % ele.text
        get_return_code(log_obj=_log, msg=_mess)
        return ele

# 输入
def input_text(driver, element, method, text,_log):
    el = find_element(driver,element, method,_log)
    el.clear()
    try:
        el.send_keys(text)
        _mess = "Input text [%s] in inputBox" % text
        get_return_code(log_obj=_log, msg=_mess)
    except Exception as e:
        _mess = "Failed to input in inputBox with %s" % e
        get_return_code(log_obj=_log, msg=_mess,_code=500)
        # get_windows_img()

# 点击元素
def click(driver, element, method,_log):
    el = find_element(driver,element, method,_log)
    if el is not 0:
        try:
            if len(el.text) == 0:
                _mess = "The element [%s] was clicked." % element
            else:
                _mess = "The element [%s] was clicked." % el.text
            el.click()
            get_return_code(log_obj=_log, msg=_mess)
        except NameError as e:
            _mess = "Failed to click the element with %s" % e
            get_return_code(log_obj=_log, msg=_mess, _code=500)

#检查网页是否正确
def check_url(driver, url, _log):
    current_url = driver.current_url
    # partial_url = current_url.split(sep="/", maxsplit=3)[3]
    if current_url == url:
        _msg = "current url [%s] is correct" %url
        get_return_code(log_obj=_log, msg=_msg)
    else:
        _msg = "current url [%s] is incorrect" %url
        get_return_code(log_obj=_log, msg=_msg,_code = 500)

#登录操作
def log_in(driver, Email, pwd, _log):
    url = ini.get_str(section='FPWEBSITETEST', option='url')
    click(driver, 'Log In / Sign Up', 'link_text', _log)
    check_url(driver, url + 'account/login', _log)
    input_text(driver, "//input[@placeholder='Email']", 'xpath', Email, _log)
    get_return_code(log_obj=_log, msg='user account is ' + Email)
    input_text(driver, "//input[@placeholder='Password']", 'xpath', pwd, _log)
    click(driver, '//*[@id="root"]/main/div/div/div[3]/form/button', 'xpath', _log)
    time.sleep(2)

# 验证元素文本值是否与期待值相同
def assert_text(driver, text, method, element, _log, correct_message, incorrect_message):
    try:
        ele = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
            lambda driver: eval('driver.find_element_by_' + method)(element))
    except TimeoutException:
        _msg = "Find element [%s] timeout" % element
        get_return_code(log_obj=_log, msg=_msg,_code = 500)
    else:
        try:
            assert text == ele.text
            get_return_code(log_obj=_log, msg=correct_message)
        except Exception as e:
            get_return_code(log_obj=_log, msg=incorrect_message.format(e),_code = 500)

# 下拉列表菜单
def dropdown_list(driver, dxpath, _log, _all=0, _number=1):
    # dxpath: dropdown_list 的xpath
    # _all: 为1表示需要点击全部的button；为0表示只点击其中的一个，并指定点击哪一个_number
    ele = find_element(driver, dxpath, 'xpath', _log)
    ele.click()
    btns_xp = dxpath.rsplit(sep='/', maxsplit=1)[0] + '/div[2]/div'
    s = find_element(driver, btns_xp, 'xpath', _log)
    selector = s.find_elements_by_tag_name('button')
    ele.click()
    if _all == 1:
        for i in range(len(selector)):
            ele.click()
            s = find_element(driver, btns_xp, 'xpath', _log)
            selector = s.find_elements_by_tag_name('button')
            selector[i].click()
            time.sleep(1)
    else:
        ele.click()
        s = find_element(driver, btns_xp, 'xpath', _log)
        selector = s.find_elements_by_tag_name('button')
        selector[_number].click()
        time.sleep(1)

#校对页面字段
# def assert_text(driver, text, method, element, _log, correct_message, incorrect_message):
#     try:
#         ele = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
#             lambda driver: eval('driver.find_element_by_' + method)(element))
#         assert text == ele.text
#         get_return_code(log_obj=_log, msg=correct_message)
#     except Exception as e:
#         get_return_code(log_obj=_log, msg=incorrect_message.format(e),_code = 500)

# 浏览器前进操作
def forward(driver,_log):
    driver.forward()
    get_return_code(log_obj=_log, msg="Click forward on current page.")

# 浏览器后退操作
def back(driver,_log):
    driver.back()
    get_return_code(log_obj=_log, msg="Click back on current page.")

# 隐式等待
def wait(driver, seconds,_log):
    driver.implicitly_wait(seconds)
    _mess ="wait for %d seconds." %seconds
    get_return_code(log_obj=_log, msg=_mess)

# 点击关闭当前窗口
def close(driver,_log):
    try:
        driver.close()
        get_return_code(log_obj=_log, msg="Close current window successfully")
    except NameError as e:
        _mess = "Failed to close current window with %s" % e
        get_return_code(log_obj=_log, msg=_mess, _code=500)

#结束进程 ，关闭所有窗口
def close_browser(driver,_log):
    try:
        driver.close()
        get_return_code(log_obj=_log, msg="Close and quit the browser.")
    except NameError as e:
        _mess = "Failed to quit the browser %s" % e
        get_return_code(log_obj=_log, msg=_mess, _code=500)

# 获得网页标题
def get_page_title(driver,_log):
    _mess = "Current page title is %s" % driver.title
    get_return_code(log_obj=_log, msg=_mess)
    return driver.title

#休眠
def sleep(seconds, _log):
    time.sleep(seconds)
    _mess = "Sleep for %d seconds" % seconds
    get_return_code(log_obj=_log, msg=_mess)


def get_status_code(driver):
    userAgent = {"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    timeOut = 10
    url = driver.current_url
    try:
        resquest = requests.get(url, headers=userAgent, timeout=timeOut)
        status = resquest.status_code
        return status
    except requests.exceptions.HTTPError as e:
        return e


def check_status_code(driver, _log):
    status = get_status_code(driver)
    if re.match(r'^2\d\d', str(status)):
        get_return_code(_log, '网页成功跳转，状态码为：%s' % status)
    elif re.match(r'^4\d\d', str(status)):
        get_return_code(_log, '网页不存在，状态码为：%s' % status, _code=500)
    elif re.match(r'^5\d\d', str(status)):
        get_return_code(_log, '服务不可用，状态码为：%s' % status, _code=500)
    else:
        get_return_code(_log, '网页跳转存在问题，状态码为：%s' % status, _code=500)

# #查找元素，找到元素后进行点击或者输入操作
# def check_element(driver, element, method, _log, operate=0, words=''):
#     # element: 如定位方式是name，则element为name；
#     # method: 元素定位方式:id,name,link_text,xpath...
#     # operate: 默认为0:click();1:send_keys(words)
#     try:
#         ele = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
#             lambda driver: eval('driver.find_element_by_' + method)(element))
#     except TimeoutException:
#         _msg = "Find element [%s] timeout" % ele.text
#         get_return_code(log_obj=_log, msg=_msg,_code = 500)
#     else:
#         _msg = "Find element [%s] successfully" % ele.text
#         get_return_code(log_obj=_log, msg=_msg)
#         if operate == 1:
#             ele.clear()
#             try:
#                 ele.send_keys(words)
#                 _mess = "Had type [%s] in inputBox" % words
#                 get_return_code(log_obj=_log, msg=_mess)
#             except NameError as e:
#                 _mess = "Failed to type in input box with %s" % e
#                 get_return_code(log_obj=_log, msg=_mess, _code=500)
#         else:
#             try:
#                 ele.click()
#                 _mess = "The element [%s] was clicked." %element
#                 get_return_code(log_obj=_log, msg=_mess)
#             except NameError as e:
#                 _mess = "Failed to click the element with %s" % e
#                 get_return_code(log_obj=_log, msg=_mess, _code=500)
