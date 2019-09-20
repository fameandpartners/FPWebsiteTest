# -*- coding:utf-8 -*-
# MTM 主流程测试 - 函数列表
import sys
import time
import struct
import os
import re
import pickle
from source.configs.readini import ConfigIni
from source.construct_project.get_project_path import PathExistProject
from source.utils.logclass.logconfig import Logger
from source.utils.file_operation import FileOperation
from source.utils.argumentparser import ArgumentParser

project_name = 'MTM'
current_path = os.path.dirname(__file__)
source_logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path)))), 'source/logs')
source_log_obj = Logger(log_path=source_logs_path)

pa = PathExistProject(project_name=project_name, log_obj=source_log_obj)
path_data = pa.return_path()
dir_test_data_path = path_data["test_data_path"]


ini = ConfigIni(log_obj=source_log_obj)
release_dir_path = ini.get_str(section='MTM', option='release')
exe_path = release_dir_path + '/USM2MShell.exe'
sys.path.append(release_dir_path)


'''True->界面执行; False->脚本执行'''
_is_UI_running_ = True

'''True->错误后交给用户操作; False->不'''
_is_user_op_after_fail = False

'''实际打开的产品路径'''
_product_path_ = "."

'''测试数据TestData的路径'''
_test_data_path_ = ""

_gui_application_ = None

current_time = str(int(time.time()))


# 日志打印
def get_return_code(log_obj, msg, _code=0):
    if _code != 0:
        if msg:
            log_obj.exception('  -* ERROR-Code: %s, ERROR-Mess: %s' % (_code, msg))
            # get_screenshots(_code, save_images_path=config.dir_mtm_eimages_path)
            exit(_code)
    else:
        if msg:
            log_obj.info('  -* %s' % msg)


# 初始化信息获取
def init_mtm(argv):
    argument = ArgumentParser(argv)
    log_path = argument.get_log_file_name()
    run_case_name = argument.get_case_name()
    file_path, file_name_with_suffix = os.path.split(log_path)
    _file_name = os.path.splitext(file_name_with_suffix)[0]
    log = Logger(log_path=file_path, log_name=_file_name, use_console=True)
    # 创建数据保存目录
    _dir = dir_test_data_path
    create_dir_name = os.path.splitext(run_case_name)[0] + '/save_mtm'
    FileOperation().create_new_dir(_dir=_dir, create_dir_name=create_dir_name)
    # 保存mtm工程名设定
    save_mtm_file_path = _dir + create_dir_name + '/'
    get_return_code(log_obj=log, msg='The main process test begins')

    return save_mtm_file_path, log, run_case_name


# 撤销
def revoked():
    import PyUSM2M
    main_module = PyUSM2M.USM2MGuiModuleMain.getMainModule()
    main_window = main_module.getMainWindow()
    action = main_window.getAction(r'撤销')
    while action.isEnabled():
        action.trigger()


# 打开项目
def open_project(project_file, _log):  # 传入参数 - 项目文件
    global _product_path_
    import PyUSM2M
    main_module = PyUSM2M.USM2MGuiModuleMain.getMainModule()
    main_window = main_module.getMainWindow()
    open_project_action = main_window.getAction("打开工程")  # 动作指令
    main_module.addCurrentFiles([project_file, ])
    # _log.info('  -* 项目文件[%s]被打开' % project_file)
    _mess = '项目文件[%s]被打开' % project_file
    get_return_code(log_obj=_log, msg=_mess)
    open_project_action.trigger()
    _product_path_ = project_file
    return


# 菜单 - 文件 - 新建工程
def create_new_project(_path, _log):  # 传入参数 - dxf文件
    global _product_path_  # 全局变量
    import PyUSM2M
    import PyUSUIBase
    sys.gui_application = PyUSM2M.USM2MApplication([exe_path])
    sys.gui_application.init(False)
    main_module = PyUSUIBase.USGuiModuleMain.getMainModule()
    main_window = main_module.getMainWindow()
    open_project_action = main_window.getAction("新建工程")
    main_module.addCurrentFiles([_path, ])
    open_project_action.trigger()
    get_return_code(log_obj=_log, msg='Create New Project Successfully')
    _product_path_ = _path
    return


# 菜单 - 文件 - 保存工程
def save_project(mtm_file, _log):  # 传入参数 - m2m文件
    global _product_path_
    import PyUSM2M
    main_module = PyUSM2M.USM2MGuiModuleMain.getMainModule()
    main_window = main_module.getMainWindow()
    open_project_action = main_window.getAction("保存工程")
    main_module.addCurrentFiles([mtm_file, ])
    open_project_action.trigger()
    # _log.info('  -* Save Project File [%s] Successfully' % mtm_file)
    _mess = 'Save Project File [%s] Successfully' % mtm_file
    get_return_code(log_obj=_log, msg=_mess)
    _product_path_ = mtm_file

    return


