#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import loongtian.util.helper.stringHelper as stringHelper
from loongtian.nvwa.runtime.msgInfo import MsgInfo
from loongtian.nvwa.runtime.reals import RealUser


def logon(msgInfo, clientHandler, memory=None):
    """
    根据当前的用户设备，目前包括：console、网页、Android、ios等，调用不同的登录、登出界面
    :param self:
    :param msgInfo:
    :param clientHandler:
    :return:
    :remarks:100-输入输出面板；200-webpage；300-Android；400-iOS
    """
    if msgInfo.facility == 100: # 100-输入输出面板
        return Console.logonOrRegiste(clientHandler, memory, logon=True)
    elif msgInfo.facility == 200: # 200-webpage
        # todo 模拟登陆
        return WebPage.logonOrRegiste(clientHandler, memory, logon=True)
    elif msgInfo.facility == 300: # 300-Android
        pass
    elif msgInfo.facility == 400: # 400-iOS
        pass
    else:
        raise Exception("未知的用户设备，应为：console、网页、Android、ios等")

class Console():

    @staticmethod
    def logonOrRegiste(clientHandler, memory=None, logon=True):
        """
        使用输入输出控制台进行用户登录
        :param ClientHandler:
        :return:
        """
        while True:
            user_name = Console.waitForUserName(clientHandler)
            if not user_name:
                continue

            password = Console.waitForPassword(clientHandler)
            if not password:
                continue

            password = stringHelper.encodeStringMD5(password)
            if stringHelper.mailValid(user_name):
                if logon:
                    real_user = RealUser(email=user_name, password=password,
                                         memory=memory).getExist()
                else:
                    real_user = RealUser(email=user_name, password=password,
                                         memory=memory).create(checkExist=False)
            elif stringHelper.phoneValid(user_name):
                if logon:
                    real_user = RealUser(phone=user_name, password=password,
                                         memory=memory).getExist()
                else:
                    real_user = RealUser(phone=user_name, password=password,
                                         memory=memory).create(checkExist=False)
            else:
                if logon:
                    real_user = RealUser(username=user_name, password=password,
                                         memory=memory).getExist()
                else:
                    real_user = RealUser(username=user_name, password=password,
                                         memory=memory).create(checkExist=False)
            if real_user:
                if logon:
                    clientHandler._send("用户已成功登录！欢迎您：%s\r\n"
                                        "        您想知道些什么？" % real_user.getShowName())
                else:
                    if real_user._isGetByConflictDBColumns: # 如果是注册，但从数据库查询到相同的，通知，并让其重新填写用户名/手机/电子邮件
                        clientHandler._send("用户名/手机/电子邮件已存在，"
                                            "请重新注册新用户！")

                        return Console.waitForRelogon(clientHandler,memory=memory)
                    else:
                        clientHandler._send("用户已成功注册！欢迎您：%s\r\n"
                                            "        您想知道些什么？" % real_user.nickname)

                return real_user
            else:
                clientHandler._send("错误的用户名或密码！")
                return Console.waitForRelogon(clientHandler,memory=memory)

    @staticmethod
    def waitForUserName(clientHandler):
        """
        通过输入输出控制台循环以等待接受用户名/邮件/手机
        :param clientHandler:
        :return:
        """

        clientHandler._send("请输入用户名/邮件/手机：")
        user_name = clientHandler.waitForReceive(returnMsgInfo=False)
        if user_name:
            if user_name.find("\r\n")<0 and len(user_name)<=80:
                return user_name
            clientHandler._send("不合法的用户名，请重新输入！")
            return Console.waitForUserName(clientHandler)

        else:
            return Console.waitForUserName(clientHandler)

    @staticmethod
    def waitForPassword(clientHandler):
        """
        通过输入输出控制台循环以等待接受用户密码
        :param clientHandler:
        :return:
        """
        clientHandler._send("请输入密码：")
        password = clientHandler.waitForReceive(returnMsgInfo=False)
        if password:
            if password.find("\r\n") < 0 and len(password) <= 80:
                return password
            clientHandler._send("不合法的密码，请重新输入！")
            return Console.waitForPassword(clientHandler)

        else:
            return Console.waitForPassword(clientHandler)

    @staticmethod
    def waitForRelogon(clientHandler,memory=None):
        """
        循环以等待接受用户重新输入或注册
        :param clientHandler:
        :return:
        """

        clientHandler._send("输入1：重新登录！\r\n"
                            "        输入2：注册新用户！")

        relogon = clientHandler.waitForReceive(returnMsgInfo=False)
        if relogon:
            if isinstance(relogon, unicode) or isinstance(relogon, str):
                try:
                    relogon = int(relogon)
                except:
                    clientHandler._send("错误的选项！")
                    return Console.waitForRelogon(clientHandler,memory=memory)

            if relogon == 1:
                return Console.logonOrRegiste(clientHandler,memory=memory,logon=True)
            elif relogon == 2:
                return Console.register(clientHandler, memory=memory)
            else:
                clientHandler._send("错误的选项！")
                return Console.waitForRelogon(clientHandler,memory=memory)

    @staticmethod
    def register(clientHandler, memory=None):
        """
        使用输入输出控制台注册新用户。
        :param clientHandler:
        :return:
        """
        clientHandler._send("开始注册新用户...")
        return Console.logonOrRegiste(clientHandler, memory, logon=False)

class WebPage():
    @staticmethod
    def logonOrRegiste(clientHandler, memory=None, logon=True):
        """
        使用输入输出控制台进行用户登录
        :param ClientHandler:
        :return:
        """
        # todo 目前为模拟登陆
        from loongtian.nvwa.runtime.reals import AdminUser
        real_user = None
        real_user = AdminUser.getAdminUser(memory=memory)
        return real_user
