#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__author__ = 'leon'

from ctypes import *
from ctypes.wintypes import *  # BOOL, HWND, RECT,HDC,LPCSTR
import binascii
import win32con
import os,platform
import ctypes
from ctypes import wintypes
# from ctypes.wintypes import *


LPTSTR = ctypes.POINTER(c_char)
LPBYTE = ctypes.POINTER(c_ubyte)
HANDLE = ctypes.c_void_p
LPDWORD = ctypes.POINTER(DWORD)
# LPTSTR = ctypes.POINTER(c_char)
LPCTSTR = ctypes.POINTER(ctypes.c_char)

# sss = u''
# nLPCWSTR = ctypes.cast(sss,ctypes.c_wchar_p)
nLPCWSTR = c_char_p
# nLPCWSTR = ctypes.POINTER(ctypes.c_wchar)
PHANDLE = ctypes.POINTER(HANDLE)

# LPBYTE = POINTER(c_ubyte)
PVOID = c_void_p
UNIT_PTR = c_ulong
SIZE_T = c_ulong
LPRECT = POINTER(RECT)

# const variable
# Establish rights and basic options needed for all process declartion / iteration

STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)
# PROCESS_ALL_ACCESS = 0x001F0FFF
# PROCESS_ALL_ACCESS = (0x000F0000L | 0x00100000L | 0xFFF)
PROCESS_VM_READ = 0x0010
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPTHREAD = 0x00000004


class __LUID(ctypes.Structure):
    """see:
http://msdn.microsoft.com/en-us/library/windows/desktop/aa379261(v=vs.85).aspx
"""
    _fields_ = [("LowPart", DWORD),
                ("HighPart", LONG), ]


LUID = __LUID
PLUID = POINTER(LUID)


class __LUID_AND_ATTRIBUTES(ctypes.Structure):
    """see:
http://msdn.microsoft.com/en-us/library/windows/desktop/aa379263(v=vs.85).aspx
"""
    _fields_ = [("Luid", LUID),
                ("Attributes", DWORD), ]


LUID_AND_ATTRIBUTES = __LUID_AND_ATTRIBUTES
PLUID_AND_ATTRIBUTES = POINTER(LUID_AND_ATTRIBUTES)


class __TOKEN_PRIVILEGES(ctypes.Structure):
    """see:
http://msdn.microsoft.com/en-us/library/windows/desktop/aa379630(v=vs.85).aspx
"""
    _fields_ = [("PrivilegeCount", DWORD),
                ("Privileges", LUID_AND_ATTRIBUTES), ]


TOKEN_PRIVILEGES = __TOKEN_PRIVILEGES
PTOKEN_PRIVILEGES = POINTER(TOKEN_PRIVILEGES)


class __STARTUPINFO(ctypes.Structure):
    """see:
http://msdn.microsoft.com/en-us/library/windows/desktop/ms686331(v=vs.85).aspx
"""
    _fields_ = [("cb", DWORD),
                ("lpReserved", LPTSTR),
                ("lpDesktop", LPTSTR),
                ("lpTitle", LPTSTR),
                ("dwX", DWORD),
                ("dwY", DWORD),
                ("dwXSize", DWORD),
                ("dwYSize", DWORD),
                ("dwXCountChars", DWORD),
                ("dwYCountChars", DWORD),
                ("dwFillAttribute", DWORD),
                ("dwFlags", DWORD),
                ("wShowWindow", WORD),
                ("cbReserved2", WORD),
                ("lpReserved2", LPBYTE),
                ("hStdInput", HANDLE),
                ("hStdOutput", HANDLE),
                ("hStdError", HANDLE), ]


STARTUPINFO = __STARTUPINFO
LPSTARTUPINFO = POINTER(STARTUPINFO)


class __PROCESS_INFORMATION(ctypes.Structure):
    """see:
http://msdn.microsoft.com/en-us/library/windows/desktop/ms684873(v=vs.85).aspx
"""
    _fields_ = [("hProcess", HANDLE),
                ("hThread", HANDLE),
                ("dwProcessId", DWORD),
                ("dwThreadId", DWORD), ]



PROCESS_INFORMATION = __PROCESS_INFORMATION
LPPROCESS_INFORMATION = POINTER(PROCESS_INFORMATION)


