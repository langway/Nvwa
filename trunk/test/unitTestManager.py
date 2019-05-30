#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'
import unittest
import re
import os
import imp
from loongtian.util.helper import fileHelper

# def getTestModules(curPath):
#     """
#     取得当前路径中（包括子路径）所有以"test"开头，以.py为结尾的文件，并加载到模块列表。
#     """
#     modules={}
#
#     for item in os.listdir(curPath):
#         curItem=os.path.join( curPath,item)
#         #如果是文件，并且以"test"开头，以.py为结尾，加载之。
#         if os.path.isfile(curItem) and item.startswith('test') and item.endswith('.py'):
#             filenameToModuleName=os.path.splitext(item)[0]
#             loadedMod=imp.load_source(filenameToModuleName,curItem)
#             modules[curItem]=loadedMod
#             continue
#
#         if os.path.isdir(curItem):
#             #检查下一个目录下的测试文件
#             subModules=getTestModules(curItem)
#             modules.update(subModules )
#
#     return modules
#
#     pass#def getTestModules(files)

def testAllinCurrent():
    """
    取得当前路径中所有测试文件，并将其打包到TestSuite中，然后执行。
    """
    curPath=os.path.split(os.path.realpath(__file__))[0]
    # modules=getTestModules(curPath)
    from loongtian.util.helper import fileHelper
    files = fileHelper.getFilesInPath(curPath, "test", ".py")

    modules = fileHelper.loadPythonModules(files)

    for modpath,mod in modules.items():
        print ('{*********************** testing %s from %s ***********************}'%(mod.__name__,modpath))
        tests = unittest.defaultTestLoader.loadTestsFromModule(mod)
        result=unittest.TestResult()
        testSuite=unittest.TestSuite(tests)
        testSuite.run(result)
        print ('{*/*/*/*/*/*/*/*/*/*/*/* testing %s end */*/*/*/*/*/*/*/*/*/*/*}'%(mod.__name__))


    pass#def testAllinCurrent()


if __name__ == "__main__":
    # unittest.main(defaultTest="regressionTest")
    testAllinCurrent()
    # print testSuite
    # result=unittest.TestResult()
    # testSuite.start(result)

