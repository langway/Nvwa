#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import loongtian.util.helper.stringHelper as StringHelper


class TestStringHelper(TestCase):

    def setUp(self):
        print("----setUp----")

    def testIsStringNullOrEmpty(self):
        print("----testIsStringNullOrEmpty----")
        isString = StringHelper.IsStringNullOrEmpty(10)
        print('%s IsStringNullOrEmpty:'%10, isString)
        isString = StringHelper.IsStringNullOrEmpty('abcd')
        print('%s IsStringNullOrEmpty:'%'\'abcd\'', isString)
        isString = StringHelper.IsStringNullOrEmpty('')
        print('%s IsStringNullOrEmpty:'%'\'\'', isString)



    def testIsNotAStringOrStringEmpty(self):
        print("----testIsNotAStringOrStringEmpty----")
        isString = StringHelper.IsNotAStringOrStringEmpty(10)
        print('%s IsNotAStringOrStringEmpty:'%10, isString)
        isString = StringHelper.IsNotAStringOrStringEmpty('abcd')
        print('%s IsNotAStringOrStringEmpty:'%'\'abcd\'', isString)
        isString = StringHelper.IsNotAStringOrStringEmpty('')
        print('%s IsNotAStringOrStringEmpty:'%'\'\'', isString)


    def testConverUnicodeToString(self):
        print("----testConverUnicodeToString----???????????")
        unic_str = u'中国, 辽宁'.encode('utf-8')
        string_str = StringHelper.ConverUnicodeToString(unic_str)
        print(string_str)

    def testConverStringToUnicode(self):
        print("----testConverStringToUnicode----?????")
        unic_str = u'中国, 辽宁'
        string_str = StringHelper.ConverStringToUnicode(unic_str)
        print(string_str)

    def testConvertToNumber(self):
        print("----testConvertToNumber----")
        num_str = u'中国, 辽宁'
        string_str = StringHelper.ConvertToNumber(num_str)
        print(string_str, type(string_str))
        num_str = u'10'
        string_str = StringHelper.ConvertToNumber(num_str)
        print(string_str, type(string_str))
        num_str = u'12.333'
        string_str = StringHelper.ConvertToNumber(num_str)
        print(string_str, type(string_str))
        num_str = u'101416132131213121213'
        string_str = StringHelper.ConvertToNumber(num_str)
        print(string_str, type(string_str))

    def testIsFloat(self):
        print("----testIsFloat----")
        num_str = u'中国, 辽宁'
        string_str = StringHelper.is_float(num_str)
        print(num_str,'IsFloat:', string_str)
        num_str = u'10'
        string_str = StringHelper.is_float(num_str)
        print(num_str,'IsFloat:', string_str)
        num_str = u'12.333'
        string_str = StringHelper.is_float(num_str)
        print(num_str,'IsFloat:', string_str)
        num_str = u'101416132131213121213L'
        string_str = StringHelper.is_float(num_str)
        print(num_str,'IsFloat:', string_str)

    def testIsLong(self):
        print("----testIsLong----")
        num_str = u'中国, 辽宁'
        string_str = StringHelper.isLong(num_str)
        print(num_str,'IsLong:', string_str)
        num_str = u'10'
        string_str = StringHelper.isLong(num_str)
        print(num_str,'IsLong:', string_str)
        num_str = u'12.333'
        string_str = StringHelper.isLong(num_str)
        print(num_str,'IsLong:', string_str)
        num_str = u'101416132131213121213L'
        string_str = StringHelper.isLong(num_str)
        print(num_str,'IsLong:', string_str)

    def testIsKexue(self):
        print("----testIsKexue----")
        num_str = '2.0001e+12'
        string_str = StringHelper.isKexue(num_str)
        print(num_str,'IsKexue:', string_str)

    def testNumberConverter(self):
        test_dig = [u'九',
                u'十一',
                u'一百二十三',
                u'一千二百零三',
                u'一万一千一百零一',
                u'十万零三千六百零九',
                u'一百二十三万四千五百六十七',
                u'一千一百二十三万四千五百六十七',
                u'一亿一千一百二十三万四千五百六十七',
                u'一百零二亿五千零一万零一千零三十八',
                u'一千一百一十一亿一千一百二十三万四千五百六十七',
                u'一兆一千一百一十一亿一千一百二十三万四千五百六十七',
                ]
        for cn in test_dig:
            print(StringHelper.chineseNumeral_to_arabicNumeral(cn))

        print(StringHelper.arabicNumeral_to_chineseNumeral('16805500010'))

    def testQuanjiaoBanjiao(self):
        print(StringHelper.strB2Q('mn2000'))

        b = StringHelper.strQ2B(u"ｍｎ123abc博客园")
        print((u"ｍｎ123abc博客园"))
        print(b)



    def tearDown(self):
        print("----tearDown----")
