#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'leon'

import time
from pywinauto.application import Application
from pywinauto.controls.common_controls import ListViewWrapper
import win32gui
from loongtian.util.uiautomation import screen, mouse_key_commond
# exe_path=r"D:\Program Files (x86)\wh6弘业期货\mytrader_spqh.exe"
# # start the application and wait for the Agent Dialog to be ready
# process_input=input("输入要连接的程序进程id：")
# process_input=int(process_input)
# handle_input=input("输入要连接的窗体handle：")
# handle_input=int(handle_input)
# app = Application().connect(process=process_input,handle=handle_input)
#
#
# while not app.Windows_():
#     time.sleep(.5)
#
# app.

hwnd_input=590250 #input("输入ListView的窗体句柄：")
hwnd_input=int(hwnd_input)
lst=ListViewWrapper(hwnd_input)
# import time
# time.sleep(5)
print(lst.item_count())

print(lst.column_count())
screen.active_window(hwnd_input)
# time.sleep(5)
item=lst.item(0)
item.select()
# item.click(double=True)
#
print(item.text())
item.click(double=True)
# item.click(double=True)


rect=item.rectangle()
print(rect)
mid_point=item.rectangle().mid_point()

print (mid_point)
screen_point=win32gui.ClientToScreen(hwnd_input,(mid_point.x,mid_point.y))
print(screen_point)

# mouse_key_commond.mouse_move_dclick(screen_point[0],screen_point[1]+8)
# for item in lst.items():
#     print (item.text())




