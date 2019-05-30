#!/usr/bin/env python
# coding=utf-8

__author__ = 'Leon'

import time
from datetime import datetime
import httplib as client
import os
from loongtian.util.common.enum import Enum

ISOTIMEFORMAT = '%Y%m%d %X'
DateTIMEFORMAT = '%Y%m%d'
TIMETIMEFORMAT = '%H:%M:%S'  # '%X'


class TimeDifferenceException(Exception):
    """
    时间差计算错误
    """
    pass


class TimeDifferenceTypeEnum(Enum):
    """
    TimeDifference.type属性的对应枚举类
    """
    total_seconds = 0  # 精确秒数
    seconds = 1  # 30 秒数
    microseconds = 2  # 毫秒数
    days = 3  # 0 天数


TimeDifferenceTypeEnum = TimeDifferenceTypeEnum()


def getNow():
    """
    返回当前时区的值。
    :return:
    """
    return strftime(ISOTIMEFORMAT, time.time())


def getTime():
    """
    返回当前时区的值。
    :return:
    """
    return strftime(TIMETIMEFORMAT, time.time())


def strftime(FORMAT, time_):
    return time.strftime(FORMAT, time.localtime(time_))


def toISOTIMEFORMAT(time_):
    """
    转换为'%Y-%m-%d %X'格式的时间
    :param time_:
    :return:
    """
    return strftime(ISOTIMEFORMAT, time_)


def toDateTIMEFORMAT(time_):
    """
    转换为'%Y-%m-%d'格式的时间
    :param time_:
    :return:
    """
    return strftime(DateTIMEFORMAT, time_)


def toTIMETIMEFORMAT(time_):
    """
    转换为'%X'格式的时间（只有具体时间，无日期）
    :param time_:
    :return:
    """
    return strftime(TIMETIMEFORMAT, time_)


def getDate():
    """
    返回当前时区的值。
    :return:
    """
    return strftime(DateTIMEFORMAT, time.time())


def getZeroZoneNow():
    """
    返回0时区的值
    :return:
    """
    return strftime(ISOTIMEFORMAT, time.time())


def ISOString2Time(s):
    """
    convert a ISO format recordTime to second
    from:2006-04-12 16:46:40 to:23123123
    把一个时间转化为秒
    """
    return time.strptime(s, ISOTIMEFORMAT)


def Time2ISOString(s):
    """
    convert second to a ISO format recordTime
    from: 23123123 to: 2006-04-12 16:46:40
    把给定的秒转化为定义的格式
    """
    return time.strftime(ISOTIMEFORMAT, time.localtime(float(s)))


def is_valid_date(str):
    """判断是否是一个有效的日期字符串"""
    try:
        time.strptime(str, ISOTIMEFORMAT)
        return True
    except:
        try:
            time.strptime(Time2ISOString(str), ISOTIMEFORMAT)
            return True
        except:
            return False


def dateplustime(d, t):
    """
    d=2006-04-12 16:46:40
    t=2小时
   return  2006-04-12 18:46:40
   计算一个日期相差多少秒的日期,time2sec是另外一个函数，可以处理，3天，13分钟，10小时等字符串，回头再来写这个，需要结合正则表达式。
    """
    return Time2ISOString(time.mktime(ISOString2Time(d)) + time2sec(t))


def time2sec(t):
    raise NotImplementedError(u'目前尚未实现！')
    pass


def dateMinDate(d1, d2):
    """
    minus to iso format date,return seconds
    计算2个时间相差多少秒
    """
    d1 = ISOString2Time(d1)
    d2 = ISOString2Time(d2)
    return time.mktime(d1) - time.mktime(d2)


def is_between(time_str, start_str=None, end_str=None):
    """
    判断一个时间是否是在开始时间和结束时间之间
    :param time_str:
    :param start_str:
    :param end_str:
    :return:
    """
    if not time_str or not isinstance(time_str, str) or not isinstance(time_str, unicode):
        return False

    return start_str <= time_str <= end_str


