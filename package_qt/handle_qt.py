#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @Description : 处理qt页面
import datetime
import os
import sys
import threading
import time
from pathlib import Path

import serial
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget

from logs.get_log import GetLog
from package_config.common_config import ConFig
from package_page.handle_page import HandlePage

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # YOLOv5 root directory
log_file = str(Path(ROOT) / "config")


# print(log_file)

class HandleQt(QWidget):
    def __init__(self):
        super().__init__()
        self.dbs = 115200
        self.timeout = 1
        self.err = 0
        self.txt_date = ''  # 写入TXT的数据
        self.ui = QUiLoader().load('C:\\Skutest.ui')
        self.ui.setMinimumSize(600, 800)
        self.ui.setMaximumSize(600, 800)
        self.ui.skuBox.addItems(
            ['H7102', 'H7124', 'H7130', 'H7131', 'H7133', 'H7135', 'H7140', 'H7143','H7148', 'H7180'])  # 下拉选择
        self.ui.skuBox.setCurrentIndex(0)  # 默认第一个H7130
        self.ui.main_funBox.clicked.connect(self.main_home_func)  # 主要功能
        self.ui.wifi_Box.clicked.connect(self.wifi_Box)  # 配网
        self.ui.stopButton.clicked.connect(self.quit)
        self.ui.refreshSerial.clicked.connect(self.handle_serial)
        self.ui.clearButton.clicked.connect(self.clear_browser)
        # 脚本日志
        if os.path.exists(r"C:\logs"):
            self.get_log = GetLog(r"C:\logs\串口断言结果.log")
        else:
            os.mkdir(r"C:\logs")
            self.get_log = GetLog(r"C:\logs\串口断言结果.log")

    # 退出程序
    @staticmethod
    def quit():
        sys.exit()

    # 清除显示面板
    def clear_browser(self) -> None:
        self.ui.resultBrowser.clear()

    # 获取串口
    def handle_serial(self):
        self.ui.serialBox.clear()
        com = ConFig().serial_comlist()
        self.ui.serialBox.addItems(com)  # 下拉选择
        self.serial = self.ui.serialBox.currentText()  # 显示选择的串口
        print(self.serial)
        return self.serial

    """
       处理主功能逻辑和断言
    """

    # 复选主功能
    def main_home_func(self):
        try:
            self.ui.main_funBox.setEnabled(False)
            self.ui.wifi_Box.setEnabled(False)
            self.ser = serial.Serial(self.handle_serial(),
                                     # self.ser = serial.Serial(com,
                                     self.dbs,
                                     timeout=self.timeout)

            self.ui.resultBrowser.append("<<<<<<<<<<<<连接串口{}成功>>>>>>>>>>>>".format(self.handle_serial()))

            # self.ui.serialBox.clear()
        except Exception as e:
            if self.ui.main_funBox.isChecked() is False:
                pass
            else:
                self.ui.resultBrowser.append("<<<<<<<<<<<<串口被占用或未接串口>>>>>>>>>>>>")
            # self.ui.serialBox.clear()
        self.err = -1
        if self.ui.main_funBox.isChecked():
            # self.ui.serialBox.clear()
            self.ui.pushButton.clicked.connect(self.thread_recv_main)
            # self.app = HandlePage()  # 设备id，app包名，点击后延迟
            self.ui.resultBrowser.append("*********选择主功能压测*********")
        else:
            self.ui.serialBox.clear()
            print("关闭串口")
            self.ui.resultBrowser.append("*********关闭串口*********")
            self.ui.all_temp_Box.setEnabled(True)
            self.ui.wifi_Box.setEnabled(True)
            self.ui.pushButton.setEnabled(True)
            self.ui.refreshSerial.setEnabled(True)
            self.ser.close()

    # 复选配网
    def wifi_Box(self):
        try:
            self.ui.main_funBox.setEnabled(False)
            self.ui.wifi_Box.setEnabled(False)
            self.ser = serial.Serial(self.handle_serial(),
                                     # self.ser = serial.Serial(com,
                                     self.dbs,
                                     timeout=self.timeout)

            self.ui.resultBrowser.append("<<<<<<<<<<<<连接串口{}成功>>>>>>>>>>>>".format(self.handle_serial()))

            # self.ui.serialBox.clear()
        except Exception as e:
            if self.ui.main_funBox.isChecked() is False:
                pass
            else:
                self.ui.resultBrowser.append("<<<<<<<<<<<<串口被占用或未接串口>>>>>>>>>>>>")
            # self.ui.serialBox.clear()
        self.err = -1
        if self.ui.wifi_Box.isChecked():
            # self.ui.serialBox.clear()
            self.ui.pushButton.clicked.connect(self.thread_start_wifi)
            # self.app = HandlePage()  # 设备id，app包名，点击后延迟
            self.ui.resultBrowser.append("*********选择配网压测*********")
        else:
            self.ui.serialBox.clear()
            print("关闭串口")
            self.ui.resultBrowser.append("*********关闭串口*********")
            self.ui.pushButton.setEnabled(True)
            self.ui.refreshSerial.setEnabled(True)
            self.ser.close()

    # 选择小家电sku主程序
    def thread_start_main(self):
        self.app = HandlePage()
        self.sku = self.ui.skuBox.currentText()  # 显示选择的sku
        if self.sku == "H7102":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7102, args=(self.sku,))
            thread.start()
        elif self.sku == "H7130":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7130, args=(self.sku,))
            thread.start()
        elif self.sku == "H7131":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7131, args=(self.sku,))
            thread.start()
        elif self.sku == "H7132":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7132, args=(self.sku,))
            thread.start()
        elif self.sku == "H7133":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7133, args=(self.sku,))
            thread.start()
        elif self.sku == "H7135":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7135, args=(self.sku,))
            thread.start()
        elif self.sku == "H713B":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H713B, args=(self.sku,))
            thread.start()
        elif self.sku == "H713C":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H713C, args=(self.sku,))
            thread.start()
        elif self.sku == "H7124":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7124, args=(self.sku,))
            thread.start()
        elif self.sku == "H7140":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7140, args=(self.sku,))
            thread.start()
        elif self.sku == "H7143":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7143, args=(self.sku,))
            thread.start()
        elif self.sku == "H7148":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7148, args=(self.sku,))
            thread.start()
        elif self.sku == "H7180":
            self.ui.resultBrowser.append("*********开始测试{}*********".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7180, args=(self.sku,))
            thread.start()
        self.ui.skuBox.currentIndexChanged.connect(self.show)

    # 配网压测
    def thread_start_wifi(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.refreshSerial.setEnabled(False)
        self.ui.main_funBox.setEnabled(False)
        self.sku = self.ui.skuBox.currentText()  # 显示选择的sku
        self.start_wifi = threading.Thread(target=self.start_wifi)
        self.start_wifi.daemon = 1
        self.start_wifi.start()

    def start_wifi(self):
        self.app = HandlePage()

    # 主功能主线程和获取数据
    def thread_recv_main(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.refreshSerial.setEnabled(False)
        self.ui.main_funBox.setEnabled(False)
        try:

            # self.app = HandlePage()  # 设备id，app包名，点击后延迟
            self.start_thread_main = threading.Thread(target=self.thread_start_main)  # 开始测试主线程
            self.read_date_thread_main = threading.Thread(target=self.read_date_main)  # 开始断言主线程
            self.read_date_thread_main.daemon = 1  # 守护线程，主线程退出，所有线程退出
            self.start_thread_main.daemon = 1
            self.read_date_thread_main.start()
            self.start_thread_main.start()
        except Exception as e:
            print("启动app报错：", e)
            self.ui.resultBrowser.append("*********未连接手机*********")
            self.ui.pushButton.setEnabled(True)

    # 处理断言数据
    def read_date_main(self):
        check_edit = self.ui.assertTextEdit.toPlainText().split(",")
        # print("cccc:",check_edit)
        check_dates = {}  # 断言数据
        while True:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S----->")
            is_success_date = ''  # 判断是否执行成功的临时数据
            # a = self.app.test_count
            try:
                date_line = self.ser.readline().decode()
                # print(date_line)
                time.sleep(0.1)
                is_success_date += date_line
                self.txt_date += str(date_line)  # 所有写入到txt文档
                # self.write_txt(self.txt_date)
                for i in range(len(check_edit)):
                    # 开机:55 19 01 01 70, 关机:55 19 01 03 72
                    check_dates[check_edit[i].split(":")[0]] = check_edit[i].split(":")[1]  # 将每个输入的键值对加入到字典里
                    check_list = []
                    # print(check_dates)
                    for j in check_dates:
                        check_list.append(j)
                    # print(check_dates[check_list[i]])
                    if check_dates[check_list[i]] in date_line:
                        # success_date = str(now_time + check_list[i]) + "."
                        success_date = str(now_time + check_list[i] + "成功")
                        self.txt_date += success_date
                        # print(success_date)
                        self.ui.resultBrowser.append(success_date)
                        self.get_log.info(success_date)
            except Exception as e:
                pass

    """
         处理绑定温湿度计/添加设备功能逻辑和断言
    """

    # 复选app绑定温湿度计

    # 添加温湿度计
    def add_temp_func(self):
        try:
            self.ser = serial.Serial(self.handle_serial(),
                                     # self.ser = serial.Serial(com,
                                     self.dbs,
                                     timeout=self.timeout)
            self.ui.resultBrowser.append("<<<<<<<<<<<<连接串口成功>>>>>>>>>>>>")
            # self.ui.serialBox.clear()
        except Exception as e:
            self.ui.resultBrowser.append("<<<<<<<<<<<<串口被占用或未接串口>>>>>>>>>>>>")
            self.ui.serialBox.clear()
        self.err = -1
        if self.ui.add_tempBox.isChecked():
            self.ui.pushButton.clicked.connect(self.thread_add_temp)  # app iu启动配置
            self.ui.resultBrowser.append("*********选择添加温湿度计压测*********")

    def thread_add_temp(self):
        self.sku = self.ui.skuBox.currentText()  # 显示选择的sku
        try:

            self.app = HandlePage()  # 设备id，app包名，点击后延迟
        except Exception as e:
            print("启动app报错：", e)
            self.ui.resultBrowser.append("*********未连接手机*********")
            self.ui.pushButton.setEnabled(True)
        try:
            self.start_thread_main = threading.Thread(target=self.app.add_temp, args=(self.sku,))
            self.start_thread_main.daemon = 1
            self.start_thread_main.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

    # 断言
    def read_date_device_temp(self):
        self.ui.main_funBox.setEnabled(False)
        self.ui.add_tempBox.setEnabled(False)
        self.ui.resultBrowser.append("*********开始测试*********")
        check_edit = self.ui.assertTextEdit.toPlainText().split(",")
        check_dates = {}  # 断言数据
        while True:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S----->")
            is_success_date = ''  # 判断是否执行成功的临时数据
            try:
                date_line = self.ser.readline().decode()
                time.sleep(0.1)
                is_success_date += date_line
                self.txt_date += str(date_line)  # 所有写入到txt文档
                self.write_txt(self.txt_date)
                for i in range(len(check_edit)):
                    # 开机:55 11 01 00 01 01 69, 关机:55 11 01 00 01 00 68
                    check_dates[check_edit[i].split(":")[0]] = check_edit[i].split(":")[1]  # 将每个输入的键值对加入到字典里
                    check_list = []
                    for j in check_dates:
                        check_list.append(j)
                    if check_dates[check_list[i]] in date_line:
                        # success_date = str(now_time + check_list[i]) + "."
                        success_date = str(now_time + check_list[i])
                        self.err_date += success_date
                        self.txt_date += success_date
                        self.ui.resultBrowser.append(success_date + "成功")
            except Exception:
                break

    """
    线程接收绑定温湿度计/添加设备功能数据
    """

    def thread_recv(self):
        try:
            self.read_thread = threading.Thread(target=self.read_date_device_temp)
            self.read_thread.start()
        except Exception as e:
            print("无法启动线程:{}".format(e))

# if __name__ == '__main__':
#     sku_list = ['H7102', 'H7122', 'H7126', 'H7130', 'H7131', 'H7133', 'H7135', 'H7140', 'H7143', 'H7161',
#                 'H7180']  # 下拉选择
#     qt = HandleQt(115200, 1, sku_list)
