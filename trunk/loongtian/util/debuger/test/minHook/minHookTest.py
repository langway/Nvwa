#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'leon'

import sys

from loongtian.util.debuger.hookHelper import *

bit = sys.maxsize

def Is64Windows():
    """
    通过\\PROGRAMFILES(X86)文件夹判断windows系统是否是64位的
    :return:
    """
    return 'PROGRAMFILES(X86)' in os.environ

Is_X64_System=False # 是否是64位系统，反之为32位系统
# 这里有个重要的区分：64位操作系统，还是64位的python运行系统
# 在32位系统中会输出False
if bool(bit > 2**32) :
    Is_X64_System=True
# Is_X64_Windows=Is64Windows()

dllPath = os.path.split(os.path.realpath(__file__))[0]
if Is_X64_System:
    dllPath +="\\MinHook.x64.dll"
else:
    dllPath += "\\MinHook.x86.dll"

MinHook=ctypes.windll.LoadLibrary(dllPath)

print(MinHook)

# MinHook Error Codes.
class MH_STATUS:

    # UNKNOWN error. Should not be returned.
    MH_UNKNOWN = -1

    # Successful.
    MH_OK = 0

    # MinHook is already initialized.
    MH_ERROR_ALREADY_INITIALIZED=1

    # MinHook is not initialized yet, or already uninitialized.
    MH_ERROR_NOT_INITIALIZED=2

    # The hook for the specified target function is already created.
    MH_ERROR_ALREADY_CREATED=3

    # The hook for the specified target function is not created yet.
    MH_ERROR_NOT_CREATED=4

    # The hook for the specified target function is already enabled.
    MH_ERROR_ENABLED=5

    # The hook for the specified target function is not enabled yet, or already
    # disabled.
    MH_ERROR_DISABLED=6

    # The specified pointer is invalid. It points the address of non-allocated
    # and/or non-executable region.
    MH_ERROR_NOT_EXECUTABLE=7

    # The specified target function cannot be hooked.
    MH_ERROR_UNSUPPORTED_FUNCTION=8

    # Failed to allocate Memory.
    MH_ERROR_MEMORY_ALLOC=9

    # Failed to change the Memory protection.
    MH_ERROR_MEMORY_PROTECT=10

    # The specified module is not loaded.
    MH_ERROR_MODULE_NOT_FOUND=11

    # The specified function is not found.
    MH_ERROR_FUNCTION_NOT_FOUND=12


# Helper function for MH_CreateHookApi().

def MH_CreateHookApiEx(pszModule, pszProcName, pDetour, ppOriginal):
    # LPCWSTR pszModule, LPCSTR pszProcName, LPVOID pDetour, T** ppOriginal

    # return MinHook.MH_CreateHookApi(pszModule, pszProcName, pDetour, reinterpret_cast<LPVOID*>(ppOriginal))
    return MinHook.MH_CreateHookApi(pszModule, pszProcName, pDetour, ppOriginal)

# typedef int (WINAPI *MESSAGEBOXW)(HWND, LPCWSTR, LPCWSTR, UINT)

# Pointer for calling original MessageBoxW.
fpMessageBoxW = ctypes.windll.user32.MessageBoxW

# Detour function which overrides MessageBoxW.
def DetourMessageBoxW(hWnd, lpText, lpCaption, uType):
    # HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, UINT uType
    # 这里进行输出lpszString的处理
    print(lpText.value)

    # 然后调用正版的TextOutA函数
    # Be a good neighbor and call the next hook./
    # return ctypes.windll.user32.CallNextHookEx(hook_id, hWnd, u"Hooked!", lpCaption, uType)
    return fpMessageBoxW(hWnd, u"Hooked!", lpCaption, uType)


def mainTest():
    # Initialize MinHook.
    result=MinHook.MH_Initialize()
    if (result != MH_STATUS.MH_OK):
        return 1

    # 接着用WINFUNCTYPE/CFUNCTYPE将其转换为可以被C调用的函数
    # Our low level handler signature.
    CMPFUNC = ctypes.CFUNCTYPE(HWND, LPCWSTR, LPCWSTR, UINT)
    # 这一句注释仅供供参考：WINFUNCTYPE的参数说明了被SetWindowsHookExA调用的函数的返回值和参数类型，其中最后一个参数是指向KBDLLHOOKSTRUCT结构体变量的指针类型。这样说明以后，我们就可以在khook_proc中用lParam.contents.vkCode这样的方式来访问结构体的域。
    # Convert the Python handler into C pointer.
    Detour_pointer = CMPFUNC(DetourMessageBoxW)
    fp_pointer = CMPFUNC(DetourMessageBoxW)
    old_pointer=CMPFUNC(ctypes.windll.user32.MessageBoxW)

    # Create a hook for MessageBoxW, in disabled state.
    # pDetour=LPVOID()
    # pDetour.value=POINTER(DetourMessageBoxW)
    # pDetour=cast(DetourMessageBoxW,c_void_p)
    # pDetour=addressof(DetourMessageBoxW)
    if (MH_CreateHookApiEx("user32", "MessageBoxW", Detour_pointer,old_pointer) != MH_STATUS.MH_OK):
        return 1

    # Enable the hook for MessageBoxW.
    if (MinHook.MH_EnableHook(old_pointer) != MH_STATUS.MH_OK):
        return 1

    # Expected to tell "Hooked!".
    ctypes.windll.user32.MessageBoxW(None, u"Not hooked...", u"MinHook Sample", MinHook.MB_OK)

    # Disable the hook for MessageBoxW.
    if (MinHook.MH_DisableHook(old_pointer) != MH_STATUS.MH_OK):
        return 1


    # Expected to tell "Not hooked...".
    ctypes.windll.user32.MessageBoxW(None, u"Not hooked...", u"MinHook Sample", MinHook.MB_OK)

    # Uninitialize MinHook.
    if (MinHook.MH_Uninitialize() != MH_STATUS.MH_OK):
        return 1

    return 0

if __name__=="__main__":
    mainTest()



