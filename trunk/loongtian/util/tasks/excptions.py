#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

"""
exceptions
定义一些Exception，用于自定义异常处理

"""

class NoResultsPending(Exception):
    """
    所有的工作项请求已经被处理完毕
    All task requests have been processed.
    """
    pass # class NoResultsPending(Exception)


class NoDelegatorsAvailable(Exception):
    """
    没有可用的代理线程可用来处理剩余的工作项请求
    No thread delegators available to process remaining requests.
    """
    pass # class NoDelegatorsAvailable(Exception)



