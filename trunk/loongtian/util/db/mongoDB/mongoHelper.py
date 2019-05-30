#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'leon'
import subprocess
import os


def startMongoDBService():
    # bat_path=os.path.split(os.path.realpath(__file__))[0]
    # # bat_path+="\\2-启动MongoDB Service.bat"
    # bat_path="2-启动MongoDB Service.bat"
    # cmd = 'cmd.exe  "' + bat_path + '"'
    # cmd = "cmd.exe /c " + bat_path #+" abc"
    cmd="net start mongodb"
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)

    p.wait()
    for curline in p.stdout.readlines():
        curline=curline.rstrip("\r\n")
        if not curline=="":
            print(curline.decode("gbk"))

    # print(p.returncode)
    # os.system(bat_path)


if __name__=="__main__":
    import os

    # a = r"D:/test.bat"
    # a = os.path.sep.join(a.split(r'/'))
    # print a
    # os.system(a)

    startMongoDBService()