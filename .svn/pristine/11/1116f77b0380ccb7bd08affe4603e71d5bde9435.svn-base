#!/usr/bin/env python
# coding: utf-8
"""
单例模式测试。
"""

from unittest import TestCase
from loongtian.util.log.logger import consoleLogger,logger



def excptionCreator():
    """
    这里虚拟了一个产生错误的函数。
    :return:
    """
    raise ValueError('You Must provide a value!')
class loggerWraper():
    """
    用于查看多层logger调用的结果
    """

    def wrappedLogger(self):
        try:
            excptionCreator()
        except Exception as e:
            logger.debug("多层logger调用的错误！！！",True)

    pass


class TestLogger(TestCase):

    def setUp(self):
        print("----setUp----")
        pass # def setUp(self):

    def testLogger(self):
        print("----testLogger----")
        consoleLogger.debug('test console logger...')

        #debug级别的测试
        logger.debug(u'test nvwa logger这里是中文信息！')
        logger.debug('start import module \'mod\'...',True)
        from test.util.logger.Example import mod

        #info级别的测试
        logger.info('let\'s test mod.testLogger()')
        mod.testLogger()
        logger.info('finish mod test...',True)

       #warning级别的测试
        logger.warning(u'warning：敌人来袭！')
        logger.warning('warning：敌人已靠近！',True)

        #测试对异常对象的处理
        try:
            excptionCreator()
        except ValueError as e:
            logger.exception('这里是程序提供的异常信息！')#这里将自动记录错误中的信息
            logger.exception(e)  #异常信息被自动添加到日志消息中

        _loggerWraper=loggerWraper()
        _loggerWraper.wrappedLogger()

        #这里将发送邮件
        # logger.critical(u'critical test(sys\mail)-Nvwa告诉你，出大事了！这里是中文信息！')

        #这里测试记录其他对象及stackTrace
        logger.info(mod,True)

        pass # def testLogger(self)

    def tearDown(self):
        print("----tearDown----")

    pass # class TestLogger(TestCase)

