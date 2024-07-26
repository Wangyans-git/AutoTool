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
import serial


from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from logs.get_log import GetLog
from package_config.common_config import ConFig
from package_page.handle_page import HandlePage
from package_page.handle_wifi import handle_wifi
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # YOLOv5 root directory
log_file = str(Path(ROOT) / "config")


# print(log_file)

class HandleQt(QWidget):
    def __init__(self):
        super().__init__()
        self.dbs = 115200
        self.timeout = 1
        self.serial_num = ''
        self.txt_date = ''  # 写入TXT的数据
        self.stop_flag = threading.Event()  # 创建一个多线程事件对象
        # self.ui = QUiLoader().load('C:\\Skutest.ui')
        self.ui = loadUi('C:\\Skutest.ui',self)
        self.setGeometry(300, 300, 300, 200)
        self.ui.skuBox.addItems(
            ['H7102', 'H7124', 'H7130', 'H7131', 'H7133', 'H7135', 'H713A', 'H713B', 'H713C', 'H7140', 'H7143', 'H7148',
             'H7180'])  # 下拉选择
        self.ui.skuBox.setCurrentIndex(0)  # 默认第一个H7130
        self.handle_serial()
        self.ui.main_funBox.clicked.connect(self.on_radio_button_toggled)  # 主要功能
        self.ui.wifi_Box.clicked.connect(self.on_radio_button_toggled)  # 配网
        self.ui.quitButton.clicked.connect(self.quit)  # 退出程序
        self.ui.stopButton.clicked.connect(self.stop)  # 暂停程序
        self.ui.refreshSerial.clicked.connect(self.handle_serial)  # 刷新串口
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

    def stop(self):
        self.stop_flag.set()  # 设置事件，通知线程退出
        self.ui.resultBrowser.append("程序暂停")
        print("程序停止")
        self.ui.startButton.setEnabled(True)
        self.ui.wifi_Box.setEnabled(True)
        self.ui.main_funBox.setEnabled(True)

    # 清除显示面板
    def clear_browser(self) -> None:
        self.ui.resultBrowser.clear()

    def handle_serial(self):
        self.ui.serialBox.clear()
        self.ui.serialBox.addItem("-选择串口-")
        if ConFig().serial_comlist():
            for i in ConFig().serial_comlist():
                self.ui.serialBox.addItem(i)
            self.ui.serialBox.activated[str].connect(self.onActivated)
            self.ui.serialBox.setCurrentIndex(0)  # 默认选择为第一个选项（索引为 0）
        else:
            self.ui.resultBrowser.append('无串口连接')
    def onActivated(self, serial_num):
        print(f'选择了串口: {serial_num}')
        self.ui.resultBrowser.append(f'选择了串口: {serial_num}')
        self.serial_num = serial_num
        try:
            self.ser = serial.Serial(self.serial_num,
                                     # self.ser = serial.Serial(com,
                                     self.dbs,
                                     timeout=self.timeout)
            self.ui.resultBrowser.append("连接串口{}成功".format(self.serial_num))
            # self.ui.serialBox.clear()
        except Exception as e:
            print(e)
            self.ui.resultBrowser.append("｛｝串口被占用或未接串口！".format(self.serial_num))

    def on_radio_button_toggled(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.resultBrowser.append(f'选择 {radioBtn.text()}')
            if "主功能" in radioBtn.text():
                self.main_home_func()
            elif "配网" in radioBtn.text():
                self.wifi_fun()
    """
       处理主功能逻辑和断言
    """

    # 复选主功能
    def main_home_func(self):

        if self.ui.main_funBox.isChecked():
            # self.ui.resultBrowser.clear()
            # self.ui.wifi_Box.setEnabled(False)
            # self.ui.wifi_Box.setChecked(False)
            # self.ui.serialBox.clear()
            self.ui.startButton.clicked.connect(self.thread_recv_main)
            # self.app = HandlePage()  # 设备id，app包名，点击后延迟
        else:
            # self.ui.serialBox.clear()
            print("串口close")
            self.ui.resultBrowser.append("串口close")
            self.ui.wifi_Box.setEnabled(True)
            self.ui.startButton.setEnabled(True)
            self.ui.refreshSerial.setEnabled(True)
            self.stop_flag.set()
            self.ser.close()

    # 复选配网
    def wifi_fun(self):
        if self.ui.wifi_Box.isChecked():
            self.ui.startButton.clicked.connect(self.thread_start_wifi)
        else:
            print("串口close")
            self.ui.resultBrowser.append("串口close")
            self.ui.startButton.setEnabled(True)
            self.ui.main_funBox.setEnabled(True)
            self.ui.refreshSerial.setEnabled(True)
            self.stop_flag.set()
            self.ser.close()

    # 选择小家电sku主程序
    def thread_start_main(self):
        self.app = HandlePage()
        self.sku = self.ui.skuBox.currentText()  # 显示选择的sku
        self.ui.resultBrowser.append("选择 ｛｝".format(self.sku))
        if self.sku[:4] in "H710X":
            self.ui.resultBrowser.append("开始测试{}".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H710X, args=(self.sku, self.stop_flag))
            thread.start()
        elif self.sku == "H7130":
            self.ui.resultBrowser.append("开始测试{}".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7130, args=(self.sku,))
            thread.start()
        elif self.sku[:4] in "H713X":
            self.ui.resultBrowser.append("开始测试{}".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H713X, args=(self.sku, self.stop_flag))
            thread.start()
        elif self.sku[:4] in "H712X":
            self.ui.resultBrowser.append("开始测试{}".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H712X, args=(self.sku, self.stop_flag))
            thread.start()
        elif self.sku[:4] in "H714X":
            self.ui.resultBrowser.append("开始测试{}".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H714X, args=(self.sku, self.stop_flag))
            thread.start()
        elif self.sku == "H7180":
            self.ui.resultBrowser.append("开始测试{}".format(self.sku))
            thread = threading.Thread(target=self.app.run_func_H7180, args=(self.sku,))
            thread.start()
        self.ui.skuBox.currentIndexChanged.connect(self.show)

    # 配网压测
    def thread_start_wifi(self):
        self.ui.startButton.setEnabled(False)
        self.ui.refreshSerial.setEnabled(False)
        self.ui.main_funBox.setEnabled(False)
        self.ui.wifi_Box.setEnabled(False)
        self.sku = self.ui.skuBox.currentText()  # 显示选择的sku
        self.start_wifi = threading.Thread(target=self.start_wifi)
        self.start_wifi.daemon = 1
        self.start_wifi.start()

    def start_wifi(self):
        self.sku_name = f"{self.sku}_" + self.ui.sku_name.text()
        print("配网测试")
        handle_wifi.add_devise_devices(self.stop_flag, self.sku, self.sku_name)

    # 主功能主线程和获取数据
    def thread_recv_main(self):
        self.stop_flag.clear()
        self.ui.startButton.setEnabled(False)
        self.ui.refreshSerial.setEnabled(False)
        self.ui.main_funBox.setEnabled(False)
        self.ui.wifi_Box.setEnabled(False)
        try:
            # self.app = HandlePage()  # 设备id，app包名，点击后延迟
            self.start_thread_main = threading.Thread(target=self.thread_start_main)  # 开始测试主线程
            self.read_date_thread_main = threading.Thread(target=self.read_date_main)  # 开始断言主线程
            self.start_thread_main.daemon = 1
            if self.ui.assertTextEdit.toPlainText().strip():
                print("空数据")
                self.read_date_thread_main.daemon = 1  # 守护线程，主线程退出，所有线程退出
                self.read_date_thread_main.start()
            self.start_thread_main.start()
        except Exception as e:
            print("启动app报错：", e)
            self.ui.resultBrowser.append("未连接手机")
            self.ui.startButton.setEnabled(True)

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
