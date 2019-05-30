#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__author__ = 'leon'

import pydbg
import subprocess

dbg = pydbg.pydbg()

# pid = os.getpid()
p = subprocess.Popen("notepad.exe")
pid = p.pid
dbg.attach(pid)

text_out_w = dbg.func_resolve_debuggee('GDI32.dll', 'TextOutW')

text_out_a = dbg.func_resolve_debuggee('GDI32.dll', 'TextOutA')


def text_out_hndler(dbg):
    print "called"
    return pydbg.defines.DBG_CONTINUE

dbg.bp_set(address=text_out_w, handler=text_out_hndler)
dbg.bp_set(address=text_out_a, handler=text_out_hndler)

dbg.run()


# if __name__ == '__main__':
    # ctypes.windll.user32.MessageBoxW(0, u"内容测试", u"测试标题", 0)

