#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 

"""
__author__ = 'Leon'

import logging
import logging.config

logging.config.fileConfig('logging.properties')
consoleLogger = logging.getLogger('root')
consoleLogger.debug('test console logger...')

logger = logging.getLogger('nvwa')
logger.info('test nvwa logger')
logger.info('start import module \'mod\'...')
# import mod
#
# logger.debug('let\'s test mod.testLogger()')
# mod.testLogger()

consoleLogger.info('finish test...')
