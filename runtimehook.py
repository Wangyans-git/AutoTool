#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @Description : 程序打包配置

import sys
import os

currentdir = os.path.dirname(sys.argv[0])
libdir = os.path.join(currentdir, "lib")
print(currentdir)
sys.path.append(libdir)
os.environ['path'] += ';./lib'