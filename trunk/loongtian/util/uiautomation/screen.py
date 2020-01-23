#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'leon'

import struct
import time
import win32api
import win32gui

import commctrl
from PIL import ImageGrab

from loongtian.util.debuger.hookHelper import *
from pywinauto.controls.common_controls import ListViewWrapper
from loongtian.util.log.logger import logger
# from win32con import PAGE_READWRITE, MEM_COMMIT, MEM_RESERVE, MEM_RELEASE,\
#     PROCESS_ALL_ACCESS
# from commctrl import LVM_GETITEMTEXT, LVM_GETITEMCOUNT,LVM_GETHEADER



class HandleInvalidateException(Exception):
    """
    句柄不合理时抛出的错误。
    """
    pass

def _validate_handle(handle,throw_excption=True):
    """
    检验句柄的合理性，例如不能为0等
    :param handle:
    :param throw_excption:
    :return:
    """
    if handle<=0 :
        if throw_excption:
            raise HandleInvalidateException("句柄不合理，handle为:"+str(handle))
        else:
            return False
    return True

def _WindowsCallback(hwnd, extra):
    """
    取得符合条件的所有窗体的句柄
    :param hwnd:
    :param extra:tuple，包括：hwnds ,class_name,title，
    hwnds：所有窗体的句柄-list
    class_name：指定窗体的类型，如果不指定，则查找所有窗体
    title：指定窗体的标题（可以是一部分），如果不指定，则查找所有窗体
    owner_parent_handle :所有者或父窗口的句柄
    :return:
    """
    hwnds ,class_name,title,owner_parent_handle,shouldWindowEnabled,shouldWindowVisible= extra
    # 去掉下面这句就所有都输出了，但是我不需要那么多
    if not win32gui.IsWindow(hwnd):
        return
    if shouldWindowEnabled and not IsWindowEnabled(hwnd):
        return
    if shouldWindowVisible and not IsWindowVisible(hwnd):
        return

    # titles.add(t)
    class_name_right=True
    title_right=True
    owner_parent_handle_right=True

    if class_name:
        c=get_class_name(hwnd)
        if c:
            c= c.decode('gbk')
            if not c==class_name:
                class_name_right=False
        else:
            class_name_right = False

    if not class_name_right:
        return

    if title:
        t = win32gui.GetWindowText(hwnd)
        if t:
            t = t.decode('gbk')
            if title in t:
                title_right = True
            else:
                title_right = False
        else:
            title_right = False

    if not title_right:
        return

    if owner_parent_handle :
        o = get_owner_parent_handle(hwnd)
        if o:
            if not o == owner_parent_handle:
                owner_parent_handle_right = False
        else:
            owner_parent_handle_right = False

    if owner_parent_handle_right:
        hwnds.append(hwnd)


def time_now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def IsWindow(hwnd):
    """
    判断是否窗体。
    :param hwnd:
    :return:
    """
    return win32gui.IsWindow(hwnd)

def IsWindowEnabled(hwnd):
    """
    判断窗体是否可用。
    :param hwnd:
    :return:
    """
    return win32gui.IsWindowEnabled(hwnd)

def waitWindowVisible(hwnd,counter=-1,sleepTime=1000):
    """
    等待窗体是否可见。
    :param hwnd:
    :return:
    """
    if counter<0:
        while True:
            if not IsWindowVisible(hwnd):
                # 继续休息，以便窗体显现
                sleep(sleepTime)
            else:
                break
    else:
        while counter>0:
            if not IsWindowVisible(hwnd):
                # 继续休息，以便窗体显现
                sleep(sleepTime)
            counter-=1

    return True

def IsWindowVisible(hwnd):
    """
    判断窗体是否可见。
    :param hwnd:
    :return:
    """

    return win32gui.IsWindowVisible(hwnd)


def get_all_windows(class_name=None, title=None, owner_parent_handle=None,
                    shouldWindowEnabled=False, shouldWindowVisible=False):
    """
    取得所有指定类型的窗体的句柄。
    :param class_name :指定窗体的类型，如果不指定，则查找所有窗体
    :param title :指定窗体的标题（可以是一部分），如果不指定，则查找所有窗体
    :param owner_parent_handle :所有者或父窗口的句柄。
    :param shouldWindowEnabled:是否需要判断窗体可用。
    :param shouldWindowVisible:是否需要判断窗体可见。
    :return:
    """
    hwnds = []

    win32gui.EnumWindows(_WindowsCallback, (hwnds, class_name, title, owner_parent_handle, shouldWindowEnabled, shouldWindowVisible))
    return hwnds

