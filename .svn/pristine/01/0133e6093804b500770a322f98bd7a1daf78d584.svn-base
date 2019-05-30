#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'leon'

import win32api
import win32con
import win32gui
from ctypes import *
import time

VK_CODE = {

    'backspace':0x08,
    'tab':0x09,
    'clear':0x0C,
    'enter':0x0D,
    'shift':0x10,
    'ctrl':0x11,
    'alt':0x12,
    'pause':0x13,
    'caps_lock':0x14,
    'esc':0x1B,
    'spacebar':0x20,
    'page_up':0x21,
    'page_down':0x22,
    'end':0x23,
    'home':0x24,
    'left_arrow':0x25,
    'up_arrow':0x26,
    'right_arrow':0x27,
    'down_arrow':0x28,
    'select':0x29,
    'print':0x2A,
    'execute':0x2B,
    'print_screen':0x2C,
    'ins':0x2D,
    'del':0x2E,
    'help':0x2F,
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    'numpad_0':0x60,
    'numpad_1':0x61,
    'numpad_2':0x62,
    'numpad_3':0x63,
    'numpad_4':0x64,
    'numpad_5':0x65,
    'numpad_6':0x66,
    'numpad_7':0x67,
    'numpad_8':0x68,
    'numpad_9':0x69,
    'multiply_key':0x6A,
    'add_key':0x6B,
    'separator_key':0x6C,
    'subtract_key':0x6D,
    'decimal_key':0x6E,
    'divide_key':0x6F,
    'F1':0x70,
    'F2':0x71,
    'F3':0x72,
    'F4':0x73,
    'F5':0x74,
    'F6':0x75,
    'F7':0x76,
    'F8':0x77,
    'F9':0x78,
    'F10':0x79,
    'F11':0x7A,
    'F12':0x7B,
    'F13':0x7C,
    'F14':0x7D,
    'F15':0x7E,
    'F16':0x7F,
    'F17':0x80,
    'F18':0x81,
    'F19':0x82,
    'F20':0x83,
    'F21':0x84,
    'F22':0x85,
    'F23':0x86,
    'F24':0x87,
    'num_lock':0x90,
    'scroll_lock':0x91,
    'left_shift':0xA0,
    'right_shift ':0xA1,
    'left_control':0xA2,
    'right_control':0xA3,
    'left_menu':0xA4,
    'right_menu':0xA5,
    'browser_back':0xA6,
    'browser_forward':0xA7,
    'browser_refresh':0xA8,
    'browser_stop':0xA9,
    'browser_search':0xAA,
    'browser_favorites':0xAB,
    'browser_start_and_home':0xAC,
    'volume_mute':0xAD,
    'volume_Down':0xAE,
    'volume_up':0xAF,
    'next_track':0xB0,
    'previous_track':0xB1,
    'stop_media':0xB2,
    'play/pause_media':0xB3,
    'start_mail':0xB4,
    'select_media':0xB5,
    'start_application_1':0xB6,
    'start_application_2':0xB7,
    'attn_key':0xF6,
    'crsel_key':0xF7,
    'exsel_key':0xF8,
    'play_key':0xFA,
    'zoom_key':0xFB,
    'clear_key':0xFE,
    '+':0xBB,
    ',':0xBC,
    '-':0xBD,
    '.':0xBE,
    '/':0xBF,
    '`':0xC0,
    ';':0xBA,
    '[':0xDB,
    '\\':0xDC,
    ']':0xDD,
    # "'":0xDE,


    # 后面为ascii表十六进制
    "(space)":0x20,
    "!":0x21,
    "\"":0x22,
    "#":0x23,
    "$":0x24,
    "%":0x25,
    "&":0x26,
    "'":0x27,
    "(":0x28,
    ")":0x29,
    "*":0x2A,
    "+":0x2B,
    ",":0x2C,
    "-":0x2D,
    ".":0x2E,
    "/":0x2F,
    ":":0x3A,
    ";":0x3B,
    "<":0x3C,
    "=":0x3D,
    ">":0x3E,
    "?":0x3F,
    "@":0x40,
    "A":0x41,
    "B":0x42,
    "C":0x43,
    "D":0x44,
    "E":0x45,
    "F":0x46,
    "G":0x47,
    "H":0x48,
    "I":0x49,
    "J":0x4A,
    "K":0x4B,
    "L":0x4C,
    "M":0x4D,
    "N":0x4E,
    "O":0x4F,
    "P":0x50,
    "Q":0x51,
    "R":0x52,
    "S":0x53,
    "T":0x54,
    "U":0x55,
    "V":0x56,
    "W":0x57,
    "X":0x58,
    "Y":0x59,
    "Z":0x5A,
    "[":0x5B,
    "\\":0x5C,
    "]":0x5D,
    "^":0x5E,
    "_":0x5F,
    "`":0x60,
    "{":0x7B,
    "|":0x7C,
    "}":0x7D,
    "~":0x7E,
    "DEL (delete)":0x7F,

}


class POINT(Structure):
    _fields_ = [("x", c_ulong),("y", c_ulong)]