# 点击菜单
def click_menu(name, _log):  # 传入参数 - 名称

    import PyUSUIBase
    main_module = PyUSUIBase.USGuiModuleMain.getMainModule()
    main_window = main_module.getMainWindow()

    action = main_window.getAction(name)
    if action:
        action.trigger()
        # _log.info('  -* Click Menu [%s]' % name)
        _mess = 'Click Menu [%s]' % name
        get_return_code(log_obj=_log, msg=_mess)
    else:
        # _log.error('  -* Menu [%s] Does Not Exist' % name)
        _mess = 'Menu [%s] Does Not Exist' % name
        get_return_code(log_obj=_log, msg=_mess, _code=500)
        return

    return


# 锁定宽容
def lock_tolerance(tolerance_level, _log):  # 传入参数 - 宽容度

    import PyUSM2M
    python_commander = PyUSM2M.USPythonCommander.getInstance()
    python_commander.setFixedTol(tolerance_level)
    # _log.info('  -* Lock Tolerance level [%s]' % tolerance_level)
    _mess = 'Lock Tolerance level [%s]' % tolerance_level
    get_return_code(log_obj=_log, msg=_mess)


# 设为上身部位点
def set_upper_body_point(x, y, _x, _y, _log):
    # 移动鼠标
    drag_mouse(x=x, y=y, _x=_x, _y=_y, _log=_log, mouse_button='左键', specifier='')
    click_button(name='设为上身部位点', _log=_log)
    # _log.info('  -* Set Upper Body Point Successfully')
    _mess = 'Set Upper Body Point Successfully'
    get_return_code(log_obj=_log, msg=_mess)


# 设为下身部位点
def set_lower_body_point(x, y, _x, _y, _log):
    # 移动鼠标
    drag_mouse(x=x, y=y, _x=_x, _y=_y, _log=_log, mouse_button='左键', specifier='')
    click_button(name='设为下身部位点', _log=_log)
    # _log.info('  -* Set Lower Body Point Successfully')
    _mess = 'Set Lower Body Point Successfully'
    get_return_code(log_obj=_log, msg=_mess)


# 设为混合类型部位点
def set_mixed_type_point(x, y, _x, _y, _log):
    # 移动鼠标
    drag_mouse(x=x, y=y, _x=_x, _y=_y, _log=_log, mouse_button='左键', specifier='')
    click_button(name='设为混合类型部位点', _log=_log)
    # _log.info('  -* Set Mixed Type Point Successfully')
    _mess = 'Set Mixed Type Point Successfully'
    get_return_code(log_obj=_log, msg=_mess)


# 设置为对称面片
def click_set_symmetrical_patch(x, y, _log):
    click_mouse(x=x, y=y, _log=_log, mouse_button="左键", specifier='')
    click_button(name='设置为对称面片', _log=_log)
    # _log.info('  -* Set Symmetrical Patch Successfully')
    _mess = 'Set Symmetrical Patch Successfully'
    get_return_code(log_obj=_log, msg=_mess)


def drag_set_symmetrical_patch(x, y, _x, _y, _log):
    drag_mouse(x=x, y=y, _x=_x, _y=_y, _log=_log, mouse_button="左键", specifier='')
    click_button(name='设置为对称面片', _log=_log)
    # _log.info('  -* Set Symmetrical Patch Successfully')
    _mess = 'Set Symmetrical Patch Successfully'
    get_return_code(log_obj=_log, msg=_mess)


# 设置绑定约束 - 内缝长
def seam_length_binding_constraints(x, y, angle, proportion, _log):
    click_mouse(x, y, _log=_log, mouse_button="左键", specifier='')
    add_binding_constraints(parts_name='内缝长', angle=angle, proportion=proportion, _log=_log)


# 设置绑定约束 - 袖长
def sleeve_length_binding_constraints(x, y, angle, proportion, _log):
    click_mouse(x, y, _log=_log, mouse_button="左键", specifier='')
    add_binding_constraints(parts_name='袖长', angle=angle, proportion=proportion, _log=_log)


# 设置绑定约束 - 浪长
def sleeve_wave_length_binding_constraints(x, y, angle, proportion, _log):
    click_mouse(x, y, _log=_log, mouse_button="左键", specifier='')
    add_binding_constraints(parts_name='整浪长', angle=angle, proportion=proportion, _log=_log)


# 设置绑定约束 - 下臀围
def hip_circumference_binding_constraints(x, y, angle, proportion, _log):
    click_mouse(x, y, _log=_log, mouse_button="左键", specifier='')
    add_binding_constraints(parts_name='下臀围', angle=angle, proportion=proportion, _log=_log)


