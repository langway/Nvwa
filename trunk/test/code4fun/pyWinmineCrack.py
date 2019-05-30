#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
python自动扫雷程序
"""
__author__ = 'leon'


# 先说下原理，原理其实很简单，设法获得“雷区”的数据，然后通过模拟鼠标动作，点击雷区上非地雷的的格子，就搞定了:) 所以技术难点只有三个：获得雷区数据、找到扫雷程序和模拟鼠标动作。
# 先说简单的，找到扫雷程序。通过win32gui.FindWindow("扫雷", "扫雷") 就可以找到扫雷程序的主窗体了，很简单吧。FindWindow这个API参数含义参看MSDN.
# 然后是模拟鼠标点击动作，这也很简单，通过win32api.SendMessage来向窗体发送鼠标的按下WM_LBUTTONDOWN和松开WM_LBUTTONUP消息就行了，这个api的主要参数是，接收信息的窗体句柄（这里是扫雷程序的主窗体）和鼠标点击的坐标。这个api的使用不难，具体参考MSDN:)
# 比较有难度的是如何获得雷区数据。这里有两个事情要做，首先要找出雷区在程序内部是如何表示的，如何区分格子是有雷还是无雷，如何知道雷区格子大小，以及这些数据保存在程序什么位置，是固定位置还是变化的。弄到这些情报后，第二件事情就简单了，我们可以通过几个api函数很轻松地就获取雷区的动态数据。
# 要完成第一件事情，我们需要一个叫ollydbg的反汇编调试工具、一些些汇编知识以及很大的耐心，呵呵，具体过程这里就不说了，主要是不知道怎样说清楚，感觉靠经验多一些。通过跟踪汇编代码，我们可以发现无雷的格子数据是0x0F，有雷的是0x8F，而雷区数据总是从0x1005340 这个逻辑地址开始。其他具体获得的数据见以下源码。
# 有了这些数据后，我们通过win32process.GetWindowThreadProcessId获得“扫雷”的进程id， 通过OpenProcess 打开该进程，然后通过ReadProcessMemory 读取0x1005340开始的雷区数据，最后根据这些数据通过SendMessage向扫雷程序发送鼠标消息，就搞定了，保证每次扫雷都是“秒杀”


import win32gui
import win32process
import win32con
import win32api
from ctypes import *

# 雷区最大行列数
MAX_ROWS = 24
MAX_COLUMNS = 30

# 雷区格子在窗体上的起始坐标及每个格子的宽度
MINE_BEGIN_X = 0xC
MINE_BEGIN_Y = 0x37
MINE_GRID_WIDTH = 0x10
MINE_GRID_HEIGHT = 0x10

# 边框、无雷、有雷的内部表示
MINE_BOARDER = 0x10
MINE_SAFE = 0x0F
MINE_DANGER = 0x8F

# “雷区”在 扫雷程序中的存储地址
BOARD_ADDR = 0x1005340


class SMineCtrl(Structure):
    _fields_ = [("hWnd", c_uint),
                ("board", (c_byte * (MAX_COLUMNS + 2)) * (MAX_ROWS + 2)),
                ("rows", c_byte),
                ("columns", c_byte)
                ]


kernel32 = windll.LoadLibrary("kernel32.dll")

ReadProcessMemory = kernel32.ReadProcessMemory

WriteProcessMemory = kernel32.WriteProcessMemory

OpenProcess = kernel32.OpenProcess
ctrlData = SMineCtrl()

# 找到扫雷程序并打开对应进程
try:
    ctrlData.hWnd = win32gui.FindWindow("扫雷", "扫雷")

except:
    win32api.MessageBox(0, "请先运行扫雷程序", "错误！", win32con.MB_ICONERROR)
    exit(0)

hreadID, processID = win32process.GetWindowThreadProcessId(ctrlData.hWnd)

hProc = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID)

# 读取雷区数据
bytesRead = c_ulong(0)

ReadProcessMemory(hProc, BOARD_ADDR, byref(ctrlData.board), SMineCtrl.board.size, byref(bytesRead))

if (bytesRead.value != SMineCtrl.board.size):
    str = "ReadProcessMemory error, only read ", bytesRead.value, " should read ", SMineCtrl.board.size
    win32api.MessageBox(0, str, "错误！", win32con.MB_ICONERROR)
    exit()

# www.iplaypy.com

# 获取本次程序雷区的实际大小
ctrlData.rows = 0

ctrlData.columns = 0

for i in range(0, MAX_COLUMNS + 2):
    if MINE_BOARDER == ctrlData.board[0]:
        ctrlData.columns += 1
    else:
        break

ctrlData.columns -= 2

for i in range(1, MAX_ROWS + 1):
    if MINE_BOARDER != ctrlData.board[1]:
        ctrlData.rows += 1
    else:
        break

# 模拟鼠标点击动作
for i in range(0, ctrlData.rows):

    for j in range(0, ctrlData.columns):

        if MINE_SAFE == ctrlData.board[i + 1][j + 1]:
            win32api.SendMessage(ctrlData.hWnd,
                                 win32con.WM_LBUTTONDOWN,
                                 win32con.MK_LBUTTON,
                                 win32api.MAKELONG(MINE_BEGIN_X + MINE_GRID_WIDTH * j + MINE_GRID_WIDTH / 2,
                                                   MINE_BEGIN_Y + MINE_GRID_HEIGHT * i + MINE_GRID_HEIGHT / 2))
            win32api.SendMessage(ctrlData.hWnd,
                                 win32con.WM_LBUTTONUP,

                                 win32con.MK_LBUTTON,
                                 win32api.MAKELONG(MINE_BEGIN_X + MINE_GRID_WIDTH * j + MINE_GRID_WIDTH / 2,
                                                   MINE_BEGIN_Y + MINE_GRID_HEIGHT * i + MINE_GRID_HEIGHT / 2))

# 完成任务
win32api.MessageBox(0, "搞定！", "信息", win32con.MB_ICONINFORMATION)