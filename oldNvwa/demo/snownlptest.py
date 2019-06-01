#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    snownlp 
Author:   fengyh 
DateTime: 2014/9/24 13:45 
UpdateLog:
1、fengyh 2014/9/24 Create this File.


"""

def encode_utf8_print(list_str):
    if isinstance(list_str,list):
        print ','.join(list_str,)
    elif isinstance(list_str,str):
        print list_str.encode('utf-8')
    else:
        print list_str
    pass

from snownlp import SnowNLP
"""
中文分词（Character-Based Generative Model）
词性标注（TnT 3-gram 隐马）
情感分析（现在训练数据主要是买卖东西时的评价，所以对其他的一些可能效果不是很好，待解决）
文本分类（Naive Bayes）
转换成拼音（Trie树实现的最大匹配）
繁体转简体（Trie树实现的最大匹配）
提取文本关键词（TextRank算法）
提取文本摘要（TextRank算法）
tf，idf
Tokenization（分割成句子）
文本相似（BM25）
支持python3（感谢erning）
"""


s = SnowNLP(u'这个东西真心很赞')

encode_utf8_print(s.words)         # [u'这个', u'东西', u'真心',
                #  u'很', u'赞']

print(s.tags)          # [(u'这个', u'r'), (u'东西', u'n'),
                #  (u'真心', u'd'), (u'很', u'd'),
                #  (u'赞', u'Vg')]

encode_utf8_print(s.sentiments)    # 0.9769663402895832 positive的概率

encode_utf8_print(s.pinyin)        # [u'zhe', u'ge', u'dong', u'xi',
                #  u'zhen', u'xin', u'hen', u'zan']

s = SnowNLP(u'「繁體字」「繁體中文」的叫法在臺灣亦很常見。')

encode_utf8_print(s.han)           # u'「繁体字」「繁体中文」的叫法
                # 在台湾亦很常见。'

text = u'''
自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
所以它与语言学的研究有着密切的联系，但又有重要的区别。
自然语言处理并不是一般地研究自然语言，
而在于研制能有效地实现自然语言通信的计算机系统，
特别是其中的软件系统。因而它是计算机科学的一部分。
'''

s = SnowNLP(text)

encode_utf8_print(s.keywords(3))   # [u'语言', u'自然', u'计算机']

encode_utf8_print(s.summary(3))    # [u'因而它是计算机科学的一部分',
                #  u'自然语言处理是一门融语言学、计算机科学、
                #    数学于一体的科学',
                #  u'自然语言处理是计算机科学领域与人工智能
                #    领域中的一个重要方向']
encode_utf8_print(s.sentences)

s = SnowNLP([[u'这篇', u'文章'],
             [u'那篇', u'论文'],
             [u'这个']])
print(s.tf)
print(s.idf)
encode_utf8_print(s.sim([u'文章']))  # [0.3756070762985226, 0, 0]


