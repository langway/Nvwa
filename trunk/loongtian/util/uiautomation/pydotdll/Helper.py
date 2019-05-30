# coding:utf-8

import sys
import os
import ctypes
import getopt


# WinNT.h
SE_DEBUG_PRIVILEGE = 0x14
PAGE_READWRITE = 0x04
VIRTUAL_MEM = (0x1000 | 0x2000)
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

# Inits
Kernel32 = ctypes.windll.Kernel32
Psapi = ctypes.windll.Psapi
Ntdll = ctypes.windll.Ntdll
Ntdll.RtlAdjustPrivilege(SE_DEBUG_PRIVILEGE, True, False, ctypes.byref(ctypes.c_ulong()))

def Inject(taget, dll):
    def _Inject(hProcs):
        buf = Kernel32.VirtualAllocEx(hProcs, 0, len(dll), VIRTUAL_MEM, PAGE_READWRITE)
        Kernel32.WriteProcessMemory(hProcs, buf, dll, len(dll), ctypes.byref(ctypes.c_ulong()))
        hLib = Kernel32.GetProcAddress(Kernel32._handle, "LoadLibraryA")
        r_tid = ctypes.c_ulong()
        Kernel32.CreateRemoteThread(hProcs, None, 0, hLib, buf, 0, ctypes.byref(r_tid))
        return (r_tid and True or False)

    dll = os.path.abspath(dll)
    try: taget=int(taget)
    except: pass

    if isinstance(taget, int):
        hProcs = Kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, taget)
        if _Inject(hProcs):
            print 'Inject Pid(%d) Success !' % target
        Kernel32.CloseHandle(hProcs)
    else:
        ProcsTotal = ctypes.c_ulong()
        ProcsIDs = (ctypes.c_ulong*1024)()
        ProcsName = (ctypes.c_wchar*1024)()
        Psapi.EnumProcesses(ProcsIDs, 1024*4, ctypes.byref(ProcsTotal))
        for idx in xrange(ProcsTotal.value/4):
            hProcs = Kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, ProcsIDs[idx])
            Psapi.GetModuleBaseNameW(hProcs, 0, ProcsName, 2*len(ProcsName))
            if ProcsName.value.lower() == taget:
                if _Inject(hProcs):
                    print 'Inject Pid(%d) Success !' % ProcsIDs[idx]
            Kernel32.CloseHandle(hProcs)

Usage = \
"""
Usage:
        --inject ProcsName/PID DllName/DllPath
                 IEXPLORE.exe pydotdll.dll
                 333 c:\pydotdll.dll
"""

if __name__ == '__main__':
    if len(sys.argv[1:]):
        try:
            opts, args = getopt.getopt(sys.argv[1:], '', ('inject'))
            if ('--inject', '') in opts:
                Inject(*args)
        except:
            print Usage
    else:
        print Usage