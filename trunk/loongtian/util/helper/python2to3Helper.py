#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "langway@163.com"

import sys
from subprocess import call
import os

writeToOriginal=False# 是否输出到源文件（默认为True）
withBak=False# 是否输出后缀为.bak的备份文件（默认为True）
withDiffs=True# 是否显示转换与源文件的差异（默认为True）

convertCommand=sys.executable
convertCommand+=" " + sys.exec_prefix +"\\Tools\\scripts\\"
convertCommand+="2to3.py "
if writeToOriginal:
    convertCommand+=" -w "
if not withBak :
    convertCommand+=" -n "
if not withDiffs:
    convertCommand+=" -no-diffs "


def convert(fileOrPath):
    if fileOrPath==None or fileOrPath=="":
        print("你应该提供要转换的文件或路径！")
        return

    if not os.path.exists(fileOrPath):
        print("提供的要转换的文件或路径错误！")
        return

    command=convertCommand + fileOrPath
    call(command, shell=False)
