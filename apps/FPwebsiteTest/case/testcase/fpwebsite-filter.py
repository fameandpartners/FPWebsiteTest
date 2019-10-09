# -*- coding: utf-8 -*-
from time import sleep, time
from apps.FPwebsiteTest.src.function.FP_function import *
import random
import warnings
warnings.filterwarnings("ignore")

# 脚本信息
max_running_time = 1000  # 最大运行时间
author = '彭柔'  # 编写作者
date = '2019-08-01'  # 创建日期
description = 'AAA'  # 脚本描述
modules = '筛选功能'  # 归属模块
screenshots = 'True'  # 是否开启出错截图


def getLiEle(driver, xpath):
    elements = driver.find_element_by_xpath(xpath).find_elements_by_tag_name('li')
    element = driver.find_element_by_xpath(xpath + '/li[' + str(random.randint(1, len(elements))) + ']')
    return element


def main(argv):
    FILTER_KIND = 8
    filter_res_text = ''
    FILTER_TEXT = ['DELIVERED IN', 'PRICE', 'COLORS', 'OCCASION', 'SILHOUETTE', 'BODYSHAPE',
                   'FIT']
    COLORS_KIND_DICT = {'White / Ivory': "245, 244, 243", 'Tan / Sand': "230, 212, 192", 'Brown': "181, 101, 29",
                       'Blush': "222, 93, 131", 'Pink': "244, 88, 166", 'Orange': "255, 165, 0", 'Red': "224, 27, 27",
                       'Wine': "114, 47, 55", 'Lilac': "182, 102, 210", 'Blue': "0, 0, 255", 'Navy': "0, 0, 128",
                       'Green': "31, 119, 43", 'Gray': "126, 126, 127", 'Black': "5, 5, 5", 'Silver': "192, 192, 192",
                       'Gold': "212, 175, 55", 'Yellow': "223, 222, 10"}
    log, run_case_name, url = init_fp(argv)
    base_url = url
    driver = start_driver(1, log)
    driver.get(url)
    driver.maximize_window()
    close_bth = WebDriverWait(driver, 10, 1, NoSuchElementException).until(
        lambda x: driver.find_element_by_xpath('//*[@id="portal-root"]/div[3]/div/div/div/div/div[1]/button'))
    close_bth.click()

    xp = find_element(driver, 'Shop', 'link_text', log)
    ActionChains(driver).move_to_element(xp).perform()
    click(driver, 'Evening', 'link_text', log)
    check_url(driver, base_url + 'dresses/evening', log)
    dropdown_list(driver, '//*[@id="root"]/main/div/section[1]/div/div[1]/div/div[1]', log, 0, 2)
    sleep(3, log)

# -*-*-*-*
    # test-filter start
    for i in range(2, FILTER_KIND + 1):
        filter_len = len(driver.find_element_by_xpath('//*[@id="root"]/main/div/section[1]/div/div[2]').\
            find_elements_by_css_selector('.jsx-1537248613.Accordion'))
        if i <= filter_len + 1:
            if i > 3:
                n = (i - 3) * 200
                js = 'var q=document.documentElement.scrollTop=' + str(n)
                driver.execute_script(js)
            text_xp = '//*[@id="root"]/main/div/section[1]/div/div[2]/div[' + str(i) + ']/section[1]/p'
            text_ele = find_element(driver, text_xp, 'xpath', log)
            if text_ele.text in FILTER_TEXT:
                mess = '筛选选项[%s]名称显示正确' % text_ele.text
                get_return_code(log, mess)
            else:
                mess = '筛选选项[%s]名称显示错误' % text_ele.text
                get_return_code(log, mess, _code=500)
            ele = getLiEle(driver, '//*[@id="root"]/main/div/section[1]/div/div[2]/div[' + str(i) + ']/section[2]/ul')
            ele.find_element_by_class_name('jsx-2285590990').click()
            # sleep(3, log)
            # ActionChains(driver).move_to_element(ele).perform()
            # ele.click()
            mess = "The element [%s] was clicked." % ele.text
            get_return_code(log, mess)
            filter_res_text = filter_res_text + '_' + ele.text
        else:
            break
        sleep(2, log)
    get_return_code(log, '截取筛选结果:' + filter_res_text, free_shot=True)