def get_all_child_windows(parent_handle):
    hwnds = []

    win32gui.EnumChildWindows(parent_handle,_WindowsCallback,(hwnds,None,None,None,True,False))
    return hwnds


def get_all_texts_by_handles(hwnds):
    """
    取得所有窗体的标题（句柄-标题的字典）
    :param hwnds:
    :return:
    """
    if len(hwnds) == 0:
        return None
    titles = {}
    for hwnd in hwnds:
        t = win32gui.GetWindowText(hwnd)
        if t:
            t = t.decode('gbk')
            titles[hwnd] = t

    return titles


def p_sub_handle(phandle):
    """输出phandle的所有子控件"""
    handle = -1
    while handle !=0 :
        if handle == -1:
            handle = 0
        handle = win32gui.FindWindowEx(phandle, handle, None, None)
        if handle != 0:
            print (win32gui.GetClassName(handle))

# def get_handle_by_text(text):
#     """
#     根据窗体的标题取得对应的句柄(完全匹配)
#     :param text: 窗体的标题
#     :return:
#     """
#     return win32gui.FindWindow(None, text)

def get_handle_by_classname(classname):
    """
    根据窗体的类名取得对应的句柄(完全匹配)
    :param classname: 类名
    :return:
    """
    return win32gui.FindWindow(classname,None)

def get_handle_by_classname_and_text(classname,text):
    """
    根据窗体的类名和标题取得对应的句柄(完全匹配)
    :param classname: 类名
    :param text: 窗体的标题
    :return:
    """
    return win32gui.FindWindow(classname,text)


def get_handle_by_parent_and_classname(parent_handle,classname):
    """
    根据父对象的句柄以及类名，取得对应的句柄(返回第一个)
    :param parent_handle: 父对象的句柄
    :param classname: 类名
    :return:
    """
    return win32gui.FindWindowEx(parent_handle,0,classname,None)



def get_handles_by_keywords_in_title(keywords):
    """
    根据窗体的标题中的关键字取得对应的句柄(部分匹配)
    :param keywords: 窗体的标题中的关键字
    :return:
    """
    if keywords == None:
        return

    if not type(keywords) is str:
        raise AttributeError("keywords: 窗体的标题中的关键字必须是unicode字符")

    handles = get_all_windows()
    texts = get_all_texts_by_handles(handles)
    results = {}
    for k, v in texts.items():
        if keywords in v:
            results[k] = v

    return results

def get_owner_parent_handle(handle):
    """
    查找所有者窗口句柄，如果没有，则返回父窗口句柄
    :param handle:
    :return:
    """
    owner_parent_handle=win32gui.GetWindow(handle,win32con.GW_OWNER)

    if not owner_parent_handle:
        owner_parent_handle=win32gui.GetParent(handle)

    return owner_parent_handle

def grab_windows(hwnd):
    """
    截取指定句柄的窗体
    :param hwnd:
    :return:
    """
    _validate_handle(hwnd)
    active_window(hwnd)# 强行显示界面后才好截图

    #  裁剪得到全图
    win_rect = win32gui.GetWindowRect(hwnd)
    src_image = ImageGrab.grab(win_rect)
    # src_image = ImageGrab.grab((game_rect[0] + 9, game_rect[1] + 190, game_rect[2] - 9, game_rect[1] + 190 + 450))
    # src_image.show()
    # src_image=src_image.convert("rgba")
    return src_image


#
# import time,Image
# import os, win32gui, win32ui, win32con, win32api
# def window_capture(dpath):
#     """''
#     截屏函数,调用方法window_capture('d:\\') ,参数为指定保存的目录
#     返回图片文件名,文件名格式:日期.jpg 如:2009328224853.jpg
#     """
#     hwnd = 0
#     hwndDC = win32gui.GetWindowDC(hwnd)
#     mfcDC=win32ui.CreateDCFromHandle(hwndDC)
#     saveDC=mfcDC.CreateCompatibleDC()
#     saveBitMap = win32ui.CreateBitmap()
#     MoniterDev=win32api.EnumDisplayMonitors(None,None)
#     w = MoniterDev[0][2][2]
#     h = MoniterDev[0][2][3]
#     #print w,h　　　#图片大小
#     saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
#     saveDC.SelectObject(saveBitMap)
#     saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY)
#     cc=time.gmtime()
#     bmpname=str(cc[0])+str(cc[1])+str(cc[2])+str(cc[3]+8)+str(cc[4])+str(cc[5])+'.bmp'
#     saveBitMap.SaveBitmapFile(saveDC, bmpname)
#     Image.open(bmpname).save(bmpname[:-4]+".jpg")
#     os.remove(bmpname)
#     jpgname=bmpname[:-4]+'.jpg'
#     djpgname=dpath+jpgname
#     copy_command = "move %s %s" % (jpgname, djpgname)
#     os.popen(copy_command)
#     return bmpname[:-4]+'.jpg'
# #调用截屏函数
# window_capture('d:\\')

