import sys
import os
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))
sys.path.append(project_path)
from time import sleep, time
from apps.FPwebsiteTest.src.function.FP_function import *
from selenium.webdriver.common.keys import Keys
import re
import xlrd
import warnings
warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 1000  # 最大运行时间
author = '彭柔'  # 编写作者
date = '2019-08-01'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '新产品'  # 归属模块
screenshots = 'False'  # 是否开启出错截图


def main(argv):
    log, run_case_name, url = init_fp(argv)
    # print(os.path.abspath(os.path.join(os.path.dirname(__file__), "../testdata/QA4-newproducts.xlsx")))
    excel_data = xlrd.open_workbook(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                 "../testdata/QA4-newproducts.xlsx")))
    sheet = excel_data.sheet_by_index(0)
    products_name = sheet.col_values(2)
    # products_name = 'Straight Neck Tiered Gown'
    products_index = sheet.col_values(1)
    products_active = sheet.col_values(12)

    driver = start_driver(3, log)
    # base_res = 'Search Results for '
    driver.get(url)
    driver.maximize_window()
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()

    for i in range(1, len(products_name)):
        if i == 1 and products_active[i] == 1:
            search_btn = find_element(driver, '//*[@id="3xmW4MhfBeGEUoUYIYEQEI"]/header/nav/ul[2]/li[2]/a', 'xpath',
                                      log)
            driver.execute_script('arguments[0].click()', search_btn)
            text_xp = find_element(driver, '/html[1]/body[1]/div[3]/div[1]/header[1]/nav[1]/ul[2]/div[1]', 'xpath', log)
            ActionChains(driver).move_to_element(text_xp).send_keys(products_name[i]).perform()
            ActionChains(driver).move_to_element(text_xp).key_down(Keys.ENTER).perform()
            now_products = find_element(driver, '//*[@id="root"]/main/div/section[2]/div/div', 'xpath', log).\
                find_elements_by_css_selector('.jsx-3604945185.ProductCard')
            l = len(now_products)
            for product in now_products:
                name = product.text.split('\n')[0]
                price = product.text.split('\n')[1]
                if name == products_name[i]:
                    get_return_code(log, '新产品[%s]名称显示正确' % products_name[i])
                else:
                    get_return_code(log, '新产品[%s]名称显示错误' % products_name[i])
            for j in range(1, l + 1):
                product_xp = '//*[@id="root"]/main/div/section[2]/div/div/div[%d]' % j
                click(driver, product_xp, 'xpath', log)
                current_url = driver.current_url
                if products_index[i] in current_url:
                    get_return_code(log, '新产品[%s]网页跳转正确,网址为：%s' %(products_name[i], current_url))
                    check_status_code(driver, log)
                    try:
                        clothing_text = find_element(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[1]', 'xpath',
                                                     log).text
                    except Exception as e:
                        get_return_code(log, e, _code=500)
                    else:
                        clothing_name = clothing_text.split('\n')[0]
                        clothing_price = clothing_text.split('\n')[1]
                        if clothing_name == products_name[i]:
                            get_return_code(log, '新产品[%s]所在网页名称显示正确' % products_name[i])
                        else:
                            get_return_code(log, '新产品[%s]所在网页名称显示错误，名称为：%s' % (products_name[i], clothing_text), _code=500)
                    sleep(3, log)
                    back(driver, log)
                else:
                    if 'FPG' in current_url:
                        get_return_code(log, '新产品网页跳转错误,网址为：%s，这是一个老产品' % current_url)
                        check_status_code(driver, log)
                        back(driver, log)
                    else:
                        get_return_code(log, '新产品网页跳转错误,网址为：%s' % current_url, _code=500)

        elif products_active[i] == 1:
            search_btn = find_element(driver, '//*[@id="root"]/header/nav/ul[2]/li[2]/a', 'xpath', log)
            driver.execute_script('arguments[0].click()', search_btn)

            text_xp = find_element(driver, '/html[1]/body[1]/div[3]/header[1]/nav[1]/ul[2]/div[1]', 'xpath', log)
            ActionChains(driver).move_to_element(text_xp).send_keys(products_name[i]).perform()
            ActionChains(driver).move_to_element(text_xp).key_down(Keys.ENTER).perform()
            now_products = find_element(driver, '//*[@id="root"]/main/div/section[2]/div/div', 'xpath', log). \
                find_elements_by_css_selector('.jsx-3604945185.ProductCard')
            l = len(now_products)
            for product in now_products:
                name = product.text.split('\n')[0]
                price = product.text.split('\n')[1]
                if name == products_name[i]:
                    get_return_code(log, '新产品[%s]名称显示正确' % products_name[i])
                else:
                    get_return_code(log, '新产品[%s]名称显示错误' % products_name[i])
            for j in range(1, l + 1):
                product_xp = '//*[@id="root"]/main/div/section[2]/div/div/div[%d]' % j
                click(driver, product_xp, 'xpath', log)
                current_url = driver.current_url
                if products_index[i] in current_url:
                    get_return_code(log, '新产品[%s]网页跳转正确,网址为：%s' % (products_name[i], current_url))
                    check_status_code(driver, log)
                    try:
                        clothing_text = find_element(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[1]', 'xpath',
                                                     log).text
                    except Exception as e:
                        get_return_code(log, e, _code=500)
                    else:
                        clothing_name = clothing_text.split('\n')[0]
                        clothing_price = clothing_text.split('\n')[1]
                        if clothing_name == products_name[i]:
                            get_return_code(log, '新产品[%s]所在网页名称显示正确' % products_name[i])
                        else:
                            get_return_code(log, '新产品[%s]所在网页名称显示错误，名称为：%s' % (products_name[i], clothing_text), _code=500)
                    sleep(3, log)
                    back(driver, log)
                else:
                    if 'FPG' in current_url:
                        get_return_code(log, '新产品网页跳转错误网址为：%s，这是一个老产品' % current_url)
                        check_status_code(driver, log)
                        back(driver, log)
                    else:
                        get_return_code(log, '新产品网页跳转错误网址为：%s' % current_url, _code=500)
        else:
            get_return_code(log, '[%s]产品已下架' % products_name[i])
    driver.quit()


if __name__ == '__main__':
    # debug 堵塞程序
    # lock_tolerance(tolerance_level=-1, _log=log)
    # sys.gui_application.exec()
    # print(sys.argv)
    main(sys.argv)
    # print(sys.argv)