class __SYSTEM_MODULE_INFORMATION(ctypes.Structure):
    _fields_ = [("ModuleCount", ULONG),
                ("WhoCares", ctypes.c_void_p * 2),
                ("BaseAddress", ctypes.c_void_p),
                ("Size", ULONG),
                ("MoarStuff", ULONG),
                ("MoarMoar", USHORT),
                ("HeyThere", USHORT),
                ("Pwned", USHORT),
                ("W00t", USHORT),
                ("ImageName", ctypes.c_char * 256), ]


SYSTEM_MODULE_INFORMATION = __SYSTEM_MODULE_INFORMATION
PSYSTEM_MODULE_INFORMATION = POINTER(SYSTEM_MODULE_INFORMATION)


class __IMAGE_DOS_HEADER(ctypes.Structure):
    _fields_ = [("e_magic", WORD),
                ("e_cblp", WORD),
                ("e_cp", WORD),
                ("e_crlc", WORD),
                ("e_cparhdr", WORD),
                ("e_minalloc", WORD),
                ("e_maxalloc", WORD),
                ("e_ss", WORD),
                ("e_sp", WORD),
                ("e_csum", WORD),
                ("e_ip", WORD),
                ("e_cs", WORD),
                ("e_lfarlc", WORD),
                ("e_ovno", WORD),
                ("e_res", WORD * 4),
                ("e_oemid", WORD),
                ("e_oeminfo", WORD),
                ("e_res2", WORD * 10),
                ("e_lfanew", LONG), ]


IMAGE_DOS_HEADER = __IMAGE_DOS_HEADER
PIMAGES_DOS_HEADER = POINTER(IMAGE_DOS_HEADER)


class __IMAGE_FILE_HEADER(ctypes.Structure):
    _fields_ = [("Machine", WORD),
                ("NumberOfSections", WORD),
                ("TimeDateStamp", DWORD),
                ("PointerToSymbolTable", DWORD),
                ("NumberOfSymbols", DWORD),
                ("SizeOfOptionalHeader", WORD),
                ("Characteristics", WORD), ]


IMAGE_FILE_HEADER = __IMAGE_FILE_HEADER
PIMAGE_FILE_HEADER = POINTER(IMAGE_FILE_HEADER)


class __IMAGE_DATA_DIRECTORY(ctypes.Structure):
    _fields_ = [("VirtualAddress", DWORD),
                ("Size", DWORD), ]


IMAGE_DATA_DIRECTORY = __IMAGE_DATA_DIRECTORY
PIMAGE_DATA_DIRECTORY = POINTER(IMAGE_DATA_DIRECTORY)


class __IMAGE_OPTIONAL_HEADER(ctypes.Structure):
    _fields_ = [("Magic", WORD),
                ("MajorLinkerVersion", BYTE),
                ("MinorLinkerVersion", BYTE),
                ("SizeOfCode", DWORD),
                ("SizeOfInitializedData", DWORD),
                ("SizeOfUninitializedData", DWORD),
                ("AddressOfEntryPoint", DWORD),
                ("BaseOfCode", DWORD),
                ("BaseOfData", DWORD),
                ("ImageBase", DWORD),
                ("SectionAlignment", DWORD),
                ("FileAlignment", DWORD),
                ("MajorOperatingSystemVersion", WORD),
                ("MinorOperatingSystemVersion", WORD),
                ("MajorImageVersion", WORD),
                ("MinorImageVersion", WORD),
                ("MajorSubsystemVersion", WORD),
                ("MinorSubsystemVersion", WORD),
                ("Win32VersionValue", DWORD),
                ("SizeOfImage", DWORD),
                ("SizeOfHeaders", DWORD),
                ("CheckSum", DWORD),
                ("Subsystem", WORD),
                ("DllCharacteristics", WORD),
                ("SizeOfStackReserve", DWORD),
                ("SizeOfStackCommit", DWORD),
                ("SizeOfHeapReserve", DWORD),
                ("SizeOfHeapCommit", DWORD),
                ("LoaderFlags", DWORD),
                ("NumberOfRvaAndSizes", DWORD),
                ("DataDirectory", IMAGE_DATA_DIRECTORY * 16), ]


IMAGE_OPTIONAL_HEADER = __IMAGE_OPTIONAL_HEADER
PIMAGE_OPTIONAL_HEADER = POINTER(IMAGE_OPTIONAL_HEADER)


class __IMAGE_NT_HEADER(ctypes.Structure):
    _fields_ = [("Signature", DWORD),
                ("FileHeader", IMAGE_FILE_HEADER),
                ("OptionalHeader", IMAGE_OPTIONAL_HEADER), ]


