#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    classifier.py 
Created by zheng on 2014/12/23.
UpdateLog:

"""

import math


class Translate:
    def __init__(self):
        self.UNITS = [u"", u"十", u"百", u"千", u"万", u"十", u"百", u"千", u"亿", u"十", u"百", u"千"]
        self.NUMS = [u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"]

        self.CN_NUM = {
            u'〇': 0,
            u'一': 1,
            u'二': 2,
            u'三': 3,
            u'四': 4,
            u'五': 5,
            u'六': 6,
            u'七': 7,
            u'八': 8,
            u'九': 9,

            u'零': 0,
            u'壹': 1,
            u'贰': 2,
            u'叁': 3,
            u'肆': 4,
            u'伍': 5,
            u'陆': 6,
            u'柒': 7,
            u'捌': 8,
            u'玖': 9,

            u'貮': 2,
            u'两': 2,
        }


        self.CN_UNIT = {
            u'十': 10,
            u'拾': 10,
            u'百': 100,
            u'佰': 100,
            u'千': 1000,
            u'仟': 1000,
            u'万': 10000,
            u'萬': 10000,
            u'亿': 100000000,
            u'億': 100000000,
            u'兆': 1000000000000,
        }


    def to_chinese(self, num):
        num = str(num.lstrip(u'0'))
        res = ''
        for p in xrange(len(num) - 1, -1, -1):
            r = int(int(num) / math.pow(10, p))
            res += self.NUMS[r % 10] + self.UNITS[p]
        for (i, j) in [(u'零十', u'零'), (u'零百', u'零'), (u'零千', u'零')]:
            res = res.replace(i, j)

        while res.find(u'零零') != -1:
            res = res.replace(u'零零', u'零')

        for (i, j) in [(u'零万', u'万'), (u'零亿', u'亿')]:
            res = res.replace(i, j)

        res = res.replace(u'亿万', u'亿')

        if res.startswith(u'一十'):
            res = res[2:]

        if res.endswith(u'零'):
            res = res[:-2]

        return res


    def to_number(self, cn):
        lcn = list(cn)
        unit = 0 #当前的单位
        ldig = []#临时数组
        while lcn:
            cndig = lcn.pop()
            if self.CN_UNIT.has_key(cndig):
                unit = self.CN_UNIT.get(cndig)
                if unit==10000:
                    ldig.append('w')    #标示万位
                    unit = 1
                elif unit==100000000:
                    ldig.append('y')    #标示亿位
                    unit = 1
                elif unit==1000000000000:#标示兆位
                    ldig.append('z')
                    unit = 1
                continue
            else:
                dig = self.CN_NUM.get(cndig)
                if unit:
                    dig = dig*unit
                    unit = 0
                ldig.append(dig)
        if unit==10:    #处理10-19的数字
            ldig.append(10)
        #print ldig #uncomment this line to watch the middle var.
        ret = 0
        tmp = 0
        while ldig:
            x = ldig.pop()
            if x=='w':
                tmp *= 10000
                ret += tmp
                tmp=0
            elif x=='y':
                tmp *= 100000000
                ret += tmp
                tmp=0
            elif x=='z':
                tmp *= 1000000000000
                ret += tmp
                tmp=0
            else:
                tmp += x
        ret += tmp
        return ret


    def strQ2B(self,ustring):
        """全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if inside_code == 12288:                              #全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
                inside_code -= 65248

            rstring += unichr(inside_code)
        return rstring

    def strB2Q(self,ustring):
        """半角转全角"""
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if inside_code == 32:                                 #半角空格直接转化
                inside_code = 12288
            elif inside_code >= 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
                inside_code += 65248

            rstring += unichr(inside_code)
        return rstring





if __name__ == '__main__':
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
        print Translate().to_number(cn)

    print(Translate().to_chinese('10005500010'))

    print Translate().strB2Q('mn2000')

    b = Translate().strQ2B(u"ｍｎ123abc博客园")
    print (u"ｍｎ123abc博客园")
    print b