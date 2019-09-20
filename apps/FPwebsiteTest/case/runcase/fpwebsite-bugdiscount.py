from time import sleep, time
import sys
import os
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))
sys.path.append(project_path)
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
modules = '劳动日打折bug'  # 归属模块
screenshots = 'False'  # 是否开启出错截图

def main(argv):
    log, run_case_name, url = init_fp(argv)
    base_url = url
    excel_data = xlrd.open_workbook(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                 "../testdata/QA4-newproducts.xlsx")))
    sheet = excel_data.sheet_by_index(0)
    products_name = sheet.col_values(2)
    # products_name = 'Straight Neck Tiered Gown'
    products_active = sheet.col_values(12)

    driver = start_driver(3, log)
    driver.get(url)
    driver.maximize_window()
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()

    for i in range(1, 21):
        if i == 1 and products_active[i] == 1:
            search_btn = find_element(driver, '//*[@id="3xmW4MhfBeGEUoUYIYEQEI"]/header/nav/ul[2]/li[2]/a', 'xpath',
                                      log)
            driver.execute_script('arguments[0].click()', search_btn)
            text_xp = find_element(driver, '/html[1]/body[1]/div[3]/div[1]/header[1]/nav[1]/ul[2]/div[1]', 'xpath', log)
        elif products_active[i] == 1:
            search_btn = find_element(driver, '//*[@id="root"]/header/nav/ul[2]/li[2]/a', 'xpath', log)
            driver.execute_script('arguments[0].click()', search_btn)
            text_xp = find_element(driver, '/html[1]/body[1]/div[3]/header[1]/nav[1]/ul[2]/div[1]', 'xpath', log)
        else:
            get_return_code(log, '[%s]产品已下架' % products_name[i])
        
        ActionChains(driver).move_to_element(text_xp).send_keys(products_name[i]).perform()
        ActionChains(driver).move_to_element(text_xp).key_down(Keys.ENTER).perform()
        product = find_element(driver, '//*[@id="root"]/main/div/section[2]/div/div', 'xpath', log).\
            find_element_by_css_selector('.jsx-3604945185.ProductCard')
        prices = product.text.split('\n')[1]
        try:
            price = prices.split('$')[1]
            discout_price = prices.split('$')[2]
        except IndexError:
            get_return_code(log, '产品[%s]劳动日打折价格没有显示' % products_name[i], _code=500)
        else:
            if float(discout_price) == float(price) * 0.75:
                get_return_code(log, '产品[%s]劳动日打折价格显示正确' % products_name[i])
            else:
                get_return_code(log, '产品[%s]劳动日打折价格显示错误,价格为：%s' % (products_name[i], discout_price), _code=500)
        product_xp = '//*[@id="root"]/main/div/section[2]/div/div/div[1]'
        click(driver, product_xp, 'xpath', log)
        pro_text = find_element(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[1]', 'xpath', log)
        prices_in = pro_text.text.split('\n')[1]
        try:
            price_in = prices_in.split('$')[1]
            discout_price_in = prices_in.split('$')[2]
        except IndexError:
            get_return_code(log, '产品[%s]：产品详情页劳动日打折价格没有显示' % products_name[i], _code=500)
        else:
            if float(discout_price_in) == float(price_in) * 0.75:
                get_return_code(log, '产品[%s]：产品详情页劳动日打折价格显示正确' % products_name[i])
            else:
                get_return_code(log, '产品[%s]：产品详情页劳动日打折价格显示错误,价格为：%s' % (products_name[i], discout_price), _code=500)
        sleep(2, log)
        back(driver, log)
    driver.quit()




if __name__ == '__main__':
    # debug 堵塞程序
    # lock_tolerance(tolerance_level=-1, _log=log)
    # sys.gui_application.exec()
    # print(sys.argv)
    main(sys.argv)