def get_text_by_handle2(handle):
    """
        取得指定控件的文本（win32gui.GetWindowText模式）
        使用第一种get_text_by_handle可能取不出来，这时需使用get_text_by_handle2
        注意：需在使用前进行反复试验，以确保能够得到正确结果！
        :param handle:
        :return:
    """
    _validate_handle(handle)

    text=win32gui.GetWindowText(handle).decode("gbk")
    return text

def get_text_by_handle(handle):
    """
    取得指定控件的文本（使用win32gui.SendMessage模式）
    使用第一种get_text_by_handle可能取不出来，这时需使用get_text_by_handle2
    注意：需在使用前进行反复试验，以确保能够得到正确结果！
    :param handle:
    :return:
    """
    _validate_handle(handle)

    len = win32gui.SendMessage(handle, win32con.WM_GETTEXTLENGTH) + 1  # 获取edit控件文本长度
    buffer =  ctypes.create_string_buffer(len) #win32gui.PyMakeBuffer(len)
    win32gui.SendMessage(handle, win32con.WM_GETTEXT, len, buffer)  # 读取文本
    text = str(buffer[:len - 1]).decode("gbk")

    return text

# from ctypes import *
# import os
#
# class GetWord():
#
#     """封装 GetWord 3.3 的取词功能"""
#     def __init__(self):
#         root_path=os.path.split(os.path.realpath(__file__))[0]
#         self.icall = windll.LoadLibrary(root_path + '\\TextCapture\\ICall.dll')
#         self.icall.GetWordEnableCap(True)
#
#     def __del__(self):
#         hdll = windll.Kernel32.GetModuleHandleA('ICall.dll')
#         windll.Kernel32.FreeLibrary(hdll)
#     def getText(self,x,y):
#         """屏幕取词，返回坐标所指的一行文字，以及所指字符在行中的索引"""
#         MAX_OUTPUT_LEN = 1024
#         hrwnd = self.icall.GetRealWindow(x, y)
#         strtmp = create_unicode_buffer('\0' * MAX_OUTPUT_LEN)
#         i = c_int(-1)
#         ok = self.icall.GetWord(hrwnd, x, y, strtmp, MAX_OUTPUT_LEN, byref(i))
#         if ok:
#             return strtmp.value, i.value
#
# # GetWord=GetWord()

def get_handle_text(pHandle, class_name, lastHandle=None, index=0,position=0, getText=True):
    """
    根据类名，取得指定父控件中的子控件的句柄
    :param pHandle: 指定父控件的句柄
    :param class_name: 子控件的类名
    :param index:指定lastHandle之后第几个子控件
    :param getText:是否取得子控件文本
    :return:
    """
    try:
        if lastHandle is None:
            # 根据类名，取得当前父控件中的子控件的句柄（第一个）
            lastHandle = win32gui.FindWindowEx(pHandle, 0, class_name, None)
        while index > 0:  # 不断循环，直到取得之后（注意：是之后！）第index个子控件的句柄
            lastHandle = win32gui.FindWindowEx(pHandle, lastHandle, class_name, None)
            index -= 1
        if lastHandle <= 0:
            print ("未能取得界面中的{0}!".format(class_name))

        text = ""
        if getText:
            text = get_text_by_handle(lastHandle)
            # print (text)


        return [lastHandle,class_name, text,position]
    except Exception as e:
        print (str(e).decode("gbk"))


def get_idxSubHandle(pHandle, class_name, index=0, getText=True):
    """
    已知子窗口的窗体类名
    寻找第index号个同类型的兄弟窗口
    """
    if type(index) == int:
        if index < 0:
            return

        handle_text = get_handle_text(pHandle, class_name, None, index,0, getText)
        return [handle_text]

    elif type(index) is list:

        result = []
        lastHandle = None
        lastIndex = 0
        for i in index:
            if i < 0 or not type(i) == int:
                continue
            handle_text = get_handle_text(pHandle, class_name, lastHandle, i - lastIndex,i, getText)
            result.append(handle_text)
            lastHandle = handle_text[0]
            lastIndex = i

        return result