IMAGE_NT_HEADER = __IMAGE_NT_HEADER
PIMAGE_NT_HEADER = POINTER(IMAGE_NT_HEADER)


class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("nLength", DWORD),
                ("lpSecurityDescriptor", LPVOID),
                ("bInheritHandle", BOOL)]


LPSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)
LPTHREAD_START_ROUTINE = LPVOID

class MEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [("BaseAddress", PVOID),
                ("AllocationBase", PVOID),
                ("AllocationProtect", DWORD),
                ("RegionSize", SIZE_T),
                ("State", DWORD),
                ("Protect", DWORD),
                ("Type", DWORD), ]


class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [("Length", DWORD),
                ("SecDescriptor", LPVOID),
                ("InheritHandle", BOOL)]


class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
        ('PrivilegeCount', c_uint),
        ('Luid', LUID),
        ('Attributes', c_uint)]



#
# processHandle = OpenProcess(0x10, False, pid)
#
# addr = 0x00000000FF900000  # Minesweeper.exe module base address
# data = ctypes.c_ulonglong()
# bytesRead = ctypes.c_ulonglong()
# result = ReadProcessMemory(processHandle, addr, ctypes.byref(data), ctypes.sizeof(data), ctypes.byref(bytesRead))
# e = GetLastError()
#
# print('result: {}, err code: {}, bytesRead: {}'.format(result,e,bytesRead.value))
# print('data: {:016X}h'.format(data.value))
#
# CloseHandle(processHandle)

# OpenProcessToken = windll.advapi32.OpenProcessToken
# OpenProcessToken.argtypes = [
#     c_int,      # HANDLE ProcessHandle
#     c_uint,     # DWORD DesiredAccess
#     c_void_p ]  # PHANDLE TokenHandle
# OpenProcessToken.restype = ErrorIfZero
#
# AdjustTokenPrivileges = windll.advapi32.AdjustTokenPrivileges
# AdjustTokenPrivileges.argtypes = [
#     c_int,      # HANDLE TokenHandle
#     c_int,      # BOOL DisableAllPrivileges
#     c_void_p,   # PTOKEN_PRIVILEGES NewState
#     c_uint,     # DWORD BufferLength
#     c_void_p,   # PTOKEN_PRIVILEGES PreviousState
#     c_void_p ]  # PDWORD ReturnLength
# AdjustTokenPrivileges.restype = ErrorIfZero
#
# LookupPrivilegeValue = windll.advapi32.LookupPrivilegeValueA
# LookupPrivilegeValue.argtypes = [
# c_char_p,   # LPCTSTR lpSystemName
# c_char_p,   # LPCTSTR lpName
# c_void_p ]  # PLUID lpLuid
# LookupPrivilegeValue.restype = ErrorIfZero
#
# access_token = c_int(0)
# privileges = TOKEN_PRIVILEGES()
#
# OpenProcessToken( GetCurrentProcess(), win32con.TOKEN_QUERY | win32con.TOKEN_ADJUST_PRIVILEGES, byref(access_token) )
# access_token = access_token.value
# LookupPrivilegeValue( None, "SeDebugPrivilege", byref(privileges.Luid) )
# privileges.PrivilegeCount = 1
# privileges.Attributes = 2
# AdjustTokenPrivileges(
#         access_token,
#         0,
#         byref(privileges),
#         0,
#         None,
#         None )
#
# CloseHandle( access_token )

class __PROCESSENTRY32(ctypes.Structure):
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

PROCESSENTRY32=__PROCESSENTRY32



#class MODULEENTRY32(Structure):
#    _fields_ = [ ( 'dwSize' , DWORD ) ,
#                ( 'th32ModuleID' , DWORD ),
#                ( 'th32ProcessID' , DWORD ),
#                ( 'GlblcntUsage' , DWORD ),
#                ( 'ProccntUsage' , DWORD ) ,
#                ( 'modBaseAddr' , LONG ) ,
#                ( 'modBaseSize' , DWORD ) ,
#                ( 'hModule' , HMODULE ) ,
#                ( 'szModule' , c_char * 256 ),
#                ( 'szExePath' , c_char * 260 ) ]


