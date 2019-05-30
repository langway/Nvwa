# coding:utf-8
import win32process
import win32api
import win32con
import ctypes
import os, sys, string

TH32CS_SNAPPROCESS = 0x00000002


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_ulong),
                ("cntUsage", ctypes.c_ulong),
                ("th32ProcessID", ctypes.c_ulong),
                ("th32DefaultHeapID", ctypes.c_ulong),
                ("th32ModuleID", ctypes.c_ulong),
                ("cntThreads", ctypes.c_ulong),
                ("th32ParentProcessID", ctypes.c_ulong),
                ("pcPriClassBase", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("szExeFile", ctypes.c_char * 260)]


def getProcList():
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Process32First = ctypes.windll.kernel32.Process32First
    Process32Next = ctypes.windll.kernel32.Process32Next
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap, ctypes.byref(pe32)) == False:
        return
    while True:
        yield pe32
        if Process32Next(hProcessSnap, ctypes.byref(pe32)) == False:
            break
    CloseHandle(hProcessSnap)


def GetProcessModules(pid):
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    hModule = win32process.EnumProcessModules(handle)
    temp = []
    for i in hModule:
        temp.append([hex(i), debugfile(win32process.GetModuleFileNameEx(handle, i))])
    win32api.CloseHandle(handle)
    return temp


def CloseProcess(pid):
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    exitcode = win32process.GetExitCodeProcess(handle)
    win32api.TerminateProcess(handle, exitcode)
    win32api.CloseHandle(handle)


def debugfile(file):
    if (file.split("\\")[-1] == "smss.exe"):
        file = "C:\\WINDOWS\\system32\\smss.exe"
        return file
    elif (file.split("\\")[-1] == "csrss.exe"):
        file = "C:\\WINDOWS\\system32\\csrss.exe"
        return file
    elif (file.split("\\")[-1] == "winlogon.exe"):
        file = "C:\\WINDOWS\\system32\\winlogon.exe"
        return file
    else:
        return file


if __name__ == '__main__':
    # 调用procup.dll的enableDebugPriv函数对本进程提权
    # procupdll = ctypes.cdll.LoadLibrary("procup.dll")
    # if procupdll.enableDebugPriv() == 0:
    #     print "提权失败"

    count = 0
    procList = getProcList()
    for proc in procList:
        count += 1
        print("name=%s\tfather=%d\tid=%d" % (proc.szExeFile, proc.th32ParentProcessID, proc.th32ProcessID))
        try:
            TempGet = GetProcessModules(proc.th32ProcessID)
        except Exception, e:
            print "pid:%d can't read" % (proc.th32ProcessID)
            continue
        # TempGet[0][1].split("\\")[-1] 路径的最后一部分

        # """
        # 枚举进程调用所有模块
        for tempnum in range(0, len(TempGet)):
            try:
                print TempGet
            except Exception, e:
                print e
                # """

    print "进程数:%d" % (count)