# 设置绑定约束 - 腰围
def waist_circumference_binding_constraints(x, y, angle, proportion, _log):
    click_mouse(x, y, _log=_log, mouse_button="左键", specifier='')
    add_binding_constraints(parts_name='腰围', angle=angle, proportion=proportion, _log=_log)


# 设置绑定约束 - 前上身长
def upper_body_length_binding_constraints(x, y, angle, proportion, _log):
    click_mouse(x, y, _log=_log, mouse_button="左键", specifier='')
    add_binding_constraints(parts_name='前上身长', angle=angle, proportion=proportion, _log=_log)


#  设置绑定约束 - 浪弯保持
def wave_bending_constraints(x, y, _log):
    click_menu(name='浪弯形状保持约束', _log=_log)
    click_mouse(x=x, y=y, _log=_log, mouse_button="左键", specifier='')
    click_button(name='增加约束', _log=_log)


# 设置罩杯旋转约束 -- 传入字典 coordinates
def cups_rotating_constrains(coordinates, _log):
    """
    coordinates = {
        '选择裁片': (-0.10252, 0.25485),
        '设置水平轴': [(12, 34), (12, 34)],
        '设置垂直轴': [(12, 34), (12, 34)],
        '设置旋转中心': (12, 34),
        '设置旋转参考点': (12, 34),
    }
    """
    click_menu(name='罩杯旋转约束', _log=_log)
    # 选择裁片
    l_r_click_mouse(x=str(coordinates['选择裁片'][0]), y=str(coordinates['选择裁片'][1]), _log=_log)
    # 设置水平轴
    click_mouse(x=str(coordinates['设置水平轴'][0][0]), y=str(coordinates['设置水平轴'][0][1]), _log=_log)
    click_mouse(x=str(coordinates['设置水平轴'][1][0]), y=str(coordinates['设置水平轴'][1][1]), _log=_log)
    # 设置垂直轴
    click_mouse(x=str(coordinates['设置垂直轴'][0][0]), y=str(coordinates['设置垂直轴'][0][1]), _log=_log)
    click_mouse(x=str(coordinates['设置垂直轴'][1][0]), y=str(coordinates['设置垂直轴'][1][1]), _log=_log)
    # 设置旋转中心
    click_mouse(x=str(coordinates['设置旋转中心'][0]), y=str(coordinates['设置旋转中心'][1]), _log=_log)
    # 设置旋转参考点
    click_mouse(x=str(coordinates['设置旋转参考点'][0]), y=str(coordinates['设置旋转参考点'][1]), _log=_log)


# 设置点平滑约束 -- 传入列表 point_list
def point_smoothing_constraint(point_list, _log):
    """
       point_list = [(),(),()......]
    """
    click_menu(name='点平滑约束', _log=_log)
    for item in point_list:
        click_mouse(x=str(item[0]), y=str(item[1]), _log=_log)
        click_button(name='增加约束', _log=_log)


# 设置固定点 -- 传入列表 fixed_list
def set_fixed_protection(fixed_list, _log):
    """
       fixed_list = [(),(),()......]
    """
    click_menu(name='设置固定点', _log=_log)
    for item in fixed_list:
        fixed_protection(x=str(item[0]), y=str(item[1]), _log=_log)


# 拷贝裁片约束 -- 传入列表 parts_list
def copy_cut_parts_constraint(parts_list, _log):
    """
       parts_list = [[(A裁片),(B裁片-A裁片约束copy到B裁片)], [(),()]......]
    """
    click_menu(name='拷贝裁片约束', _log=_log)
    for item in parts_list:
        l_r_click_mouse(x=str(item[0][0]), y=str(item[0][1]), _log=_log)
        l_r_click_mouse(x=str(item[1][0]), y=str(item[1][1]), _log=_log)


# 输入文本
def input_txt(name, txt, _log):  # 传入参数 - 名称, 文本
    control = find_controls(name=name, _log=_log)
    if control is None:
        return
    control.setText(str(txt))


# 添加测试点
def new_add_test(name, case_name, _log, is_test=False):  # 传入参数 - 测试点名称, 文本

    # 保存测试点数据
    if not is_test:
        a = OrderData(log_obj=_log, test_case_file_name=case_name, _test_point_name=name)
        a.get_current_order()
        a.save_current_order_data()
        # _log.info('  -* 测试点 [%s] 创建成功' % name)
        _mess = '测试点 [%s] 创建成功' % name
        get_return_code(log_obj=_log, msg=_mess)
        return
    else:
        # 数据对比
        b = CompareData(current_case_name=case_name, current_test_point_name=name, log_obj=_log)
        compare_result = b.compare_save_and_run_data()  # [num, msg] 0, 1, 2, 3, 4, 5
        # _log.info('  *this is compare result: %s' % str(compare_result))
        _mess = 'this is compare result: %s' % str(compare_result)
        get_return_code(log_obj=_log, msg=_mess)

        if compare_result[0] == 0:
            msg = compare_result[1]
            get_return_code(log_obj=_log, msg=msg)
        else:
            msg = compare_result[1]
            get_return_code(log_obj=_log, msg=msg, _code=500)

        if _is_user_op_after_fail and not _is_UI_running_:
            _log.info("  -* 执行权交给用户")
            _gui_application_.exec()