def get_subHandles(pHandle, winClassList):
    """
    循环寻找子窗口（控件）的句柄
    pHandle是祖父窗口的句柄
    winClassList是各个子窗口（控件）的class列表，父辈的list-index小于子辈
    直接这样调用即可：
    handle = find_subHandle(self.Mhandle, [("ComboBoxEx32", 1), ("ComboBox", 0), ("Edit", 0)])
    """
    assert type(winClassList) == list

    subHandles_text = []

    for i in range(len(winClassList)):
        class_name = winClassList[i][0]
        index = winClassList[i][1]
        if len(winClassList[i]) == 3:
            getText = winClassList[i][2]
        else:
            getText = True

        subHandle_texts = get_idxSubHandle(pHandle, class_name, index, getText)
        if len(subHandle_texts) > 0:
            subHandles_text.extend(subHandle_texts)

                # return find_subHandle(pHandle, winClassList[1:])
    return subHandles_text


def get_subHandle_in_path(pHandle, path):
    """
    递归寻找子窗口的句柄
    pHandle是祖父窗口的句柄
    path是各个子窗口的class列表,是查找路径，父辈的list-index小于子辈
    直接这样调用即可：
    handle = get_subHandle_in_path(Mhandle, [("ComboBoxEx32", 1), ("ComboBox", 0), ("Edit", 0)])
    """
    assert type(path) == list
    if len(path) == 1:
        return get_idxSubHandle(pHandle, path[0][0], path[0][1])
    else:
        pHandle = get_idxSubHandle(pHandle, path[0][0], path[0][1])
        return get_subHandle_in_path(pHandle[0][0], path[1:])


def get_class_name(handle,validate_handle=True):
    """
    根据窗体（控件）句柄取得类名称。
    :param handle:
    :return:
    """
    if validate_handle:
        _validate_handle(handle)
    # win32gui.ListView_SortItems()
    # win32gui.PyGetString()
    # win32api.

    return win32gui.GetClassName(handle)


# def set_text1(control_handle, text):
#     """
#     将文本设置到指定句柄的窗体（控件）（win32api.SetWindowText模式）
#     注意：需在使用前与其他同名函数进行反复试验，以确保能够得到正确结果！
#     :param control_handle:
#     :param text:
#     :return:
#     """
#     _validate_handle(control_handle)
#     text = str(text).encode("gbk")
#     return win32gui.SetWindowText(control_handle, text)

def set_text(control_handle, text):
    """
    将文本设置到指定句柄的窗体（控件）（win32api.SendMessage模式）
    注意：需在使用前与其他同名函数进行反复试验，以确保能够得到正确结果！
    :param control_handle:
    :param text:
    :return:
    """
    _validate_handle(control_handle)

    text=str(text).encode("gbk")
    message= win32api.SendMessage(control_handle, win32con.WM_SETTEXT, 0, text)
    # message=win32gui.SendMessage(control_handle, win32con.WM_SETTEXT, None, text)
    # win32api.Sleep(5)
    if message==0:
        print("----未能将文本设置到指定句柄的窗体（控件）！\r\n文本内容为："+text)
        return False
    elif message==1:
        print ("----文本设置成功！文本内容为："+text.decode("gbk"))
        return True


# def set_text3(control_handle, text):
#     """
#     将文本设置到指定句柄的窗体（控件）（虚拟键盘鼠标模式）
#     注意：需在使用前与其他同名函数进行反复试验，以确保能够得到正确结果！
#     :param control_handle:
#     :param text:
#     :return:
#     """
#     _validate_handle(control_handle)
#     # import win32ui
#
#     pass
# def set_text4(hwnd, control_handle, text):
#     # win=win32gui.FindWindow("TFrmKJDownOrder",None)
#     control_id=win32gui.GetDlgCtrlID(control_handle)
#     control=win32gui.GetDlgItem(hwnd,control_handle)
#     message2 = control.SendMessage(win32con.WM_SETTEXT,text)
#     # win32api.Sleep(10)
#     pass

def active_window(handle):
    """
    激活窗体，并显示到最前。
    :param handle:
    :return:
    """
    try:
        win32gui.ShowWindow(handle, win32con.SW_RESTORE)  # 强行显示界面
        # win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
        win32gui.EnableWindow(handle, True)
        win32gui.SetForegroundWindow(handle)  # 将窗口提到最前
    except:
        pass



