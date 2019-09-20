# -*- coding: utf-8 -*-
# 引入网页驱动  chrome 版本 75.0.3770.100（正式版本） （32 位）
import time
import sys
from selenium import webdriver as web_driver
from selenium.common.exceptions import NoSuchElementException
from apps.FPWebsite.src.function.FP_function import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import  WebDriverWait
from selenium.webdriver.support.select import Select
# driver = web_driver.PhantomJS(executable_path='C:\\Users\\TuhuaC\Desktop\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
import warnings
warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 500  # 最大运行时间
author = 'Test'  # 编写作者
date = '2019-06-03'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '主流程'  # 归属模块
screenshots = 'False'  # 是否开启出错截图

def main(argv):
    log, run = init_fp(argv)
    driver = web_driver.Chrome()  # Chrome(), Firefox()
    driver.get('https://www.fameandpartners.com/')
    driver.maximize_window()
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()
    sleep(1, log)

    click(driver, 'Log In / Sign Up', 'link_text', log)
    click(driver, 'Create a new account', 'link_text', log)
    check_url(driver, 'account/signup', log)

    input_text(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[1]/input[1]', 'xpath', '高', log)
    input_text(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[2]/input[1]', 'xpath', '超', log)
    input_text(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[3]/input[1]', 'xpath', 'g543410475@163.com', log)
    input_text(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[4]/div[1]/input[1]', 'xpath', 'gaochao1',log)
    click(driver, "/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/button[1]/span[1]", 'xpath', log)
    time.sleep(2)


if __name__ == '__main__':
    main(sys.argv)