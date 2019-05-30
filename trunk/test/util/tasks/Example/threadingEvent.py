#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import threading
import time
from loongtian.util.log.logger import *

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

def worker(event):
    while not event.is_set():
        logger.debug('Waiting for redis ready...')
        event.wait(1)
    logger.debug('redis ready, and connect to redis server and do some work [%s]'%(time.ctime()))
    time.sleep(1)

readis_ready = threading.Event()
t1 = threading.Thread(target=worker, args=(readis_ready,), name='t1')
t1.start()

t2 = threading.Thread(target=worker, args=(readis_ready,), name='t2')
t2.start()

logger.debug('first of all, check redis server, make sure it is OK, and then trigger the redis ready event')
time.sleep(3) # simulate the check progress
readis_ready.set()