# class MODULEENTRY32(Structure):
#     _fields_ = [ ( 'dwSize' , c_long ) ,
#                 ( 'th32ModuleID' , c_long ),
#                 ( 'th32ProcessID' , c_long ),
#                 ( 'GlblcntUsage' , c_long ),
#                 ( 'ProccntUsage' , c_long ) ,
#                 ( 'modBaseAddr' , c_long ) ,
#                 ( 'modBaseSize' , c_long ) ,
#                 ( 'hModule' , c_void_p ) ,
#                 ( 'szModule' , c_char * 256 ),
#                 ( 'szExePath' , c_char * 260 ) ]



class __MODULEENTRY32(Structure):
    _fields_ = [('dwSize', DWORD),
                ('th32ModuleID', DWORD),
                ('th32ProcessID', DWORD),
                ('GlblcntUsage', DWORD),
                ('ProccntUsage', DWORD),
                ('modBaseAddr', POINTER(BYTE)),
                ('modBaseSize', DWORD),
                ('hModule', HMODULE),
                ('szModule', c_char * 256),
                ('szExePath', c_char * 260)]
MODULEENTRY32=__MODULEENTRY32




GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
OpenProcess = ctypes.windll.kernel32.OpenProcess
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
OpenProcess.restype = HANDLE
WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [HANDLE, LPCVOID, LPVOID, ctypes.c_size_t,
                              ctypes.POINTER(ctypes.c_size_t)]
ReadProcessMemory.restype = BOOL
memcpy = ctypes.cdll.msvcrt.memcpy

GetLastError = ctypes.windll.kernel32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = DWORD

CloseHandle = ctypes.windll.kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL

CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
Process32First = ctypes.windll.kernel32.Process32First
Process32Next = ctypes.windll.kernel32.Process32Next
Module32First = ctypes.windll.kernel32.Module32First
Module32Next = ctypes.windll.kernel32.Module32Next

ImageDirectoryEntryToData=ctypes.windll.imagehlp.ImageDirectoryEntryToData

def getProcPid(procName):
    """
    根据进程名取进程的pid
    :param procName: 进程名
    :return:
    """

    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap, ctypes.byref(pe32)) == False:
        return
    if pe32.szExeFile == procName:
        CloseHandle(hProcessSnap)
        return pe32.th32ProcessID

    while True:
        # yield pe32 #save the pe32
        if Process32Next(hProcessSnap, ctypes.byref(pe32)) == False:
            break
        if pe32.szExeFile == procName:
            CloseHandle(hProcessSnap)
            return pe32.th32ProcessID

    CloseHandle(hProcessSnap)

def launch(path_to_exe):
    """
    运行程序
    :param path_to_exe: 程序所在的路径
    :return: 进程pid
    """
    CREATE_NEW_CONSOLE = 0x00000010
    CREATE_PRESERVE_CODE_AUTHZ_LEVEL = 0x02000000

    startupinfo = STARTUPINFO()
    process_information = PROCESS_INFORMATION()
    security_attributes = SECURITY_ATTRIBUTES()

    startupinfo.dwFlags = 0x1
    startupinfo.wShowWindow = 0x0

    startupinfo.cb = sizeof(startupinfo)
    security_attributes.Length = sizeof(security_attributes)
    security_attributes.SecDescriptior = None
    security_attributes.InheritHandle = True

    if windll.kernel32.CreateProcessA(path_to_exe,
                                      None,
                                      byref(security_attributes),
                                      byref(security_attributes),
                                      True,
                                      CREATE_PRESERVE_CODE_AUTHZ_LEVEL,
                                      None,
                                      None,
                                      byref(startupinfo),
                                      byref(process_information)):

        pid = process_information.dwProcessId
        print "Success: CreateProcess - ", path_to_exe
    else:
        pid = None
        print "Failed: Create Process - Error code: ", windll.kernel32.GetLastError()

    return pid


def get_handle(pid):
    """
    取得进程的句柄
    :param pid: 进程的pid
    :return:
    """

    h_process = windll.kernel32.OpenProcess(PROCESS_VM_READ, False, pid)
    if h_process:
        print ("Success: Got Handle - PID:" + str(pid))

        return h_process
    else:
        print ("Failed: Get Handle - Error code: ", windll.kernel32.GetLastError())
        windll.kernel32.SetLastError(10000)