# -*-*-*-*
    # 检测已选筛选收起显示是否正确
    # 收起筛选选项
    filters = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[1]/div/div[2]'). \
        find_elements_by_css_selector('.jsx-1537248613.Accordion')
    sleep(3, log)
    for filter in filters:
        filter.find_element_by_tag_name('section').click()
        mess = "The element [%s] was clicked." % filter.text.split('\n', maxsplit=1)[0]
        get_return_code(log, mess)
        sleep(2, log)
    # 检测收起选项是否显示正确
    clicked_filters = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[1]/div/div[2]'). \
                              find_elements_by_css_selector('.jsx-4086559974.Accordion')
    clicked_filters_len = len(clicked_filters)
    check_texts = filter_res_text.split(sep='_')
    sleep(2, log)
    for i in range(2, clicked_filters_len + 2):
        clicked_filter_all_xp = '//*[@id="root"]/main/div/section[1]/div/div[2]/div[' + str(i) + \
                                ']/section[1]/span'
        if check_texts[i-1] in COLORS_KIND_DICT:
            color_ele = find_element(driver, clicked_filter_all_xp, 'xpath', log)
            sleep(2, log)
            color_text_ele = color_ele.find_element_by_tag_name('div')
            color_text = color_text_ele.get_attribute('style')
            if COLORS_KIND_DICT[check_texts[i-1]] in color_text:
                get_return_code(log, '已选筛选选项[%s]收起显示正确' % check_texts[i-1])
            else:
                get_return_code(log, '已选筛选选项[%s]收起显示错误' % check_texts[i-1], _code=500)
        else:
            assert_text(driver, check_texts[i-1], 'xpath', clicked_filter_all_xp, log,
                        '已选筛选选项[%s]收起显示正确' % check_texts[i-1], '已选筛选选项[%s]收起显示错误' % check_texts[i-1])
    for filter in clicked_filters:
        filter.find_element_by_tag_name('section').click()
        mess = "The element [%s] was clicked." % filter.text.split('\n', maxsplit=1)[0]
        get_return_code(log, mess)
        sleep(2, log)

# -*-*-*-*
    js = 'var q=document.documentElement.scrollTop=0'
    driver.execute_script(js)

    # clear filter
    clear_filter_xp = '//*[@id="root"]/main/div/section[1]/div/div[2]/div[1]/a/span'
    assert_text(driver, 'Clear', 'xpath', clear_filter_xp, log,
                '筛选清除Clear显示正确', '筛选清除Clear显示错误')
    click(driver, clear_filter_xp, 'xpath', log)
    sleep(3, log)

# -*-*-*-*
    # 收起筛选选项
    filters = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[1]/div/div[2]').\
        find_elements_by_css_selector('.jsx-1537248613.Accordion')
    sleep(2, log)
    for filter in filters:
        filter.find_element_by_tag_name('section').click()
        mess = "The element [%s] was clicked." % filter.text.split('\n', maxsplit=1)[0]
        get_return_code(log, mess)
        sleep(3, log)
    # 检测收起选项all是否显示正确
    clicked_filters_len = len(driver.find_element_by_xpath('//*[@id="root"]/main/div/section[1]/div/div[2]').\
        find_elements_by_css_selector('.jsx-4086559974.Accordion'))

    for i in range(2, clicked_filters_len + 2):
        clicked_filter_all_xp = '//*[@id="root"]/main/div/section[1]/div/div[2]/div[' + str(i) + \
                                ']/section[1]/span'
        assert_text(driver, 'All', 'xpath', clicked_filter_all_xp, log, '筛选选项收起显示正确', '筛选选项收起显示错误')
    driver.quit()

if __name__ == '__main__':
    # debug 堵塞程序
    # lock_tolerance(tolerance_level=-1, _log=log)
    # sys.gui_application.exec()
    # print(sys.argv)
    main(sys.argv)


