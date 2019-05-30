#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009-2016, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from winappdbg import Debug, EventHandler
from ctypes import windll
from loongtian.util.debuger.hookHelper import HDC, c_int, LPCSTR,LPCWSTR


# This function will be called when the hooked function is entered.

def H_TextOutA(event, ra, hdc, nXStart, nYStart, lpszString, cbString):
    # Get the format string.
    process = event.get_process()

    print(lpszString)
    # lpFmt = process.peek_string(lpFmt, fUnicode=True)
    #
    # # Get the vararg parameters.
    # count = lpFmt.replace('%%', '%').count('%')
    # thread = event.get_thread()
    # if process.get_bits() == 32:
    #     parameters = thread.read_stack_dwords(count, offset=3)
    # else:
    #     parameters = thread.read_stack_qwords(count, offset=3)
    #
    # # Show a message to the user.
    # showparams = ", ".join([hex(x) for x in parameters])
    # print "wsprintf( %r, %s );" % (lpFmt, showparams)


# 定义将要被SetWindowsHookExA调用的Python函数khook_proc——MyTextOutA
def H_TextOutW(hdc, nXStart, nYStart, lpszString, cbString):
    """
    我们的替换函数，可以在里面实现我们所要做的功能
    这里我做的是显示一个对话框，指明是替换了哪个函数
    函数原型：BOOL WINAPI H_TextOutW(HDC hdc, int nXStart, int nYStart, LPCWSTR lpszString, int cbString)
    """
    # 这里进行输出lpszString的处理
    print(lpszString.value)

    # 然后调用正版的TextOutA函数，以显示字符
    windll.user32.TextOutW(hdc, nXStart, nYStart, lpszString, cbString)

    return True
    # # Be a good neighbor and call the next hook./
    # return windll.user32.CallNextHookEx(hook_id, hdc, nXStart, nYStart, lpszString, cbString)


class MyEventHandler(EventHandler):

    def load_dll(self, event):
        # Get the new module object.
        module = event.get_module()

        # If it's user32...
        if module.match_name("GDI32.dll"):
            # Get the process ID.
            pid = event.get_pid()

            # Get the address of wsprintf.
            address = module.resolve("TextOutA")

            # This is an approximated signature of the wsprintf function.
            # Pointers must be void so ctypes doesn't try to read from them.
            # Varargs are obviously not included.
            signature = (HDC, c_int, c_int, c_int, LPCSTR, c_int)

            # Hook the wsprintf function.
            event.debug.hook_function(pid, address, H_TextOutA, signature=signature)

            # Get the address of wsprintf.
            address = module.resolve("TextOutW")


            # This is an approximated signature of the wsprintf function.
            # Pointers must be void so ctypes doesn't try to read from them.
            # Varargs are obviously not included.
            signature = (HDC, c_int, c_int, c_int, LPCWSTR, c_int)

            # Hook the wsprintf function.
            event.debug.hook_function(pid, address, H_TextOutW, signature=signature)


            # Use stalk_function instead of hook_function
            # to be notified only the first time the function is called.
            #
            # event.debug.stalk_function( pid, address, wsprintf, signature = signature)


def simple_debugger(argv):
    # Instance a Debug object, passing it the MyEventHandler instance.
    with Debug(MyEventHandler(), bKillOnExit=True) as debug:
        # Start a new process for debugging.
        debug.execv(argv)

        # Wait for the debugee to finish.
        debug.loop()


# When invoked from the command line,
# the first argument is an executable file,
# and the remaining arguments are passed to the newly created process.
if __name__ == "__main__":
    import sys
    #
    sys.argv.append("c:\\windows\\system32\\notepad.exe")
    simple_debugger(sys.argv[1:])



    # from winappdbg import Debug, EventHandler
    # import sys
    # import os
    #
    # class MyEventHandler( EventHandler ):
    #
    #     # Add the APIs you want to hook
    #     apiHooks = {
    #
    #         'msvbvm60.dll' : [( 'rtcMsgBox'  ,   7  ),],'kernel32.dll' : [( 'CreateFileW'  ,   7  ),],
    #         }
    #
    #     # The pre_ functions are called upon entering the API
    #
    #     def pre_CreateFileW(self, event, ra, lpFileName, dwDesiredAccess,
    #              dwShareMode, lpSecurityAttributes, dwCreationDisposition,
    #                                 dwFlagsAndAttributes, hTemplateFile):
    #
    #         fname = event.get_process().peek_string(lpFileName, fUnicode=True)
    #         print "CreateFileW: %s" % (fname)
    #
    #     # The post_ functions are called upon exiting the API
    #
    #     def post_CreateFileW(self, event, retval):
    #         if retval:
    #             print 'Suceeded (handle value: %x)' % (retval)
    #         else:
    #             print 'Failed!'
    #
    # if __name__ == "__main__":
    #
    #     if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
    #         # print sys.argv[1]
    #         print "\nUsage: %s <File to monitor> [arg1, arg2, ...]\n" % sys.argv[0]
    #         sys.exit()
    #
    #     # Instance a Debug object, passing it the MyEventHandler instance
    #     debug = Debug( MyEventHandler())
    #
    #     try:
    #         # Start a new process for debugging
    #         p = debug.execv(sys.argv[1:], bFollow=True)
    #
    #         # Wait for the debugged process to finish
    #         debug.loop()
    #
    #     # Stop the debugger
    #     finally:
    #         debug.stop()
