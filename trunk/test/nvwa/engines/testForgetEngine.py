#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from loongtian.nvwa.engines.forgetEngine import ForgetEngine
import numpy as np
import matplotlib.pyplot as plt


class MyTestCase(TestCase):
    def setUp(self):
        print("----setUp----")

    def testGetThresholdByDifferenceDate(self):
        print("----testGetThresholdByDifferenceDate----")
        zero = ForgetEngine.getThresholdByDifferenceDate(0)
        one = ForgetEngine.getThresholdByDifferenceDate(1)
        forgetDay = ForgetEngine.getThresholdByDifferenceDate(ForgetEngine.FORGETDAY)
        forgerDayPlus = ForgetEngine.getThresholdByDifferenceDate(ForgetEngine.FORGETDAY+1)
        self.assertEquals(ForgetEngine.AMPLIFICATION, zero)
        self.assertEquals(ForgetEngine.AMPLIFICATION, one)
        self.assertEquals(0, forgetDay)
        self.assertEquals(0, forgerDayPlus)
        for i in range(1, ForgetEngine.FORGETDAY+1):
            print("{Day:%03d} ==> {Threshold:%0.2f}" % (i, ForgetEngine.getThresholdByDifferenceDate(i)))

    def testGetDifferenceDateByThreshold(self):
        print("----testGetDifferenceDateByThreshold----")
        negative = ForgetEngine.getDifferenceDateByThreshold(-1)
        zero = ForgetEngine.getDifferenceDateByThreshold(0)
        amplification = ForgetEngine.getDifferenceDateByThreshold(ForgetEngine.AMPLIFICATION)
        amplificationPlus = ForgetEngine.getDifferenceDateByThreshold(ForgetEngine.AMPLIFICATION+1)
        self.assertEquals(ForgetEngine.FORGETDAY, negative)
        self.assertEquals(ForgetEngine.FORGETDAY, zero)
        self.assertEquals(1, amplification)
        self.assertEquals(0, amplificationPlus)
        for i in range(1, int(ForgetEngine.AMPLIFICATION+2)):
            print("{Threshold:%.2f} ==> {Day:%d}" % (i, ForgetEngine.getDifferenceDateByThreshold(i)))

    def testDrawForget(self):
        day = np.linspace(1, 100, 100)
        threshold = ForgetEngine.AMPLIFICATION * day ** -ForgetEngine.POWER - ForgetEngine.CORRECTION * (day - 1)
        plt.plot(day, threshold, color="red", linewidth=2)
        forget = ForgetEngine.AMPLIFICATION * day ** -ForgetEngine.POWER
        plt.plot(day, forget, color="green", linewidth=2)
        plt.xlabel("Day")
        plt.ylabel("Threshold")
        plt.title("Forget")
        plt.show()

    def tearDown(self):
        print("----tearDown----")