def read_memory(h_process, address):
    # buffer = c_char_p("The data goes here")
    # bufferSize = len(buffer.value)
    bufferSize = 32
    buffer = create_string_buffer(bufferSize)
    bytesRead = c_ulong(0)
    if windll.kernel32.ReadProcessMemory(h_process, address, buffer, bufferSize, byref(bytesRead)):
        print ("Success: Read Memory - ", buffer.value)
    else:
        print "Failed: Read Memory - Error Code: ", windll.kernel32.GetLastError()
        windll.kernel32.CloseHandle(h_process)
        windll.kernel32.SetLastError(10000)

    return buffer


def write_memory(h_process, address, data):
    count = c_ulong(0)
    length = len(data)
    c_data = c_char_p(data[count.value:])
    null = c_int(0)
    if not windll.kernel32.WriteProcessMemory(h_process, address, c_data, length, byref(count)):
        print  "Failed: Write Memory - Error Code: ", windll.kernel32.GetLastError()
        windll.kernel32.SetLastError(10000)
    else:
        return False


def virtual_query(address):
    basic_memory_info = MEMORY_BASIC_INFORMATION()
    windll.kernel32.SetLastError(10000)
    result = windll.kernel32.VirtualQuery(address, byref(basic_memory_info), byref(basic_memory_info))
    if result:
        return True
    else:
        print  "Failed: Virtual Query - Error Code: ", windll.kernel32.GetLastError()


