# -*- coding: utf-8 -*-
# 引入网页驱动  chrome 版本 75.0.3770.100（正式版本） （32 位）

# 脚本信息
max_running_time = 600  # 最大运行时间
author = 'wangxiaolei'  # 编写作者
date = '2019/8/1'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '购物车'  # 归属模块
screenshots = 'True'  # 是否开启出错截图

import sys
import struct
import time
import os


from apps.FPWebsite.src.function.FP_function import *

#购物车操作：打开，新增服装，服装详情，删除衣服，关闭购物车
def shopping_bag(argv):
    log, run_case_name, url = init_fp(argv)
    driver = start_driver(way=1, _log=log)
    driver.maximize_window()

    # 访问主页
    driver.get(url)
    get_return_code(log, "start visit home page")

    sleep(2, log)

    #关闭弹窗
    click(driver,"//*[@id='portal-root']/div[3]/div/div/div/div/div[1]/button",'xpath',log)
    # 打开购物车&验证空购物车显示
    get_return_code(log, "---打开购物车&验证空购物车显示测试---")
    sleep(1, log)
    click(driver,"//*[@id='3xmW4MhfBeGEUoUYIYEQEI']/header/nav/ul[2]/li[3]/a",'xpath',log)
    sleep(1, log)
    assert_text(driver,'Shopping bag','xpath',"//*[@id='portal-root']/div[2]/div/div/div/div/div[1]/h4/span", log,
                'open shopping-bag page successfully', 'open shopping-bag page failed')
    assert_text(driver, 'Your Bag is Empty', 'xpath', '//*[@id="portal-root"]/div[2]/div/div/div/div/div[2]/div/h3', log,
                '购物车页面衣服详情字段[Your Bag is Empty]显示正确',
                '购物车页面衣服详情字段[Your Bag is Empty]显示错误')
    assert_text(driver, 'Continue Shopping', 'link_text','Continue Shopping',log,
                '购物车页面衣服详情字段[Continue Shopping]显示正确',
                '购物车页面衣服详情字段[Continue Shopping]显示错误')

    # 关闭购物车
    get_return_code(log, "---关闭购物车测试---")
    svg_elem = find_element(driver, '//*[@id="portal-root"]/div[2]/div/div/div/div/div[1]/a/*[name()="svg"]',
                            'xpath', log)
    action = ActionChains(driver)
    action.click(svg_elem).perform()
    get_return_code(log, "close shopping bag successfully")

    #新增服装到购物车
    get_return_code(log, "---新增服装到购物车测试---")
    sleep(2, log)
    click(driver, "//*[@id='3xmW4MhfBeGEUoUYIYEQEI']/header/nav/ul[2]/li[3]/a", 'xpath', log)
    sleep(2, log)
    click(driver, "Continue Shopping", 'link_text', log)
    shop_link = find_element(driver, "Shop", 'link_text', log)
    ActionChains(driver).move_to_element(shop_link).perform()
    sleep(1, log)
    click(driver,"Spring Summer",'link_text',log)
    sleep(10, log)
    # assert_text(driver, 'Spring Collection', 'xpath', "//*[@id='root']/main/section/h1", log,
    #             'open [Spring Collection] page successfully', 'open [Spring Collection] page failed')
    sleep(5, log)
    # click(driver,"//*[@id='root']/main/div/section[2]/div/div[1]/div[1]/a/div[1]/div[1]/div/picture/img",'xpath',log)
    click(driver, "//*[@id='root']/main/div/section[2]/div/div[1]/div[1]/a/div[1]/div[1]/div", 'xpath', log)
    sleep(5, log)
    click(driver,"//*[@id='root']/main/div[1]/div[2]/div/button",'xpath',log)
    click(driver,"//*[@id='root']/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]",
                           'xpath',log)
    click(driver,"//*[@id='root']/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/button[1]"
                   ,'xpath',log)
    sleep(1, log)
    click(driver,"//*[@id='root']/main/div[1]/div[2]/div/div[2]/div/div[2]/div/div[1]"
                  ,'xpath',log)
    sleep(1, log)
    click(driver, "//*[@id='root']/main/div[1]/div[2]/div/div[3]/button", 'xpath', log)

    sleep(5, log)

    #判断购物车页面衣服详情显示
    get_return_code(log, "---判断购物车页面衣服详情显示测试---")
    assert_text(driver,'Shopping bag','xpath',"//*[@id='portal-root']/div[2]/div/div/div/div/div[1]/h4/span", log,
                'open shopping-bag page successfully', 'open shopping-bag page failed')
    assert_text(driver, '1', 'xpath', '//*[@id="portal-root"]/div[2]/div/div/div/div/div[1]/span', log,
                '购物车页面衣服详情字段[衣服数量]显示正确', '购物车页面衣服详情字段[衣服数量]显示错误')
    assert_text(driver, 'Gathered Full Dress', 'xpath', "//*[@id='portal-root']/div[2]/div/div/div/div/ul/li/div[2]/p/strong", log,
                '购物车页面衣服详情字段[Gathered Full Dress]显示正确', '购物车页面衣服详情字段[Gathered Full Dress]显示错误')
    assert_text(driver, 'Feline Spot Tan Light Georgette', 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/ul/li/div[2]/div/div[1]', log,
                '购物车页面衣服详情字段[Feline Spot Tan Light Georgette]显示正确', '购物车页面衣服详情字段[Feline Spot Tan Light Georgette]显示错误')
    assert_text(driver, 'Customizations', 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/ul/li/div[2]/div/div[2]/div[1]', log,
                '购物车页面衣服详情字段[Customizations]显示正确', '购物车页面衣服详情字段[Customizations]显示错误')
    assert_text(driver, 'Casual Maxi', 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/ul/li/div[2]/div/div[2]/div[2]', log,
                '购物车页面衣服详情字段[Casual Maxi]显示正确', '购物车页面衣服详情字段[Casual Maxi]显示错误')
    assert_text(driver, 'Size', 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/ul/li/div[2]/div/div[3]/div[1]', log,
                '购物车页面衣服详情字段[Size]显示正确', '购物车页面衣服详情字段[Size]显示错误')
    assert_text(driver, "US 0 • 4' 10\"", 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/ul/li/div[2]/div/div[3]/div[2]', log,
                '购物车页面衣服详情字段[US 0 • 4 10]显示正确', '购物车页面衣服详情字段[US 0 • 4 10]显示错误')
    assert_text(driver, "Delivery", 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/ul/li/div[2]/div/div[4]/div[1]', log,
                '购物车页面衣服详情字段[Delivery]显示正确', '购物车页面衣服详情字段[Delivery]显示错误')
    assert_text(driver, "Standard Delivery", 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/ul/li/div[2]/div/div[4]/div[2]', log,
                '购物车页面衣服详情字段[Standard Delivery]显示正确', '购物车页面衣服详情字段[Standard Delivery]显示错误')
    assert_text(driver, "Subtotal", 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/div[2]/div/span[1]', log,
                '购物车页面衣服详情字段[Subtotal]显示正确', '购物车页面衣服详情字段[Subtotal]显示错误')
    assert_text(driver, "CHECKOUT", 'xpath',
                '//*[@id="portal-root"]/div[2]/div/div/div/div/div[2]/a', log,
                '购物车页面衣服详情字段[CHECKOUT]显示正确', '购物车页面衣服详情字段[CHECKOUT]显示错误')
    #关闭购物车
    get_return_code(log, "---关闭购物车测试---")
    svg_elem = find_element(driver,'//*[@id="portal-root"]/div[2]/div/div/div/div/div[1]/a/*[name()="svg"]',
                           'xpath',log)
    action = ActionChains(driver)
    action.click(svg_elem).perform()
    get_return_code(log, "close shopping bag successfully")

    #新增第二件衣服到购物车
    get_return_code(log, "---新增第二件衣服到购物车测试---")
    shop_link = find_element(driver, "Shop", 'link_text', log)
    ActionChains(driver).move_to_element(shop_link).perform()
    sleep(3, log)
    click(driver,"Evening",'link_text',log)
    sleep(5, log)
    # assert_text(driver, 'Custom Evening Dresses', 'xpath', '//*[@id="root"]/main/section/h1', log,
    #             'open [Custom Evening Dresses] page successfully', 'open [Custom Evening Dresses] page failed')
    sleep(10,log)
    click(driver,'//*[@id="root"]/main/div/section[2]/div/div[1]/div[2]/a/div[1]/div[1]/div/picture/img',
                  'xpath',log)
    sleep(5, log)
    click(driver, "//*[@id='root']/main/div[1]/div[2]/div/button", 'xpath', log)
    sleep(5, log)
    assert_text(driver, '2', 'xpath', '//*[@id="portal-root"]/div[5]/div/div/div/div/div[1]/span', log,
                '购物车页面衣服详情字段[衣服数量]显示正确', '购物车页面衣服详情字段[衣服数量]显示错误')
    assert_text(driver, 'Drape Front Set', 'xpath', '//*[@id="portal-root"]/div[5]/div/div/div/div/ul/li[2]/div[2]/p/strong', log,
                'The cloth [Drape Front Set] added to shopping bag successfully',
                'The cloth [Drape Front Set] added to shopping bag failed.')

    #验证价格总额是否正确
    get_return_code(log, "---验证价格总额是否正确测试---")
    price1 = find_element(driver,'//*[@id="portal-root"]/div[5]/div/div/div/div/ul/li[1]/div[2]/p/span/span/span',
                          'xpath',log).text
    price2 = find_element(driver,'//*[@id="portal-root"]/div[5]/div/div/div/div/ul/li[2]/div[2]/p/span/span/span',
                          'xpath',log).text
    total_price = find_element(driver,'//*[@id="portal-root"]/div[5]/div/div/div/div/div[2]/div/span[2]/span/span',
                          'xpath',log).text
    price1 = price1[1:]
    price2 = price2[1:]
    total_price = total_price[1:]
    if int(total_price)== int(price1)+ int(price2):
        get_return_code(log,"购物车价格总额显示正确")
    else:
        get_return_code(log,"购物车价格总额显示错误",_code=500)

    #购物车删除一件衣服
    get_return_code(log, "---购物车删除一件衣服测试---")
    click(driver, '//*[@id="portal-root"]/div[5]/div/div/div/div/ul/li[1]/div[1]/a[2]/span',
          'xpath', log)
    sleep(5, log)
    assert_text(driver, '1', 'xpath', '//*[@id="portal-root"]/div[5]/div/div/div/div/div[1]/span', log,
                '购物车页面衣服详情字段[衣服数量]显示正确', '购物车页面衣服详情字段[衣服数量]显示错误')
    assert_text(driver, 'Drape Front Set', 'xpath', '//*[@id="portal-root"]/div[5]/div/div/div/div/ul/li/div[2]/p/strong', log,
                'The cloth [Gathered Full Dress] deleted from shopping bag successfully',
                'The cloth [Gathered Full Dress] deleted from shopping bag failed')

    #验证删除一件衣服后价格总额显示
    get_return_code(log, "---验证删除一件衣服后价格总额显示测试---")
    price1 = find_element(driver, '//*[@id="portal-root"]/div[5]/div/div/div/div/ul/li/div[2]/p/span/span/span',
                          'xpath', log).text
    total_price = find_element(driver, '//*[@id="portal-root"]/div[5]/div/div/div/div/div[2]/div/span[2]/span/span',
                               'xpath', log).text
    price1 = price1[1:]
    total_price = total_price[1:]
    # if int(total_price)== int(price1):
    #     get_return_code(log,"购物车价格总额显示正确")
    # else:
    #     get_return_code(log,"购物车价格总额显示错误",_code=500)

    driver.quit()
    return True


if __name__ == '__main__':
    shopping_bag(sys.argv)