#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  : https://blog.csdn.net/zhouzhiwengang/article/details/119735750
# @File    : https://blog.csdn.net/zhouzhiwengang/article/details/119735750
# @Description : 公共属性
import datetime
import time

import serial
import serial.tools.list_ports
import uiautomator2 as u2
import datetime
import threading
import time


class ConFig:

    # 获取串口列表
    def serial_comlist(self):
        port_list = []
        self.ports_list = list(serial.tools.list_ports.comports())
        # print("ports_lsit:", self.ports_list)
        if len(self.ports_list) <= 0:
            print("无串口设备。")
        else:
            for comport in self.ports_list:
                # print(list(comport)[0], list(comport)[1])  # 串口信息
                print("可用的串口设备如下：", list(comport)[0])
                port = list(comport)[0]
                port_list.append(port)
            # print("返回：",port_list)
            return port_list

    def sleep_with_fractional_seconds(self, seconds):
        whole_seconds = int(seconds)  # 获取整数部分
        fractional_seconds = seconds - whole_seconds  # 获取小数部分

        # 等待整数秒
        time.sleep(whole_seconds)

        # 等待小数秒（使用 threading.Timer）
        t = threading.Timer(fractional_seconds, lambda: None)
        t.start()
        t.join()


config = ConFig()
