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
    sleep(1,log)
    log_in(driver, '543410475@qq.com', 'gaocaho1', log)
    time.sleep(0.5)


    click(driver, "About Us", 'link_text', log)
    check_url(driver, 'about', log)
    click(driver, "Contact Us", 'link_text', log)
    check_url(driver, 'contact', log)
    click(driver, "FAQs", 'link_text', log)
    check_url(driver, 'faqs', log)
    click(driver, "Size Guide", 'link_text', log)
    check_url(driver, 'size-guide', log)
    click(driver, "Privacy Policy", 'link_text', log)
    check_url(driver, 'privacy', log)
    click(driver, "Terms", 'link_text', log)
    check_url(driver, 'terms', log)
    click(driver, "Returns Policy", 'link_text', log)
    check_url(driver, 'faqs/returns', log)
    click(driver, "customerservice@fameandpartners.com", 'link_text', log)
    check_url(driver, 'contact', log)

    click(driver, "Fame & Partners X Atlanta de Cadenet Taylor", 'link_text', log)
    check_url(driver, 'atlanta', log)
    click(driver, '/html[1]/body[1]/div[3]/div[1]/header[1]/nav[1]/a[1]/*', 'xpath', log)

    click(driver, "Express Delivery", 'link_text', log)
    check_url(driver, 'dresses/express-delivery-dresses', log)
    click(driver, '/html[1]/body[1]/div[3]/header[1]/nav[1]/a[1]/*', 'xpath', log)

    click(driver, "Summer", 'link_text', log)
    check_url(driver, 'dresses/spring-summer', log)
    click(driver, '/html[1]/body[1]/div[1]/header[1]/nav[1]/a[1]/*', 'xpath', log)

    click(driver, "Wedding Guests", 'link_text', log)
    check_url(driver, 'wedding-guests', log)
    click(driver, '/html[1]/body[1]/div[3]/header[1]/nav[1]/a[1]/*', 'xpath', log)

    click(driver, "Evening Gowns", 'link_text', log)
    check_url(driver, 'dresses/evening', log)
    click(driver, '/html[1]/body[1]/div[1]/header[1]/nav[1]/a[1]/*', 'xpath', log)


    # select = driver.find_element_by_xpath("//*[@id='root']/main/div/section[1]/div/div[1]/div/div/select")
    # select = Select(select)
    # select.select_by_index(0)
    # time.sleep(5)

    # time.sleep(0.5)
    # # element = WebDriverWait(driver, 10).until(lambda x:x.find_element_by_css_selector("div.jsx-416275461.wrapper header.jsx-2507546937.Header.Header--background-light-pink nav.jsx-2507546937.Header__Content ul.jsx-2876305034.header-action-buttons li.jsx-2876305034.user-menu-wrapper:nth-child(1) div:nth-child(1) span.DropdownContainer__Trigger--open > a.UserMenu__Trigger.no-underline"))
    # user = driver.find_element_by_xpath( '/html[1]/body[1]/div[3]/div[1]/header[1]/nav[1]/ul[2]/li[1]/div[1]/span[1]/a[1]')
    # ActionChains(driver).move_to_element(user).perform()
    # check_element(driver, 'Log Out', 'link_text', log)
    #
    # check_element(driver, 'Log In / Sign Up', 'link_text', log)
    # check_element(driver, 'Create a new account', 'link_text', log)
    # check_url(driver, 'account/signup', log)
    #
    # check_element(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[1]/input[1]', 'xpath', log, 1, '高')
    # check_element(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[2]/input[1]', 'xpath', log, 1, '超')
    # check_element(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[3]/input[1]', 'xpath', log, 1, 'g543410475@163.com')
    # check_element(driver, '/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/form[1]/div[4]/div[1]/input[1]', 'xpath', log, 1, 'gaochao1')
    # check_element(driver, '//*[@id="root"]/main/div/div/div[3]/form/div[4]/svg', 'xpath', log)
    # time.sleep(2)

    # print(driver.page_source)
    #driver.close()
    # driver.page_source

if __name__ == '__main__':
    main(sys.argv)