def refresh_window(hwnd):
    """
    刷新窗体（控件）。
    :param hwnd:
    :return:
    """
    r=win32gui.InvalidateRect(hwnd, None, True)
    # print(r,time.time())
    r=win32gui.UpdateWindow(hwnd)
    # print(r,time.time())
    r=win32gui.RedrawWindow(hwnd,
                            None,
                            None,
                            win32con.RDW_FRAME|
                                win32con.RDW_INVALIDATE|
                                win32con.RDW_UPDATENOW|
                                win32con.RDW_ALLCHILDREN)

    # print(r,time.time())

def highlight_window(hwnd):
    """
    高亮窗口的函数
    :param hwnd:
    :return:
    """
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    windowDc = win32gui.GetWindowDC(hwnd)
    rectanglePen=None
    raise NotImplementedError("rectanglePen not defined!")
    if windowDc:
        prevPen = win32gui.SelectObject(windowDc, rectanglePen)
        prevBrush = win32gui.SelectObject(windowDc, win32gui.GetStockObject(win32con.HOLLOW_BRUSH))

        win32gui.Rectangle(windowDc, 0, 0, right - left, bottom - top)
        win32gui.SelectObject(windowDc, prevPen)
        win32gui.SelectObject(windowDc, prevBrush)
        win32gui.ReleaseDC(hwnd, windowDc)

def get_DC(hwnd):
    return win32gui.GetDC(hwnd)

def get_window_from_DC(hdc):
    return win32gui.WindowFromDC(hdc)


def close_window(handle):
    """
    关闭指定句柄的窗体
    :param handle: 指定句柄
    :return:
    """
    # win32gui.CloseWindow(handle)
    win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)

def get_menu_item(hwnd, subMenu_postion, menuItem_postion):
    """
    在窗体中，取得第n个子菜单下的从0开始，第m个菜单项的ID（MenuItemID）
    :param hwnd: 窗体的handle
    :param subMenu_postion: 第n个子菜单
    :param menuItem_postion: 从0开始，第m个菜单项
    :return:第m个菜单项的ID（MenuItemID）
    """
    # 获取窗口的菜单句柄。
    hd_menu = win32gui.GetMenu(hwnd)
    # 第n个子菜单
    hd_submenu = win32gui.GetSubMenu(hd_menu, subMenu_postion)
    # 从0开始，第m个菜单项的ID（MenuItemID）
    hd_menuid = win32gui.GetMenuItemID(hd_submenu, menuItem_postion)

    return hd_menuid

def sleep(time=20):
    """
    休眠指定的时间（毫秒）
    :param time:milli-seconds
    :return:
    """
    win32api.Sleep(time)


def get_listView_items(hwnd, column_index=-1):
    """
    从内存中读取指定的LV控件的文本内容。
    :param hwnd:
    :param column_index:
    :return:
    """
    lst = ListViewWrapper(hwnd)

    # 取得行数
    # num_rows =lst.item_count()
    # 取得列数
    num_column=lst.column_count()
    column_counter=num_column
    # time.sleep(5)
    # item=lst.item(0)
    # # item.select()
    # item.click()
    #
    # item.click(double=True)
    rows = []
    if column_index < 0:  # 取全部列
        current_row=[]

        for item in lst.items():
            if column_counter>0:
                current_row.append (item.text())
                column_counter-=1
            else:
                if current_row:
                    rows.append(current_row)
                column_counter = num_column-1
                current_row = []
                current_row.append(item.text())
        # 最后一行，直接添加
        if current_row:
            rows.append(current_row)
    return rows

def get_listView_rowIndex_by_items(hwnd, dict):
    """
    根据给定的第几列的内容dict，取得listView的第几行
    例如：根据第2列的“购销计划”为“S17093”，第5列的“价格”为“6803”，取得的行数
    :param hwnd:
    :param dict:
    :return:
    """
    rows = get_listView_items(hwnd)

    for i in range(len(rows)):
        row=rows[i]
        if not row:
            continue
        matched=True
        for j,text in dict.items():
            if not row[j]==text:
                matched=False
                break
        if matched:
            return i,row



