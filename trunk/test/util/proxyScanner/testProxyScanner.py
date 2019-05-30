#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from unittest import TestCase
from loongtian.util.proxy.proxyScanner import ProxyScanner

class MyTestCase():
    def setUp(self):
        print ("----setUp----")

    def testSomething(self):
        print ("----testSomething----")
        _scanner = ProxyScanner()
        try:
            #  1.1.1.1-1.1.2.255 -p 8080 -t 50 -s test.txt
            # opts =[('-v','version'),("--ips","192.168.1.1-192.168.1.255"),("--port","8080"),("--thread","50"),("--save","test.txt")] #, 'help', 'ips=', 'port=', 'thread=', 'save=']
            # _scanner.start(opts)
            _scanner.runScanner("192.168.1.1-192.168.1.255",8080,50,"test.txt")
        except Exception as e:
            _scanner.usage()

    def tearDown(self):
        print ("----tearDown----")

if __name__=="__main__":
    _MyTestCase=MyTestCase()
    _MyTestCase.testSomething()
