#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : app页面定位操作
import threading
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

    def handle_pop_thread(self,stop_flag):
        t = threading.Thread(target=self.handle_pop,args=(stop_flag,))
        t.start()

    """测试H7122主动能"""

    def run_func_H712X(self, sku, stop_flag):
        test_count = 0
        if self.device(text=sku).exists(timeout=5):
            self.device(text=sku).click_exists(timeout=2)
        if self.enter_device(sku):
            while not stop_flag.is_set():
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
                        self.dev_common()
                    else:
                        self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5)
                        self.get_log.error("设备关机过，重新开机测试..")
                        print("设备关机过，重新开机测试..")
                    test_count += 1
                except Exception as e:

                    print(e)
        else:
            while True:
                self.device(text=sku).click_exists(timeout=5.0)
                if self.enter_device():
                    break
                else:
                    time.sleep(5)
        self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    """测试H713系列主功能"""

    # sku压测时使用，不被走查代码调用
    def run_func_H713X(self, sku, stop_flag):
        if not stop_flag.is_set():
            print(F"测试{sku}主功能")
            self.handle_pop_thread(stop_flag)
            test_count = 0
            # 判断当前是否需要进入详情页
            if self.device(text=sku).exists(timeout=2):
                self.device(text=sku).click_exists(timeout=2)
            if self.enter_device(sku):
                while not stop_flag.is_set():
                    try:

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
                        print(e)
            else:
                while True:
                    self.device(text=sku).click_exists(timeout=5.0)
                    if self.enter_device():
                        break
                    else:
                        time.sleep(5)
            self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    # 测试H7130主功能
    def run_func_H7130(self, sku, stop_flag):
        print("测试H7130主功能")

    # 测试H7140主功能
    def run_func_H714X(self, sku, stop_flag):
        print(f"测试{sku}主功能")
        # 判断当前是否需要进入详情页te
        test_count = 0
        if self.device(text=sku).exists(timeout=5):
            self.device(text=sku).click_exists(timeout=2)
        if self.enter_device(sku):
            while not stop_flag.is_set():
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

                    print(e)
        else:
            while True:
                self.device(text=sku).click_exists(timeout=5.0)
                if self.enter_device():
                    break
                else:
                    time.sleep(5)
        self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    # 测试H7180主功能
    def run_func_H7180(self, sku, stop_flag):
        print("测试H7180主功能")
        test_count = 0
        # 判断当前是否需要进入详情页
        if self.device(text=sku).exists(timeout=5):
            self.device(text=sku).click_exists(timeout=5)
        if self.enter_device(sku):
            while not stop_flag.is_set():
                try:
                    flag = 1  # 开机状态
                    if flag:  # 如果设备处于可点击状态
                        self.kitchen_appliances()
                    else:
                        self.device(resourceId='com.govee.home:id/iv_switch').click_exists(timeout=5.0)
                        self.get_log.error("设备关机过，重新开机测试..")
                        print("设备关机过，重新开机测试..")
                    test_count += 1
                except Exception as e:
                    print(e)
        else:
            while True:
                self.device(text=sku).click_exists(timeout=5.0)
                if self.enter_device():
                    break
                else:
                    time.sleep(5)
        self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

    def run_func_H710X(self, sku, stop_flag):
        if not stop_flag.is_set():
            print(f"测试{sku}系列主功能")
            test_count = 0
            # 判断当前是否需要进入详情页
            if self.device(text=sku).exists(timeout=2):
                self.device(text=sku).click_exists(timeout=2)
            if self.enter_device(sku):
                while not stop_flag.is_set():
                    try:

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

                        print(e)
            else:
                while True:
                    self.device(text=sku).click_exists(timeout=5.0)
                    if self.enter_device():
                        break
                    else:
                        time.sleep(5)
            self.get_log.info("{0}已测试了测试{1}次。".format(sku, test_count))

