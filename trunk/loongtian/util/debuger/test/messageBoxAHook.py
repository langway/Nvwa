#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__author__ = 'leon'

from ctypes import c_int, WINFUNCTYPE, windll
from ctypes.wintypes import HWND, LPCSTR, UINT
prototype = WINFUNCTYPE(c_int, HWND, LPCSTR, LPCSTR, UINT)
paramflags = (1, "hwnd", 0), (1, "text", "Hi"), (1, "caption", u"测试"), (1, "flags", 0)
MessageBox = prototype(("MessageBoxA", windll.user32), paramflags)
MessageBox()
MessageBox(text="Spam, spam, spam")
MessageBox(flags=2, text="foo bar")

