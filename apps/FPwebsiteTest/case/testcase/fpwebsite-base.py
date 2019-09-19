# -*- coding: utf-8 -*-
# 测试用例 - 主流程测试
from time import sleep, time
from apps.FPWebsite.src.function.FP_function import *
import warnings
warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 500  # 最大运行时间
author = 'Test'  # 编写作者
date = '2019-06-03'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '主流程'  # 归属模块
screenshots = 'True'  # 是否开启出错截图


def main(argv):
    sleep_time = 2
    log, run_case_name = init_fp(argv)

    menu_kinds = ['Shop', 'Weddings', 'About']
    shop_elements = {'Evening': 'dresses/evening',
                     'Express Delivery': 'dresses/express-delivery-dresses',
                     'Spring Summer': 'dresses/spring-summer', 'Maxi': 'dresses/maxi',
                     'Special Events': 'dresses/special-event', 'Best Sellers': 'dresses/featured',
                     'Day': 'dresses/daywear', 'Resort': 'dresses/vacation',
                     'Cocktail': 'dresses/cocktail', 'Midi & Mini': 'dresses/midi-mini',
                     'Jumpsuits': 'jumpsuits', 'Skirts': 'skirts', 'Suiting & Coats': 'outerwear',
                     'Pants': 'pants', 'Tops': 'tops', 'The Vacation Shop': 'dresses/vacation',
                     'The Workwear Shop': 'dresses/workwear', 'The Wrap Dress Shop': 'dresses/wrap',
                     'The Plaid Dress Shop': 'dresses/custom-plaid-shop',
                     'The Little Black Dress Shop': 'dresses/little-black-dresses',
                     'The Spring Summer Shop': 'dresses/spring-summer', 'The Lace & Tulle Shop': 'dresses/lace',
                     'The Floral Shop': 'dresses/florals', 'Fall Winter': 'dresses/fw18',
                     'Spring Summer': 'dresses/spring-summer', 'Resort': 'dresses/vacation',
                     'Fame & Partners X Atlanta de Cadenet Taylor': 'atlanta'}
    weddings_elements = {'Bridesmaid Dresses': 'dresses/bridesmaid', 'Wedding Guests': 'dresses/wedding-guests',
                         'Dresses for the Bride': 'dresses/bridal',
                         'Custom Dresses: Start Here': 'custom-clothes/the-custom-clothing-studio',
                         'Fame & Partners X Atlanta de Cadenet Taylor': 'atlanta',
                         'Custom Wedding Guest Dresses': 'custom-clothes/custom-wedding-guest',
                         'Custom Dresses for Brides': 'custom-clothes/custom-studio-brides',
                         'Custom Honeymoon Dresses': 'custom-clothes/custom-honeymoon',
                         'Start with a Base Design': 'custom-clothes/shop-by-silhouette',
                         'Buy Swatches': 'custom-clothes/order-swatches',
                         'Spring Summer Bridesmaid Favorites': 'custom-clothes/pre-customized-styles'}
    about_elements = {'Why custom': 'about', '$20 off to try custom': 'account/signup',
                      'Contact Us': 'contact'}

    shop_all = {"//div[@class='jsx-81871819 HeaderMegaMenuContainer']//div[1]//ul[1]//li[1]//a[1]": 'dresses',
                '//div[2]//ul[1]//li[1]//a[1]': 'clothing'}

    # start = time()

    driver = start_driver(log, 3)

    driver.implicitly_wait(10)
    driver.get("https://www.fameandpartners.com")

    driver.maximize_window()
    sleep(2)
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()
    # check_element(driver, '//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button', 'xpath')
    sleep(2)

    for kind in menu_kinds:
        if kind == 'Shop':
            for link in shop_elements:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                driver.save_screenshot('img.png')
                # check_element(driver, kind, 'link_text')
                check_element(driver, link, 'link_text', log)
                current_url = driver.current_url
                partial_url = current_url.split(sep="/", maxsplit=3)[3]
                if partial_url == shop_elements[link]:
                    get_return_code(log_obj=log, msg=link + ' website is correct')
                else:
                    get_return_code(log_obj=link, msg=' website is incorrect')
            # Shop All
            for link in shop_all:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                check_element(driver, link, 'xpath', log)
                current_url = driver.current_url
                partial_url = current_url.split(sep="/", maxsplit=3)[3]
                if partial_url == shop_all[link]:
                    get_return_code(log_obj=log, msg=link + ' website is correct')
                else:
                    get_return_code(log_obj=link, msg=' website is incorrect')
        elif kind == 'Weddings':
            for link in weddings_elements:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                check_element(driver, link, 'link_text', log)
                current_url = driver.current_url
                partial_url = current_url.split(sep="/", maxsplit=3)[3]
                if partial_url == weddings_elements[link]:
                    get_return_code(log_obj=log, msg=link + ' website is correct')
                else:
                    get_return_code(log_obj=link, msg=' website is incorrect')
        else:
            for link in about_elements:
                xp = driver.find_element_by_link_text(kind)
                ActionChains(driver).move_to_element(xp).perform()
                check_element(driver, link, 'link_text', log)
                current_url = driver.current_url
                partial_url = current_url.split(sep="/", maxsplit=3)[3]
                if partial_url == about_elements[link]:
                    get_return_code(log_obj=log, msg=link + ' website is correct')
                else:
                    get_return_code(log_obj=link, msg=' website is incorrect')
    # time = time() - start
    get_return_code(log_obj=log, msg='used time ' + str(time))

    driver.quit()


if __name__ == '__main__':
    # debug 堵塞程序
    # lock_tolerance(tolerance_level=-1, _log=log)
    # sys.gui_application.exec()
    main()
