#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib as urllib
# import urllib2
import shelve


db = shelve.open('pinyin.db', 'c')

def lookup_pinyin(words):
    assert isinstance(words, str)
    if all(map(lambda w: w.encode('utf-8') in db, words)):
        return {char: db[char.encode('utf-8')] for char in words}
    url = "http://www.51windows.net/pages/pinyin.asp?"
    params = dict(txt=words.encode('gbk'),
                  pincolor='blue')
    req = urllib.request(url, urllib.urlencode(params))
    resp = urllib.request.urlopen(req)
    html = str(resp.read(), 'gbk').split('table')[1]
    html = re.sub(r'(<span class="h">.*?</span>)', '', html, flags=re.U)
    pattern = re.compile('<nobr>(.*?)</nobr><br>(.*?)</span>', re.U)
    matches = re.findall(pattern, html)
    ret = {k: v for v, k in matches}
    for k in ret:
        db[k.encode('utf-8')] = ret[k]
    return ret


def to_ping_ze(words):
    prouncations = lookup_pinyin(words)
    ret = []
    # u'áǎàóǒòéěèíǐìúǔùǘǚǜ'
    ze = u'ǎàǒòěèǐìǔùǚǜ'
    for char in words:
        is_ze = False
        p = prouncations.get(char, 'dmmy')
        for vowel in ze:
            if vowel in p:
                is_ze = True
                break
        ret.append(u'仄' if is_ze else u'平')

    return u''.join(ret)


if __name__ == '__main__':
    print (lookup_pinyin(u'你好啊'))
    print (to_ping_ze(u'旧事凭谁诉'))
