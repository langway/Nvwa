#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import codecs
import collections


counter = collections.defaultdict(int)

ignorence_chars = u'[，。（）{}·！？、●：|<>‘’“”:,t/]'
ignorence_pattern = re.compile(ignorence_chars, re.U)

single_cnt = collections.defaultdict(int)
double_cnt = collections.defaultdict(int)

for raw_line in codecs.open('./quan_song_ci.txt', 'r', 'utf-8', 'ignore'):
    line = raw_line.strip(u'　\r\n').encode('gbk', 'ignore').decode('gbk').replace(u'\u25a1', '')
    if not line or line == u'全宋词' or len(line) < 18:
        continue
    counter[len(line)] += 1
    segs = re.sub(ignorence_pattern, ' ', line).split()
    for seg in segs:
        for char in seg:
            single_cnt[char] += 1
        if len(seg) <= 1:
            continue
            #single_cnt[seg] += 1
        else:
            for i in range(len(seg)-1):
                word = seg[i:i+2]
                double_cnt[word] += 1
        import utils
        print (utils.to_ping_ze(seg),)


#    if u'十二' in line:
#        print line



#words = []

#for num, word in sorted((v, k) for k,v in single_cnt.items())[-100:]:
#    words.append(word)
#    print num, word

print words