# =================================================原函数===============================================================
# 增加绑定约束
def add_binding_constraints(parts_name, angle, proportion, _log):  # 传入参数 - 部位名称, 角度, 比例
    import PyUSM2M
    parts_name = re.sub('\s', '', parts_name)
    python_commander = PyUSM2M.USPythonCommander.getInstance()
    if not python_commander.addBindConstraint(parts_name, angle, proportion):
        # _log.error('  -* 增加绑定约束[%s,%.3f,%.3f]失败' % (parts_name, angle, proportion))
        _mess = '增加绑定约束[%s,%.3f,%.3f]失败' % (parts_name, angle, proportion)
        get_return_code(log_obj=_log, msg=_mess, _code=500)


# 定点绑定约束
def fixed_point_binding_constraints(x, y, parts_name, angle, proportion, _log):
    click_mouse(x, y, _log=_log, mouse_button="左键", specifier="")
    add_binding_constraints(parts_name=parts_name, angle=angle, proportion=proportion, _log=_log)


# 删除绑定约束
def delete_binding_constraints(subscript, _log):  # 传入参数 - 下标
    import PyUSM2M
    if not isinstance(subscript, int) or subscript <= 0:
        # _log.error('  -* 删除绑定约束需要正整数下标 [%s]' % str(subscript))
        _mess = '删除绑定约束需要正整数下标 [%s]' % str(subscript)
        get_return_code(log_obj=_log, msg=_mess, _code=500)
    python_commander = PyUSM2M.USPythonCommander.getInstance()
    if not python_commander.deleteBindConstraint(subscript - 1):
        # _log.error('  -* 删除绑定约束 [%d] 失败' % subscript)
        _mess = '删除绑定约束 [%d] 失败' % subscript
        get_return_code(log_obj=_log, msg=_mess, _code=500)


# 修改绑定约束
def modify_binding_constraints(parts_name, angle, proportion, _log):  # 传入参数 - 部位名称, 角度, 比例
    import PyUSM2M
    parts_name = re.sub('\s', '', parts_name)
    python_commander = PyUSM2M.USPythonCommander.getInstance()
    if not python_commander.alterBindConstraint(parts_name, angle, proportion):
        # _log.error('  -* 修改绑定约束[%s,%.3f,%.3f]失败' % (parts_name, angle, proportion))
        _mess = '修改绑定约束[%s,%.3f,%.3f]失败' % (parts_name, angle, proportion)
        get_return_code(log_obj=_log, msg=_mess, _code=500)


# 定固定点
def fixed_protection(x, y, _log):  # 传入参数 - 横坐标, 纵坐标，鼠标键， 修饰符
    click_mouse(x=x, y=y, _log=_log, mouse_button='左键', specifier='')
    click_button(name="设置固定点", _log=_log)


# ======================================================鼠标事件========================================================

# 移动鼠标
def move_mouse(x, y, _log, mouse_button="左键", specifier=""):
    send_mouse_events(x=x, y=y, _log=_log, _m_events="移动", m_button=mouse_button, specifier=specifier)


# 释放鼠标
def release_mouse(x, y, _log, mouse_button="左键", specifier=""):
    send_mouse_events(x=x, y=y, _log=_log, _m_events="释放", m_button=mouse_button, specifier=specifier)


# 按下鼠标
def press_mouse(x, y, _log, mouse_button="左键", specifier=""):
    send_mouse_events(x=x, y=y, _log=_log, _m_events="按下", m_button=mouse_button, specifier=specifier)


# 拖动鼠标
def drag_mouse(x, y, _x, _y, _log, mouse_button="左键", specifier=""):
    press_mouse(x=x, y=y, _log=_log, mouse_button=mouse_button, specifier=specifier)
    move_mouse(x=_x, y=_y, _log=_log, mouse_button=mouse_button, specifier=specifier)
    release_mouse(x=_x, y=_y, _log=_log, mouse_button=mouse_button, specifier=specifier)


# 点击鼠标
def click_mouse(x, y, _log, mouse_button="左键", specifier=""):
    move_mouse(x=x, y=y, _log=_log, mouse_button=mouse_button, specifier=specifier)
    press_mouse(x=x, y=y, _log=_log, mouse_button=mouse_button, specifier=specifier)
    release_mouse(x=x, y=y, _log=_log, mouse_button=mouse_button, specifier=specifier)


