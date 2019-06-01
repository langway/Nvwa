#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 

"""
__author__ = 'Leon'
import os,sys
import logging
import logging.handlers
import logging.config
import datetime
from loongtian.util.helper import timeHelper

from logging.handlers import SMTPHandler

# reload(sys)
# sys.setdefaultencoding('utf-8')

__settingFileName="logging.properties"
#取得当前对象的真正的文件路径，非os.getcwd()
loggerPath=os.path.split(os.path.realpath(__file__))[0]
logConfigPath= os.path.join(loggerPath, __settingFileName)
logging.config.fileConfig(logConfigPath)

#程序的控制台输出logger
consoleLogger = logging.getLogger('root')

"""
注意：要更改
\Lib\logging\__init__.py\LogRecord.getMessage最后一句话：
if self.args:
    msg = msg % self.args

if self.args:
    try:
        msg = msg % self.args
    except:
        pass
        
\Lib\logging\handlers
class RotatingFileHandler(BaseRotatingHandler):
    def doRollover(self):
        def doRollover(self):
            原语句：
            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
            
            
            更改为：
            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                try:
                    os.rename(self.baseFilename, dfn)
                except:
                    pass
"""



class __CommonLogger(object):
    """
    可处理错误的通用日志的包装类。
    level log的等级，包括：
                CRITICAL = 50\
                FATAL = CRITICAL critical级输出，严重错误信息\
                ERROR = 40 error级输出，错误信息\
                WARNING = 30 warning级输出，与warn相同，警告信息\
                WARN = WARNING \
                INFO = 20 info 级输出，重要信息\
                DEBUG = 10 debug级输出\
                NOTSET = 0
                五个等级从低到高分别是debug到critical。
                一旦设置了日志等级，则调用比等级低的日志记录函数则不会输出
    """
        #系统默认的应向上查找的深度（4正好调用到logger的上一层）
    __loggerCallerDepth=4
    # 系统默认的最大查找数量
    __loggerCallerMaxDepth=10

    def __init__(self):
        #程序的默认logger（控制台输出、文件输出及SMTP邮件输出（WARNNING级别及以上））
        self.__logger = logging.getLogger('nvwa')
        self.timeMarks={} # 用来记录对应时间，格式为：{timeMark:timeStart} # 只需记录开始时间，结束就pop出去了
                        # 例如：logger.debug("程序1开始",timeStartMark="程序1")——logger.debug("程序1结束",timeEndMark="程序1")
                        # 将记录以"程序1"为标记的两段时间的差值。这里可以使用不同的日志级别。
                        # 注意：当系统完成一对的时差计算时，将会删除该时间对，所以这里要注意不能多次出现相同的timeEndMark
        if __debug__: # debug状态下最好跟踪内部数据
            self.logInnerStackTrace =True
        else:
            self.logInnerStackTrace = False
    @property
    def handlers(self):
        """
        向外提供当前nvwa logger的handlers
        """
        return self.__logger.handlers
        pass#def handlers(self)

    @handlers.setter
    def handlers(self,value):
        self.__logger.handlers=value


    def debug(self, obj2log, logInnerStackTrace=None, timeStartMark=None,timeEndMark=None ,*args, **kwargs):
        """
        debug级输出，一般只输出在控制台
        Log 'obj2log % args' with severity 'DEBUG'.

        :rawParam obj2log 需要记录的日志对象，有两种：（1）字符串。直接记录。（2）错误类。取得其message

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if logInnerStackTrace is None:
            logInnerStackTrace=self.logInnerStackTrace
        return self.log(logging.DEBUG, obj2log,logInnerStackTrace, timeStartMark,timeEndMark,args, **kwargs)

        pass#def debug(self, obj2log, *args, **kwargs)

    def info(self, obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None,*args, **kwargs):
        """
        info 级输出，重要信息。
        Log 'obj2log % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if logInnerStackTrace is None:
            logInnerStackTrace=self.logInnerStackTrace
        return self.log(logging.INFO, obj2log,logInnerStackTrace, timeStartMark,timeEndMark,args, **kwargs)

        pass#def info(self, obj2log, *args, **kwargs)

    def warning(self, obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None, *args, **kwargs):
        """
        warning级输出，与warn相同，警告信息
        Log 'obj2log % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        if logInnerStackTrace is None:
            logInnerStackTrace=self.logInnerStackTrace
        return self.log(logging.WARNING, obj2log,logInnerStackTrace, timeStartMark,timeEndMark,args, **kwargs)

        pass#def warning(self, obj2log, *args, **kwargs)


    def error(self, obj2log,logInnerStackTrace=None,timeStartMark=None,timeEndMark=None, *args, **kwargs):
        """
        error级输出，一般错误信息（需记录，不需通知）
        Log 'obj2log % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        if logInnerStackTrace is None:
            logInnerStackTrace=self.logInnerStackTrace
        return self.log(logging.ERROR, obj2log,logInnerStackTrace, timeStartMark,timeEndMark,args, **kwargs)

        pass#def error(self, obj2log, *args, **kwargs)

    def exception(self, obj2log,logInnerStackTrace=None,timeStartMark=None,timeEndMark=None, *args, **kwargs):
        """
        在error级输出的基础上，记录一般错误信息及StackTrace（需记录，不需通知）
        Convenience method for logging an ERROR with exception information.
        """
        if logInnerStackTrace is None:
            logInnerStackTrace=self.logInnerStackTrace
        kwargs['exc_info']=1

        return self.log(logging.ERROR, obj2log,False, timeStartMark,timeEndMark,args, **kwargs)

        pass#def exception(self, obj2log, *args, **kwargs)


    def critical(self, obj2log,logInnerStackTrace=None,timeStartMark=None,timeEndMark=None, *args, **kwargs):
        """
        critical级输出，严重错误信息(一般会进行邮件通知等处理，有些错误可能不需要进行critical级处理)
        Log 'obj2log % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if logInnerStackTrace is None:
            logInnerStackTrace=self.logInnerStackTrace
        return self.log(logging.CRITICAL, obj2log,False, timeStartMark,timeEndMark,args, **kwargs)

        pass#def critical(self, obj2log, *args, **kwargs)



    def log(self, level, obj2log, logInnerStackTrace,timeStartMark=None,timeEndMark=None, *args, **kwargs):
        """
        日志记录，需输入日志等级
        Log 'obj2log % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        :rawParam level log的等级，包括：
                CRITICAL = 50\
                FATAL = CRITICAL critical级输出，严重错误信息\
                ERROR = 40 error级输出，错误信息\
                WARNING = 30 warning级输出，与warn相同，警告信息\
                WARN = WARNING \
                INFO = 20 info 级输出，重要信息\
                DEBUG = 10 debug级输出\
                NOTSET = 0
                五个等级从低到高分别是debug到critical。
                一旦设置了日志等级，则调用比等级低的日志记录函数则不会输出
        :rawParam obj2log 需要记录的日志对象，有两种：（1）字符串。直接记录。（2）错误类。取得其message
        :rawParam logInnerStackTrace 是否记录StackTrace的标记
        """
        #如果要记录的对象不存在，直接返回
        if obj2log is None:
            return

        #如果要记录的level不正确，抛出错误或返回
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return

        #如果logger不能够记录当前级别，直接返回
        if not self.__logger.isEnabledFor(level):
            return

        #如果已经到了CRITICAL级别，由系统记录StackTrace
        if level>=logging.CRITICAL :
            kwargs['exc_info']=1
            logInnerStackTrace=False

        #由于logging原程序对StackTrace的记录需与level绑定（level>=WARNING），导致INFO等级别不能自动记录StackTrace
        # 所以这里需要进行特殊处理：

        #当前的StackTrace
        curStack=''

        if logInnerStackTrace:
            #取得当前的StackTrace
            curStack=self.__getInnerStackTrace()

        # 原来的logging.logger不对输入对象进行区分，会有错误抛出，
        # 这里根据输入的对象进行不同的处理
        msg=""
        if isinstance(obj2log,str): #or isinstance(obj2log,unicode ):
            msg+=obj2log+curStack
        elif isinstance(obj2log,Exception ):
            msg+=obj2log.args[0]+curStack
        elif not hasattr(obj2log,'__dict__'):# 基本数据类型，转成字符串
            msg+=str(obj2log)+curStack
        elif hasattr(obj2log,'__str__'):
            str2log=''
            try:
                str2log=str(obj2log)
            except:
                str2log=obj2log.__str__
            msg+=str2log+curStack
        else:
            msg+="name:"+obj2log.__name__ + " "+curStack

        # 记录时间差
        if timeStartMark:
            start = datetime.datetime.now()
            self.timeMarks[timeStartMark]=start
        if timeEndMark:
            if timeEndMark in self.timeMarks:
                end = datetime.datetime.now()
                time_differ=timeHelper.get_time_difference(self.timeMarks[timeEndMark],end) # 精确秒数
                msg += " total_seconds:" +str(time_differ)
                self.timeMarks.pop(timeEndMark) # 删除该时间对
            else:
                raise timeHelper.TimeDifferenceException("con not find start time,time mark is:" + timeEndMark)


        return self.__log(level,msg,args,**kwargs)

        pass#def log(self, obj2log, *args, **kwargs)

    def __getInnerStackTrace2(self):
        """
        取得logger之前，Python系统文件之后的调用顺序。
        :return:lines
        """
        notIsSys=True#不是Python系统文件
        curDepth=self.__loggerCallerDepth#当前的读取深度（这里是logger向上返）
        lines=[]

        while curDepth>=0:

            try:
                rv = self.__findCaller(curDepth)
            except ValueError:
                rv = "(unknown file)", 0, "(unknown function)"
            #判断是否已经到了系统级的文件，如果是，停止循环，如果否，继续向上循环
            #正常的程序调用关系是：IDE（PyCharm etc.如果有的话）——>Python(console、debug等)——>正在执行的文件，
            #所以只需要判断该程序文件是否位于Python的根目录下即可。
            if not rv[0].startswith(sys.prefix):
                curLine="""File "%s", line %d, in %s"""%rv
                lines.append(curLine)
            curDepth-=1


        if not lines:
            return ''

        strStack='\nInnerTraceback (most recent call last):\n'
        #拼接出字符串
        for line in lines:
            strStack+=line+'\n'
        #去掉最后的换行符
        strStack=strStack.rstrip('\n')

        return strStack

    def __getInnerStackTrace(self):
        """
        取得logger之前，Python系统文件之后的调用顺序。
        :return:lines
        """
        notIsSys=True#不是Python系统文件
        curDepth=self.__loggerCallerDepth#当前的读取深度（这里是logger向上返）
        lines=[]

        while notIsSys:
            if curDepth>=self.__loggerCallerMaxDepth:
                break

            try:
                rv = self.__findCaller(curDepth)
            except ValueError:
                notIsSys=False
                rv = "(unknown file)", 0, "(unknown function)"
            #判断是否已经到了系统级的文件，如果是，停止循环，如果否，继续向上循环
            #正常的程序调用关系是：IDE（PyCharm etc.如果有的话）——>Python(console、debug等)——>正在执行的文件，
            #所以只需要判断该程序文件是否位于Python的根目录下即可。
            if not rv[0].startswith(sys.prefix):
                curLine="""File "%s", line %d, in %s"""%rv
                curDepth+=1
                lines.append(curLine)
            else:
                notIsSys=False


        if not lines:
            return ''

        strStack='\nInnerTraceback (most recent call last):\n'
        #拼接出字符串
        for line in lines:
            strStack+=line+'\n'
        #去掉最后的换行符
        strStack=strStack.rstrip('\n')

        return strStack


    def __log(self, level, msg, args, exc_info=None, extra=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if logging._srcfile:
            #IronPython doesn't track Python frames, so __findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                filename, linenum, funcname = self.__findCaller()
            except ValueError:
                filename, linenum, funcname = "(unknown file)", 0, "(unknown function)"
        else:
            filename, linenum, funcname = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.__logger.makeRecord(self.__logger.name, level, filename, linenum, msg, args, exc_info, funcname, extra)
        self.__logger.handle(record)



    def __currentframe(self,depth=4):
        """
        取得当前文件的上几层（depth）的调用对象
        """
        if hasattr(sys, '_getframe'):
            return sys._getframe(depth)

    def __findCaller(self,depth=4):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = self.__currentframe(depth)
        #On some versions of IronPython, __currentframe() returns None if
        #IronPython isn't start with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

    pass#class __CommonLogger:


"""
程序的默认logger（控制台输出、文件输出及SMTP邮件输出（WARNNING级别及以上））
"""
logger = __CommonLogger()


def debug(obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None):
    """
    debug级输出，一般只输出在控制台
    :param obj2log:
    :param logInnerStackTrace:
    :return:
    """
    logger.debug(obj2log, logInnerStackTrace,timeStartMark,timeEndMark)


def info(obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None):
    """
    info 级输出，重要信息。
    :param obj2log:
    :param logInnerStackTrace:
    :return:
    """
    logger.info(obj2log, logInnerStackTrace,timeStartMark,timeEndMark)

def warning(obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None):
    """
    warning 级输出，重要信息。
    :param obj2log:
    :param logInnerStackTrace:
    :return:
    """
    logger.warning(obj2log, logInnerStackTrace,timeStartMark,timeEndMark)


def error(obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None):
    """
    error级输出，一般错误信息（需记录，不需通知）
    :param obj2log:
    :param logInnerStackTrace:
    :return:
    """
    logger.error(obj2log, logInnerStackTrace,timeStartMark,timeEndMark)


def exception(obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None):
    """
    在error级输出的基础上，记录一般错误信息及StackTrace（需记录，不需通知）
    :param obj2log:
    :param logInnerStackTrace:
    :return:
    """
    logger.exception(obj2log, logInnerStackTrace,timeStartMark,timeEndMark)

def critical(obj2log, logInnerStackTrace=None,timeStartMark=None,timeEndMark=None):
    """
    critical级输出，严重错误信息(一般会进行邮件通知等处理，有些错误可能不需要进行critical级处理)
    :param obj2log:
    :param logInnerStackTrace:
    :return:
    """
    logger.critical(obj2log, logInnerStackTrace,timeStartMark,timeEndMark)

def log( obj2log,level=logging.DEBUG,logInnerStackTrace=None,timeStartMark=None,timeEndMark=None, *args, **kwargs):
    """
    日志记录，需输入日志等级
    :param obj2log:
    :param logInnerStackTrace:
    :return:
    """
    logger.log(level, obj2log,logInnerStackTrace,args, **kwargs)

class __EncodingFormatter(logging.Formatter):
    """
    由于SMTPHandler不能发送unicode编码的logging, 会抛UnicodeError
    需要重写SMTPHandler的formatter
    """
    def __init__(self, fmt, datefmt=None, encoding=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.encoding = encoding

    def format(self, record):
        result = logging.Formatter.format(self, record)
        if isinstance(result, str):
            result = result.encode(self.encoding or 'utf-8')
        return result

# 由于SMTPHandler不能发送unicode编码的logging, 会抛UnicodeError
# 重写SMTPHandler的formatter
__smtpHandler=None

#取得__smtpHandler
for h in logger.handlers:
    if isinstance(h,logging.handlers.SMTPHandler):
        __smtpHandler=h
        break
    pass #for h in logger.handlers

#重设为__EncodingFormatter
if not __smtpHandler is None:
    __smtpHandler.setFormatter(__EncodingFormatter(__smtpHandler.formatter._fmt,__smtpHandler.formatter.datefmt, encoding='utf-8'))

if __name__=="__main__":
    consoleLogger.debug('test console logger...')
    #debug级别的测试
    logger.debug(u'test nvwa logger这里是中文信息！')
    logger.debug('start import module \'mod\'...',True)
    #info级别的测试
    logger.info('let\'s test mod.testLogger()')


   #warning级别的测试
    logger.warning(u'warning：敌人来袭！')
    logger.warning('warning：敌人已靠近！',True)
    e=Exception("这里是错误Exception的测试")
    logger.error(e)
