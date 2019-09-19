# -*- coding: utf-8 -*-
import warnings
import sys
import os
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))
sys.path.append(project_path)
from selenium.webdriver.common.keys import Keys
from apps.FPwebsiteTest.src.function.FP_function import *


warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 1000  # 最大运行时间
author = '彭柔'  # 编写作者
date = '2019-08-01'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '搜索功能'  # 归属模块
screenshots = 'False'  # 是否开启出错截图


def main(argv):
    FILTER_KIND = [
        'COLLECTION',
        'DELIVERED IN',
        'PRICE',
        'COLORS',
        'OCCASION',
        'SILHOUETTE',
        'BODYSHAPE',
        'FIT',
        'STYLE',
        'PATTERN',
        'OTHER',
        'EVENT',
        'NECKLINE',
        'SLEEVE',
        'LENGTH',
        'FABRIC',
        'DESIGN FEATURES']
    log, run_case_name, url = init_fp(argv)
    driver = start_driver(3, log)
    base_res = 'Search Results for '
    driver.get(url)
    driver.maximize_window()
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()
    sleep(5, log)

    # 搜索关键词 red
    search_btn = find_element(
        driver,
        '//*[@id="3xmW4MhfBeGEUoUYIYEQEI"]/header/nav/ul[2]/li[2]/a',
        'xpath',
        log)
    driver.execute_script('arguments[0].click()', search_btn)
    text_xp = find_element(
        driver,
        '/html[1]/body[1]/div[3]/div[1]/header[1]/nav[1]/ul[2]/div[1]',
        'xpath',
        log)
    ActionChains(driver).move_to_element(text_xp).send_keys('red').perform()
    ActionChains(driver).move_to_element(
        text_xp).key_down(Keys.ENTER).perform()
    assert_text(
        driver,
        base_res + '"red"',
        'xpath',
        '//*[@id="root"]/main/section/h1/span',
        log,
        "The search result's "
        "context is right!",
        "The search result's context is wrong!")
    # # 检测搜索关键词 red 右侧筛选项是否正确
    assert_text(
        driver,
        'FILTER BY:',
        'xpath',
        '//*[@id="root"]/main/div/section[1]/div/div[2]/div[1]/p',
        log,
        'FILTER BY显示正确',
        'FILTER BY显示错误')
    elements = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[1]/div/div[2]').\
        find_elements_by_css_selector('.jsx-1537248613.Accordion')
    # # # 判断筛选长度是否一致
    if len(elements) == len(FILTER_KIND):
        get_return_code(log, '筛选项长度一致')
        for i in range(2, len(elements) + 1):
            text_xp = '//*[@id="root"]/main/div/section[1]/div/div[2]/div[' + \
                str(i) + ']/section[1]/p'
            text_ele = find_element(driver, text_xp, 'xpath', log)
            if text_ele.text in FILTER_KIND:
                mess = '筛选选项[%s]名称显示正确' % text_ele.text
                get_return_code(log, mess)
            else:
                mess = '筛选选项[%s]名称显示错误' % text_ele.text
                get_return_code(log, mess, _code=500)
    else:
        get_return_code(
            log,
            '筛选项长度不一致，筛选项长度为[%d],实际筛选项长度为[%d]' %
            len(FILTER_KIND) %
            len(elements),
            _code=500)
    # get_return_code(log, '截取关键词‘red’搜索结果', free_shot=True)
    sleep(8, log)

    # 搜索错误的关键词时出现的提示
    search_btn = find_element(
        driver,
        '//*[@id="root"]/header/nav/ul[2]/li[2]/a',
        'xpath',
        log)
    driver.execute_script('arguments[0].click()', search_btn)
    text_xp = driver.find_element_by_xpath(
        '/html[1]/body[1]/div[3]/header[1]/nav[1]/ul[2]/div[1]')
    ActionChains(driver).move_to_element(
        text_xp).send_keys('dfagsgsagtet').perform()
    ActionChains(driver).move_to_element(
        text_xp).key_down(Keys.ENTER).perform()
    result_xp_text = find_element(
        driver,
        '//*[@id="root"]/main/section/h1/span',
        'xpath',
        log).text
    res_wrong_xp = find_element(
        driver,
        '//*[@id="root"]/main/div/section[2]/div/h4/span/a',
        'xpath',
        log)
    if result_xp_text == base_res + \
            '"dfagsgsagtet"' and res_wrong_xp.text == 'View our best selling dresses.':
        get_return_code(log, "The search result's context is right!")
    else:
        get_return_code(
            log,
            "The search result's context is wrong!",
            _code=500)
    # get_return_code(log, '截取关键词‘dfagsgsagtet’搜索结果', free_shot=True)
    sleep(8, log)

    # 搜索关键词为空时
    search_btn = find_element(
        driver,
        '//*[@id="root"]/header/nav/ul[2]/li[2]/a',
        'xpath',
        log)
    driver.execute_script('arguments[0].click()', search_btn)
    text_xp = driver.find_element_by_xpath(
        '/html[1]/body[1]/div[3]/header[1]/nav[1]/ul[2]/div[1]')
    ActionChains(driver).move_to_element(text_xp).send_keys('').perform()
    ActionChains(driver).move_to_element(
        text_xp).key_down(Keys.ENTER).perform()
    result_xp = find_element(
        driver,
        '//*[@id="root"]/main/section/h1/span',
        'xpath',
        log)
    if result_xp.text == 'Search Results':
        get_return_code(log, "The search result's context is right!")
    else:
        get_return_code(
            log,
            "The search result's context is wrong!",
            _code=500)
    # # 检测搜索关键词为空右侧筛选项是否正确
    assert_text(
        driver,
        'FILTER BY:',
        'xpath',
        '//*[@id="root"]/main/div/section[1]/div/div[2]/div[1]/p',
        log,
        'FILTER BY显示正确',
        'FILTER BY显示错误')
    elements = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[1]/div/div[2]'). \
        find_elements_by_css_selector('.jsx-1537248613.Accordion')
    # # # 判断筛选长度名称是否一致
    if len(elements) == len(FILTER_KIND):
        get_return_code(log, '筛选项长度一致')
        for i in range(2, len(elements) + 1):
            text_xp = '//*[@id="root"]/main/div/section[1]/div/div[2]/div[' + \
                str(i) + ']/section[1]/p'
            text_ele = find_element(driver, text_xp, 'xpath', log)
            if text_ele.text in FILTER_KIND:
                mess = '筛选选项[%s]名称显示正确' % text_ele.text
                get_return_code(log, mess)
            else:
                mess = '筛选选项[%s]名称显示错误' % text_ele.text
                get_return_code(log, mess, _code=500)
    else:
        get_return_code(
            log, '筛选项长度不一致，筛选项长度为[%d],实际筛选项长度为[%d]' %
            (len(FILTER_KIND), len(elements)), _code=500)
    # get_return_code(log, '截取关键词为空搜索结果', free_shot=True)
    sleep(8, log)
    driver.quit()


if __name__ == '__main__':
    # debug 堵塞程序
    # lock_tolerance(tolerance_level=-1, _log=log)
    # sys.gui_application.exec()
    # print(sys.argv)
    main(sys.argv)
    # print(sys.argv)
