# -*- coding: utf-8 -*-
# 引入网页驱动  chrome 版本 75.0.3770.100（正式版本） （32 位）
import sys
import os
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))
sys.path.append(project_path)
# 脚本信息

max_running_time = 900  # 最大运行时间
author = 'wangxiaolei'  # 编写作者
date = '2019/8/1'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '下单'  # 归属模块
screenshots = 'False'  # 是否开启出错截图

import sys
import struct
import time
import os


from apps.FPwebsiteTest.src.function.FP_function import *

#下单
def ordering(argv):
    log, run_case_name,url = init_fp(argv)
    driver = start_driver(way=3, _log=log)
    driver.maximize_window()

    # 访问主页
    driver.get(url)
    get_return_code(log, "start visit home page")
    sleep(2, log)

    #关闭弹窗
    click(driver,"//*[@id='portal-root']/div[3]/div/div/div/div/div[1]/button",'xpath',log)

    #新增服装到购物车
    get_return_code(log, "---新增服装到购物车测试---")
    sleep(2, log)
    shop_link = find_element(driver, "Shop", 'link_text', log)
    ActionChains(driver).move_to_element(shop_link).perform()
    sleep(1, log)
    click(driver, "Evening", 'link_text', log)

    assert_text(driver, 'Custom Evening Dresses', 'xpath', '//*[@id="root"]/main/section/h1', log,
                'open [Custom Evening Dresses] page successfully', 'open [Custom Evening Dresses] page failed')
    sleep(1, log)
    driver.get(url + 'dresses/custom-dress-FPG1273~1066~107~FM')
    # click(driver,'//*[@id="root"]/main/div/section[2]/div/div[1]/div[2]/a/div[1]/div[1]/div/picture/img','xpath',log)
    # click(driver, '//*[@id="root"]/main/div/section[2]/div/div[1]/div[2]/a/div[1]/div[1]/div', 'xpath', log)
    sleep(1, log)

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

    sleep(1, log)

    #点击[CHECKOUT]后delivery details页测试
    get_return_code(log, "---点击[CHECKOUT]后delivery details页测试---")
    click(driver,'//*[@id="portal-root"]/div[2]/div/div/div/div/div[2]/a','xpath',log)
    sleep(5, log)
    #验证用户购买信息页显示
    assert_text(driver,'CONTINUE SHOPPING','xpath','//*[@id="checkout"]/div[2]/div/div[1]/a/div[1]',log,
                'delivery details页字段[CONTINUE SHOPPING]显示正确',
                'delivery details页字段[CONTINUE SHOPPING]显示错误')
    click(driver, 'CONTINUE SHOPPING', 'link_text', log)
    sleep(5, log)
    check_url(driver,'https://www.fameandpartners.com/dresses',log)
    back(driver,log)
    sleep(2, log)

    click(driver, '//*[@id="checkout"]/div[4]/div[2]/div[1]/div[1]/form[1]/div[2]/div/a', 'xpath', log)
    assert_text(driver,'Facebook','xpath','//*[@id="blueBarDOMInspector"]/div/div[1]/div/div/h1/a/i',log,'成功跳转到facebook网站','跳转facebook网站失败')
    back(driver, log)
    sleep(1,log)

    assert_text(driver,'Step 1: Delivery details','xpath',
                '//*[@id="checkout"]/div[3]/div/div/div[1]/ol/li[1]',log,
                'delivery details页字段[Step 1: Delivery details]显示正确',
                'delivery details页字段[Step 1: Delivery details]显示错误')
    assert_text(driver,'Step 2: Payment details','xpath',
                '//*[@id="checkout"]/div[3]/div/div/div[1]/ol/li[2]',log,
                'delivery details页字段[Step 2: Payment details]显示正确',
                'delivery details页字段[Step 2: Payment details]显示错误')
    assert_text(driver,'Secure checkout','xpath',
                '//*[@id="checkout"]/div[3]/div/div/div[2]/span',log,
                'delivery details页字段[Secure checkout]显示正确',
                'delivery details页字段[Secure checkout]显示错误')
    assert_text(driver,'Deliver to','xpath','//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[1]/div/h2',log,
                'delivery details页字段[Deliver to]显示正确',
                'delivery details页字段[Deliver to]显示错误')
    assert_text(driver,'First Name','xpath','//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[2]/div[1]/label',log,
                'delivery details页字段[First Name]显示正确',
                'delivery details页字段[First Name]显示错误')
    assert_text(driver,'Last Name','xpath','//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[2]/div[2]/label',log,
                'delivery details页字段[Last Name]显示正确',
                'delivery details页字段[Last Name]显示错误')
    assert_text(driver,'Email address','xpath','//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[3]/div/label',log,
                'delivery details页字段[Email address]显示正确',
                'delivery details页字段[Email address]显示错误')
    assert_text(driver,'Receive new styles in my inbox each week','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[4]/div/div/label',log,
                'delivery details页字段[Receive new styles in my inbox each week]显示正确',
                'delivery details页字段[Receive new styles in my inbox each week]显示错误')
    assert_text(driver,'Phone number','xpath','//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[5]/div/label',log,
                'delivery details页字段[Phone number]显示正确',
                'delivery details页字段[Phone number]显示错误')
    assert_text(driver,'in case we need to contact you about your order','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[5]/div/p',log,
                'delivery details页字段[in case we need to contact you about your order]显示正确',
                'delivery details页字段[in case we need to contact you about your order]显示错误')

    assert_text(driver,'Delivery Address','xpath','//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[6]/div/h2',log,
                'delivery details页字段[Delivery Address]显示正确',
                'delivery details页字段[Delivery Address]显示错误')
    assert_text(driver,'Country','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[7]/div/label',log,
                'delivery details页字段[Country]显示正确',
                'delivery details页字段[Country]显示错误')
    assert_text(driver,'Street Address','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[8]/div/label',log,
                'delivery details页字段[Street Address]显示正确',
                'delivery details页字段[Street Address]显示错误')
    assert_text(driver,'this must be a physical address, not a P.O. Box','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[8]/div/p',log,
                'delivery details页字段[this must be a physical address, not a P.O. Box]显示正确',
                'delivery details页字段[this must be a physical address, not a P.O. Box]显示错误')
    assert_text(driver,'Street Address (line 2)','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[9]/div/label',log,
                'delivery details页字段[Street Address (line 2)]显示正确',
                'delivery details页字段[Street Address (line 2)]显示错误')
    assert_text(driver,'(optional)','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[9]/div/p',log,
                'delivery details页字段[(optional)]显示正确',
                'delivery details页字段[(optional)]显示错误')
    assert_text(driver,'City / Suburb','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[10]/div/label',log,
                'delivery details页字段[City / Suburb]显示正确',
                'delivery details页字段[City / Suburb]显示错误')
    assert_text(driver,'Zipcode','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[11]/div[1]/label',log,
                'delivery details页字段[Zipcode]显示正确',
                'delivery details页字段[Zipcode]显示错误')
    assert_text(driver,'State','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[11]/div[2]/label',log,
                'delivery details页字段[State]显示正确',
                'delivery details页字段[State]显示错误')
    assert_text(driver,'This is also my billing address','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[4]/div/div/label',log,
                'delivery details页字段[This is also my billing address]显示正确',
                'delivery details页字段[This is also my billing address]显示错误')


    assert_text(driver,'Shipping Methods','xpath','//*[@id="shopping-cart-delivery-times"]/h2',log,
                'delivery details页字段[Shipping Methods]显示正确',
                'delivery details页字段[Shipping Methods]显示错误')
    assert_text(driver,'Choose when you want to receive your order.','xpath',
                '//*[@id="shopping-cart-delivery-times"]/p',log,
                'delivery details页字段[Choose when you want to receive your order.]显示正确',
                'delivery details页字段[Choose when you want to receive your order.]显示错误')
    assert_text(driver,'Drape Front Set','xpath','//*[@id="shopping-cart-delivery-times"]/div/section/div[1]/div[2]/h3',log,
                'delivery details页字段[Drape Front Set]显示正确',
                'delivery details页字段[Drape Front Set]显示错误')
    assert_text(driver,'SIZE:','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[1]/div[2]/dd[1]/span',log,
                'delivery details页字段[SIZE:]显示正确',
                'delivery details页字段[SIZE:]显示错误')
    size_detail = find_element(driver,'//*[@id="shopping-cart-delivery-times"]/div/section/div[1]/div[2]/dd[1]','xpath',log)
    if size_detail is not 0:
       if size_detail.text.find('US 0') != -1:
           get_return_code(log, 'delivery details页字段[US 0]显示正确')
       else:
           get_return_code(log, 'delivery details页字段[US 0]显示错误',500)

    assert_text(driver,'COLOR:','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[1]/div[2]/dd[2]/span',log,
                'delivery details页字段[COLOR:]显示正确',
                'delivery details页字段[COLOR:]显示错误')
    color_detail = find_element(driver,'//*[@id="shopping-cart-delivery-times"]/div/section/div[1]/div[2]/dd[2]','xpath',log)
    if color_detail is not 0:
       if size_detail.text.find('Silver') != -1:
           get_return_code(log, 'delivery details页字段[Silver]显示正确')
       else:
           get_return_code(log, 'delivery details页字段[Silver]显示错误')

    assert_text(driver,'Not In A Rush: 8 - 10 weeks','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[1]/div/label/div[1]',log,
                'delivery details页字段[Not In A Rush: 8 - 10 weeks]显示正确',
                'delivery details页字段[Not In A Rush: 8 - 10 weeks]显示错误')
    assert_text(driver,'10% OFF','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[1]/div/div',log,
                'delivery details页字段[10% OFF]显示正确',
                'delivery details页字段[10% OFF]显示错误')
    assert_text(driver,'Standard Delivery: 4 - 7 weeks','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[2]/div/label/div[1]',log,
                'delivery details页字段[Standard Delivery: 4 - 7 weeks]显示正确',
                'delivery details页字段[Standard Delivery: 4 - 7 weeks]显示错误')
    assert_text(driver,'FREE','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[2]/div/div',log,
                'delivery details页字段[FREE]显示正确',
                'delivery details页字段[FREE]显示错误')
    assert_text(driver,'Express Delivery: 2 - 3 weeks','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[3]/div/label/div[1]',log,
                'delivery details页字段[Express Delivery: 2 - 3 weeks]显示正确',
                'delivery details页字段[Express Delivery: 2 - 3 weeks  ]显示错误')
    assert_text(driver,'$7.00','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[3]/div/div',log,
                'delivery details页字段[$7.00]显示正确',
                'delivery details页字段[$7.00]显示错误')
    assert_text(driver,'VIP Delivery: 7 - 10 days','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[4]/div/label/div[1]',log,
                'delivery details页字段[VIP Delivery: 7 - 10 days]显示正确',
                'delivery details页字段[VIP Delivery: 7 - 10 days]显示错误')
    assert_text(driver,'$14.00','xpath',
                '//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[4]/div/div',log,
                'delivery details页字段[$14.00]显示正确',
                'delivery details页字段[$14.00]显示错误')

    assert_text(driver,'Drape Front Set','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div[1]/span',log,
                'delivery details页字段[Drape Front Set]显示正确',
                'delivery details页字段[Drape Front Set]显示错误')
    assert_text(driver,'APPLY','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[2]/div[2]/div/form/div/span/button',log,
                'delivery details页字段[APPLY]显示正确',
                'delivery details页字段[APPLY]显示错误')
    sub_total = find_element(driver,'//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[2]/div[3]/div/div/p[1]','xpath',log)
    if sub_total is not 0:
        if sub_total.text[0:sub_total.text.index('\n')] == 'Sub Total':
            get_return_code(log, 'delivery details页字段[Sub Total]显示正确')
        else:
            get_return_code(log, 'delivery details页字段[Sub Total]显示错误')

    Shipping = find_element(driver,'//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[2]/div[3]/div/div/p[3]','xpath',log)
    if Shipping is not 0:
        if Shipping.text.split('\n')[0] == 'Shipping':
            get_return_code(log, 'delivery details页字段[Shipping]显示正确')
        else:
            get_return_code(log, 'delivery details页字段[Shipping]显示错误',500)

    Order_Total = find_element(driver,'//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[2]/div[3]/div/div/p[5]','xpath',log)
    if Order_Total is not 0:
        if Order_Total.text.split('\n')[0] == 'Order Total':
            get_return_code(log, 'delivery details页字段[Order Total]显示正确')
        else:
            get_return_code(log, 'delivery details页字段[Order Total]显示错误')
    assert_text(driver,'Free shipping to USA, Canada and the UK','xpath',
                '//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[3]/div/div/p[1]',log,
                'delivery details页字段[Free shipping to USA, Canada and the UK]显示正确',
                'delivery details页字段[Free shipping to USA, Canada and the UK]显示错误')
    assert_text(driver,'Easy Returns. Find out more','link_text',
                'Easy Returns. Find out more',log,
                'delivery details页字段[Easy Returns. Find out more]显示正确',
                'delivery details页字段[Easy Returns. Find out more]显示错误')
    assert_text(driver,'CONTINUE TO PAYMENT','xpath','//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[9]/div/button',log,
                'delivery details页字段[CONTINUE TO PAYMENT]显示正确',
                'delivery details页字段[CONTINUE TO PAYMENT]显示错误')
    order_number = find_element(driver,'//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[4]/div/div','xpath',log)
    if order_number is not 0:
        if order_number.text.split(':')[0] == 'Your Order Number':
            get_return_code(log, 'delivery details页字段[Your Order Number]显示正确')
        else:
            get_return_code(log, 'delivery details页字段[Your Order Number]显示错误',500)
    assert_text(driver,'© 2019 Fame and Partners. All rights reserved.','xpath','//*[@id="top"]/footer/div/div/div/div',log,
                'delivery details页字段[© 2019 Fame and Partners. All rights reserved.]显示正确',
                'delivery details页字段[© 2019 Fame and Partners. All rights reserved.]显示错误')
    target = driver.find_element_by_link_text('Privacy Policy')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    sleep(1,log)
    click(driver,'Privacy Policy','link_text',log)
    check_url(driver,url+'privacy',log)
    back(driver,log)
    target = driver.find_element_by_link_text('Returns Policy')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    sleep(1,log)
    click(driver, 'Returns Policy', 'link_text', log)
    check_url(driver, url + 'faqs#collapse-returns-policy', log)
    back(driver, log)
    # 输入信息
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    input_text(driver,'order_ship_address_attributes_firstname','id','xiaolei',log)
    input_text(driver,'order_ship_address_attributes_lastname','id','wang', log)
    input_text(driver, 'order_ship_address_attributes_email', 'id', 'wangxiaolei@graphicchina.com', log)
    click(driver,'//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[4]/div/div','xpath',log)
    sleep(1, log)
    click(driver, '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[3]/div[4]/div/div', 'xpath', log)
    input_text(driver, 'order_ship_address_attributes_phone', 'id', '226666', log)
    click(driver,'//*[@id="order_ship_address_attributes_country_id"]','xpath',log)
    sleep(0.5,log)
    click(driver,'//*[@id="order_ship_address_attributes_country_id"]/option[35]','xpath',log)
    sleep(0.5, log)
    input_text(driver,'order_ship_address_attributes_address1','id','address1',log)
    input_text(driver,'order_ship_address_attributes_address2','id','address2',log)
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    input_text(driver, 'order_ship_address_attributes_city', 'id', 'city', log)
    sleep(1, log)
    input_text(driver, 'order_ship_address_attributes_zipcode', 'id', '102105', log)
    click(driver, '//*[@id="order_ship_address_attributes_state_id"]', 'xpath', log)
    sleep(1, log)
    click(driver, '//*[@id="order_ship_address_attributes_state_id"]/option[19]', 'xpath', log)
    sleep(1, log)
    click(driver,'//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[4]/div/div','xpath',log)
    sleep(1, log)
    click(driver, '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[4]/div/div', 'xpath', log)
    click(driver,'//*[@id="shopping-cart-delivery-times"]/div/section/div[2]/fieldset/div[1]/div/label/div[1]','xpath',log)
    sleep(1, log)
    target = driver.find_element_by_xpath('//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[2]/div[3]/div/div/p[5]')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    sleep(1, log)
    input_text(driver,'//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[2]/div[2]/div/form/div/input','xpath','test123',log)
    sleep(1, log)
    click(driver,'//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[2]/div[2]/div/form/div/span','xpath',log)
    sleep(4, log)

    # 获取当前的handle名字
    handle = driver.current_window_handle
    ele = find_element(driver, '//*[@id="checkout"]/div[4]/div[2]/div[2]/div/div[3]/div/div/p[2]/a', 'xpath', log)
    try:
        ele.click()
    except Exception as e:
        mess = "Failed to click the element with %s" % e
        get_return_code(log, mess,500)
    else:
        mess = "The element [Easy Returns. Find out more] was clicked."
        get_return_code(log, mess)

    # 获取全部的handle
    handles = driver.window_handles
    driver.switch_to_window(handles[-1])
    check_url(driver,url+'faqs/returns',log)
    driver.close()
    driver.switch_to_window(handle)

    target = driver.find_element_by_xpath('//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[9]/div/button')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    sleep(1, log)
    click(driver,'//*[@id="checkout"]/div[4]/div[2]/div[1]/div/form[1]/div[9]/div/button','xpath',log)
    sleep(2, log)