# 左右键点击鼠标
def l_r_click_mouse(x, y, _log):
    press_mouse(x=x, y=y, _log=_log, mouse_button='左键', specifier='')
    release_mouse(x=x, y=y, _log=_log, mouse_button='左键', specifier='')
    press_mouse(x=x, y=y, _log=_log, mouse_button='右键', specifier='')
    release_mouse(x=x, y=y, _log=_log, mouse_button='右键', specifier='')


# 发送鼠标事件
def send_mouse_events(x, y, _log, _m_events, m_button="左键", specifier=""):
    import PyQt5
    import PyUSM2M
    _mouse_event_map = {
        "按下": PyQt5.QtCore.QEvent.MouseButtonPress,
        "释放": PyQt5.QtCore.QEvent.MouseButtonRelease,
        "双击": PyQt5.QtCore.QEvent.MouseButtonDblClick,
        "移动": PyQt5.QtCore.QEvent.MouseMove
    }
    _mouse_button_map = {
        "左键": PyQt5.QtCore.Qt.LeftButton,
        "右键": PyQt5.QtCore.Qt.RightButton
    }
    _modifier_map = {
        "ctrl": PyQt5.QtCore.Qt.ControlModifier,
        "shift": PyQt5.QtCore.Qt.ShiftModifier,
        "alt": PyQt5.QtCore.Qt.AltModifier
    }

    # 鼠标事件
    _m_events = re.sub('\s', '', _m_events)
    mouse_event = _mouse_event_map.get(_m_events)
    if not mouse_event:
        # _log.error('  -* Mouse Event [%s] Unable to identify' % _m_events)
        _mess = 'Mouse Event [%s] Unable to identify' % _m_events
        get_return_code(log_obj=_log, msg=_mess, _code=500)
        return
    # 鼠标左右键
    m_button = re.sub('\s', '', m_button)
    mouse_button = _mouse_button_map.get(m_button)
    if not mouse_button:
        # _log.error('  -* Mouse Button [%s] Unable to identify' % m_button)
        _mess = 'Mouse Button [%s] Unable to identify' % m_button
        get_return_code(log_obj=_log, msg=_mess, _code=500)
        return
    # 键盘修饰符
    modifiers = PyQt5.QtCore.Qt.NoModifier
    modifier_str_s = re.sub('\s', '', specifier)
    modifier_str_s = modifier_str_s.split('|')
    for modifier_str in modifier_str_s:
        if modifier_str == '':
            continue
        modifier = _modifier_map.get(modifier_str)
        if not modifier:
            # _log.error('  -* Keyboard modifier [%s] Unable to identify' % modifier_str)
            _mess = 'Keyboard modifier [%s] Unable to identify' % modifier_str
            get_return_code(log_obj=_log, msg=_mess, _code=500)
            return
        modifiers = modifiers + modifier
    python_commander = PyUSM2M.USPythonCommander.getInstance()
    python_commander.sendMouseEvent(float(x), float(y), mouse_event, mouse_button, modifiers)


# 点击按钮
def click_button(name, _log):  # 传入参数 - 名称
    control = find_controls(name=name, _log=_log)
    if control is None:
        return
    control.click()
    # _log.info('  -* Click Button [%s]' % name)
    _mess = 'Click Button [%s]' % name
    get_return_code(log_obj=_log, msg=_mess)


# 查找控件
def find_controls(name, _log, type=None):  # 传入参数 - 名称, 类型

    import PyQt5
    import PyUSUIBase
    main_module = PyUSUIBase.USGuiModuleMain.getMainModule()
    main_window = main_module.getMainWindow()
    widget_class = type
    if not widget_class:
        widget_class = PyQt5.QtWidgets.QWidget
    found_control = None
    for control in main_window.findChildren(widget_class):
        if control.objectName() == name:
            if not found_control or control.isVisible():
                found_control = control
    if found_control:
        return found_control
    else:
        # _log.error('  -* Found Control [%s] Failed')
        _mess = 'Found Control [%s] Failed' % name
        get_return_code(log_obj=_log, msg=_mess, _code=500)
        return None


# 切换页面
def switch_page(name, _log):  # 传入参数 - 名称
    control = find_controls(name=name, _log=_log)
    if control is None:
        return
    if control.parent() != None and control.parent().parent() != None and hasattr(control.parent().parent(),
                                                                                  "setCurrentWidget"):
        control.parent().parent().setCurrentWidget(control)
    else:
        # _log.error('  -* 控件[%s]不可切换页面' % name)
        _mess = '控件[%s]不可切换页面' % name
        get_return_code(log_obj=_log, msg=_mess, _code=500)


# 点击多选
def click_multi_select(name, _log):  # 传入参数 - 名称
    click_button(name=name, _log=_log)


