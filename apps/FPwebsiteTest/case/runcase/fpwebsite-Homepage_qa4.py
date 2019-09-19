# -*- coding: utf-8 -*-
# 引入网页驱动  chrome 版本 75.0.3770.100（正式版本） （32 位）
import warnings
import sys
import os
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))
sys.path.append(project_path)
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from apps.FPwebsiteTest.src.function.FP_function import *
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver as web_driver
import time

# driver = web_driver.PhantomJS(executable_path='C:\\Users\\TuhuaC\Desktop\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
warnings.filterwarnings("ignore")


# 脚本信息
max_running_time = 500  # 最大运行时间
author = 'Test'  # 编写作者
date = '2019-06-03'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '主流程'  # 归属模块
screenshots = 'False'  # 是否开启出错截图


def main(argv):
    try:
        log, run, url = init_fp(argv)
        driver = start_driver(3, log)  # Chrome(), Firefox()
        # 官方网址
        # driver.get('https://www.fameandpartners.com/')

        # 测试网址
        url = 'https://qa4.fameandpartners.com/'
        base_url = url
        driver.get(url)

        driver.maximize_window()
        close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
            lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
        close_bth.click()
        sleep(5, log)
        # 登录
        click(driver, 'Log In / Sign Up', 'link_text', log)
        check_url(driver, base_url + 'account/login', log)
        log_in(driver, '543410475@qq.com', 'gaocaho1', log)
        time.sleep(0.5)

        # 测试网站
        user = driver.find_element_by_xpath(
            '/html[1]/body[1]/div[1]/div[1]/header[1]/nav[1]/ul[2]/li[1]/div[1]/span[1]/a[1]')
        ActionChains(driver).move_to_element(user).perform()
        click(driver, 'My Account', 'link_text', log)
        back(driver, log)

        # element = WebDriverWait(driver, 10).until(lambda x:x.find_element_by_css_selector("div.jsx-416275461.wrapper header.jsx-2507546937.Header.Header--background-light-pink nav.jsx-2507546937.Header__Content ul.jsx-2876305034.header-action-buttons li.jsx-2876305034.user-menu-wrapper:nth-child(1) div:nth-child(1) span.DropdownContainer__Trigger--open > a.UserMenu__Trigger.no-underline"))
        # 测试
        user = driver.find_element_by_xpath(
            '/html[1]/body[1]/div[1]/div[1]/header[1]/nav[1]/ul[2]/li[1]/div[1]/span[1]/a[1]')
        ActionChains(driver).move_to_element(user).perform()
        click(driver, 'Orders', 'link_text', log)
        back(driver, log)

        # #帮助
        click(driver, "About Us", 'link_text', log)
        check_url(driver, base_url + 'about', log)
        click(driver, "Contact Us", 'link_text', log)
        check_url(driver, base_url + 'contact', log)
        click(driver, "FAQs", 'link_text', log)
        check_url(driver, base_url + 'faqs', log);
        click(driver, "Size Guide", 'link_text', log)
        check_url(driver, base_url + 'size-guide', log)
        click(driver, "Privacy Policy", 'link_text', log)
        check_url(driver, base_url + 'privacy', log)
        click(driver, "Terms", 'link_text', log)
        check_url(driver, base_url + 'terms', log)
        click(driver, "Returns Policy", 'link_text', log)
        check_url(driver, base_url + 'faqs/returns', log)

        # 测试网址
        click(driver, "/html[1]/body[1]/div[1]/div[1]/footer[1]/div[1]/div[4]/ul[1]/li[8]/a[1]", 'xpath', log)
        check_url(driver, base_url + 'contact', log)

        #
        # #文字导航

        # 测试网址
        click(driver, "/html[1]/body[1]/div[1]/div[1]/header[1]/nav[1]/a[1]/*", 'xpath', log)
        click(driver, "Fame & Partners X Atlanta de Cadenet Taylor", 'link_text', log)
        check_url(driver, base_url + 'atlanta', log)
        # click(driver, "/html[1]/body[1]/div[3]/div[1]/header[1]/nav[1]/a[1]/*", 'xpath', log)
        back(driver, log)
        #
        click(driver, "Express Delivery", 'link_text', log)
        check_url(driver, base_url + 'dresses/express-delivery-dresses', log)
        # click(driver, "/html[1]/body[1]/div[3]/header[1]/nav[1]/a[1]/*", 'xpath', log)
        back(driver, log)

        click(driver, "Summer", 'link_text', log)
        check_url(driver, base_url + 'dresses/spring-summer', log)
        # click(driver, "/html[1]/body[1]/div[3]/header[1]/nav[1]/a[1]/*", 'xpath', log)
        back(driver, log)

        click(driver, "Wedding Guests", 'link_text', log)
        check_url(driver, base_url + 'dresses/wedding-guests', log)
        # click(driver, "/html[1]/body[1]/div[3]/header[1]/nav[1]/a[1]/*", 'xpath', log)
        back(driver, log)

        click(driver, "Evening Gowns", 'link_text', log)
        check_url(driver, base_url + 'dresses/evening', log)
        # click(driver, "/html[1]/body[1]/div[3]/header[1]/nav[1]/a[1]/*", 'xpath', log)
        back(driver, log)

        # 测试网址
        click(driver, "/html[1]/body[1]/div[1]/div[1]/div[1]/span[1]/p[1]/span[1]/a[1]", 'xpath', log)
        check_url(driver, base_url + 'dresses/express-delivery-dresses', log)
        # click(driver, "/html[1]/body[1]/div[3]/header[1]/nav[1]/a[1]/*", 'xpath', log)
        back(driver, log)
        #
        # # 切换城市

        # 测试网址
        select = driver.find_element_by_xpath(
            "/html[1]/body[1]/div[1]/div[1]/footer[1]/div[1]/div[6]/form[1]/div[1]/select[1]")
        select = Select(select)
        select.select_by_index(1)
        time.sleep(5)

        # 关闭Facebook

        # 测试网址
        click(driver, "/html[1]/body[1]/div[1]/div[1]/footer[1]/div[1]/div[3]/div[1]/a[1]/*", 'xpath', log)
        windows = driver.current_window_handle  # 定位当前页面句柄
        driver.switch_to.window(windows)

        # 关闭Ins

        # 测试网址
        click(driver, "/html[1]/body[1]/div[1]/div[1]/footer[1]/div[1]/div[3]/div[1]/a[2]/*", 'xpath', log)
        windows = driver.current_window_handle  # 定位当前页面句柄
        driver.switch_to.window(windows)

        # 关闭twitter

        # 测试网址
        click(driver, "/html[1]/body[1]/div[3]/div[1]/footer[1]/div[1]/div[3]/div[1]/a[3]/*", 'xpath', log)
        windows = driver.current_window_handle  # 定位当前页面句柄
        driver.switch_to.window(windows)
        time.sleep(5)

        # print(driver.page_source)
        # driver.close()
        # driver.page_source
    except Exception:
        pass
    finally:
        driver.quit()

    # print(driver.page_source)
    # driver.close()
    # driver.page_source


if __name__ == '__main__':
    main(sys.argv)
