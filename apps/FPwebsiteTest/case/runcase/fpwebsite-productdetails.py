import sys
import os
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))
sys.path.append(project_path)
from apps.FPwebsiteTest.src.function.FP_function import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import unittest
import warnings
from time import sleep, time
from selenium.webdriver.support import expected_conditions as EC


warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 2000  # 最大运行时间
author = '倪洁'  # 编写作者
date = '2019-07-29'  # 创建日期
description = 'FP网站-图片详情'  # 脚本描述
modules = '主流程'  # 归属模块
screenshots = 'False'  # 是否开启出错截图


def main(argv):
    status = 1
    # sleep_time = 2
    log, run_case_name, url = init_fp(argv)
    get_return_code(log_obj=log, msg='test')
    # driver = webdriver.Firefox()  # 初始化浏览器实例driver,默认浏览器安装位置，若自定义浏览器安装位置，可定制
    driver = start_driver(3, log)
    driver.maximize_window()
    # url = 'https://qa4.fameandpartners.com'
    # url = 'https://www.fameandpartners.com/'
    # driver.get(url)
    driver.implicitly_wait(10)
    sleep(2)
    # url = 'http://192.168.1.143:3002/dresses/dress-strappy-tri-cup-gown-1843?color=champagne-medium-matte-satin'
    url = 'https://www.fameandpartners.com/dresses/dress-strappy-tri-cup-gown-1843?color=champagne-medium-matte-satin'
    # url = 'https://qa4.fameandpartners.com/dresses/dress-strappy-tri-cup-gown-1843?color=champagne-medium-matte-satin'
    driver.get(url)
    sleep(5)
    click(driver, "//button[contains(@class, 'close')]", "xpath", log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/a',
          'xpath', log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/section[1]',
          'xpath', log)
    sleep(2)
    click(driver, "//*[@id='root']/main/div[1]/div[2]/div/div[2]/div/div[2]/section[2]/div/div/div[1]/div/div[1]/div/"
                  "div/picture/img", "xpath", log)
    sleep(2)
    js = 'document.getElementsByClassName("jsx-952236335 CustomizeInline__Content")[0].scrollTop=10000'
    driver.execute_script(js)
    sleep(2)  # 休眠2秒
    click(driver, '#root > main > div.jsx-286955943.PDP__Section.PDP__Section--Information.PDP__Section--Information--'
                  'customizing > div.jsx-1095644963.Sticky.PDP__Column__Configuration.Sticky--Desktop > div > div.jsx-'
                  '952236335.CustomizeInline__Content > div > div.jsx-4086559974.Accordion > section.jsx-4086559974.Ac'
                  'cordion--header', 'css_selector', log)
    sleep(2)
    js = 'document.getElementsByClassName("jsx-952236335 CustomizeInline__Content")[0].scrollTop=10000'
    driver.execute_script(js)
    sleep(2)
    click(driver,
          '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[3]/section[2]/div/div/div[10]/div/div[1]/div/div',
          'xpath', log)
    sleep(2)
    click(driver,'//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', 'xpath', log)
    sleep(2)
    assert_text(driver, "Light Nude Matte Satin", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div/ul/li', log,
                ' color显示类型2选择通过.', ' color显示类型2不通过.')
    #进入分类页面
    sleep(2)
    url = 'https://www.fameandpartners.com/dresses/custom-dress-FPG1003~1006~102~B25~B4~C1~CM~T18~T25~T86'
    # url = 'https://qa4.fameandpartners.com/dresses/custom-dress-FPG1003~1006~102~B25~B4~C1~CM~T18~T25~T86'
    driver.get(url)
    driver.implicitly_wait(10)
    sleep(2)
    # 测试进入首页
    try:
        assert "No results found." not in driver.page_source
        get_return_code(log_obj=log, msg=' --成功进入网站首页--')
    except Exception as e:
        get_return_code(log_obj=log, msg=' --进入网站首页发生异常--'.format(e))
    # click(driver, "//button[contains(@class, 'close')]", "xpath", log)
    sleep(2)
    click(driver, '#root > main > div.jsx-519801380.PDP__Section.PDP__Section--Information >'
                  'div.jsx-1095644963.Sticky.PDP__Column__Configuration.Sticky--Desktop > div >'
                  'div.jsx-1573779626.customization-overview > div > div:nth-child(3) >div.jsx-4086112330.title >'
                  'a', 'css_selector', log)
    sleep(2)
    click(driver, '#root > main > div.jsx-286955943.PDP__Section.PDP__Section--Information.PDP__Section--Information--'
                  'customizing > div.jsx-1095644963.Sticky.PDP__Column__Configuration.Sticky--Desktop > div > div.jsx-'
                  '3871296015.customization-footer > button', 'css_selector', log)
    sleep(2)
    click(driver, '#root > main > div.jsx-286955943.PDP__Section.PDP__Section--Information.PDP__Section--Information--'
                  'customizing > div.jsx-1095644963.Sticky.PDP__Column__Configuration.Sticky--Desktop > div > div.jsx-3'
                  '871296015.customization-footer > button.jsx-1369247218.button.Button.Button--secondary.Button--fullw'
                  'idth.action-buttons', 'css_selector', log)
    sleep(2)
    click(driver, '#root > main > div.jsx-286955943.PDP__Section.PDP__Section--Information.PDP__Section--Information--'
                  'customizing > div.jsx-1095644963.Sticky.PDP__Column__Configuration.Sticky--Desktop > div > div.jsx-'
                  '3871296015.customization-footer > button.jsx-1369247218.button.Button.Button--secondary.Button--ful'
                  'lwidth.action-buttons', 'css_selector', log)
    sleep(2)
    click(driver, '#root > main > div.jsx-286955943.PDP__Section.PDP__Section--Information.PDP__Section--Information--'
                  'customizing > div.jsx-1095644963.Sticky.PDP__Column__Configuration.Sticky--Desktop > div > div.jsx-'
                  '952236335.CustomizeInline__Content > div > div.jsx-3042810891.OptionsList__List.OptionsList__List--'
                  'MobileVerticalScroll > div:nth-child(5) > div > div.jsx-1235191726.image > div > div > picture > img'
          , 'css_selector', log)
    sleep(10)
    click(driver, '#root > main > div.jsx-286955943.PDP__Section.PDP__Section--Information.PDP__Section--Information--c'
                  'ustomizing > div.jsx-1095644963.Sticky.PDP__Column__Configuration.Sticky--Desktop > div > div.jsx-38'
                  '71296015.customization-footer > button.jsx-1369247218.button.Button.Button--secondary.Button--fullwi'
                  'dth.action-buttons', 'css_selector', log)
    sleep(2)
    # url = 'https://www.fameandpartners.com/'
    # driver.get(url)
    # # click(driver, "//button[contains(@class, 'close')]", "xpath", log)
    # sleep(2)
    # xp = driver.find_element_by_xpath('//*[@id="3xmW4MhfBeGEUoUYIYEQEI"]/header/nav/ul[1]/li[2]/a')
    # ActionChains(driver).move_to_element(xp).perform()
    # sleep(2)
    # click(driver, "//*[@id='portal-root']/div[1]/div/div/div/div/div/div[1]/ul/li[2]/a", "xpath", log)
    # sleep(2)
    # driver.switch_to.window(driver.window_handles[-1])
    # try:
    #     assert "No results found." not in driver.page_source
    #     get_return_code(log_obj=log, msg=' --evening分类成功访问--.')
    # except Exception as e:
    #     print("访问网页失败", format(e))
    #     get_return_code(log_obj=log, msg=' --evening分类访问网页失败--')
    # assert_text(driver, "Custom Evening Dresses", "xpath", '//*[@id="root"]/main/section/h1', log,
    #             ' 分类-Custom Evening Dresses界面标题校对通过.', ' 分类-Custom Evening Dresses界面标题校对不通过.')

    #点击进入商品详情页面（图片详情界面-01）
    # click(driver, '//*[@id="root"]/main/div/section[2]/div/div[1]/div[3]/a/div[1]/div[1]/div/picture/img',
    #               "xpath", log)
    # url = 'https://qa4.fameandpartners.com/dresses/custom-dress-FPG1273~1066~107~FM'
    url = 'https://www.fameandpartners.com/dresses/custom-dress-FPG1273~1066~107~FM'
    driver.get(url)
    sleep(2)
    # click(driver, "//button[contains(@class, 'close')]", "xpath", log)
    try:
        assert "No results found." not in driver.page_source
        get_return_code(log_obj=log, msg=' --商品详情-Drape Front Set成功访问--.')
    except Exception as e:
        get_return_code(log_obj=log, msg=' --商品详情-Drape Front Set访问网页失败--'.format(e))

    #页面布局图片滚轮下拉（图片详情-02）
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(2)
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
    sleep(2)

    #商品详情字段校对（图片详情-03）
    assert_text(driver, "Drape Front Set", "xpath", '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/h1', log,
                ' 商品详情界面字段-Drape Front Set通过.', ' 商品详情界面字段-Drape Front Set不通过.')
    assert_text(driver, "FABRIC & COLOR", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span', log,
                ' 商品详情界面字段-FABRIC & COLOR通过.', ' 商品详情界面字段-FABRIC & COLOR不通过.')
    assert_text(driver, "LENGTH", "xpath", '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/span', log,
                ' 商品详情界面字段-LENGTH通过.', ' 商品详情界面字段-LENGTH不通过.')
    assert_text(driver, "CUSTOMISATIONS", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[3]/div[1]/span', log,
                ' 商品详情界面字段-CUSTOMISATIONS通过.', ' 商品详情界面字段-CUSTOMISATIONS不通过.')
    assert_text(driver, "SIZE", "xpath", '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[4]/div[1]/span', log,
                ' 商品详情界面字段-SIZE通过.', ' 商品详情界面字段-SIZE不通过.')
    assert_text(driver, "ADD TO BAG", "xpath", '//*[@id="root"]/main/div[1]/div[2]/div/button/span', log,
                ' 商品详情界面字段-ADD TO BAG通过.', ' 商品详情界面字段-ADD TO BAG不通过.')
    assert_text(driver, "Shipping is free on your customized item. Learn more", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/p/span', log,
                ' 商品详情界面字段-learn more提示语通过.', ' 商品详情界面字段-learn more提示语不通过.')



    #test_Color01（图片详情-05）
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/a/span',
                  "xpath", log)
    sleep(2)
    svgelementXpath = "//*[@id='root']/main/div[1]/div[2]/div/div[1]/*[name()='svg']"
    svgelem = driver.find_element_by_xpath(svgelementXpath)
    action = ActionChains(driver)
    action.click(svgelem).perform()
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/a/span',
                  "xpath", log)
    assert_text(driver, "Fabric & Color", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div/h2', log,
                ' Color界面大标题-Fabric & Color测试通过.', ' Color界面大标题-Fabric & Color测试不通过.')
    assert_text(driver, "Matte Satin", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/h4', log,
                ' Color界面小标题-Matte Satin测试通过.', ' Color界面小标题-Matte Satin测试不通过.')


    # test_Color02
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div/div/div[3]/div/div[1]/div/div/picture/img',
                  "xpath", log)
    try:
        driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div/div/div[3]/div/div[1]/div/'
                                     'div/picture/img').is_selected()
        get_return_code(log_obj=log, msg=' 成功选中颜色')
    except Exception as e:
        get_return_code(log_obj=log, msg=' 选中颜色失败'.format(e))
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', "xpath", log)
    # EC.element_located_to_be_selected(driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div'
    #                                                                '/div/div/div[3]/div/div[1]/div/div/picture/img'))
    assert_text(driver, "Champagne, ", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div/ul/li[1]', log,
                ' Size界面属性选择测试通过.', ' Size界面属性选择测试不通过.')


    # 点击change进入size（图片详情-08）
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[4]/div[1]/a/span', "xpath", log)
    assert_text(driver, "Size", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div/h2', log,
                ' Size界面大标题-Size测试通过.', ' Size界面大标题-Size测试不通过.')
    assert_text(driver, "HEIGHT", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/p/span[1]', log,
                ' Size界面中标题-HEIGHT测试通过.', 'Size界面中标题-HEIGHT测试不通过.')
    assert_text(driver, "Tell us your height without heels and we'll do the rest", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/p/span[2]', log,
                ' Size界面中标题-Tell us your height without heels and we\'ll do the rest测试通过.',
                'Size界面中标题-Tell us your height without heels and we\'ll do the rest测试不通过.')
    assert_text(driver, "SIZE", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/p[1]/span', log,
                ' Size界面小标题-SIZE测试通过.', 'Size界面小标题-SIZE测试不通过.')
    assert_text(driver, 'View our size guide', 'xpath',
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/p[2]/a/span', log,
                'Size界面size guide链接字段校对通过', 'Size界面size guide链接字段校对不通过')
    handle = driver.current_window_handle
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/p[2]/a', 'xpath', log)
    sleep(5)
    handles = driver.window_handles
    for newhandle in handles:
        if newhandle != handle:
            driver.switch_to.window(newhandle)
            assert_text(driver, 'Size Guide', 'xpath',
                        '//*[@id="lEfrXagjoye6mAaQKKW0w"]/section/div/div/div/h1/span/p', log,
                        'size guide界面进入通过', 'size guide界面进入不通过')
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(2)
            # 切换页签
            # driver.switch_to.window(handles[0])
            driver.close()
    get_return_code(log_obj=log, msg=' 成功关闭size guide页签')
    driver.switch_to.window(handles[0])
    sleep(2)
    try:
        num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        size = ["US 0", "US 2", "US 4", "US 6", "US 8", "US 10", "US 12", "US 14", "US 16", "US 18", "US 20",
                "US 22"]
        for i in range(0, 12):
            assert size[i] == driver.find_element_by_xpath(
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div/div[' + num[i] + ']/div').text
            # print("size界面尺码{0}通过".format(size[i]))
            get_return_code(log_obj=log, msg="size界面尺码{0}通过".format(size[i]))
    except Exception as e:
        print("Size页面字段有异常", format(e))
        get_return_code(log_obj=log, msg=' Size页面字段有异常')
        sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/div[2]/span[2]/span',
                  "xpath", log)

    sleep(2)

    #校对size提示语（图片详情-08）
    op = driver.find_element_by_xpath(
        '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/input')
    op.clear()
    sleep(2)
    op.send_keys('142')
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/p/span[1]', "xpath", log)
    assert_text(driver, "Please enter your height between 147 and 193", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/span', log,
                ' size界面提示语1验证通过.', 'size界面提示语1验证不通过.')
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', "xpath", log)
    assert_text(driver, "Oh no, it seems that you haven't completed this, yet.", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div[2]/span', log,
                ' size界面提示语2验证通过.', 'size界面提示语2验证不通过.')
    assert_text(driver, "Please select your size.", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div/div[13]/span', log,
                ' size界面提示语3验证通过.', 'size界面提示语3验证不通过.')


    #size界面cm/in选择（图片详情-08）
    op = driver.find_element_by_xpath(
        '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/div[1]/div/input')
    sleep(2)
    op.clear()
    sleep(2)
    op.send_keys('156')
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div/div[1]/div', "xpath", log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', "xpath", log)
    assert_text(driver, "US 0 • 156cm", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[4]/div[2]/div/ul/li', log,
                ' cm选择size显示正常.', 'cm选择size显示不正常.')
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[4]/div[1]/a/span', "xpath", log)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/span[2]/span',
                  "xpath", log)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]', "xpath",
                  log)
    try:
        driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/'
                                     'div[1]').is_selected()
        get_return_code(log_obj=log, msg="in尺码下拉框选择成功")
    except Exception as e:
        get_return_code(log_obj=log, msg="in尺码下拉框选择失败".format(e))
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[2]/div/button[4]',
                  "xpath", log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', "xpath", log)
    assert_text(driver, "US 0 • 5' 1\"", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[4]/div[2]/div/ul/li', log,
                ' in选择size显示正常.', 'in选择size显示不正常.')
    sleep(2)

    #length界面字段校对（图片详情-06）
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/a/span', "xpath",
                  log)
    assert_text(driver, "Length", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div[1]/h2', log,
                ' length标题显示正常.', 'length标题显示不正常.')
    try:
        num = ["1", "2", "3", "4", "5"]
        size = ["Midi +$20", "Ankle +$20", "Casual Maxi +$30", "Formal Maxi +$30", "Petti +$10"]
        for i in range(0, 5):
            a = driver.find_element_by_xpath(
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[' + num[i] + ']/p').text
            assert size[i] == driver.find_element_by_xpath(
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[' + num[i] + ']/p').text
            get_return_code(log_obj=log, msg="Lenth界面尺码{0}通过".format(size[i]))
    except Exception as e:
        print("Length页面字段有异常", format(e))
        get_return_code(log_obj=log, msg=' Length页面字段有异常')
        sleep(2)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[3]', "xpath",
                  log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', "xpath", log)
    assert_text(driver, "Casual Maxi", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/div/ul/li', log,
                ' length选择属性后显示正常.', 'length选择属性后显示不正常.')
    sleep(2)

    #Customisations界面测试（图片详情-07）
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[3]/div[1]/a/span', "xpath", log)
    assert_text(driver, "Customisations", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div[1]/h2', log,
                ' 进入Customisations界面通过.', '进入Customisations界面不通过.')
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[1]', "xpath", log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', "xpath", log)
    assert_text(driver, "Side pockets", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/ul/li', log,
                ' Customisations界面属性选择通过.', 'Customisations界面属性选择不通过.')

    #按钮功能-add to bag（图片详情-09）
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/button', "xpath", log)
    sleep(5)
    svgelementXpath = '//*[@id="portal-root"]/div[2]/div/div/div/div/div[1]/a/*[name()="svg"]'
    svgelem = driver.find_element_by_xpath(svgelementXpath)
    action = ActionChains(driver)
    action.click(svgelem).perform()
    sleep(2)


    #learn more 界面测试（图片详情-10）
    handle = driver.current_window_handle
    click(driver, 'Learn more', "link_text", log)
    sleep(5)
    handles = driver.window_handles
    for newhandle in handles:
        if newhandle != handle:
            driver.switch_to.window(newhandle)
            assert_text(driver, "Frequently Asked Questions", "xpath",
                        '//*[@id="1nkKj217v2IC6GeYACmUGO"]/section/div/div/div/h1/span/p', log,
                        ' 进入learn more 界面通过.', '进入learn more 界面不通过.')
            sleep(2)
            click(driver, 'Delivery', "link_text", log)
            assert_text(driver, "Do you deliver to PO Boxes, military addresses or Parcel Lockers?", "id",
                        'doyoudelivertopoboxesmilitaryaddressesorparcellockers', log,
                        ' 进入Delivery页签通过.', '进入Delivery页签不通过.')
            sleep(2)
            click(driver, 'Returns & Exchanges', "link_text", log)
            assert_text(driver, "What is our returns policy?", "id",
                        'whatisourreturnspolicy', log,
                        ' 进入Returns & Exchanges页签通过.', '进入Returns & Exchanges页签不通过.')
            sleep(2)
            click(driver, 'My Order', "link_text", log)
            assert_text(driver, "Can I cancel my order?", "id",
                        'canicancelmyorder', log,
                        ' 进入My Order页签通过.', '进入My Order页签不通过.')
            sleep(2)
            #切换页签
            # driver.switch_to.window(handles[0])
            driver.close()
    get_return_code(log_obj=log, msg=' 成功关闭当前页签')
    driver.switch_to.window(handles[0])
    sleep(2)


    # chorme分享转发弹窗（图片详情-11）
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/a[1]', "xpath", log)
    sleep(2)
    assert_text(driver, "SHARE", "xpath",
                '//*[@id="portal-root"]/div[4]/div/div/div/div/div[2]/p/span', log,
                ' 进入分享弹窗界面字段1通过.', '进入分享弹窗界面字段1不通过.')
    assert_text(driver, "Drape Front Set", "xpath",
                '//*[@id="portal-root"]/div[4]/div/div/div/div/div[2]/h4', log,
                ' 进入分享弹窗界面字段2通过.', '进入分享弹窗界面字段2不通过.')
    handle = driver.current_window_handle
    click(driver, 'Facebook', 'link_text', log)
    sleep(5)
    handles = driver.window_handles
    for newhandle in handles:
        if newhandle != handle:
            driver.switch_to.window(newhandle)
            assert_text(driver, 'Facebook', 'id', 'homelink', log, 'facebook分享界面进入成功', 'facebook分享界面进入失败')
            sleep(2)
            driver.close()
    get_return_code(log_obj=log, msg=' 成功关闭facebook分享页签')
    driver.switch_to.window(handles[0])
    sleep(2)
    handle = driver.current_window_handle
    click(driver, 'Twitter', 'link_text', log)
    sleep(5)
    handles = driver.window_handles
    for newhandle in handles:
        if newhandle != handle:
            driver.switch_to.window(newhandle)
            assert_text(driver, 'Share a link with your followers', 'xpath', '//*[@id="bd"]/h2', log,
                        'Twitter分享界面进入成功', 'Twitter分享界面进入失败')
            # assert_text(driver, '与你的关注者分享链接', 'xpath', '//*[@id="bd"]/h2', log,
            #             'Twitter分享界面进入成功', 'Twitter分享界面进入失败')
            sleep(2)
            driver.close()
    get_return_code(log_obj=log, msg=' 成功关闭twitter分享页签')
    driver.switch_to.window(handles[0])
    handle = driver.current_window_handle
    click(driver, 'Pinterest', 'link_text', log)
    sleep(5)
    handles = driver.window_handles
    for newhandle in handles:
        if newhandle != handle:
            driver.switch_to.window(newhandle)
            sleep(5)
            assert_text(driver, 'Not on Pinterest yet? Sign up', 'xpath',
                        '/html/body/div[1]/div/div/div/div[3]/div/div/div[4]/div[2]/div/a'
                        , log, 'Pinterest分享界面进入成功', 'Pinterest分享界面进入失败')
            # assert_text(driver, '还不是 Pinterest 用户？ 注册', 'xpath',
            #             '/html/body/div[1]/div/div/div/div[3]/div/div/div[4]/div[2]/div/a'
            #             , log, 'Pinterest分享界面进入成功', 'Pinterest分享界面进入失败')
            sleep(2)
            driver.close()
    get_return_code(log_obj=log, msg=' 成功关闭Pinterest分享页签')
    driver.switch_to.window(handles[0])
    sleep(2)
    sleep(2)
    click(driver, '//*[@id="portal-root"]/div[4]/div/div/div/div/div[3]/div/input', 'xpath', log)
    sleep(2)
    svgelementXpath = "//*[@id='portal-root']/div[4]/div/div/div/div/div[1]/a/*[name()='svg']"
    svgelem = driver.find_element_by_xpath(svgelementXpath)
    action = ActionChains(driver)
    action.click(svgelem).perform()
    sleep(2)


    # #火狐分享转发弹窗
    # sleep(2)
    # driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/div[2]/div/div[3]/a[1]').click()
    # sleep(2)
    # assert_text(driver, "SHARE", "xpath",
    #             '//*[@id="portal-root"]/div[4]/div/div/div/div/div[2]/p/span', log,
    #             ' 进入分享弹窗界面字段1通过.', '进入分享弹窗界面字段1不通过.')
    # assert_text(driver, "Drape Front Set", "xpath",
    #             '//*[@id="portal-root"]/div[4]/div/div/div/div/div[2]/h4', log,
    #             ' 进入分享弹窗界面字段2通过.', '进入分享弹窗界面字段2不通过.')
    #
    # sleep(2)
    # driver.find_element_by_link_text("Facebook").click()
    # sleep(2)
    # windows = driver.window_handles
    # driver.switch_to.window(windows[1])
    # driver.close()
    # get_return_code(log_obj=log, msg=' 成功关闭当前页签')
    # driver.switch_to.window(windows[0])
    # sleep(2)
    # driver.find_element_by_link_text("Twitter").click()
    # sleep(2)
    # windows = driver.window_handles
    # driver.switch_to.window(windows[1])
    # driver.close()
    # get_return_code(log_obj=log, msg=' 成功关闭当前页签')
    # driver.switch_to.window(windows[0])
    # sleep(2)
    # driver.find_element_by_xpath('//*[@id="portal-root"]/div[4]/div/div/div/div/div[3]/div/input').click()
    # sleep(2)
    # svgelementXpath = "//*[@id='portal-root']/div[4]/div/div/div/div/div[1]/a/*[name()='svg']"
    # svgelem = driver.find_element_by_xpath(svgelementXpath)
    # action = ActionChains(driver)
    # action.click(svgelem).perform()
    # sleep(2)


    #布料小样选择页面（图片详情-12）
    handle = driver.current_window_handle
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/a[2]', 'xpath', log)
    sleep(5)
    handles = driver.window_handles
    for newhandle in handles:
        if newhandle != handle:
            driver.switch_to.window(newhandle)
            assert_text(driver, "Order Fabric Swatches", "xpath",
                        '//*[@id="3SEt4w3fOMyGioS24CqE8W"]/section/div/div/div/h1/span/p', log,
                        ' 颜色布料小样选择界面字段1通过.', '颜色布料小样选择界面字段1不通过.')
            assert_text(driver, "Select as many swatches of our georgette as you like and we will post them to you "
                                "within a few days. We will be adding other fabric swatches soon.", "xpath",
                        '//*[@id="3SEt4w3fOMyGioS24CqE8W"]/section/div/div/div/h2/span/p', log,
                        ' 颜色布料小样选择界面字段2通过.', '颜色布料小样选择界面字段2不通过.')
            click(driver, '//*[@id="1nrimfjEeYIWosM2qicm6i"]/section/div/div[1]/div[1]/div/div/picture/img', 'xpath',
                  log)
            sleep(5)
            svgelementXpath = "//*[@id='portal-root']/div[3]/div/div/div/div/div[1]/a/*[name()='svg']"
            svgelem = driver.find_element_by_xpath(svgelementXpath)
            action = ActionChains(driver)
            action.click(svgelem).perform()
            sleep(2)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(2)
            driver.close()
    get_return_code(log_obj=log, msg=' 成功关闭布料小样页签')
    driver.switch_to.window(handles[0])

    # #火狐颜色布料选择页面
    # driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/div[2]/div/div[3]/a[2]').click()
    # sleep(2)
    # windows = driver.window_handles
    # driver.switch_to.window(windows[1])
    # sleep(2)
    # assert_text(driver, "Order Fabric Swatches", "xpath",
    #             '//*[@id="3SEt4w3fOMyGioS24CqE8W"]/section/div/div/div/h1/span/p', log,
    #             ' 颜色布料选择界面字段1通过.', '颜色布料选择界面字段1不通过.')
    # assert_text(driver,
    #             "Select as many swatches of our georgette as you like and we will post them to you within a few days. We will be adding other fabric swatches soon.",
    #             "xpath",
    #             '//*[@id="3SEt4w3fOMyGioS24CqE8W"]/section/div/div/div/h2/span/p', log,
    #             ' 颜色布料选择界面字段2通过.', '颜色布料选择界面字段2不通过.')
    # driver.find_element_by_xpath(
    #     '//*[@id="1nrimfjEeYIWosM2qicm6i"]/section/div/div[1]/div[1]/div/div/picture/img').click()
    # sleep(5)
    # svgelementXpath = "//*[@id='portal-root']/div[3]/div/div/div/div/div[1]/a/*[name()='svg']"
    # svgelem = driver.find_element_by_xpath(svgelementXpath)
    # action = ActionChains(driver)
    # action.click(svgelem).perform()
    # sleep(2)
    # driver.close()
    # get_return_code(log_obj=log, msg=' 成功关闭当前页签')
    # driver.switch_to.window(windows[0])


    # #联系我们chat弹窗（图片详情-13）
    # click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/a[3]', 'xpath', log)
    # driver.implicitly_wait(5)
    # #切换到元素所在的frame
    # driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@title,'Zendesk Chat widget window')]"))
    # sleep(2)
    # try:
    #     assert driver.find_element_by_xpath(
    #         '/html/body/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/form/div[1]/div[1]/div[2]').text == \
    #            "Welcome! Let me help you with the perfect Outfit!"
    #     status == 1
    #     get_return_code(log_obj=log, msg=' 弹窗在线通过')
    # except Exception as e:
    #     assert driver.find_element_by_xpath(
    #         '/html/body/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/form/div[1]/div[1]/div[4]').text == \
    #            "Sorry, we aren't online at the moment."
    #     get_return_code(log_obj=log, msg=' 弹窗不在线通过'.format(e))
    #     status == 0
    # if status == 0:
    #     click(driver, '___$_31__submit', 'id', log)
    # else:
    #     click(driver, '/html/body/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div', 'xpath', log)
    # driver.switch_to.default_content()
    sleep(5)

    # 判断商品详情页面SILHOUETTE属性（分类显示部分，图片详情-14）
    xp = driver.find_element_by_xpath('//*[@id="root"]/header/nav/ul[1]/li[3]/a')
    ActionChains(driver).move_to_element(xp).perform()
    sleep(2)
    click(driver, "//*[@id='portal-root']/div[1]/div/div/div/div/div/div[2]/ul/li[3]/a", "xpath", log)
    sleep(2)
    click(driver, '//*[@id="75y2u0h9ciVst9ZAn9SQCi"]/section/div/div[1]/article/a/div/div[1]/div/picture/img', 'xpath',
          log)
    sleep(2)
    assert_text(driver, "Wrap", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/h1',
                log, 'create-Brides商品详情进入通过.', 'create-Brides商品详情进入不通过.')
    assert_text(driver, "SILHOUETTE", "xpath",
                '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/span',
                log, '商品详情-SILHOUETTE通过.', '商品详情-SILHOUETTE不通过.')
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/a', 'xpath', log)
    sleep(2)
    assert_text(driver, "Silhouette", "xpath", '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div[1]/h2', log,
                ' SILHOUETTE界面进入通过.', 'SILHOUETTE界面进入不通过.')
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button', 'xpath', log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button[2]', 'xpath', log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button[1]', 'xpath', log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[3]/button[1]', 'xpath', log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div[2]/span[2]', 'xpath', log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[1]/div[2]/span[3]', 'xpath', log)
    sleep(2)
    click(driver, '//*[@id="root"]/main/div[1]/div[2]/div/div[2]/div/div[2]/div[3]/div/div[1]/div/div/picture/img',
          'xpath', log)
    sleep(2)
    click(driver, '//*[@class="jsx-1369247218 button Button Button--secondary Button--fullwidth action-buttons"]',
          'xpath', log)
    sleep(2)


    #create分类中的自定制（分类显示部分，图片详情-14）
    # url = 'https://www.fameandpartners.com/dresses/custom-dress-FPG1003~1006~102~B28~C1~CM~T0~T67~T86'
    # driver.get(url)
    xp = driver.find_element_by_xpath('//*[@id="root"]/header/nav/ul[1]/li[3]/a')
    ActionChains(driver).move_to_element(xp).perform()
    sleep(2)
    click(driver, "//*[@id='portal-root']/div[1]/div/div/div/div/div/div[2]/ul/li[6]/a", "xpath", log)
    sleep(2)
    assert_text(driver, "Select your favourite and then customise into 22 colours, 6 lengths and multiple neckline and "
                        "sleeve options.", "id",
                'selectyourfavouriteandthencustomiseinto22colours6lengthsandmultiplenecklineandsleeveoptions', log,
                ' create-Starts字段1通过.', 'create-Starts字段1不通过.')
    target = driver.find_element_by_id("selectyourfavouriteandthencustomiseinto22colours6lengthsandmultiplenecklin"
                                       "eandsleeveoptions")
    driver.execute_script("arguments[0].scrollIntoView();", target)
    sleep(5)
    click(driver, '//*[@id="35SbhgNOlqwiqWoMGUIkCg"]/section/div/div[1]/article/a/div/div[1]/div/picture/img', 'xpath', log)
    sleep(5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(5)
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
    sleep(5)
    click(driver, '//*[@id="root"]/main/div[1]/div[1]/div/div[2]/div[2]', 'xpath', log)
    sleep(5)
    click(driver, '//*[@id="root"]/main/div[1]/div[1]/div/div[2]/div[1]', 'xpath', log)
    sleep(5)
    click(driver, '//*[@id="root"]/main/div[1]/div[1]/div/div[2]/div[2]', 'xpath', log)
    sleep(5)
    click(driver, '//*[@id="root"]/main/div[1]/div[1]/div/div[1]/picture/img', 'xpath', log)
    sleep(5)
    svgelementXpath = "//*[@id='root']/div/div[1]/div/div/*[name()='svg']"
    svgelem = driver.find_element_by_xpath(svgelementXpath)
    action = ActionChains(driver)
    action.click(svgelem).perform()
    sleep(2)
    assert_text(driver, "The Slip", "xpath", '//*[@class="jsx-1573779626 DressTitleWrapper__Title"]', log,
                'create-Starts商品详情字段1通过.', 'create-Starts商品详情字段1不通过.')
    sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    click(driver, '//*[@id="root"]/main/div[4]/div/a/div[1]/div/picture/img', 'xpath', log)
    sleep(2)
    get_return_code(log, "fpwebsite-productdetails.py脚本运行结束")


if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv)
