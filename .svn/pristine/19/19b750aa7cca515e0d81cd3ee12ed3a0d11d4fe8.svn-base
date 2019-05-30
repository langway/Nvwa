#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  loongtian/fuxi
Title:    runserver 
Author:   xujz 
DateTime: 2015/6/10 11:13 
UpdateLog:
1、xujz 2015/6/10 Create this File.
runserver
2、script 2015/11/23 update this File.
"""
import time
from loongtian.fuxi import app, console
from loongtian.util.tasks.runnable import run


__author__ = 'leon'

if __name__ == '__main__':

    run(console)
    print ("-"*10 + "sleeping 5秒，以等待http_console" + "-"*10)
    time.sleep(5)
    print ("-"*10 +" sleeping 结束 " + "-"*10)
    app.run(host='127.0.0.1', port=1547)