#******
    # 验证Payment details页
    get_return_code(log, "---Payment details页测试---")
    assert_text(driver,'Step 2: Payment details','xpath','//*[@id="checkout"]/div[3]/div/div/div[1]/ol/li[2]',log,
                'Payment details页字段[Step 2: Payment details]显示正确',
                'Payment details页字段[Step 2: Payment details]显示错误')
    assert_text(driver, 'Payment method', 'xpath', '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[1]/div/h2', log,
                'Payment details页字段[Payment method]显示正确',
                'Payment details页字段[Payment method]显示错误')
    assert_text(driver, 'How would you like to pay?', 'xpath', '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[1]/div/p', log,
                'Payment details页字段[How would you like to pay?]显示正确',
                'Payment details页字段[How would you like to pay?]显示错误')
    assert_text(driver, 'Credit Card', 'xpath', '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[1]/div/ul/li[1]/a', log,
                'Payment details页字段[Credit Card]显示正确',
                'Payment details页字段[Credit Card]显示错误')
    assert_text(driver, 'Paypal', 'xpath', '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[1]/div/ul/li[2]/a', log,
                'Payment details页字段[Paypal]显示正确',
                'Payment details页字段[Paypal]显示错误')
    assert_text(driver, 'PLACE YOUR ORDER NOW', 'id', 'payment-form', log,
                'Payment details页字段[PLACE YOUR ORDER NOW]显示正确',
                'Payment details页字段[PLACE YOUR ORDER NOW]显示错误')
    sleep(1, log)
    click(driver,'//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[1]/div/ul/li[2]','xpath',log)
    sleep(1,log)
    assert_text(driver,'Place your order and you will complete your purchase via the Paypal.','xpath','//*[@id="paypal"]/p',log,
                'Payment details页字段[Place your order and you will complete your purchase via the Paypal.]显示正确',
                'Payment details页字段[Place your order and you will complete your purchase via the Paypal.]显示错误')
    click(driver,'//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[1]/div/ul/li[1]','xpath',log)
    sleep(1, log)

    assert_text(driver, 'By making this purchase you are agreeing to the Term & Conditions.', 'xpath', '//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[2]/div/p', log,
                'Payment details页字段[By making this purchase you are agreeing to the Term & Conditions.]显示正确',
                'Payment details页字段[By making this purchase you are agreeing to the Term & Conditions.]显示错误')
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    click(driver,'//*[@id="checkout"]/div[4]/div[2]/div[1]/div/div[2]/div/p/a','xpath',log)
    check_url(driver,url+'terms',log)
    sleep(1,log)
    back(driver,log)
    sleep(1, log)
    click(driver,'//*[@id="checkout"]/div[2]/div/div[1]/a/div[1]','xpath',log)
    sleep(3, log)

    driver.quit()
    get_return_code(log,'fpwebsite-ordering.py运行结束')

if __name__ == '__main__':
    ordering(sys.argv)