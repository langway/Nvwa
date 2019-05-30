#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test_main 
Author:   fengyh 
DateTime: 2015/1/27 11:15 
UpdateLog:
1、fengyh 2015/1/27 Create this File.
2、                 将测试案例整合便于运行

"""
from unittest import TestSuite, TextTestRunner, TestLoader

from test.test_associatingEngine import TestAssociatingEngine
from test.test_associatingEngineSimple import TestAssociatingEngineSimple
from test.test_endTypeEnum import TestEndTypeEnum
from test.test_threshold_processing import TestThresholdProcessing


if __name__ == "__main__":
    # 构造测试集
    _test_case_list = []
    _test_case_list.append(TestLoader().loadTestsFromTestCase(TestAssociatingEngineSimple))
    _test_case_list.append(TestLoader().loadTestsFromTestCase(TestAssociatingEngine))
    _test_case_list.append(TestLoader().loadTestsFromTestCase(TestEndTypeEnum))
    _test_case_list.append(TestLoader().loadTestsFromTestCase(TestThresholdProcessing))
    # new test case append here

    suite = TestSuite(_test_case_list)

    # 执行测试
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)