# 滑动滑块
def move_slider(name, proportion, _log):  # 传入参数 - 名称, 比例
    control = find_controls(name=name, _log=_log)
    if control is None:
        return
    if proportion < 0 or proportion > 1:
        # _log.error('  -* 滑块范围[%.3f]不在(0,1)之间' % proportion)
        _mess = '滑块范围[%.3f]不在(0,1)之间' % proportion
        get_return_code(log_obj=_log, msg=_mess, _code=500)
    range = (control.maximum() - control.minimum())
    control.setValue(control.minimum() + proportion * range)


# 切换订单
def switch_order(order_number, _log):  # 传入参数 - 订单编号
    order_number = re.sub('\s', '', order_number)
    python_commander = PyUSM2M.USPythonCommander.getInstance()
    if not python_commander.setCurrentOrder(order_number):
        # _log.error('  -* 切换订单[%s]失败' % order_number)
        _mess = '切换订单[%s]失败' % order_number
        get_return_code(log_obj=_log, msg=_mess, _code=500)
    return


# 切换版型
def switch_model(model_name, _log):  # 传入参数 - 版型名称
    control = find_controls(name=model_name, _log=_log)
    if control is None:
        return
    python_commander = PyUSM2M.USPythonCommander.getInstance()
    python_commander.switchPattern(control)


def GetProductPath():
    return _product_path_


def GetProductDir():
    return os.path.dirname(_product_path_)


def GetProductName():
    return os.path.basename(GetProductDir())


class OrderData:

    def __init__(self, log_obj, test_case_file_name, _test_point_name):
        self.current_case_name = str(test_case_file_name)
        self.test_point_name = str(_test_point_name)
        self.order_count = ''  # 订单数量
        self.patterns_num = ''  # 订单场景中版型的 pattern 数量
        self.patterns_objects_list = []  # 订单场景中版型的 pattern 的对象列表
        self.log_obj = log_obj

        self.current_order_pattern_data = {}
        # self.point_coordinate = []

        self.save_data = ''

    def get_current_order(self):

        import PyUSM2M
        import PyUSPlatform
        data_manager = PyUSM2M.USM2MDataManager.getCurrentDataManager()  # 数据管理
        order_manager = data_manager.getOrderManager()  # 订单管理
        order_count = order_manager.getOrderCount()  # 订单数量

        if order_count == 0:
            # self.log_obj.info('  -*当前订单数量为 %s ' % str(order_count))
            _mess = '当前订单数量为 %s ' % str(order_count)
            get_return_code(log_obj=self.log_obj, msg=_mess)
            return

        self.order_count = order_count
        order_id = order_manager.getCurrentOrder()
        curent_order = PyUSM2M.USOrder.FromObject(data_manager.LoadObject(order_id))  # 当前订单

        # 获取订单中的结果版型
        patterns_ids = curent_order.getResultPatterns()
        self.patterns_num = patterns_ids.count()

        # 获取所有 patterns 对象列表
        for item in range(self.patterns_num):
            pattern_index_data = []
            vertex_data = []
            pattern_obj = PyUSM2M.USPattern.FromObject(data_manager.LoadObject(patterns_ids[item]))
            pattern_obj_index = pattern_obj.GetPatternIndex()  # 获取每个 pattern 的 index 索引 固定
            pattern_obj_name = pattern_obj.GetName()  # TODO 面片名称可能会重复
            self.patterns_objects_list.append(pattern_obj)
            if self.current_order_pattern_data.get(str(pattern_obj_index)) is None:
                self.current_order_pattern_data[str(pattern_obj_index)] = pattern_index_data
            else:
                # self.log_obj.error("duplicated pattern name: " + str(pattern_obj_index))
                _mess = 'duplicated pattern name: [%s]' % str(pattern_obj_index)
                get_return_code(log_obj=self.log_obj, msg=_mess, _code=500)

            # 获取订单中每个 pattern 的边的数量
            edge_ids = pattern_obj.GetEdges()  # 获取每个 pattern_obj 的所有边的 id
            pattern_index_data.append(str(len(edge_ids)))  # 存入边的数量
            pattern_index_data.append(vertex_data)  # 存入顶点数据

            # 获取 pattern 顶点的数量 和 坐标
            vertex_count = pattern_obj.GetVertexCount()  # 获取对应 pattern 的顶点的数量
            vertex_ids_list = pattern_obj.GetVertices()  # 获取对应pattern的所有顶点的id type list
            vertex_data.append(vertex_count)
            dict_data_vertex = {}
            vertex_data.append(dict_data_vertex)

            for index, vertex_id in enumerate(vertex_ids_list):
                single_vertex_obj = PyUSM2M.USPatternVertex.FromObject(data_manager.LoadObject(vertex_ids_list[index]))
                # 获取 vertex index
                single_vertex_obj_index = pattern_obj.GetVertexIndex(vertex_id)  # USID
                _L = single_vertex_obj.GetGeometry()
                vertex_xyz = _L.GetCoordinates()
                vertex_x = vertex_xyz[0]
                vertex_y = vertex_xyz[1]
                vertex_z = vertex_xyz[2]
                dict_data_vertex[str(single_vertex_obj_index)] = (vertex_x, vertex_y, vertex_z)

            edge_data = {}
            for _item in edge_ids:

                # 获取每条边的index 索引 固定
                edge_index = pattern_obj.GetEdgeIndex(_item)
                edge = PyUSM2M.USPatternEdge.FromObject(data_manager.LoadObject(edge_ids[edge_index]))
                ln = edge.GetGeometry()
                ln_points = []
                points_count = ln.GetPointCount()

                for __item in range(0, 11):
                    _ratio = __item / 10
                    XYZ = ln.Evaluate(_ratio)  # 等比例采样
                    x = XYZ[0]
                    y = XYZ[1]
                    z = XYZ[2]
                    ln_points.append([x, y, z])
                edge_data[str(edge_index)] = ln_points

            pattern_index_data.append(edge_data)

        save_data = {
            "order_num": self.order_count,
            "current_order_patterns_num": self.patterns_num,
            "current_order_pattern_data": self.current_order_pattern_data
        }
        self.save_data = save_data
        return save_data

    def save_current_order_data(self):

        # 在 testcase 目录下 创建以 测试用例名命名的文件夹 - 保存二进制测试数据
        (_name, _name_suffix) = os.path.splitext(self.current_case_name)
        create_file_path = dir_test_data_path + _name
        if _name not in os.listdir(dir_test_data_path):
            mk_dir = create_file_path + '/save_mtm'
            try:
                os.makedirs(mk_dir)
            except Exception as e:
                # self.log_obj.error('  -*文件夹 %s 创建失败' % self.current_case_name)
                _mess = '文件夹 %s 创建失败' % self.current_case_name
                get_return_code(log_obj=self.log_obj, msg=_mess, _code=500)
                return

        # 保存测试数据
        run_compare_data = self.save_data
        file_name = create_file_path + '/' + str(self.test_point_name) + '.data'
        try:
            with open(file_name, 'wb') as f:
                pickle.dump(run_compare_data, f)
        except Exception as e:
            _mess = 'Save compare data filed, test point name: %s, Error: %s' % (str(self.test_point_name), str(e))
            get_return_code(log_obj=self.log_obj, msg=_mess, _code=500)
            return


