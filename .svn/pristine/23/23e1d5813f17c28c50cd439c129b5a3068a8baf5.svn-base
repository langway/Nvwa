#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    test_unicode 
Author:   fengyh 
DateTime: 2014/11/20 9:47 
UpdateLog:
1、fengyh 2014/11/20 Create this File.


"""

if __name__=='__main__':
    a = u'牛有腿什么有腿'
    print a.find(u'什么111')
    print "-------------code 1----------------"
    a = "和谐b你b可爱女人"
    print a
    print a.find("你")   #index=7,对于一般字符串,按照了指定的编码方式(这里为utf-8)
                        #并不像unicode字符串一样,把任何字符视为长度1,
                        #而是视为字节长度(7=3+3+1).
    b = a.replace("爱", "喜欢")
    print b
    print "--------------code 2----------------"
    x = "和谐b你b可爱女人"
    print a.find("你")#同----code 1----,index=7
    y = unicode(x) #此处将x解码(成字符串),如果有编码第二参数,应该和第一行指示编码相同
    print "直接print::",y
    print "若和指示编码不一样,以下两行有一行会打印乱码"
    print "UTF-8::",y.encode("utf-8")
    print "GB2312::",y.encode("gb2312")

    print y.find(u"你")  #index=3,因为unicode字符都视为1长度
    z = y.replace(u"爱", u"喜欢小")
    print "若和指示编码不一样,以下两行有一行会打印乱码"
    print z.encode("utf-8")
    print z.encode("gb2312")
    print "---------------code 3----------------"
    print "直接print::",y
    newy = unicode(x,"gb2312") #如果和指示编码行的指示不一样的话,将报错
    print newy
