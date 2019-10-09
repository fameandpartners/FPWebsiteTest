# -*- coding: utf-8 -*-
# 测试用例 - 主流程测试
from time import sleep, time
import requests
from bs4 import BeautifulSoup
from apps.FPWebsite.src.function.FP_function import *
import warnings
warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 500  # 最大运行时间
author = '彭柔'  # 编写作者
date = '2019-08-02'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '链接测试'  # 归属模块
screenshots = 'True'  # 是否开启出错截图


def main(argv):
    log, run_case_name = init_fp(argv)
    driver = start_driver(1, log)
    driver.get("https://www.fameandpartners.com")
    driver.maximize_window()
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()