class Process():
    """This class can be used for dll or shellcode injection.
Process(pid=pid)
This will attach to process with pid=pid assuming
you have proper privileges

Process(pe=path)
Starts the executable at path

self.inject(dllpath)
Injects dll at dllpath

self.injectshellcode(shellcode)
Injects raw shellcode in the string shellcode

self.terminate(code)
This will terminate the process in use regardless of where it was
started from. code is the exit code"""

    def __init__(self, pid=None, pe=None, handle=None):
        self.kernel32 = ctypes.windll.kernel32
        self.SE_DEBUG_NAME = "SeDebugPrivilege"
        self.TOKEN_ADJUST_PRIVILEGES = 0x20
        self.SE_PRIVILEGE_ENABLED = 0x00000002
        self.request_debug_privileges()

        if pid:  # attach to current file
            self.kernel32.OpenProcess.restype = HANDLE
            self.kernel32.OpenProcess.argtypes = [DWORD,
                                                  BOOL,
                                                  DWORD]

            result = self.handle = self.kernel32.OpenProcess(
                PROCESS_ALL_ACCESS,
                False,
                pid
            )
            self.get_last_error("OpenProcess", result)
            self.pid = pid
        elif pe:  # create new process
            startupinfo = STARTUPINFO()
            process_information = PROCESS_INFORMATION()
            startupinfo.dwFlags = 0x1
            startupinfo.wShowWindow = 0x0
            startupinfo.cb = ctypes.sizeof(startupinfo)
            self.kernel32.CreateProcessA.restype = BOOL
            self.kernel32.CreateProcessA.argtypes = [LPCSTR,
                                                     LPTSTR,
                                                     LPSECURITY_ATTRIBUTES,
                                                     LPSECURITY_ATTRIBUTES,
                                                     BOOL,
                                                     DWORD,
                                                     LPVOID,
                                                     LPCTSTR,
                                                     LPSTARTUPINFO,
                                                     LPPROCESS_INFORMATION]
            result = self.kernel32.CreateProcessA(
                pe,
                None,
                None,
                None,
                True,
                0,
                None,
                None,
                ctypes.byref(startupinfo),
                ctypes.byref(process_information)
            )
            self.get_last_error("CreateProcessA", result)
            if result == 0:
                print "CreateProcessA Failed!"
                return None
            self.handle = process_information.hProcess
            self.pid = process_information.dwProcessId
        elif handle:
            self.handle = handle
            self.pid = None
        else:
            return None

        self.arch = platform.architecture()[0][:2]
        if self.arch == 32:
            self.addrlen = 4
        else:
            self.addrlen = 8

    def get_last_error(self, desc, val):
        return  # Comment out the return to see return and error values
        print ("{0}=0x{1}, GetCurrentError=0x{2} ({3})".format (desc, val, self.kernel32.GetLastError(), self.kernel32.GetLastError()))

    def request_debug_privileges(self):
        """Adds SeDebugPrivilege to current process for various needs"""
        privs = LUID()
        ctypes.windll.advapi32.LookupPrivilegeValueA.restype = BOOL
        ctypes.windll.advapi32.LookupPrivilegeValueA.argtypes = [LPCTSTR,
                                                                 LPCTSTR,
                                                                 PLUID]
        result = ctypes.windll.advapi32.LookupPrivilegeValueA(
            None,
            self.SE_DEBUG_NAME,
            ctypes.byref(privs)
        )
        self.get_last_error("LookupPrivilegeValueA", result)
        token = TOKEN_PRIVILEGES(
            1,
            LUID_AND_ATTRIBUTES(
                privs,
                self.SE_PRIVILEGE_ENABLED
            )
        )
        hToken = HANDLE()
        ctypes.windll.advapi32.OpenProcessToken.restype = BOOL
        ctypes.windll.advapi32.OpenProcessToken.argtypes = [HANDLE,
                                                            DWORD,
                                                            PHANDLE]
        result = ctypes.windll.advapi32.OpenProcessToken(
            HANDLE(self.kernel32.GetCurrentProcess()),
            self.TOKEN_ADJUST_PRIVILEGES,
            ctypes.byref(hToken)
        )
        self.get_last_error("OpenProcessToken", result)
        ctypes.windll.advapi32.AdjustTokenPrivileges.restype = BOOL
        ctypes.windll.advapi32.AdjustTokenPrivileges.argtypes = [HANDLE,
                                                                 BOOL,
                                                                 PTOKEN_PRIVILEGES,
                                                                 DWORD,
                                                                 PTOKEN_PRIVILEGES,
                                                                 LPDWORD]
        result = ctypes.windll.advapi32.AdjustTokenPrivileges(
            hToken,
            False,
            ctypes.byref(token),
            0x0,
            None,
            None
        )
        self.get_last_error("AdjustTokenPrivileges", result)

        ctypes.windll.kernel32.CloseHandle.restype = BOOL
        ctypes.windll.kernel32.CloseHandle.argtypes = [HANDLE]
        result = ctypes.windll.kernel32.CloseHandle(hToken)
        self.get_last_error("CloseHandle", result)

    def inject(self, dllpath):
        """This function injects dlls the smart way
specifying stack rather than pushing and calling"""
        dllpath = os.path.abspath(dllpath)

        self.kernel32.GetModuleHandleA.restype = HANDLE
        self.kernel32.GetModuleHandleA.argtypes = [LPCTSTR]
        ModuleHandle = self.kernel32.GetModuleHandleA("kernel32.dll")
        self.get_last_error("GetModuleHandle", ModuleHandle)

        self.kernel32.GetProcAddress.restype = LPVOID
        self.kernel32.GetProcAddress.argtypes = [HANDLE, LPCSTR]
        LoadLibraryA = self.kernel32.GetProcAddress(
            HANDLE(ModuleHandle),
            "LoadLibraryA")
        self.get_last_error("GetProcAddress", LoadLibraryA)

        self.kernel32.VirtualAllocEx.restype = LPVOID
        self.kernel32.VirtualAllocEx.argtypes = [HANDLE,
                                                 LPVOID,
                                                 ctypes.c_size_t,
                                                 DWORD,
                                                 DWORD]
        RemotePage = self.kernel32.VirtualAllocEx(
            self.handle,
            None,
            len(dllpath) + 1,
            0x1000,  # MEM_COMMIT
            0x40  # PAGE_EXECUTE_READWRITE
        )
        self.get_last_error("VirtualAllocEx", RemotePage)

        self.kernel32.WriteProcessMemory.restype = BOOL
        self.kernel32.WriteProcessMemory.argtypes = [HANDLE,
                                                     LPVOID,
                                                     LPCVOID,
                                                     ctypes.c_size_t,
                                                     ctypes.POINTER(ctypes.c_size_t)]
        result = self.kernel32.WriteProcessMemory(
            self.handle,
            RemotePage,
            dllpath,
            len(dllpath),
            None
        )
        self.get_last_error("WriteProcessMemory", result)

        self.kernel32.CreateRemoteThread.restype = HANDLE
        self.kernel32.CreateRemoteThread.argtypes = [HANDLE,
                                                     LPSECURITY_ATTRIBUTES,
                                                     ctypes.c_size_t,
                                                     LPTHREAD_START_ROUTINE,
                                                     LPVOID,
                                                     DWORD,
                                                     LPVOID]
        RemoteThread = self.kernel32.CreateRemoteThread(
            self.handle,
            None,
            0,
            LoadLibraryA,
            RemotePage,
            0,
            None
        )
        self.get_last_error("CreateRemoteThread", RemoteThread)

        self.kernel32.WaitForSingleObject.restype = DWORD
        self.kernel32.WaitForSingleObject.argtypes = [HANDLE, DWORD]
        # Wait 10 seconds then barrel on...
        result = self.kernel32.WaitForSingleObject(
            RemoteThread,
            10 * 1000  # 10 seconds.  -1 for infinite
        )
        self.get_last_error("WaitForSingleObject", result)

        exitcode = DWORD(0)
        self.kernel32.GetExitCodeThread.restype = BOOL
        self.kernel32.GetExitCodeThread.argtypes = [HANDLE, LPDWORD]
        result = self.kernel32.GetExitCodeThread(
            RemoteThread,
            ctypes.byref(exitcode)
        )
        self.get_last_error("GetExitCodeThread", result)
        # print "exitcode = %s" % str(exitcode)

        self.kernel32.VirtualFreeEx.restype = BOOL
        self.kernel32.VirtualFreeEx.argtypes = [HANDLE,
                                                LPVOID,
                                                ctypes.c_size_t,
                                                DWORD]
        result = self.kernel32.VirtualFreeEx(
            self.handle,
            RemotePage,
            0,  # Size.  Must be 0 for MEM_RELEASE
            0x8000  # MEM_RELEASE
        )
        self.get_last_error("VirtualFreeEx", result)
        return exitcode.value

    def injectshellcode(self, shellcode):
        """This function merely executes what it is given"""
        self.kernel32.VirtualAllocEx.restype = LPVOID
        self.kernel32.VirtualAllocEx.argtypes = [HANDLE,
                                                 LPVOID,
                                                 ctypes.c_size_t,
                                                 DWORD,
                                                 DWORD]
        shellcodeaddress = self.kernel32.VirtualAllocEx(
            self.handle,
            None,
            len(shellcode),
            0x1000,  # MEM_COMMIT
            0x40  # PAGE_EXECUTE_READWRITE
        )
        self.get_last_error("VirtualAllocEx", shellcodeaddress)

        self.kernel32.WriteProcessMemory.restype = BOOL
        self.kernel32.WriteProcessMemory.argtypes = [HANDLE,
                                                     LPVOID,
                                                     LPCVOID,
                                                     ctypes.c_size_t,
                                                     ctypes.POINTER(ctypes.c_size_t)]
        result = self.kernel32.WriteProcessMemory(
            self.handle,
            shellcodeaddress,
            shellcode,
            len(shellcode),
            None
        )
        self.get_last_error("WriteProcessMemory", result)

        self.kernel32.CreateRemoteThread.restype = HANDLE
        self.kernel32.CreateRemoteThread.argtypes = [HANDLE,
                                                     LPSECURITY_ATTRIBUTES,
                                                     ctypes.c_size_t,
                                                     LPTHREAD_START_ROUTINE,
                                                     LPVOID,
                                                     DWORD,
                                                     LPVOID]
        thread = self.kernel32.CreateRemoteThread(
            self.handle,
            None,
            0,
            shellcodeaddress,
            None,
            0,
            None
        )
        self.get_last_error("CreateRemoteThread", thread)

    def injectshellcodefromfile(self, file, bzipd=False):
        """This function merely executes what it is given as a raw file"""
        fh = open(file, 'rb')
        shellcode = fh.read()
        fh.close()
        if bzipd:
            import bz2
            shellcode = bz2.decompress(shellcode)
        self.injectshellcode(shellcode)

    def terminate(self, code=0):
        """This function terminates the process from the current handle"""
        self.kernel32.TerminateProcess.restype = BOOL
        self.kernel32.TerminateProcess.argtypes = [HANDLE, UINT]
        result = self.kernel32.TerminateProcess(
            self.handle,
            code
        )
        self.get_last_error("TerminateProcess", result)
        self.kernel32.CloseHandle(self.handle)



if __name__ == "__main__":
    pid = launch(r"C:\windows\system32\notepad.exe")
    print(pid)
    h_process = get_handle(pid)
    print(h_process)
    # main.write_memory(address, "\x61")
    while 1:
        print '1 to enter an address'
        print '2 to virtual query address'
        print '3 to read address'
        choice = raw_input('Choice: ')
        if choice == '1':
            address = raw_input('Enter and address: ')
        if choice == '2':
            virtual_query(address)
        if choice == '3':
            read_memory(h_process, address)
