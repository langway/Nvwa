#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase
import os
from loongtian.util.helper import fileHelper

class TestFileHelper(TestCase):
    path = fileHelper.getRealPath(__file__) # os.path.split(os.path.realpath(__file__))[0]


    def setUp(self):
        print("----setUp----")

    def testGetFilesInPath(self):
        print("----testGetFilesInPath----")
        for f in fileHelper.getFilesInPath(self.path):
            print(f)



    def testGetTree(self):
        print("----testGetTree----")
        for f in fileHelper.getTree(self.path):
            print(f['path'])
            if f['type'] == 'dire' and f['child'].__len__() > 0:
                for fc in f['child']:
                    print('--', fc['path'])

    def testGetTreePlane(self):
        print("----testGetTreePlane----")
        fh_data = fileHelper.getTreePlane(self.path)
        for f in fh_data:
            print('-'*int(f['depth']),f)
        print("-"*10 + "以下内容输出仅限文件"+"-"*10)
        for f in fh_data:
            if f['type']=='file':
                print(f)

    def tearDown(self):
        print("----tearDown----")

