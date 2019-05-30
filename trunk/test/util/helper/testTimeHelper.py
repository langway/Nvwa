#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from unittest import TestCase
import loongtian.util.helper.timeHelper as TimeHelper


class TestTimeHelper(TestCase):

    date_time_now = datetime.datetime.now()
    def setUp(self):
        print("----setUp----")

    def testISOString2Time(self):
        print("----testISOString2Time----")
        time_back = TimeHelper.ISOString2Time('2006-04-12 16:46:40')
        print(time_back)

    def testTime2ISOString(self):
        print("----testTime2ISOString----")
        time_back = TimeHelper.Time2ISOString('23123123')
        print(time_back)

    def testIs_valid_date(self):
        print("----testIs_valid_date----")
        time_back = TimeHelper.is_valid_date('2312123')
        print('\'2312123\'Is_valid_date:', time_back)
        time_back = TimeHelper.is_valid_date('2006-04-12 16:46:40')
        print('\'2006-04-12 16:46:40\'Is_valid_date:', time_back)
        time_back = TimeHelper.is_valid_date('2006-047/12 136:46:40')
        print('\'2006-047/12 136:46:40\'Is_valid_date:', time_back)

    def testDateplustime(self):
        print("----testDateplustime----")
        time_back = TimeHelper.dateplustime('2006-04-12 16:46:40', 2)
        print(time_back)

    def testTime2sec(self):
        print("----testTime2sec----")
        time_back = TimeHelper.time2sec('2006-04-12 16:46:40')
        print(time_back)

    def testDateMinDate(self):
        print("----testDateMinDate----")
        time_back = TimeHelper.dateMinDate('2006-04-12 16:46:40', '2006-04-12 12:46:40')
        print(time_back)
        time_back = TimeHelper.dateMinDate('2006-04-12 16:46:40', '2006-04-12 16:46:38')
        print(time_back)
        time_back = TimeHelper.dateMinDate('2006-04-12 16:46:00', '2006-04-12 16:45:00')
        print(time_back)

    def tearDown(self):
        print("----tearDown----")