def get_mouse_point():
    """
    取得当前鼠标的坐标
    :return:
    """
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def mouse_click():
    """
    在鼠标当前位置模拟鼠标单击操作。
    :return:
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.Sleep(5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def mouse_dclick():
    """
    在鼠标当前位置模拟鼠标单击操作。
    :return:
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.Sleep(5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.Sleep(5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.Sleep(5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def mouse_click_control(handle):
    """
    对指定句柄的控件模拟鼠标单击操作。
    :param handle:
    :return:
    """
    # win32gui.PostMessage(handle, win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    # win32api.Sleep(5)
    # win32gui.PostMessage(handle, win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    # win32api.Sleep(5)

    m=win32gui.SendMessage(handle, win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    # # win32api.Sleep(5)
    # print (m)
    m=win32gui.SendMessage(handle, win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    # # win32api.Sleep(5)
    # print (m)

def mouse_dclick_control(handle):
    """
    对指定句柄的控件模拟鼠标双击操作。
    :param handle:
    :return:
    """
    message= win32gui.SendMessage(handle, win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    if message:
        message = win32gui.SendMessage(handle, win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    if message:
        return True
    return False

def mouse_move(x,y):
    """
    将鼠标移动到指定位置
    :param x:
    :param y:
    :return:
    """
    if not x is None and not y is None:
        # print (win32gui.GetCursorPos())
        try:
            windll.user32.SetCursorPos(x, y)
            # win32api.SetCursorPos([x,y])  # 光标定位
        except Exception as e:
            print (e)

        win32api.Sleep(5)
        # print (win32gui.GetCursorPos())

def mouse_move_rect(rect):
    """
    将鼠标移动到指定位置
    :param x:
    :param y:
    :return:
    """
    left, top, right, bottom = rect
    # print (rect)
    # x=
    mouse_move(left + (right - left) / 2, top + (bottom - top) / 2)

    # win32api.SetCursorPos(x,y)  # 光标定位
    # win32api.Sleep(5)

def mouse_move_click_rect(rect):
    left, top, right, bottom=rect
    print (rect)
    # x=
    mouse_move_click(left + (right - left) / 2, top + (bottom - top) / 2)

def mouse_move_click_control(handle):
    rect=win32gui.GetWindowRect(handle)
    return mouse_move_click_rect(rect)


def mouse_move_click(x=None, y=None):
    """
    将鼠标移动到指定位置，并单击。
    :param x:
    :param y:
    :return:
    """

    if not x is None and not y is None:
        mouse_move(x,y)
        win32api.Sleep(5)
    mouse_click()
    # return mouse_click


def mouse_move_dclick(x=None, y=None):
    """
    将鼠标移动到指定位置，并双击。
    :param x:
    :param y:
    :return:
    """
    if not x is None and not y is None:
        mouse_move(x,y)
        win32api.Sleep(5)
    mouse_dclick()

def press_enter_by_conntrol(handle):
    """
    回车确认（在窗体或控件上）。
    :param handle:
    :return:
    """

    win32gui.PostMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32api.Sleep(5)
    win32gui.PostMessage(handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    win32api.Sleep(5)

def press_enter():
    """
    回车确认
    :return:
    """
    key_input("enter")


def key_input(str='',asOne=True):
    """
    模拟键盘输入字符串。
    :param str:字符串
    :param asOne:是否作为一个整体，例如：输入字符串“F5”，如作为整体，则是F5刷新键，否则，则是一个字符
    :return:
    """
    if asOne:
        vk=VK_CODE.get(str,None)
        if vk:
            win32api.keybd_event(vk, 0, 0, 0)
            win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.Sleep(10)
            return

    for c in str:
        win32api.keybd_event(VK_CODE[c],0,0,0)
        win32api.keybd_event(VK_CODE[c],0,win32con.KEYEVENTF_KEYUP,0)
        # print (VK_CODE[c])
        win32api.Sleep(10)


#如果类名不能获取窗口句柄，文件名不能完整找到，可以枚举窗口，需找符合条件的窗口。
def findPicPick():
    hd_list = []

    #回调函数
    def foo(hwnd, mouse):
        # 去掉下面这句会使所有窗口都输出
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            #注意大写
            #print win32gui.GetWindowText(hwnd)
            if "PicPick" in win32gui.GetWindowText(hwnd):
                hd_list.append(hwnd)

    win32gui.EnumWindows(foo, 0)

    #hd_notepad = win32gui.FindWindow("notepad", None) 成功
    #hd2 = win32gui.FindWindow(None, "TfrmMDIEditor") 失败，找不到picpcik
    #print hd_notepad
    #print hd2

    win32api.keybd_event(18,0,0,0)    # Alt
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(70,0,0,0)    # F
    win32api.keybd_event(70, 0, win32con.KEYEVENTF_KEYUP, 0)

def commond(hwnd,control_id):
    """
    当用户选择了菜单（或按钮等控件的）命令，或控件发送通知到父窗口，
    或加速键击（accelerator keystroke is translated）时发送。
    :param hwnd:父窗口句柄
    :param control_id:菜单（或按钮等控件的）id
    :return:返回值：如果窗体处理了消息，应返回0
    """
    # 这里不用win32gui.SendMessage，是因为SendMessage需要等待结果，可能并没有结果，就死循环了。
    message=win32gui.PostMessage(hwnd, win32con.WM_COMMAND, control_id, 0)
    #win32gui.PostMessage必须有时间间隔，否则无法获得handle
    win32api.Sleep(200)
    return message

if __name__ == "__main__":

    def t0():
        mouse_move_click(100, 30)
        pass


    def t2():
        mouse_move_click(20, 20)
        for c in 'hello':
            win32api.keybd_event(65, 0, 0, 0)  # a键位码是86
            win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)
            # print get_mouse_point()


    def t1():
        # mouse_move(1024,470)aa
        # time.sleep(0.05)
        # mouse_dclick()HELLO
        mouse_move_dclick(1024, 470)


    def t3():
        mouse_move_click(1024, 470)
        str = 'hello'
        for c in str:
            win32api.keybd_event(VK_CODE[c], 0, 0, 0)  # a键位码是86
            win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.01)


    def t4():
        mouse_move_click(1024, 470)
        str = 'hello'
        key_input(str)

    # t4()
    # t3()
    # t2()
    # t1()
    t0()