class CompareData:
    """
    return code:
    code 0， 比对数据一致，成功
    code 1， 总订单数量不一致
    code 2， 当前订单 pattern 数量不一致
    code 3， 当前订单 edge 数量 或者 vertex 数量不一致
    code 4， vertex 点坐标不一致
    code 5， 边采样点数量不一致
    code 6， 边采样点坐标不一致

    """

    def __init__(self, current_case_name, current_test_point_name, log_obj):
        self.current_case_name = current_case_name
        self.current_test_point_name = current_test_point_name
        self.log = log_obj
        self.epsilon = 0.003

    def pickup_run_compare_data(self):
        a = OrderData(log_obj=self.log, test_case_file_name=self.current_case_name,
                      _test_point_name=self.current_test_point_name)
        current_run_compare_data = a.get_current_order()
        run_order_nums = current_run_compare_data["order_num"]
        run_current_order_patterns_num = current_run_compare_data["current_order_patterns_num"]
        run_current_order_pattern_data = current_run_compare_data["current_order_pattern_data"]

        return run_order_nums, run_current_order_patterns_num, run_current_order_pattern_data

    def load_save_compare_data(self):
        (point_name, point_name_suffix) = os.path.splitext(self.current_test_point_name)
        (case_name, case_name_suffix) = os.path.splitext(self.current_case_name)
        test_point_path = dir_test_data_path + str(case_name) + '/' + str(point_name) + '.data'
        try:
            with open(test_point_path, 'rb') as f:
                original_data = pickle.load(f)
        except Exception as e:
            # self.log.error('  *Load save compare data filed, test point name: %s' % str(case_name))
            _mess = 'Load save compare data filed, test point name: %s' % str(case_name)
            get_return_code(log_obj=self.log, msg=_mess, _code=500)
            return

        # 数据处理
        save_order_num = original_data["order_num"]
        save_current_order_patterns_num = original_data["current_order_patterns_num"]
        save_current_order_pattern_data = original_data["current_order_pattern_data"]

        return save_order_num, save_current_order_patterns_num, save_current_order_pattern_data

    def compare_save_and_run_data(self):
        run_order_nums, run_current_order_patterns_num, run_current_order_pattern_data = self.pickup_run_compare_data()
        save_order_num, save_current_order_patterns_num, save_current_order_pattern_data = self.load_save_compare_data()
        if run_order_nums != save_order_num:
            msg = '订单数量不一致， run_order_nums:%s, save_order_nums:%s' % (str(run_order_nums), str(save_order_num))
            return [1, msg]

        if run_current_order_patterns_num != save_current_order_patterns_num:
            msg = '当前订单的 pattern 数量不一致， run_current_order_patterns_num:%s, save_current_order_patterns_num:%s' % (
                str(run_current_order_patterns_num), str(save_current_order_patterns_num))
            return [2, msg]

        # logger_compare.info("this is save_current_order_pattern_data %s" % str(save_current_order_pattern_data))
        # 循环字典， 获取键值
        for key_pattern_index in save_current_order_pattern_data:
            # edges num int
            save_pattern_edges_num = str(save_current_order_pattern_data[str(key_pattern_index)][0])
            run_pattern_edges_num = str(run_current_order_pattern_data[str(key_pattern_index)][0])

            if run_pattern_edges_num != save_pattern_edges_num:
                msg = '当前订单 pattern name: %s 中边数量不一致，run_pattern_edges_num:%s, save_pattern_edges_num:%s' % (
                    str(key_pattern_index), str(run_pattern_edges_num), str(save_pattern_edges_num))
                return [3, msg]

            # vertex  list nums
            save_vertex_num = save_current_order_pattern_data[key_pattern_index][1][0]
            run_vertex_num = run_current_order_pattern_data[key_pattern_index][1][0]

            if run_vertex_num != save_vertex_num:
                msg = '当前订单 pattern name: %s 中顶点数量不一致，run_vertex_num:%s, save_vertex_num:%s' % (
                    str(key_pattern_index), str(run_vertex_num), str(save_vertex_num))
                return [3, msg]

            # vertex point dict
            save_vertex_point = save_current_order_pattern_data[key_pattern_index][1][1]
            run_vertex_point = run_current_order_pattern_data[key_pattern_index][1][1]
            for key_vertex_point in save_vertex_point:
                save_point_x = save_vertex_point[key_vertex_point][0]  # 元组
                save_point_y = save_vertex_point[key_vertex_point][0]
                save_point_z = save_vertex_point[key_vertex_point][0]

                run_point_x = run_vertex_point[key_vertex_point][0]  # 元组
                run_point_y = run_vertex_point[key_vertex_point][0]
                run_point_z = run_vertex_point[key_vertex_point][0]

                if abs(save_point_x - run_point_x) > self.epsilon or abs(
                        save_point_y - run_point_y) > self.epsilon or abs(save_point_z - run_point_z) > self.epsilon:
                    msg = '点坐标不一致，pattern name: %s, run_vertex_point:%s, save_vertex_point:%s' % (
                        str(key_pattern_index), str((run_point_x, run_point_y, run_point_z)),
                        str((save_point_x, save_point_y, save_point_z)))
                    return [4, msg]

            # edge dict
            save_edge = save_current_order_pattern_data[key_pattern_index][2]
            run_edge = run_current_order_pattern_data[key_pattern_index][2]
            for key_save_edge in save_edge:
                save_edge_point = save_edge[key_save_edge]  # list
                run_edge_point = run_edge[key_save_edge]

                if len(run_edge_point) != len(save_edge_point):
                    msg = '边采样点数量不一致，pattern name: %s, run_edge_point_num:%s, save_edge_point_num:%s' % (
                        str(key_pattern_index), str(len(run_edge_point)), str(len(save_edge_point)))
                    return [5, msg]

                # 比较 edges 采样点坐标 11 个
                for item_point in range(len(save_edge_point)):
                    save_edge_point_x = save_edge_point[item_point][0]
                    save_edge_point_y = save_edge_point[item_point][1]
                    save_edge_point_z = save_edge_point[item_point][2]

                    run_edge_point_x = run_edge_point[item_point][0]
                    run_edge_point_y = run_edge_point[item_point][1]
                    run_edge_point_z = run_edge_point[item_point][2]

                    if abs(save_edge_point_x - run_edge_point_x) > self.epsilon or abs(
                            save_edge_point_y - run_edge_point_y) > self.epsilon or abs(
                        save_edge_point_z - run_edge_point_z) > self.epsilon:
                        msg = '点坐标不一致，pattern name: %s, edge index: %s, run_edge_point:%s, save_edge_point:%s' % (
                            str(key_pattern_index), str(), str((run_edge_point_x, run_edge_point_y, run_edge_point_z)),
                            str((save_edge_point_x, save_edge_point_y, save_edge_point_z)))
                        return [6, msg]
        msg = '测试点 [%s] 数据比对成功' % str(self.current_test_point_name)
        return [0, msg]
