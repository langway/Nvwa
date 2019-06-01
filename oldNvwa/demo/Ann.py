#!/usr/bin/env python
# coding: utf-8
"""
Project:  sourcecode
Title:    Ann 
Author:   fengyh 
DateTime: 2014/8/18 14:35 
UpdateLog:
1、fengyh 2014/8/18 Create this File.


"""

import numpy
import sys
import math
import pylab


class NueralNetwork:
    def __init__(self):
        b = 1
        self.learnRatio = 0.5
        self.trainData = numpy.array(
            [
                [b, 1, 3],
                [b, 2, 3],
                [b, 1, 8],
                [b, 2, 15],
                [b, 3, 7],
                [b, 4, 29],
                [b, 4, 8],
                [b, 4, 20]
            ])
        self.trainResult = numpy.array(
            [
                1,
                1,
                -1,
                -1,
                1,
                -1,
                1,
                -1
            ])
        self.weight = numpy.array(
            [
                b,
                0,
                0
            ])
        self.error = 0.001
        pass

    def out(self, v):
        """
        激活函数
        阈值为0
        :param v:
        :return:
        """
        if v >= 0:
            return 1
        else:
            return -1

    def except_signal(self, oldw, inx):
        """

        :param oldw:
        :param inx:
        :return:
        """
        ans = numpy.dot(oldw.T, inx)
        return self.out(ans)

    def train_once(self, oldw, inx, correct_result):
        """one training"""
        error = correct_result - self.except_signal(oldw, inx)
        new_weight = oldw + self.learnRatio * error * inx
        self.weight = new_weight
        return error

    def train_weight(self):
        """traing the weight of dataDict"""
        error2 = 1
        while error2 > self.error:
            i = 0
            error2 = 0
            for inx in self.trainData:
                error2 += abs(self.train_once(self.weight, inx, self.trainResult[i]))
                i += 1


    def drawTrainResult(self):
        """ draw graph of Result"""
        xor = self.trainData[:, 1]  # 切片，获取第一列，x坐标
        yor = self.trainData[:, 2]  # 切片，获取第二列，y坐标
        pylab.subplot(111)
        xMax = numpy.max(xor) + 15
        xMin = numpy.min(xor) - 5
        yMax = numpy.max(yor) + 50
        yMin = numpy.min(yor) - 5
        pylab.xlabel(u'xor')
        pylab.ylabel(u'yor')
        pylab.xlim(xMin, xMax)
        pylab.ylim(yMin, yMax)

        # draw point
        for i in range(0, len(self.trainResult)):
            if self.trainResult[i] == 1:
                pylab.plot(xor[i], yor[i], 'r*')
            else:
                pylab.plot(xor[i], yor[i], 'ro')


    def drawTestResult(self, data):
        test = data  # numpy.array(dataDict)
        if self.except_signal(self.weight, test) > 0:
            pylab.plot(test[1], test[2], 'b*')
        else:
            pylab.plot(test[1], test[2], 'bo')


    def drawTrueLine(self):
        """真实函数分界线"""
        xtest = numpy.array(range(0, 20))
        ytest = xtest * 2 + 1.68
        pylab.plot(xtest, ytest, 'g--')


    def showGraph(self):
        pylab.show()


testData = [[1, 5, 11], [1, 5, 12], [1, 4, 16], [1, 6, 7], [1, 3, 12], [1, 2, 22]]
neural = NueralNetwork()

print 'before study'
print 'init weight:'
print neural.weight
print 'test dataDict:'
for td in testData:
    print td
    print neural.except_signal(neural.weight, td)

neural.train_weight()

print 'after study'
print 'weight:'
print neural.weight
print 'test dataDict:'
for td in testData:
    print td
    print neural.except_signal(neural.weight, td)

neural.drawTrainResult()
# neural.drawTrueLine()
for test in testData:
    neural.drawTestResult(test)
neural.showGraph()
