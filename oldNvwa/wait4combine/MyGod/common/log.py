#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
log功能类
>>> logger = Log().logger('doctest')
>>> logger.debug("11")
>>> logger.error("22")
22
>>> logger.info("33")
33
"""
from conf import config_parser

__author__ = 'Liuyl'
from conf.config import configs as configs
import singleton
import logging
import logging.config
import os


@singleton.singleton
class Log(object):
    def __init__(self):
        conf = configs['path']
        self.__path = os.path.join(conf['root'], conf['log_conf'])
        logging.config.fileConfig(self.__path)

    def logger(self, key):
        return logging.getLogger(key)


if __name__ == '__main__':
    import doctest

    doctest.testmod()