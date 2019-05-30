#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文本处理的帮助类
"""
__author__ = 'Leon'

# #第一种方法
# obj_list.sort(cmp=None, key=lambda x:x.salary, reverse=False)

# 第二种方法,更适合于大量数据的情况.
try:
    import operator
except ImportError:
    cmpfun= lambda x: x.probability # use a lambda if no operator module
else:
    cmpfun= operator.attrgetter("probability") # use operator since it's faster than lambda

from loongtian.util.common.generics import GenericsList

class SegmentedResults(GenericsList):
    """
    对很多字符串分割的结果（也可能是一个长字符串经过初分后进一步分割的结果）
    """

    def __init__(self,rawInput=None):
        super(SegmentedResults, self).__init__(SegmentedResult)
        self.rawInput=rawInput

    pass


class SegmentedResult:
    """
    对任意输入的字符串分割的结果
    """

    def __init__(self,rawInput):
        self.rawInput=rawInput
        self.bigramResult=[] # 二元的分解结果，是BlockChain的list
        self.trigramResult=[] # 三元的分解结果，是BlockChain的list
        self.curBigramResultIndex=0 # 当前未处理的二元字符块链的位置
        self.curTrigramResultIndex=0 # 当前未处理的三元字符块链的位置
        self.__calcBigramResult=False
        self.__calcTrigramResult=False

    @staticmethod
    def createSingleWordResult(word,position,isMeta,frequncy):
        """
        创建一个单字的分割结果。
        :param word:
        :param position:
        :param isMeta:
        :param frequncy:
        :return:
        """
        _segmentedResult=SegmentedResult(word)
        _cur_block=Block(word,position,isMeta,frequncy)
        cur_chain=BlockChain()
        cur_chain.chain.append(_cur_block)
        cur_chain.probability=frequncy
        _segmentedResult.bigramResult.append(cur_chain)
        return _segmentedResult

    def sortBigramResult(self):
        """
        对二元的分解结果进行排序（根据可能性）
        :return:
        """
        self.____calcBigramResult()
        self.bigramResult.sort(key=cmpfun, reverse=True)

    def ____calcBigramResult(self):
        """
        计算二元关系的probability（如果有一个probability是负数，都调整到正数）
        :return:
        """
        if self.__calcBigramResult:
            return
        step=1 # 如果有一个probability是负数，都调整到正数
        while SegmentedResult.__hasLessThenZero(self.bigramResult):
            for blockchain in self.bigramResult:
                blockchain.probability+=step

        for blockchain in self.bigramResult:
            blockchain.probability=blockchain.probability/(len(blockchain.chain)**2)
        self.__calcBigramResult=True

    def ____calcTrigramResult(self):
        """
        计算二元关系的probability（如果有一个probability是负数，都调整到正数）
        :return:
        """
        if self.__calcTrigramResult:
            return
        step=1 # 如果有一个probability是负数，都调整到正数
        while SegmentedResult.__hasLessThenZero(self.trigramResult):
            for blockchain in self.trigramResult:
                blockchain.probability+=step

        for blockchain in self.trigramResult:
            blockchain.probability=blockchain.probability/(len(blockchain.chain)**3)
        self.__calcTrigramResult=True


    @staticmethod
    def __hasLessThenZero(result):
        """
        判断是否有probability是负数
        :param result:
        :return:
        """
        for blockchain in result:
            if blockchain.probability<=0:
                return True

        return False



    def sortTrigramResult(self):
        """
        对三元的分解结果进行排序（根据可能性）
        :return:
        """
        self.____calcTrigramResult()
        self.trigramResult.sort(key=cmpfun, reverse=True)

    def getCurBigramBlockChain(self):
        """
        从二元结果中取得当前未处理的BlockChain
        :return:
        """
        if self.curBigramResultIndex<len(self.bigramResult):
            cur_block_chain= self.bigramResult[self.curBigramResultIndex]
            self.curBigramResultIndex +=1
            return cur_block_chain
        return None

    def getCurTrigramBlockChain(self):
        """
        从三元结果中取得当前未处理的BlockChain
        :return:
        """
        if self.curTrigramResultIndex<len(self.trigramResult):
            result= self.trigramResult[self.curTrigramResultIndex]
            self.curTrigramResultIndex +=1
            return result
        return None

    def restoreResultIndex(self):
        """
        重置索引，以便从0开始
        :return:
        """
        self.curBigramResultIndex = 0  # 当前未处理的二元字符块链的位置
        self.curTrigramResultIndex = 0  # 当前未处理的三元字符块链的位置

    def isNotSegmented(self):
        """
        判断是否根本没有能够进行分割（整句输入，整句输出）
        :return:
        """
        if len(self.bigramResult) == 1 and \
                len(self.bigramResult[0].chain) == 1 and \
                self.bigramResult[0].chain[0].isMeta==False and \
                self.bigramResult[0].chain[0].word==self.rawInput:
            return True
        return False


    def __repr__(self):
        _str="{<rawInput>:%s\n<bigramResult>:%s\n<trigramResult>:%s\n}" % (self.rawInput,str(self.bigramResult),str(self.trigramResult) )

        return _str

class BlockChain:
    """
    多个字符串在长字符串的链式信息（单词、起始位置,是否元数据，频率）
    """
    def __init__(self):
        self.chain=[] # 是Block的list
        self.probability=0.0


    def __repr__(self):
        _str="{<probability>:%s\n" % (self.probability)
        for block in self.chain:
            _str+= str(block) +"\n"

        _str +="}"
        return _str



class Block:
    """
    单个字符串在长字符串中的信息（单词、起始位置,是否元数据，频率）
    """

    def __init__(self,word,position,isMeta,frequncy):
        self.word=word # 匹配到的单词
        self.position=position# 起始位置
        self.isMeta=isMeta # 是否元数据
        self.frequncy=frequncy # 频率

        pass

    def __repr__(self):
        return "{<word>:%s, <position>:%s, <isMeta>:%s, <frequncy>:%s)}" % (self.word, self.position, str(self.isMeta),str(self.frequncy))

class ArticlesSegmentResults(dict):
    """
    文章列表的分割结果
    """
    pass


class ArticleSegmentResult():
    """
    文章的分割结果
    """

    def __init__(self,filename):
        self.filename=filename
        self.segmentedResults=SegmentedResults()

    def __repr__(self):
        return "<filename>:%s\n<segmentedResults>:%s" %(self.filename,str(self.segmentedResults))