def click_listView_row(hwnd,rowIndex, double=True,offset=8):
    """
    模拟鼠标单击ListView的某一行
    :param hwnd:listView的窗体句柄
    :param rowIndex: 行序号
    :param button: 鼠标左键或右键
    :param double: 是否双击
    :param where:where can be any one of "all", "icon", "text", "select", "check"
                    defaults to "text"
    :param pressed:
    :return:
    """
    lst = ListViewWrapper(hwnd)

    try:
        item = lst.item(rowIndex)
    except IndexError as ex:
        logger.exception(ex)
        return

    if item:
        mid_point=item.rectangle().mid_point()
        screen_point=win32gui.ClientToScreen(hwnd,(mid_point.x,mid_point.y))
        from loongtian.util.uiautomation.mouse_key_commond import mouse_move_dclick,mouse_move_click
        if double:
            mouse_move_dclick(screen_point[0],screen_point[1]+ offset)
        else:
            mouse_move_click(screen_point[0], screen_point[1] + offset)

def click_listView_row2(hwnd,rowIndex,button="left", double=False, where="text", pressed=""):
    """
    模拟鼠标单击ListView的某一行
    :param hwnd:listView的窗体句柄
    :param rowIndex: 行序号
    :param button: 鼠标左键或右键
    :param double: 是否双击
    :param where:where can be any one of "all", "icon", "text", "select", "check"
                    defaults to "text"
    :param pressed:
    :return:
    """
    lst = ListViewWrapper(hwnd)

    try:
        item = lst.item(rowIndex)
    except IndexError as ex:
        logger.exception(ex)
        return

    if item:
        item.select()
        item.click(button, double, where, pressed)



def get_listView_items2(hwnd, column_index=-1):
    """
    从内存中读取指定的LV控件的文本内容。
    :param hwnd:
    :param column_index:
    :return:
    """

    # Allocate virtual Memory inside target process
    pid = ctypes.create_string_buffer(4)
    p_pid = ctypes.addressof(pid)
    GetWindowThreadProcessId(hwnd, p_pid) # process owning the given hwnd
    # 打开并插入进程
    hProcHnd = OpenProcess(win32con.PROCESS_ALL_ACCESS, False, struct.unpack("i",pid)[0])
    # 申请代码的内存区, 返回申请到的虚拟内存首地址
    pLVI = VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    pBuffer = VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)

    # 取得列数
    header_handle=win32gui.SendMessage(hwnd, commctrl.LVM_GETHEADER)
    num_column=win32gui.SendMessage(header_handle, commctrl.HDM_GETITEMCOUNT)
    # 取得行数
    num_rows = win32gui.SendMessage(hwnd, commctrl.LVM_GETITEMCOUNT)
    item_texts = []

    # iterate items in the SysListView32 control
    for _row_index in range(num_rows):
        row_texts=[]
        if column_index < 0: # 取全部列
            current_row=[]
            for _column_index in range(num_column):
                text=__get_listview_item_by_columnindex(_column_index,_row_index,pBuffer,hProcHnd,pLVI,hwnd)
                current_row.append(text)
            row_texts.append(current_row)
        else: # 取指定列
            text = __get_listview_item_by_columnindex(column_index, _row_index, pBuffer, hProcHnd, pLVI, hwnd)
            row_texts.append(text)

        item_texts.append(row_texts)

    VirtualFreeEx(hProcHnd, pBuffer, 0, win32con.MEM_RELEASE)
    VirtualFreeEx(hProcHnd, pLVI, 0, win32con.MEM_RELEASE)
    win32api.CloseHandle(hProcHnd)
    return item_texts


def __get_listview_item_by_columnindex(column_index,row_index,pBuffer,hProcHnd,pLVI,hwnd):
    # Prepare an LVITEM record and write it to target process Memory
    lvitem_str = struct.pack('iiiiiiiii', *[0, 0, column_index, 0, 0, pBuffer, 4096, 0, 0])
    lvitem_buffer = ctypes.create_string_buffer(lvitem_str)
    copied = ctypes.create_string_buffer(4)
    p_copied = ctypes.addressof(copied)

    # 把数据写到vItem中
    # ·     hProcess：要写内存的进程句柄。
    # ·     lpBaseAddress：要写的内存起始地址。
    # ·     lpBuffer：写入值的地址。
    # ·     nSize：写入值的大小。
    # ·     lpNumberOfBytesWritten   ：实际写入的大小。
    WriteProcessMemory(hProcHnd, pLVI, ctypes.addressof(lvitem_buffer), ctypes.sizeof(lvitem_buffer), p_copied)

    # 发送LVM_GETITEMW消息给hwnd,将返回的结果写入pointer指向的内存空间
    win32gui.SendMessage(hwnd, commctrl.LVM_GETITEMTEXT, row_index, pLVI)
    target_buff = ctypes.create_string_buffer(4096)
    ReadProcessMemory(hProcHnd, pBuffer, ctypes.addressof(target_buff), 4096, p_copied)
    text = target_buff.value.decode("gbk")

    return text

