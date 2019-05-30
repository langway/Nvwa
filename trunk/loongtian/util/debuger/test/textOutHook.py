#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__author__ = 'leon'

from ctypes import windll, CFUNCTYPE, byref

import atexit
import win32api
import win32con
import win32gui

from loongtian.util.debuger.hookHelper import *


def listen():
    def GetMsgProc(code, wParam, lParam):
        """
        钩子子程。与其它钩子子程不大相同，没做什么有意义的事情，继续调用下一个钩子子程，形成循环
        函数原型：LRESULT CALLBACK GetMsgProc(int code, WPARAM wParam, LPARAM lParam)
        :param code:
        :param wParam:
        :param lParam:
        :return:
        """

        # Be a good neighbor and call the next hook./
        return windll.user32.CallNextHookEx(hook_id, code, wParam, lParam)

    # 定义将要被SetWindowsHookExA调用的Python函数khook_proc——MyTextOutA
    def H_TextOutA(hdc, nXStart, nYStart, lpszString, cbString):
        """
        我们的替换函数，可以在里面实现我们所要做的功能
        这里我做的是显示一个对话框，指明是替换了哪个函数
        函数原型：BOOL WINAPI H_TextOutA(HDC hdc, int nXStart, int nYStart, LPCTSTR lpszString, int cbString)
        """
        # 这里进行输出lpszString的处理
        print(lpszString.value)

        # 然后调用正版的TextOutA函数，以显示字符
        windll.user32.TextOutA(hdc, nXStart, nYStart, lpszString, cbString)
        return True
        # # Be a good neighbor and call the next hook./
        # return windll.user32.CallNextHookEx(hook_id, hdc, nXStart, nYStart, lpszString, cbString)

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

    def InstallHook(IsHook, dwThreadId=0):
        """
        安装或卸载钩子，BOOL IsHook参数是标志位
        对要钩哪个API函数进行初始化
        我们这里装的钩子类型是WH_GETMESSAGE
        函数原型：void __declspec(dllexport) WINAPI InstallHook(BOOL IsHook, DWORD dwThreadId)
        :param IsHook:
        :param dwThreadId:
        :return:
        """
        if (IsHook):
            # 接着用WINFUNCTYPE/CFUNCTYPE将其转换为可以被C调用的函数
            # Our handler signature.
            CMPFUNC = CFUNCTYPE(int, WPARAM, LPARAM)  # GetMsgProc的signature
            # CMPFUNC = CFUNCTYPE(HDC, c_int, c_int, c_int, LPCTSTR, c_int) # H_TextOutA的signature
            # 这一句注释仅供供参考：WINFUNCTYPE的参数说明了被SetWindowsHookExA调用的函数的返回值和参数类型，其中最后一个参数是指向KBDLLHOOKSTRUCT结构体变量的指针类型。这样说明以后，我们就可以在khook_proc中用lParam.contents.vkCode这样的方式来访问结构体的域。
            # Convert the Python handler into C pointer.
            pointer = CMPFUNC(GetMsgProc)

            # Hook both key up and key down events for common keys (non-system).
            # 把这个pointer传递给SetWindowsHookExA
            # SetWindowsHookExA(消息类型, dll的回调函数地址, dll句柄, 窗口线程)
            # 我们这里装的钩子类型是WH_GETMESSAGE
            # 函数原型：HHOOK SetWindowsHookEx( int idHook, HOOKPROC lpfn,HINSTANCE hMod,DWORD dwThreadId );
            hook_id = windll.user32.SetWindowsHookExA(win32con.WH_GETMESSAGE,
                                                      pointer,
                                                      win32api.GetModuleHandle("GDI32.dll"),
                                                      # win32api.GetProcAddress(win32api.GetModuleHandle("GDI32.dll"),"TextOutW"),
                                                      dwThreadId)
            # win32api.GetModuleHandle(None), 0)

            # GetProcAddress(GetModuleHandle("GDI32.dll"),"ExtTextOutA")：取得要钩的函数在所在dll中的地址

            # 调用原型：
            # HookAllAPI((LPCTSTR)"GDI32.dll",
            #             GetProcAddress(GetModuleHandle((LPCTSTR)"GDI32.dll"),"TextOutA"),
            #             (PROC) & H_TextOutA, None);
            HookAllAPI("GDI32.dll",
                       win32api.GetProcAddress(win32api.GetModuleHandle("GDI32.dll"), "TextOutW"),
                       H_TextOutW,
                       None)
            HookAllAPI("GDI32.dll",
                       win32api.GetProcAddress(win32api.GetModuleHandle("GDI32.dll"), "TextOutA"),
                       H_TextOutA,
                       None)

            return hook_id

        else:

            UnInstallHook()

            # 调用原型：
            # HookAllAPI((LPCTSTR)"GDI32.dll",
            #             GetProcAddress(GetModuleHandle((LPCTSTR)"GDI32.dll"),"TextOutA"),
            #             (PROC) & H_TextOutA, None);
            UnhookAllAPIHooks("GDI32.dll",
                              win32api.GetProcAddress(win32api.GetModuleHandle("GDI32.dll"), "TextOutW"),
                              H_TextOutW,
                              None)
            UnhookAllAPIHooks("GDI32.dll",
                              win32api.GetProcAddress(win32api.GetModuleHandle("GDI32.dll"), "TextOutA"),
                              H_TextOutA,
                              None)

    def UnInstallHook():
        """
        卸载钩子
        函数原型：BOOL WINAPI UnInstallHook()
        :return:
        """
        return windll.user32.UnhookWindowsHookEx(hook_id)

    def UnhookAllAPIHooks(pszCalleeModuleName, pfnOriginApiAddress, pfnDummyFuncAddress, hModCallerModule):
        """
        通过使pfnDummyFuncAddress与pfnOriginApiAddress相等的方法，取消对IAT的修改。
        函数原型：BOOL WINAPI UnhookAllAPIHooks(LPCTSTR pszCalleeModuleName, PROC pfnOriginApiAddress,
	        PROC pfnDummyFuncAddress, HMODULE hModCallerModule)
        :param pszCalleeModuleName:
        :param pfnOriginApiAddress:
        :param pfnDummyFuncAddress:
        :param hModCallerModule:
        :return:
        """

        temp = pfnOriginApiAddress
        pfnOriginApiAddress = pfnDummyFuncAddress
        pfnDummyFuncAddress = temp
        return HookAllAPI(pszCalleeModuleName, pfnOriginApiAddress,
                          pfnDummyFuncAddress, hModCallerModule)

    def HookAllAPI(pszCalleeModuleName, pfnOriginApiAddress,pfnDummyFuncAddress, hModCallerModule):
        """
        查找所挂钩的进程所应用的dll模块的
        函数原型：BOOL WINAPI HookAllAPI(LPCTSTR pszCalleeModuleName, PROC pfnOriginApiAddress,
	    PROC pfnDummyFuncAddress, HMODULE hModCallerModule)
        函数原型：
        :param pszCalleeModuleName:
        :param pfnOriginApiAddress:
        :param pfnDummyFuncAddress:
        :param hModCallerModule:
        :return:
        """

        if (pszCalleeModuleName == None):
            return False
        
        if (pfnOriginApiAddress == None):
            return False
        
        # 如果没传进来要挂钩的模块名称，枚举被挂钩进程的所有引用的模块，
        # 并对这些模块进行传进来的相应函数名称的查找

        if (hModCallerModule == None):
        
            # MEMORY_BASIC_INFORMATION mInfo;
            # HMODULE hModHookDLL;
            # HANDLE hSnapshot;

            # 方案1：
            # hModuleSnap = DWORD
            # windll.kernel32.SetLastError(10000)
            # me = MODULEENTRY32()
            # me.dwSize = sizeof(MODULEENTRY32)
            # # me.dwSize = 5000
            # hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, 0)
            # bOk = Module32First(hModuleSnap, pointer(me))

            # 方案2：
            mInfo = MEMORY_BASIC_INFORMATION()
            windll.kernel32.SetLastError(10000)
            # 原型：VirtualQuery(HookOneAPI, byref(mInfo), sizeof(mInfo));
            result = windll.kernel32.VirtualQuery(addressof(HookOneAPI), byref(mInfo), byref(mInfo))

            hModHookDLL = mInfo.AllocationBase

            hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, 0)
            # MODULEENTRY32:描述了一个被指定进程所应用的模块的struct
            me = sizeof(MODULEENTRY32)
            bOk = Module32First(hModuleSnap, pointer(me))

            while (bOk):
                global PROGMainBase
                PROGMainBase = False

                if (me.hModule != hModHookDLL):
                    hModCallerModule = me.hModule # 赋值
                    # me.hModule:指向当前被挂钩进程的每一个模块
                    HookOneAPI(pszCalleeModuleName, pfnOriginApiAddress,
                        pfnDummyFuncAddress, hModCallerModule)

                bOk = Module32Next(hModuleSnap, pointer(me))
            else:
                CloseHandle(hModuleSnap)
            
            return True
        # 如果传进来了，进行查找
        else:
        
            HookOneAPI(pszCalleeModuleName, pfnOriginApiAddress,
                pfnDummyFuncAddress, hModCallerModule)
            return True
        
        return False

    def HookOneAPI(pszCalleeModuleName, pfnOriginApiAddress,pfnDummyFuncAddress, hModCallerModule):
        """
        进行IAT转换的关键函数。
        函数原型：void WINAPI HookOneAPI(LPCTSTR pszCalleeModuleName, PROC pfnOriginApiAddress,
                                        PROC pfnDummyFuncAddress, HMODULE hModCallerModule)
        :param pszCalleeModuleName: 需要hook的模块名
        :param pfnOriginApiAddress: 要替换的自己API函数的地址
        :param pfnDummyFuncAddress: 需要hook的模块名的地址
        :param hModCallerModule: 我们要查找的模块名称，如果没有被赋值，将会被赋值为枚举的程序所有调用的模块
        :return:
        """

        size=ULONG
        # 获取指向PE文件中的Import中IMAGE_DIRECTORY_DESCRIPTOR数组的指针
        # pImportDesc = ImageDirectoryEntryToData(hModCallerModule, True, IMAGE_DIRECTORY_ENTRY_IMPORT, &size);
        # if (pImportDesc == None):
        #     return
        # # 查找记录,看看有没有我们想要的DLL
        # for (; pImportDesc->Name; pImportDesc++):
        #
        #     pszDllName = (LPSTR)((PBYTE)hModCallerModule + pImportDesc->Name)
        #     if (lstrcmpiA(pszDllName, pszCalleeModuleName) == 0):
        #         break
        #
        # if (pImportDesc->Name == None):
        #     return
        #
        # # 寻找我们想要的函数
        # PIMAGE_THUNK_DATA pThunk =
        #     (PIMAGE_THUNK_DATA)((PBYTE)hModCallerModule + pImportDesc->FirstThunk) #IAT
        # for (; pThunk->u1.Function; pThunk++):
        #
        #     # ppfn记录了与IAT表项相应的函数的地址
        #     PROC * ppfn = (PROC *)&pThunk->u1.Function;
        #     if (*ppfn == pfnOriginApiAddress):
        #         # 如果地址相同，也就是找到了我们想要的函数，进行改写，将其指向我们所定义的函数
        #         WriteProcessMemory(GetCurrentProcess(), ppfn, &(pfnDummyFuncAddress),
        #             sizeof(pfnDummyFuncAddress), None);
        #         return



    hook_id = InstallHook(True)

    # Register to remove the hook when the interpreter exits. Unfortunately a
    # try/finally block doesn't seem to work here.
    atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)

    while True:
        msg = win32gui.GetMessage(None, 0, 0)
        win32gui.TranslateMessage(byref(msg))
        win32gui.DispatchMessage(byref(msg))


if __name__ == '__main__':
    # listen()
    mInfo = MEMORY_BASIC_INFORMATION()
    windll.kernel32.SetLastError(10000)
    # 原型：VirtualQuery(HookOneAPI, byref(mInfo), sizeof(mInfo));
    result = windll.kernel32.VirtualQuery(addressof(HookOneAPI), byref(mInfo), byref(mInfo))

    hModHookDLL = mInfo.AllocationBase

    hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, 0)
    # MODULEENTRY32:描述了一个被指定进程所应用的模块的struct
    me = sizeof(MODULEENTRY32)
    bOk = Module32First(hModuleSnap, pointer(me))

    while (bOk):
        global PROGMainBase
        PROGMainBase = False

        if (me.hModule != hModHookDLL):
            hModCallerModule = me.hModule  # 赋值
            # me.hModule:指向当前被挂钩进程的每一个模块
            HookOneAPI(pszCalleeModuleName, pfnOriginApiAddress,
                       pfnDummyFuncAddress, hModCallerModule)

        bOk = Module32Next(hModuleSnap, pointer(me))
    else:
        CloseHandle(hModuleSnap)