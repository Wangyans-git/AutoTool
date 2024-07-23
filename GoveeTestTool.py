#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @Description : 程序入口


import sys

from PyQt5.QtWidgets import QApplication
from package_qt.handle_qt import HandleQt

if __name__ == '__main__':
    app = QApplication([])
    program = HandleQt()
    program.ui.show()
    sys.exit(app.exec_())
