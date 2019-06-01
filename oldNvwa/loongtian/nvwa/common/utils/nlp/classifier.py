#!/usr/bin/env python
# coding: utf-8
""" nlp
自然语言处理包
"""

import jieba
import re
import codecs

def split(word_list):
    '''
    _file = codecs.open("classifier.txt",'r')
    _list = []
    for line in _file:
        _list.append(line.strip('\n'))
    _r=""
    for item in _list:
        _r += ",'"+item+"'"
    print  _r
    '''

    _list = [u'帮', u'杯', u'本', u'笔', u'部', u'册', u'层', u'场', u'次', u'撮', u'代', u'袋',
             u'担', u'道', u'滴', u'顶', u'栋', u'肚子', u'段', u'堆', u'对', u'顿', u'朵', u'份',
             u'封', u'幅', u'副', u'杆', u'秆', u'个', u'根', u'股', u'挂', u'锅', u'盒', u'伙',
             u'集', u'家', u'架', u'间', u'件', u'截', u'句', u'棵', u'颗', u'口', u'块', u'捆',
             u'类', u'粒', u'脸', u'辆', u'摞', u'枚', u'名', u'盘', u'盆', u'捧', u'匹', u'片',
             u'篇', u'瓶', u'群', u'扇', u'勺', u'身', u'声', u'首', u'束', u'双', u'艘', u'所',
             u'台', u'滩', u'堂', u'套', u'挑', u'条', u'桶', u'头', u'碗', u'位', u'线', u'盏',
             u'张', u'章', u'阵', u'支', u'枝', u'只', u'种', u'幢', u'组', u'座', u'把']
    pattern = re.compile(u'([0123456789〇一二三四五六七八九十]+)([^0123456789〇一二三四五六七八九十]+)')

    _ret = []
    for item in word_list:
        match = pattern.match(item)
        if match and _list.__contains__(match.group(2)):
            _ret.append(match.group(1))
            _ret.append(match.group(2))
        else:
            _ret.append(item)
    return _ret


if __name__ == '__main__':
    seg_list = jieba.cut(u'牛有三只耳朵', False)
    print "/".join(seg_list)
    seg_list = jieba.cut(u'牛有三只耳朵', False)
    _ret = split(seg_list)
    print '/'.join(_ret)