def get_webservertime(host):
    """
    取得网络时间
    :param host:
    :return:
    """
    conn = client.HTTPConnection(host)
    conn.request("GET", "/")
    r = conn.getresponse()
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    local_time = time.mktime(time.strptime(ts[5:], "%d %b %Y %H:%M:%S GMT")) + (8 * 60 * 60)
    ltime = time.gmtime(local_time)
    # 使用date设置时间
    dat = 'date -u -s "%d-%d-%d %d:%d:%d" ' % (
        ltime.tm_year, ltime.tm_mon, ltime.tm_mday, ltime.tm_hour, ltime.tm_min, ltime.tm_sec)
    os.system(dat)


def get_time_difference(start, end=None, TimeDifferenceType=TimeDifferenceTypeEnum.total_seconds):
    """
    取得时间差
    :param start: 开始时间（必须提供）
    :param end:结束时间（可以不提供，系统默认当前时间）
    :return:
    """
    if not end:
        end = datetime.datetime.now()
    time_differ = None
    if TimeDifferenceType == TimeDifferenceTypeEnum.total_seconds:
        time_differ = (end - start).total_seconds()  # 精确秒数
    elif TimeDifferenceType == TimeDifferenceTypeEnum.seconds:
        time_differ = (end - start).seconds  # 秒数
    elif TimeDifferenceType == TimeDifferenceTypeEnum.microseconds:
        time_differ = (end - start).microseconds  # 毫秒数
    elif TimeDifferenceType == TimeDifferenceTypeEnum.days:
        time_differ = (end - start).days  # 天数

    return time_differ


def join_date_time(date, time):
    """
    以一定的格式连接日期和时间。
    :param date:
    :param time:
    :return:
    """
    try:
        return datetime.datetime.strptime(' '.join([date, time]), '%Y%m%d %H:%M:%S.%f')
    except ValueError:
        try:
            return datetime.datetime.strptime(' '.join([date, time]), '%Y%m%d %H:%M:%S')
        except ValueError:
            import traceback
            print (traceback.format_exc())


# get_webservertime('www.baidu.com')

# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import datetime
import pytz


def datetime_is_naive(dateTime):
    """ Returns True if dateTime is naive."""
    return dateTime.tzinfo is None or dateTime.tzinfo.utcoffset(dateTime) is None


# Remove timezone information.
def unlocalize(dateTime):
    return dateTime.replace(tzinfo=None)


def localize(dateTime, timeZone):
    """Returns a datetime adjusted to a timezone:

     * If dateTime is a naive datetime (datetime with no timezone information), timezone information is added but date
       and time remains the same.
     * If dateTime is not a naive datetime, a datetime object with new tzinfo attribute is returned, adjusting the date
       and time data so the result is the same UTC time.
    """

    if datetime_is_naive(dateTime):
        ret = timeZone.localize(dateTime)
    else:
        ret = dateTime.astimezone(timeZone)
    return ret


def as_utc(dateTime):
    return localize(dateTime, pytz.utc)


def datetime_to_timestamp(dateTime):
    """ Converts a datetime.datetime to a UTC timestamp."""
    diff = as_utc(dateTime) - epoch_utc
    return diff.total_seconds()


def timestamp_to_datetime(timeStamp, localized=True):
    """ Converts a UTC timestamp to a datetime.datetime."""
    ret = datetime.datetime.utcfromtimestamp(timeStamp)
    if localized:
        ret = localize(ret, pytz.utc)
    return ret


def get_first_monday(year):
    ret = datetime.date(year, 1, 1)
    if ret.weekday() != 0:
        diff = 7 - ret.weekday()
        ret = ret + datetime.timedelta(days=diff)
    return ret


def get_last_monday(year):
    ret = datetime.date(year, 12, 31)
    if ret.weekday() != 0:
        diff = ret.weekday() * -1
        ret = ret + datetime.timedelta(days=diff)
    return ret


epoch_utc = as_utc(datetime.datetime(1970, 1, 1))