class LVITEM(ctypes.Structure):
    _fields_ = [
        ('mask', c_uint32),
        ('iItem', c_int32),
        ('iSubItem', c_int32),
        ('state', c_uint32),
        ('stateMask', c_uint32),
        ('pszText', c_uint32),
        ('cchTextMax', c_int32),
        ('iImage', c_int32),
        ('lParam', c_uint64),
        ('iIndent', c_int32),
        ('iGroupId', c_int32),
        ('cColumns', c_uint32),
        ('puColumns', c_uint32),
        ('piColFmt', c_int32),
        ('iGroup', c_int32)
    ]
class LVITEMW(ctypes.Structure):
    _fields_ = [
        ('mask', c_uint32),
        ('iItem', c_int32),
        ('iSubItem', c_int32),
        ('state', c_uint32),
        ('stateMask', c_uint32),
        ('pszText', c_uint64),
        ('cchTextMax', c_int32),
        ('iImage', c_int32),
        ('lParam', c_uint64), # On 32 bit should be c_long
        ('iIndent', c_int32),
        ('iGroupId', c_int32),
        ('cColumns', c_uint32),
        ('puColumns', c_uint64),
        ('piColFmt', c_int64),
        ('iGroup', c_int32),
    ]

def set_listView_item_focused(hwnd, column_index,row_index):
    """
    从内存中读取指定的LV控件的文本内容。
    :param hwnd:
    :param column_index:
    :return:
    """

    # Allocate virtual Memory inside target process
    pid = ctypes.create_string_buffer(4)
    p_pid = ctypes.addressof(pid)
    GetWindowThreadProcessId(hwnd, p_pid) # process owning the given hwnd
    # 打开并插入进程
    hProcHnd = OpenProcess(win32con.PROCESS_ALL_ACCESS, False, struct.unpack("i",pid)[0])
    # 申请代码的内存区, 返回申请到的虚拟内存首地址
    pLVI = VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    pBuffer = VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)

    # Prepare an LVITEM record and write it to target process Memory
    lvitem_str = struct.pack('iiiiiiiii', *[0, 0, column_index, 0, 0, pBuffer, 4096, 0, 0])
    lvitem_buffer = ctypes.create_string_buffer(lvitem_str)
    copied = ctypes.create_string_buffer(4)
    p_copied = ctypes.addressof(copied)

    # 把数据写到vItem中
    # ·     hProcess：要写内存的进程句柄。
    # ·     lpBaseAddress：要写的内存起始地址。
    # ·     lpBuffer：写入值的地址。
    # ·     nSize：写入值的大小。
    # ·     lpNumberOfBytesWritten   ：实际写入的大小。
    WriteProcessMemory(hProcHnd, pLVI, ctypes.addressof(lvitem_buffer), ctypes.sizeof(lvitem_buffer), p_copied)

    # 发送LVM_GETITEMW消息给hwnd,将返回的结果写入pointer指向的内存空间
    win32gui.SendMessage(hwnd, commctrl.LVM_SETITEMSTATE, row_index, pLVI)

    VirtualFreeEx(hProcHnd, pBuffer, 0, win32con.MEM_RELEASE)
    VirtualFreeEx(hProcHnd, pLVI, 0, win32con.MEM_RELEASE)
    win32api.CloseHandle(hProcHnd)



#     # return text
# def DoItemSelect(lhWnd, lItemIndex, fSelect= True):
#     # win32gui.L
#     mhwnd = lhWnd
#     Dim i     As Long, s       As String
#     Dim dwProcessId     As Long, hProcess       As Long
#     Dim dwBytesRead     As Long, dwBytesWrite       As Long
#     pid = ctypes.create_string_buffer(4)
#     p_pid = ctypes.addressof(pid)
#     GetWindowThreadProcessId(mhwnd, p_pid)
#     Dim lpListItemRemote     As Long
#     Dim lvItemLocal     As LV_ITEM
#     Dim bWriteOK     As Long
#
#     hProcess = OpenProcess(win32con.PROCESS_VM_OPERATION or win32con.PROCESS_VM_READ or win32con.PROCESS_VM_WRITE, 0&, dwProcessId)
#     if hProcess <> 0 :
#           lpListItemRemote = VirtualAllocEx(hProcess, ByVal 0&, Len(lvItemLocal), MEM_COMMIT, PAGE_READWRITE)
#
#
#           lvItemLocal.mask = wintypes.LVIF_STATE
#           lvItemLocal.State = IIf(fSelect, LVIS_SELECTED Or LVIS_FOCUSED, 0)
#           lvItemLocal.stateMask = LVIS_SELECTED Or LVIS_FOCUSED
#
#           dwBytesWrite = 0
#           bWriteOK = WriteProcessMemory(hProcess, lpListItemRemote, VarPtr(lvItemLocal), sizeof(lvItemLocal), dwBytesWrite)
#           DoItemSelect = PostMessage(lhWnd, LVM_SETITEMSTATE, lItemIndex, lpListItemRemote)
#           time.sleep(0.2)
#            # 'MsgBox DoItemSelect
#           VirtualFreeEx(hProcess,lpListItemRemote, 0, MEM_DECOMMIT)
#
#     CloseHandle(hProcess)


