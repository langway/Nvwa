#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

# encoding: UTF-8
import threading
import time,datetime
con = threading.Condition()
product=None

def produce():
    global product
    while True:
        if con.acquire():
            if not product:
                product='add new'
                print 'produce',datetime.datetime.now()
                time.sleep(3)
                con.notify()
        con.wait()
def consume():
    global product
    while True:
        if con.acquire():
            if product:
                print 'consume',datetime.datetime.now()
                product=None
                con.notify()
            con.wait()

t1 = threading.Thread(target=produce)
t2 = threading.Thread(target=consume)
t1.start()
t2.start()
