#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
MessageBox（win32）的帮助类
"""
__author__ = 'leon'


import win32api, win32con
import platform
import winsound
def show(content,capital,style=win32con.MB_YESNO,playsound=True,sound="SystemHand",soundStyle=winsound.SND_ASYNC):
    """
    显示MessageBox（win32）
    :param content:显示的信息
    :param capital:标题
    :param style: 样式 意义:
            MB_ICONWARNING 含图标、固定按钮 警告信息框
            MB_ICONQUESTION 含图标、固定按钮 疑问信息框
            MB_IConERROR 含图标、固定按钮 错误信息框
            MB_ICONASTERISK 含图标、固定按钮 提示信息框
            MB_HELP 不含图标、可改变按钮 说明信息框
            MB_OK 不含图标、可改变按钮 提示信息框
            MB_OKCANCEL 不含图标、可改变按钮 确认信息框
            MB_RETRYCANCEL 不含图标、可改变按钮 重试信息框
            MB_YESNO 不含图标、可改变按钮 是否信息框
            MB_YESNOCANCEL 不含图标、可改变按钮 是否取消信息框
    :param playsound:是否播放声音
    :param sound:要播放的声音
                    'SystemAsterisk' Asterisk
                    'SystemExclamation' Exclamation
                    'SystemExit' Exit Windows
                    'SystemHand' Critical Stop
                    'SystemQuestion' Question
    :param soundStyle:播放声音的模式
                    SND_LOOP            重复地播放声音。SND_ASYNC标识也必须被用来避免堵塞。不能用 SND_MEMORY。
                                        SND_MEMORY 提供给PlaySound()的 sound 参数是一个 WAV 文件的内存映像(Memory image)，作为一个字符串。
                                        注意：这个模块不支持从内存映像中异步播放，因此这个标识和 SND_ASYNC 的组合将挂起 RuntimeError。
                    SND_PURGE           停止播放所有指定声音的实例。
                    SND_ASYNC           立即返回，允许声音异步播放。
                    SND_NODEFAULT       不过指定的声音没有找到，不播放系统缺省的声音。
                    SND_NOSTOP          不中断当前播放的声音。
                    SND_NOWAIT          如果声音驱动忙立即返回。
                    MB_ICONASTERISK     播放 SystemDefault 声音。
                    MB_ICONEXCLAMATION  播放 SystemExclamation 声音。
                    MB_ICONHAND         播放 SystemHand 声音。
                    MB_ICONQUESTION     播放 SystemQuestion 声音。
                    MB_OK               播放 SystemDefault 声音。


    :return:返回值 数值 意义
            IDOK 1 确定
            IDCANCEL 2 取消
            IDABORT 3 中断
            IDRETRY 4 重试
            IDIGNORE 5 忽略
            IDYES 6 是
            IDNO 7 否
    """
    content = str(content)
    capital = str(capital)
    if playsound:
        if platform.uname()[0] == 'Windows':
            winsound.PlaySound(sound, soundStyle)
    return win32api.MessageBox(0, content, capital, style)