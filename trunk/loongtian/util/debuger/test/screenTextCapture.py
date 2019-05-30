#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
屏幕自动校准器
"""
__author__ = 'leon'

# bool winapi mytextouta(hdc hdc, int nxstart, int nystart, lpcstr lpszstring,int cbstring)
# {
# // 这里进行输出lpszstring的处理
# // 然后调用正版的textouta函数
# }

# TextOut，ExtTextOut，DrawText，DrawTextEx，PolyTextOut，TabbedTextOut，作了一番学习。
#
# 以前只是使用，HOOK以后才发现它们有很大的不同。
#
#
# // TextOut（分为TextOutA及TextOutW）
# //仅可输出单行文字
# BOOL TextOut(
#   HDC hdc,           // handle to DC—— device context
#   int nXStart,       // x-coordinate of starting position
#   int nYStart,       // y-coordinate of starting position
#   LPCTSTR lpString,  // character string——pointer to string
# int cbString       // number of characters in string
# );
#

# //而ExtTextOut进一步,多了fuOptions及lprc, lpDx参数, 可利用这3个参数进行剪切,遮挡等操作
# BOOL ExtTextOut(
#   HDC hdc,          // handle to DC
#   int X,            // x-coordinate of reference point
#   int Y,            // y-coordinate of reference point
#   UINT fuOptions,   // text-output options
#   CONST RECT *lprc, // optional dimensions
#   LPCTSTR lpString, // string
#   UINT cbCount,     // number of characters in string
#   CONST INT *lpDx   // array of spacing values
# );
#
# //DrawText可用于多行输出,计算即将输出的位置等,考虑Tab字符等
# int DrawText(
#   HDC hDC,          // handle to DC
#   LPCTSTR lpString, // text to draw
#   int nCount,       // text length
#   LPRECT lpRect,    // formatting dimensions
#   UINT uFormat      // text-drawing options
# );


#
# //
# int DrawTextEx(
#   HDC hdc, // handle to DC
#   LPTSTR lpchText,             // text to draw
#   int cchText,                 // length of text to draw
#   LPRECT lprc,                 // rectangle coordinates
#   UINT dwDTFormat,             // formatting options
#   LPDRAWTEXTPARAMS lpDTParams  // more formatting options );
#
# 　　
# PolyTextOut　　
# 函数功能：该函数在指定设备环境下以当前所选的字体和正文颜色绘制多个字符串。
# 函数原型：BOOL PolyTextOut(HDC hdc, CONST POLYTEXT *pptxt, int cStrings)；
# TabbedTextOut　　
# 函数功能：该函数将一个字符串写到指定的位置，并按制表位位置数组里的值展开制表符。正文以当前选择的字体、背景色和字体写入。
# 函数原型：；LONG TabbedTextOut(HDC hdc, int X, int Y, LPCTSTR lpString, int nCount, int nTabPositions, LPINT lpn TabStopPositions, int nTabOrigin)；
#
#
# 经过分析拦截的输入文本发现，TextOut实际继续调用了ExtTextOut，因此最后只拦截了ExtTextOut就实现了程序要求。