def readMemoryText(hwnd):

    # Allocate virtual Memory inside target process
    pid = ctypes.create_string_buffer(4)
    p_pid = ctypes.addressof(pid)
    GetWindowThreadProcessId(hwnd, p_pid) # process owning the given hwnd
    # 3． 截获对系统函数的调用，取得参数，也就是我们要取的词。
    # 对于大多数的windows应用程序来说，如果要取词，我们需要截获的是
    # "gdi32.dll"
    # 中的
    # "textouta"
    # 函数。
    # 我们先仿照textouta函数写一个自己的mytextouta函数，如：
    # bool
    # winapi
    # mytextouta(hdc
    # hdc, int
    # nxstart, int
    # nystart, lpcstr
    # lpszstring, int
    # cbstring)
    # {
    # // 这里进行输出lpszstring的处理
    # // 然后调用正版的textouta函数
    # }
    hProcHnd = OpenProcess(win32con.PROCESS_ALL_ACCESS, False, struct.unpack("i",pid)[0])
    # 用PID来打开进程，并得到创建线程和写的权限。
    pLVI = VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    pBuffer = VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)

    # Prepare an LVITEM record and write it to target process Memory
    # 申请代码的内存区
    lvitem_str = struct.pack('iiiiiiiii', *[0,0,0,0,0,pBuffer,4096,0,0])
    lvitem_buffer = ctypes.create_string_buffer(lvitem_str)
    copied = ctypes.create_string_buffer(4)
    p_copied = ctypes.addressof(copied)
    # 把数据写到申请的内存中
    WriteProcessMemory(hProcHnd, pLVI, ctypes.addressof(lvitem_buffer), ctypes.sizeof(lvitem_buffer), p_copied)

    refresh_window(hwnd)
    # win32gui.SendMessage(hwnd, win32con.EXTTEXTOUT) #win32con.RDW_INVALIDATE | win32con.RDW_INTERNALPAINT)
    target_buff = ctypes.create_string_buffer(4096)
    # 读取申请的内存
    ReadProcessMemory(hProcHnd, pBuffer, ctypes.addressof(target_buff), 4096, p_copied)
    text=target_buff.value.decode("gbk")

    print("wow..." +text)

    # 释放内存，关闭句柄。
    VirtualFreeEx(hProcHnd, pBuffer, 0, win32con.MEM_RELEASE)
    VirtualFreeEx(hProcHnd, pLVI, 0, win32con.MEM_RELEASE)
    win32api.CloseHandle(hProcHnd)
    return text

#
# def mouseReleaseEvent(self, event):
#     if self.spying:
#         if self.prevWindow:
#             self.refreshWindow(self.prevWindow)
#         win32gui.ReleaseCapture()
#         self.spying = False
#
# def mouseMoveEvent(self, event):
#     if self.spying:
#         curX, curY = win32gui.GetCursorPos()
#         hwnd = win32gui.WindowFromPoint((curX, curY))
#
#         if self.checkWindowValidity(hwnd):
#             if self.prevWindow:
#                 self.refreshWindow(self.prevWindow)
#             self.prevWindow = hwnd
#             self.highlightWindow(hwnd)
#             self.displayWindowInformation(hwnd)



if __name__ == "__main__":

    win32gui.In
    # TestEnumWindows()

    # print (getHwndByKeywordsTitle("PyCharm"))
    # hwnd=getHwndByKeywordsTitle("Trader")
    # print (hwnd)
    #
    # grabWindows(hwnd)


    # import mouse_key_commond
    #
    # _getWord = GetWord()
    #
    # while 1:
    #
    #     x,y=mouse_key_commond.get_mouse_point()
    #
    #
    #     print(_getWord.getText(x,y))
    #
    #     time.sleep(1)

    pass
