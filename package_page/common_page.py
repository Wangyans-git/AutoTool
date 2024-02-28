#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 页面公共元素
import datetime
import os
import time

import uiautomator2 as u2

from logs.get_log import GetLog


# from Govee_Autotool.package_serial.common import ConFig

class CommonPage:
    def __init__(self):
        self.device = u2.connect_usb()
        self.device.app_start('com.govee.home')
        self.device.settings['wait_timeout'] = 10  # 元素等待时间30s
        self.device.settings['operation_delay'] = 0.5  # 每次点击后等待1s
        # 脚本日志
        if os.path.exists("C:\\logs"):
            self.get_log = GetLog(r"C:\logs\\app测试数据.log")
        else:
            os.mkdir("C:\\logs")
            self.get_log = GetLog(r"C:\logs\\app测试数据.log")
        # self.logs = GetLog("C:\wys\AutoTestProjects\Govee_Autotool\logs\测试次数.log")
        # 获取手机分辨率
        self.width, self.height = self.device.window_size()
        self.test_count = 0

    """
    检测是否连接成功
    """

    # 进入详情页验证
    def enter_device(self, sku=None):
        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=30):
            print("进入详情页")
            self.get_log.info("进入{0}详情页成功".format(sku))
            return True
        else:

            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=5.0)
                print("30秒还未进入详情页，连接设备失败，退出详情页")
                self.get_log.info('30秒还未进入详情页，连接设备失败，退出详情页')
            except Exception as e:
                print(e)
            return False

    # 连接验证
    def check_connect(self):
        if self.device(resourceId="com.govee.home:id/iv_switch").exists(timeout=5):
            return True
        else:
            # 退出详情页
            try:
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=2)
                self.get_log.info('10秒wifi仍未连接成功，连接异常退出详情页')
            except Exception as e:
                print(e)
            return False

    """
    设置页操作
    """

    def dev_setting(self):
        self.device(resourceId='com.govee.home:id/btn_setting').click_exists(timeout=2)
        time.sleep(2)
        if self.device.xpath(  # 倾倒通知
                '//*[@resource-id="com.govee.home:id/cslDumpNotify"]/android.view.ViewGroup[1]/android.widget.ImageView[2]').exists():
            print("有元素")
            for i in range(2):
                self.device.xpath(
                    '//*[@resource-id="com.govee.home:id/cslDumpNotify"]/android.view.ViewGroup[1]/android.widget.ImageView[2]').click_exists(
                    timeout=2)
        if self.device.xpath(  # 24h push通知
                '//*[@resource-id="com.govee.home:id/csl_24_shut_down_off"]/android.view.ViewGroup[1]/android.widget.ImageView[2]').exists():
            for i in range(2):
                self.device.xpath(
                    '//*[@resource-id="com.govee.home:id/csl_24_shut_down_off"]/android.view.ViewGroup[1]/android.widget.ImageView[2]').click_exists(
                    timeout=2)
        if self.device.xpath(  # 展示露点
                '//*[@resource-id="com.govee.home:id/cslVpd"]/android.view.ViewGroup[1]/android.widget.ImageView[3]').exists():
            for i in range(2):
                self.device.xpath(
                    '//*[@resource-id="com.govee.home:id/cslVpd"]/android.view.ViewGroup[1]/android.widget.ImageView[3]').click_exists(
                    timeout=2)
        if self.device.xpath(  # 卡片页展示温湿度
                '//*[@resource-id="com.govee.home:id/cslSensorCard"]/android.view.ViewGroup[1]/android.widget.ImageView[3]').exists():
            for i in range(2):
                self.device.xpath(
                    '//*[@resource-id="com.govee.home:id/cslSensorCard"]/android.view.ViewGroup[1]/android.widget.ImageView[3]').click_exists(
                    timeout=2)
        if self.device(resourceId='com.govee.home:id/setting_calibration_tempture_minus').exists():  # 加减校准
            for i in range(5):
                self.device(resourceId='com.govee.home:id/setting_calibration_tempture_minus').click_exists(timeout=2)
        if self.device(resourceId='com.govee.home:id/setting_calibration_tempture_add').exists():
            for i in range(10):
                self.device(resourceId='com.govee.home:id/setting_calibration_tempture_add').click_exists(timeout=2)
        self.device(resourceId='com.govee.home:id/btn_back').click_exists(timeout=2)

    """
    处理弹窗
    """

    def handle_pop(self):
        if self.device(resourceId='com.govee.home:id/btn_cancel').exists():
            self.device(resourceId='com.govee.home:id/btn_cancel').click_exists(timeout=2)
            self.get_log.info("又有弹窗了，哪里来的？")
        elif self.device(resourceId='com.govee.home:id/dialog_done').exists():
            self.device(resourceId='com.govee.home:id/dialog_done').click_exists(timeout=2)
            self.get_log.info("又有弹窗了，哪里来的？")
        elif self.device(resourceId='com.govee.home:id/btn_done').exists():
            self.device(resourceId='com.govee.home:id/btn_done').click_exists(timeout=2)
            self.get_log.info("又有弹窗了，哪里来的？")
        elif self.device(resourceId='com.govee.home:id/btn_got_it').exists():
            self.device(resourceId='com.govee.home:id/btn_got_it').click_exists(timeout=2)
            self.get_log.info("又有弹窗了，哪里来的？")
        elif self.device(text='知道了').exists():
            self.device(text='知道了').click_exists(timeout=2)
            self.get_log.info("又有弹窗了，哪里来的？")
        else:
            pass

    # 下滑
    def down(self):
        self.device.swipe(0.5 * self.width, 0.9 * self.height, 0.5 * self.width,
                          0.1 * self.height)  # 向下滑动

    # 上滑
    def up(self):
        self.device.swipe(0.5 * self.width, 0.1 * self.height, 0.5 * self.width,
                          0.9 * self.height)  # 向上滑动

    """
    通用功能
    """

    # 摇头、夜灯、锁、显示
    def dev_common(self):
        self.down()
        self.handle_pop()
        # 摇头
        if self.device(resourceId='com.govee.home:id/iv_shake_switch').exists():
            print("有摇头")
            for i in range(2):
                self.device(resourceId='com.govee.home:id/iv_shake_switch').click_exists(timeout=2)
            if self.check_connect():
                self.get_log.info("开启关闭摇头成功！")
            else:
                self.get_log.error("开启关闭摇头后连接失败！")
        # 摆页  7133
        if self.device(resourceId='com.govee.home:id/ivSpeedSwitch').exists():
            print("有摆叶")
            for i in range(2):
                self.device(resourceId='com.govee.home:id/ivSpeedSwitch').click_exists(timeout=2)
            if self.check_connect():
                self.get_log.info("开启关闭摆页成功！")
            else:
                self.get_log.error("开启关闭摇页后连接失败！")
        # 夜灯
        if self.device(resourceId='com.govee.home:id/iv_light_rgb_switch_ext1').exists():
            for i in range(2):
                self.device(resourceId='com.govee.home:id/iv_light_rgb_switch_ext1').click_exists(timeout=2)
            if self.check_connect():
                self.get_log.info("开启关闭夜灯成功！")
            else:
                self.get_log.error("开启关闭夜灯后连接失败！")
        # 童锁
        if self.device(resourceId='com.govee.home:id/iv_lock_switch').exists():
            for i in range(2):
                self.device(resourceId='com.govee.home:id/iv_lock_switch').click_exists(timeout=2)
            if self.check_connect():
                self.get_log.info("开启关闭童锁成功！")
            else:
                self.get_log.error("开启关闭童锁后连接失败！")
        # 显示
        if self.device(resourceId='com.govee.home:id/iv_light_indicator_switch').exists():
            for i in range(2):
                self.device(resourceId='com.govee.home:id/iv_light_indicator_switch').click_exists(timeout=2)
            if self.check_connect():
                self.get_log.info("开启关闭显示成功！")
            else:
                self.get_log.error("开启关闭显示后连接失败！")
        self.up()
        self.handle_pop()

    def timer(self):
        # 预约定时
        if self.device(resourceId='com.govee.home:id/tv_timer_title').exists():
            self.device(resourceId='com.govee.home:id/tv_timer_title').click_exists(timeout=2)
            self.device(resourceId='com.govee.home:id/btn_add').click_exists(timeout=2)
            self.device(resourceId='d(resourceId="com.govee.home:id/type_1_choose")').click_exists(timeout=2)
            self.device(resourceId='d(resourceId="com.govee.home:id/btn_sure")').click_exists(timeout=2)
            self.device(resourceId='d(resourceId="com.govee.home:id/btn_back")').click_exists(timeout=2)
            if self.check_connect():
                self.get_log.info("设置预约定时成功！")
            else:
                self.get_log.error("设置预约定时后连接失败！")
        # 倒计时关机
        if self.device(resourceId='com.govee.home:id/tv_delay_off_title').exists():
            self.device(resourceId='com.govee.home:id/tv_delay_off_title').click_exists(timeout=2)
            for i in range(2):
                self.device(resourceId='com.govee.home:id/ivForbid').click_exists(timeout=2)
            self.handle_pop()
            if self.check_connect():
                self.get_log.info("设置倒计时关机成功！")
            else:
                self.get_log.error("设置倒计时关机后连接失败！")

    """
    加湿器
    """

    # 1-8档
    def humi_gear(self):
        self.device(resourceId='com.govee.home:id/iv_gear_icon').click_exists(timeout=5.0)  # 手动挡
        if self.check_connect():
            self.get_log.info("切换至手动挡位成功！")
            print("切换至手动挡位成功！")
        else:
            self.get_log.error("切换至手动挡后连接失败！")
        self.device.click(0.162, 0.812)  # 1档

        self.device.click(0.26, 0.812)  # 2档

        self.device.click(0.36, 0.812)  # 3档

        self.device.click(0.45, 0.812)  # 4档

        self.device.click(0.55, 0.812)  # 5档

        self.device.click(0.65, 0.812)  # 6档

        self.device.click(0.73, 0.812)  # 7档

        self.device.click(0.827, 0.812)  # 8档
        self.handle_pop()
        time.sleep(2)
        if self.check_connect():
            self.get_log.info("切换至1-8挡成功！")
        else:
            self.get_log.error("切换至1-8挡后连接失败！")

    # 自定义
    def humi_diy(self):
        self.device(resourceId='com.govee.home:id/iv_custom_icon').click_exists(timeout=5)
        self.handle_pop()
        if self.check_connect():
            self.get_log.info("切换至自定义模式成功！")
        else:
            self.get_log.error("切换自定义模式后连接失败！")
        self.device.xpath(
            '//*[@resource-id="com.govee.home:id/custom_item_2"]/android.widget.ImageView[4]').click_exists(
            timeout=5)
        self.handle_pop()
        if self.check_connect():
            self.get_log.info("切换至自定义任务二成功！")
        else:
            self.get_log.error("切换至自定义任务二后连接失败！")
        self.device.xpath(
            '//*[@resource-id="com.govee.home:id/custom_item_3"]/android.widget.ImageView[3]').click_exists(
            timeout=5)
        self.handle_pop()
        if self.check_connect():
            self.get_log.info("切换至自定义任务三成功！")
        else:
            self.get_log.error("切换至自定义任务三后连接失败！")
        self.device.xpath(
            '//*[@resource-id="com.govee.home:id/custom_item_1"]/android.widget.ImageView[5]').click_exists(
            timeout=5)
        self.handle_pop()
        if self.check_connect():
            self.get_log.info("切换至自定义任务一成功！")
        else:
            self.get_log.error("切换至自定义任务一后连接失败！")

    # 自动档
    def humi_auto(self):
        self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5)
        # 如果有确认弹窗，点击取消
        self.handle_pop()
        if self.check_connect():
            self.get_log.info("切换至自动模式成功！")
            print("切换至自动模式成功")
        else:
            self.get_log.error("切换自动模式后连接失败！")
            print("切换自动模式后连接失败")

    """
    取暖器
    """

    def Heater_gear(self):
        self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(
            timeout=5.0)  # 低档
        if self.check_connect():
            self.get_log.info("切换至低挡位成功！")
        else:
            self.get_log.error("切换至低挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(
            timeout=5.0)  # 中档
        if self.check_connect():
            self.get_log.info("切换至中挡位成功！")
        else:
            self.get_log.error("切换至中挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(
            timeout=5.0)  # 高档
        if self.check_connect():
            self.get_log.info("切换至高挡位成功！")
        else:
            self.get_log.error("切换至高挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(
            timeout=5.0)  # 自动档
        if self.device(resourceId='com.govee.home:id/iv_auto_stop_switch').exists():
            for i in range(2):
                self.device(resourceId='com.govee.home:id/iv_auto_stop_switch').click_exists(
                    timeout=5.0)  # 自动停止按钮
        self.handle_pop()
        if self.device(resourceId='com.govee.home:id/ivAutoStopSwitch').exists():
            for i in range(2):
                self.device(resourceId='com.govee.home:id/ivAutoStopSwitch').click_exists(
                    timeout=5.0)  # 自动停止按钮
        self.handle_pop()
        if self.check_connect():
            self.get_log.info("切换至自动挡位成功！")
        else:
            self.get_log.error("切换至自动挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_fan_icon').click_exists(timeout=5.0)  # 风档
        if self.check_connect():
            self.get_log.info("切换至风扇挡位成功！")
        else:
            self.get_log.error("切换至风扇挡位失败！")

    """
    风扇
    """

    def Fan_gear(self):
        self.device(resourceId='com.govee.home:id/iv_sleep_icon').click_exists(timeout=5.0)  # 睡眠
        if self.check_connect():
            self.get_log.info("切换至睡眠挡位成功！")
        else:
            self.get_log.error("切换至睡眠挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_natural_icon').click_exists(timeout=5.0)  # 自然风
        if self.check_connect():
            self.get_log.info("切换至自然风挡位成功！")
        else:
            self.get_log.error("切换至自然风挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_custom_icon').click_exists(timeout=5.0)  # 自定义
        self.handle_pop()
        if self.check_connect():
            self.get_log.info("切换至自定义挡位成功！")
        else:
            self.get_log.error("切换至自定义挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)  # 自动
        if self.check_connect():
            self.get_log.info("切换至自动挡位成功！")
        else:
            self.get_log.error("切换至自动挡位失败！")
        self.device(resourceId='com.govee.home:id/iv_normal_icon').click_exists(timeout=5.0)  # 正常风
        if self.check_connect():
            self.get_log.info("切换至正常风挡位成功！")
        else:
            self.get_log.error("切换至正常风挡位失败！")

    """
    除湿器
    """

    def Dehumidifier(self):

        self.device.xpath('//*[@text="低档"]').click_exists(
            timeout=5.0)  # 手动挡
        if self.check_connect():
            self.get_log.info("切换至低档挡位成功！")
            print("切换至低档挡位成功！")
        else:
            self.get_log.error("切换至低挡后连接失败！")
        self.handle_pop()
        self.device.xpath('//*[@text="中档"]').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("切换至中档位成功！")
            print("切换至中档挡位成功！")
        else:
            self.get_log.error("切换至中挡后连接失败！")
        self.handle_pop()
        self.device.xpath('//*[@text="高档"]').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("切换至高档位成功！")
            print("切换至高档挡位成功！")
        else:
            self.get_log.error("切换至高挡后连接失败！")
        self.handle_pop()
        self.device.xpath('//*[@text="睡眠"]').click_exists(
            timeout=5.0)  # 手动挡
        if self.check_connect():
            self.get_log.info("切换至睡眠挡位成功！")
            print("切换至睡眠挡位成功！")
        else:
            self.get_log.error("切换至睡眠挡后连接失败！")
        self.handle_pop()
        self.device.xpath('//*[@text="自动"]').click_exists(
            timeout=5.0)  # 手动挡
        if self.check_connect():
            self.get_log.info("切换至自动挡位成功！")
            print("切换至自动挡位成功！")
        else:
            self.get_log.error("切换至自动挡后连接失败！")
        self.device.xpath('//*[@text="强劲"]').click_exists(timeout=5)
        if self.check_connect():
            self.get_log.info("切换至强劲模式成功！")
            print("切换至强劲挡位成功！")
        else:
            self.get_log.error("切换强劲模式后连接失败！")
        if self.device(resourceId='com.govee.home:id/iv_gear_low_icon').exists():
            self.device(resourceId='com.govee.home:id/iv_gear_low_icon').click_exists(timeout=5.0)
        if self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').exists():
            self.device(resourceId='com.govee.home:id/iv_gear_mid_icon').click_exists(timeout=5.0)
        if self.device(resourceId='com.govee.home:id/iv_gear_high_icon').exists():
            self.device(resourceId='com.govee.home:id/iv_gear_high_icon').click_exists(timeout=5.0)
        if self.device(resourceId='com.govee.home:id/iv_auto_icon').exists():
            self.device(resourceId='com.govee.home:id/iv_auto_icon').click_exists(timeout=5.0)
        if self.device(resourceId='com.govee.home:id/iv_dry_clothes_icon').exists():
            self.device(resourceId='com.govee.home:id/iv_dry_clothes_icon').click_exists(timeout=5.0)
        else:
            pass


    def kitchen_appliances(self):
        """
                                    切换档位
                                    """
        # 米饭
        self.device(resourceId='com.govee.home:id/tvRice').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/tvStart').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/ivState').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/btn_done').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("米饭开始成功！")
        else:
            self.get_log.error("米饭结束后连接失败！")
        # 慢炖
        self.device(resourceId='com.govee.home:id/ivSlowCooker').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/tvStart').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/ivState').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/btn_done').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("慢炖开始成功！")
        else:
            self.get_log.error("慢炖结束后连接失败！")
        # 嫩煎
        self.device(resourceId='com.govee.home:id/tvSaute').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/tvStart').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/ivState').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/btn_done').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("嫩煎开始成功！")
        else:
            self.get_log.error("嫩煎结束后连接失败！")
        # DIY
        self.device(resourceId='com.govee.home:id/tvDiy').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/tvStart').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/ivState').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/btn_done').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("DIY开始成功！")
        else:
            self.get_log.error("DIY结束后连接失败！")
        # 蒸
        self.device(resourceId='com.govee.home:id/tvSteam').click_exists(timeout=5.0)
        self.device(resourceId='com.govee.home:id/tvStart').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/ivState').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/btn_done').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("蒸开始成功！")
        else:
            self.get_log.error("蒸结束后连接失败！")
        # 保温
        self.device(resourceId='com.govee.home:id/tvSteam').click_exists(timeout=5.0)
        self.device(resourceId='com.govee.home:id/tvStart').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/ivState').click_exists(
            timeout=5.0)
        self.device(resourceId='com.govee.home:id/btn_done').click_exists(
            timeout=5.0)
        if self.check_connect():
            self.get_log.info("保温开始成功！")
        else:
            self.get_log.error("保温结束后连接失败！")