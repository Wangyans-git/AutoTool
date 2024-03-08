#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : app页面定位操作
import time

import serial

from package_page.common_page import CommonPage


class HandlePage(CommonPage):
    def serial_config(self, temp_serials):
        try:
            self.ser = serial.Serial(temp_serials,
                                     9600,
                                     timeout=1)
            return self.ser
        except Exception as e:
            print("Hnadlepage没有可用串口了", e)

    """测试H7122主动能"""

    def run_func_H712X(self, sku):
        test_count = 0
        if self.device(text=sku).exists(timeout=5):
            self.device(text=sku).click_exists(timeout=2)
            self.handle_pop()
            if self.enter_device(sku):
                while True:
                    try:
                        # 判断是否弹窗提示72h清洗
                        # 判断设备是否是关机状态，如果是就先开机
                        flag = self.device.xpath('//*[@text="低档"]').info['enabled']  # 开机状态
                        # print(flag)
                        if flag:  # 如果设备处于可点击状态
                            """
                            切换档位
                            """
                            self.Dehumidifier()
                            self.handle_pop()
                            self.dev_common()
                        else:
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5)
                            self.get_log.error("设备关机过，重新开机测试..")
                            print("设备关机过，重新开机测试..")
                        test_count += 1
                    except Exception as e:
                        self.handle_pop()
                        print(e)
            else:
                while True:
                    self.device(text=sku).click_exists(timeout=5.0)
                    if self.enter_device():
                        break
                    else:
                        time.sleep(5)
        else:
            print("没有改找到该设备名的设备!")
        self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    def run_func_H7124(self, sku):
        print("测试H7124主功能")
        self.run_func_H712X(sku)

    """测试H713系列主功能"""

    # sku压测时使用，不被走查代码调用
    def run_func_H713x(self, sku):
        print("测试H713系列主功能")
        test_count = 0
        # 判断当前是否需要进入详情页
        self.handle_pop()
        if self.device(text=sku).exists(timeout=2):
            self.device(text=sku).click_exists(timeout=2)
            if self.enter_device(sku):
                while True:
                    try:
                        self.handle_pop()
                        # 判断设备是否是关机状态，如果是就先开机
                        if self.device(resourceId='com.govee.home:id/iv_timer_protected').exists():
                            self.Heater_gear()  # 切换档位
                            self.dev_common()  # 通用功能
                            # self.dev_setting()  # 设置页
                        else:
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.get_log.error("设备关机过，重新开机测试..")
                            print("设备关机过，重新开机测试..")
                            self.Heater_gear()  # 切换档位
                            self.dev_common()  # 通用功能
                            # self.dev_setting()  # 设置页
                        test_count += 1
                    except Exception as e:
                        self.handle_pop()
                        print(e)
            else:
                while True:
                    self.device(text=sku).click_exists(timeout=5.0)
                    if self.enter_device():
                        break
                    else:
                        time.sleep(5)
        else:
            print("没有改找到该设备名的设备!")
        self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    # 测试H7130主功能
    def run_func_H7130(self, sku):
        print("测试H7130主功能")

    # 测试H7131主功能
    def run_func_H7131(self, sku):
        print("测试H7131主功能")
        self.run_func_H713x(sku)

    # 测试H7132主功能
    def run_func_H7132(self, sku):
        print("测试H7132主功能")
        self.run_func_H713x(sku)

    # 测试H7133主功能
    def run_func_H7133(self, sku):
        print("测试H7133主功能")
        self.run_func_H713x(sku)

    # 测试H7135主功能
    def run_func_H7135(self, sku):
        print("测试H7135主功能")
        self.run_func_H713x(sku)

    # 测试H7133主功能
    def run_func_H713B(self, sku):
        print("测试H713B主功能")
        self.run_func_H713x(sku)

    # 测试H713C主功能
    def run_func_H713C(self, sku):
        print("测试H713C主功能")
        self.run_func_H713x(sku)

    # 测试H7140主功能
    def run_func_H7140(self, sku):
        print("测试H7140")
        self.run_func_H714X(sku)

    def run_func_H7148(self, sku):
        print("测试H7148")
        self.run_func_H714X(sku)

    def run_func_H714X(self, sku):
        # 判断当前是否需要进入详情页te
        test_count = 0
        self.handle_pop()
        if self.device(text=sku).exists(timeout=5):
            self.device(text=sku).click_exists(timeout=2)
            self.handle_pop()
            if self.enter_device(sku):
                while True:
                    try:
                        # 判断设备是否是关机状态，如果是就先开机
                        flag = self.device(resourceId='com.govee.home:id/iv_gear_icon').info['enabled']  # 开机状态
                        # print(flag)
                        if flag:  # 如果设备处于可点击状态
                            self.humi_diy()  # 自定义档位
                            self.humi_auto()  # 自动挡位
                            self.humi_gear()  # 档位1-8档
                            self.dev_common()  # 通用功能
                        else:
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5)
                            self.get_log.error("设备关机过，重新开机测试..")
                            print("设备关机过，重新开机测试..")
                        test_count += 1
                    except Exception as e:
                        self.handle_pop()
                        print(e)
            else:
                while True:
                    self.device(text=sku).click_exists(timeout=5.0)
                    if self.enter_device():
                        break
                    else:
                        time.sleep(5)
        else:
            print("没有改找到该设备名的设备!")
            self.check_connect()
        self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    # 测试H7143主功能
    def run_func_H7143(self, sku):
        print("测试H7143主功能")
        self.run_func_H714X(sku)

    # 测试H7180主功能
    def run_func_H7180(self, sku):
        print("测试H7180主功能")
        test_count = 0
        # 判断当前是否需要进入详情页
        while True:
            if self.device(text=sku).exists(timeout=5):
                self.device(text=sku).click_exists(timeout=5)
                if self.enter_device(sku):
                    try:
                        self.handle_pop()
                        flag = 1  # 开机状态
                        if flag:  # 如果设备处于可点击状态
                            self.kitchen_appliances()
                        else:
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.get_log.error("设备关机过，重新开机测试..")
                            print("设备关机过，重新开机测试..")
                        test_count += 1
                    except Exception as e:
                        self.handle_pop()
                        print(e)
                else:
                    while True:
                        self.device(text=sku).click_exists(timeout=5.0)
                        if self.enter_device():
                            break
                        else:
                            time.sleep(5)
            else:
                print("没有改找到该设备名的设备!")
            self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    def run_func_H710x(self, sku):
        # print("测试H710x系列主功能")
        test_count = 0
        # 判断当前是否需要进入详情页
        self.handle_pop()
        if self.device(text=sku).exists(timeout=2):
            self.device(text=sku).click_exists(timeout=2)
            if self.enter_device(sku):
                while True:
                    try:
                        self.handle_pop()
                        # 判断设备是否是关机状态，如果是就先开机
                        print(self.device(resourceId='com.govee.home:id/gear_operate_seek_bar').info["enabled"])
                        if self.device(resourceId='com.govee.home:id/gear_operate_seek_bar').info["enabled"]:
                            print("档位")
                            self.Fan_gear()  # 切换档位
                            self.dev_common()  # 通用功能
                        else:
                            self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                            self.get_log.error("设备关机过，重新开机测试..")
                            print("设备关机过，重新开机测试..")
                            self.Fan_gear()  # 切换档位
                            self.dev_common()  # 通用功能
                        test_count += 1
                    except Exception as e:
                        self.handle_pop()
                        print(e)
            else:
                while True:
                    self.device(text=sku).click_exists(timeout=5.0)
                    if self.enter_device():
                        break
                    else:
                        time.sleep(5)
        else:
            print("没有改找到该设备名的设备!")
        self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    def run_func_H7102(self, sku):
        print("测试H7102主功能")
        self.run_func_H710x(sku)

    def run_func_wifi(self):
        self.app = HandlePage()
        print("配网中...")
