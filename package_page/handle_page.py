#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 定位操作
import datetime
import time
import serial

from package_page.common_page import CommonPage
from package_config.common_config import config


class HandlePage(CommonPage):
    def serial_config(self, temp_serials):
        try:
            self.ser = serial.Serial(temp_serials,
                                     9600,
                                     timeout=1)
            return self.ser
        except Exception as e:
            print("Hnadlepage没有可用串口了", e)

    # app执行添加温湿度计设备
    def add_temp_devices(self, temp_list):
        get_serial_nums = 0
        serial_list = config.serial_comlist()
        for sku in temp_list:  # 遍历设备列表
            for i in serial_list:
                self.serial_config(i)  # 遍历调用串口
                """添加设备"""
                # 添加”+“
                self.device(resourceId="com.govee.home:id/ivDevAdd").click_exists(timeout=60)
                # 输入要添加的SKU
                self.device(resourceId="com.govee.home:id/tv_search").click_exists(timeout=60)
                self.device(resourceId="com.govee.home:id/et_search").send_keys(sku)
                # 点击SKU
                self.device(resourceId="com.govee.home:id/sku_name").click_exists(timeout=60)
                time.sleep(5)
                # 选择设备
                self.device.xpath(
                    '//*[@resource-id="com.govee.home:id/device_list"]/android.widget.RelativeLayout[1]').click_exists(
                    timeout=60)
                # 命名设备
                print("点击配对")
                time.sleep(10)
                try:
                    get_serial_nums += 1
                    if get_serial_nums <= len(serial_list):
                        self.ser.write(bytes.fromhex('A0 01 01 A2'))
                        time.sleep(1)
                        self.ser.write(bytes.fromhex('A0 01 00 A1'))
                    elif get_serial_nums > len(serial_list):
                        print("添加不需要点击按键添加的设备")
                        pass
                except Exception as e:
                    print("继电器串口错误：", e)
                self.device(resourceId="com.govee.home:id/sensor_name_edit").click_exists(timeout=60)
                self.device(resourceId="com.govee.home:id/sensor_name_edit").send_keys(sku)
                self.device(resourceId="com.govee.home:id/done").click_exists(timeout=60)
                # wifi配置
                try:
                    self.device(resourceId="com.govee.home:id/et_pwd").clear_text()
                    self.device(resourceId="com.govee.home:id/et_pwd").send_keys("starstarlight")
                    self.device(resourceId="com.govee.home:id/send_wifi").click_exists(timeout=60)
                except Exception as e:
                    print("不需要配网的设备：", e)
                now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S----->")
                if self.device(resourceId="com.govee.home:id/group_year").exists(timeout=60):
                    if self.device(resourceId="com.govee.home:id/btn_chart").exists(timeout=60):
                        self.get_log.info("{0}添加{1}成功。".format(now_time, sku))
                        print("{0}添加{1}成功。".format(now_time, sku))
                time.sleep(60)  # 添加获取校准校准
                self.device(resourceId="com.govee.home:id/btn_back").click_exists(timeout=60)

                # """ 删除设备 """
                # 点击设备设置按钮
                # TouchAction(program.device).press(x=1000, y=150).release().perform()  # 通过定位坐标
                # time.sleep(2)
                # common.swipe_down(self)  # 下滑
                # program.device(resourceId= "btn_delete").click()
                # time.sleep(2)
                # program.device(resourceId= "btn_done").click()
                # time.sleep(5)
                # except Exception:
                #     pass
                #     program.ui.resultBrowser.append("找不到定位元素了..")
                #     err_test_count += 1
                # n += 1
                # if n == test_count:
                #     program.ui.resultBrowser.append("测试完成！")
                # success_count = test_count - err_test_count  # 成功次数
                # success_rate = success_count / test_count  # 成功率
                # program.ui.resultBrowser.append(
                #     "测试完成！共测试{}次,成功{}次,成功率{:.2%}".format(test_count, success_count, success_rate))
                # program.ui.pushButton.setEnabled(True)  # 开始测试使能
            # else:
            #     program.ui.resultBrowser.append("输入测试次数...")
            #     program.ui.pushButton.setEnabled(True)  # 开始测试使能
            #     program.ui.add_deviceBox.setEnabled(True)  # 添加设备使能使能

    # 判断设备是否正在连接温湿度计
    def t_or_f(self, element):
        source = self.device.page_source
        if element in source:
            return True
        else:
            return False

    # app执行绑定温湿度计
    def add_temp(self, sku):
        success_test_count = 0
        test_all_count = 0
        while True:
            if self.device(text=sku).exists(timeout=5):
                self.device(text=sku).click_exists(timeout=2)
                if self.enter_device(sku):
                    try:
                        print("\n--------进入设备详情页--------")
                        self.down()
                        self.device(resourceId="com.govee.home:id/iv_bind_temperature_arrow").click()
                        self.device(resourceId="com.govee.home:id/item_icon_choose_iv").click()
                        self.device(resourceId="com.govee.home:id/btn_ok").click()
                        test_all_count += 1
                        time.sleep(10)
                        if self.device(resourceId="com.govee.home:id/iv_bind_temperature_arrow").exists(timeout=30):
                            success_test_count += 1
                            self.device(resourceId="com.govee.home:id/iv_bind_temperature_arrow").click()
                            self.device(resourceId="com.govee.home:id/btn_delete").click()
                            self.device(resourceId="com.govee.home:id/btn_done").click()
                            if self.device(resourceId="com.govee.home:id/tv_bind_temperature_title").exists(timeout=5):
                                self.get_log.info("删除温湿度计成功")
                        elif self.t_or_f("连接中"):
                            self.get_log.info("60s内未添加成功！")
                        self.get_log.info("测试完成！")
                        success_rate = success_test_count / test_all_count  # 成功率
                        self.get_log.info(
                            "测试完成！共测试{}次,成功{}次,成功率{:.2%}".format(test_all_count, success_test_count,
                                                                               success_rate))
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

                # self.device(By.XPATH,
                #                          "//android.widget.ScrollView/android.widget.FrameLayout/android.view.ViewGrou"
                #                          "p/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]")

    # 测试H7122主动能
    def run_func_H712X(self, sku):
        test_count = 0
        while True:
            if self.device(text=sku).exists(timeout=5):
                self.device(text=sku).click_exists(timeout=2)
                self.handle_pop()
                if self.enter_device(sku):
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
        while True:
            if self.device(text=sku).exists(timeout=2):
                self.device(text=sku).click_exists(timeout=2)
                if self.enter_device(sku):
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
        print("测试H7140主功能")
        # 判断当前是否需要进入详情页te
        test_count = 0
        self.handle_pop()
        while True:
            if self.device(text=sku).exists(timeout=5):
                self.device(text=sku).click_exists(timeout=2)
                self.handle_pop()
                if self.enter_device(sku):
                    try:
                        # 判断设备是否是关机状态，如果是就先开机
                        flag = self.device(resourceId='com.govee.home:id/iv_gear_icon').info['enabled']  # 开机状态
                        # print(flag)
                        if flag:  # 如果设备处于可点击状态
                            self.humi_gear()  # 档位1-8档
                            self.humi_diy()  # 自定义档位
                            self.humi_auto()  # 自动挡位
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
        self.run_func_H7140(sku)


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

    # sku压测，不被走查代码调用
    def run_func_H710x(self, sku):
        # print("测试H710x系列主功能")
        test_count = 0
        # 判断当前是否需要进入详情页
        self.handle_pop()
        while True:
            if self.device(text=sku).exists(timeout=2):
                self.device(text=sku).click_exists(timeout=2)
                if self.enter_device(sku):
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