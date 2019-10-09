# -*- coding: utf-8 -*-
# 测试用例 - 主流程测试
import warnings
import sys
import os
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))
sys.path.append(project_path)
from apps.FPwebsiteTest.src.function.FP_function import *
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 1000  # 最大运行时间
author = 'Test'  # 编写作者
date = '2019-07-31'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '菜单栏分类'  # 归属模块
screenshots = 'False'  # 是否开启出错截图


def main(argv):

    log, run_case_name, url = init_fp(argv)
    base_url = url

    menu_kinds = ['Shop', 'Weddings', 'About']
    shop_elements = {
        'Evening': base_url + 'dresses/evening',
        'Express Delivery': base_url + 'dresses/express-delivery-dresses',
        'Spring Summer': base_url + 'dresses/spring-summer',
        'Maxi': base_url + 'dresses/maxi',
        'Special Events': base_url + 'dresses/special-event',
        'Best Sellers': base_url + 'dresses/featured',
        'Day': base_url + 'dresses/daywear',
        'Resort': base_url + 'dresses/vacation',
        'Cocktail': base_url + 'dresses/cocktail',
        'Midi & Mini': base_url + 'dresses/midi-mini',
        'Jumpsuits': base_url + 'jumpsuits',
        'Skirts': base_url + 'skirts',
        'Suiting & Coats': base_url + 'outerwear',
        'Pants': base_url + 'pants',
        'Tops': base_url + 'tops',
        'The Vacation Shop': base_url + 'dresses/vacation',
        'The Workwear Shop': base_url + 'dresses/workwear',
        'The Wrap Dress Shop': base_url + 'dresses/wrap',
        'The Plaid Dress Shop': base_url + 'dresses/custom-plaid-shop',
        'The Little Black Dress Shop': base_url + 'dresses/little-black-dresses',
        'The Spring Summer Shop': base_url + 'dresses/spring-summer',
        'The Lace & Tulle Shop': base_url + 'dresses/lace',
        'The Floral Shop': base_url + 'dresses/florals',
        'Fall Winter': base_url + 'dresses/fw18',
        'Spring Summer': base_url + 'dresses/spring-summer',
        'Resort': base_url + 'dresses/vacation',
        'Fame & Partners X Atlanta de Cadenet Taylor': base_url + 'atlanta'}
    weddings_elements = {
        'Bridesmaid Dresses': base_url + 'dresses/bridesmaid',
        'Wedding Guests': base_url + 'dresses/wedding-guests',
        'Dresses for the Bride': base_url + 'dresses/bridal',
        'Custom Dresses: Start Here': base_url + 'custom-clothes/the-custom-clothing-studio',
        'Fame & Partners X Atlanta de Cadenet Taylor': base_url + 'atlanta',
        'Custom Wedding Guest Dresses': base_url + 'custom-clothes/custom-wedding-guest',
        'Custom Dresses for Brides': base_url + 'custom-clothes/custom-studio-brides',
        'Custom Honeymoon Dresses': base_url + 'custom-clothes/custom-honeymoon',
        'Start with a Base Design': base_url + 'custom-clothes/shop-by-silhouette',
        'Buy Swatches': base_url + 'custom-clothes/order-swatches',
        'Spring Summer Bridesmaid Favorites': base_url + 'custom-clothes/pre-customized-styles'}
    about_elements = {
        'Why custom': base_url + 'about',
        '$20 off to try custom': base_url + 'account/signup',
        'Contact Us': base_url + 'contact'}

    shop_all = {
        "//div[@class='jsx-81871819 HeaderMegaMenuContainer']//div[1]//ul[1]//li[1]//a[1]": base_url + 'dresses',
        '//div[2]//ul[1]//li[1]//a[1]': base_url + 'clothing'}

    # start = time()
    driver = start_driver(3, log)
    # driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    driver.maximize_window()
    sleep(2, log)
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()
    # check_element(driver, '//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button', 'xpath')
    sleep(5, log)

    # driver.set_page_load_timeout(10)
    # driver.set_script_timeout(10)
    for kind in menu_kinds:
        if kind == 'Shop':
            for link in shop_elements:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                # 检测菜单栏名称是否显示正确
                assert_text(
                    driver,
                    link,
                    'link_text',
                    link,
                    log,
                    '菜单栏名称[%s]显示正确' %
                    link,
                    '菜单栏名称[%s]显示错误' %
                    link)
                # 检测对应的url是否正确
                # try:
                #     wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT, link)))
                # except TimeoutException:
                #     get_return_code(log, '加载超时强制停止')
                #     driver.execute_script('window.stop();')
                # else:
                #     click(driver, link, 'link_text', log)
                #     check_url(driver, shop_elements[link], log)
                try:
                    click(driver, link, 'link_text', log)
                except TimeoutException:
                    get_return_code(log, '网页加载超时')
                    # driver.execute_script('window.stop();')
                    # stopLoading()
                    # get_return_code(log, '加载超时强制停止')
                # click(driver, link, 'link_text', log)
                else:
                    check_url(driver, shop_elements[link], log)
                # click(driver, link, 'link_text', log)
                # check_url(driver, weddings_elements[link], log)
            sleep(2, log)
            # Shop All
            for link in shop_all:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                assert_text(
                    driver,
                    'Shop All',
                    'xpath',
                    link,
                    log,
                    '菜单栏名称Shop All显示正确',
                    '菜单栏名称Shop All显示错误')
                try:
                    click(driver, link, 'xpath', log)
                except TimeoutException:
                    get_return_code(log, '网页加载超时')
                    # driver.execute_script('window.stop();')
                    # stopLoading()
                    # get_return_code(log, '加载超时强制停止')
                # click(driver, link, 'link_text', log)
                else:
                    check_url(driver, shop_all[link], log)
                # click(driver, link, 'xpath', log)
                # check_url(driver, shop_all[link], log)
                sleep(0.5, log)
        elif kind == 'Weddings':
            for link in weddings_elements:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                assert_text(
                    driver,
                    link,
                    'link_text',
                    link,
                    log,
                    '菜单栏名称[%s]显示正确' %
                    link,
                    '菜单栏名称[%s]显示错误' %
                    link)
                try:
                    click(driver, link, 'link_text', log)
                except TimeoutException:
                    get_return_code(log, '网页加载超时')
                    # driver.execute_script('window.stop();')
                    # stopLoading()
                    # get_return_code(log, '加载超时强制停止')
                # click(driver, link, 'link_text', log)
                else:
                    check_url(driver, weddings_elements[link], log)
                # click(driver, link, 'link_text', log)
                # check_url(driver, weddings_elements[link], log)
        else:
            for link in about_elements:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                assert_text(
                    driver,
                    link,
                    'link_text',
                    link,
                    log,
                    '菜单栏名称[%s]显示正确' %
                    link,
                    '菜单栏名称[%s]显示错误' %
                    link)
                try:
                    click(driver, link, 'link_text', log)
                except TimeoutException:
                    get_return_code(log, '网页加载超时')
                    # driver.execute_script('window.stop();')
                    # stopLoading()
                    # get_return_code(log, '加载超时强制停止')
                # click(driver, link, 'link_text', log)
                else:
                    check_url(driver, about_elements[link], log)
                # click(driver, link, 'link_text', log)
                # check_url(driver, about_elements[link], log)
    driver.quit()


if __name__ == '__main__':
    # debug 堵塞程序
    # lock_tolerance(tolerance_level=-1, _log=log)
    # sys.gui_application.exec()
    # print(sys.argv)
    main(sys.argv)
