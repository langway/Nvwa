# -*- coding:utf-8 -*-
"""
	@name		Python console ColorSetter-Outputer ui (PycUI)
	@blog		https://ursb.org
	@github		https://github.com/h01/Outputer
	@update		2014/10/29
	@author		Holger
	@version	1.0
"""
from os import name
from loongtian.util.log.logger import consoleLogger,logger

class ColorSetter:
    def __init__(self):
        if name == "nt":
            # Windows
            self.RED = 0x04
            self.GREY = 0x08
            self.BLUE = 0x01
            self.CYAN = 0x03
            self.BLACK = 0x0
            self.GREEN = 0x02
            self.WHITE = 0x07
            self.PURPLE = 0x05
            self.YELLOW = 0x06
            from ctypes import windll
            def s(color, h = windll.kernel32.GetStdHandle(-11)):
                return windll.kernel32.SetConsoleTextAttribute(h, color)

            def p(msg, color = self.BLACK, e = True):
                s(color or color or color)
                if e:
                    print (msg)
                else:
                    print (msg,s(self.RED or self.GREEN or self.BLUE))
        else:
            # Other system(unix)
            self.RED = '\033[31m'
            self.GREY = '\033[38m'
            self.BLUE = '\033[34m'
            self.CYAN = '\033[36m'
            self.BLACK = '\033[0m'
            self.GREEN = '\033[32m'
            self.WHITE = '\033[37m'
            self.PURPLE = '\033[35m'
            self.YELLOW = '\033[33m'

            def p(m, c = self.BLACK, e = True):
                if e:
                    print("%s%s%s" % (c, m, self.BLACK))
                else:
                    print("%s%s%s" % (c, m, self.BLACK))
        self.p = p

class Outputer:
    """
    输出的帮助类。
    可以分颜色输出不同的信息，同时可以选择记录日志文件中
    """
    cs = ColorSetter()

    @staticmethod
    def write(msg):
        print(msg)


    @staticmethod
    def p(msg):
        print(msg)

    @staticmethod
    def warning(msg,log=True):
        """
        记录警告信息
        :rawParam msg: 要记录的信息
        :rawParam log: 是否记入日志
        :return:
        """
        msg="[-] %s" % msg
        Outputer.cs.p(msg, Outputer.cs.PURPLE)
        if log:
            logger.warning(msg)

    @staticmethod
    def info(msg,log=True):
        """
        记录警告信息
        :rawParam msg: 要记录的信息
        :rawParam log: 是否记入日志
        :return:
        """
        msg="[-] %s" % msg
        Outputer.cs.p("[i] %s" % msg, Outputer.cs.YELLOW)
        if log:
            logger.info(msg)

    @staticmethod
    def error(msg,log=True):
        """
        记录错误信息
        :rawParam msg: 要记录的信息
        :rawParam log: 是否记入日志
        :return:
        """
        msg="[-] %s" % msg
        Outputer.cs.p("[!] %s" % msg, Outputer.cs.RED)
        if log:
            logger.info(msg)

    @staticmethod
    def success(msg,log=True):
        """
        记录成功信息
        :rawParam msg: 要记录的信息
        :rawParam log: 是否记入日志
        :return:
        """
        msg="[-] %s" % msg
        Outputer.cs.p("[*] %s" % msg, Outputer.cs.GREEN)
        if log:
            logger.info(msg)

    # short-func
    @staticmethod
    def w(msg):
        Outputer.warning(msg)

    @staticmethod
    def i(msg):
        Outputer.info(msg)

    @staticmethod
    def e(msg):
        Outputer.error(msg)

    @staticmethod
    def s(msg):
        Outputer.success(msg)
