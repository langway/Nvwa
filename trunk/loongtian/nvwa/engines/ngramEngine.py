#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.models.metaNet import MetaNet
from loongtian.nvwa.engines.engineBase import EngineBase

class NgramEngine(EngineBase):

    @staticmethod
    def loadNgramDictFromDB(NgramDict,NgramNum,memory=None):
        """
        加载数据库中所有的N元关系到内存中的NgramDict
        :return:allMetaNet
        """
        allMetaNet=MetaNet.getAllInDB(memory=memory)
        if not allMetaNet:
            return None
        # 加载到内存的NgramDict
        if isinstance(allMetaNet,list):
            for metaNetItem in allMetaNet:
                NgramEngine.loadNgramDictFromMetaNet(metaNetItem,NgramDict,NgramNum)
        elif isinstance(allMetaNet,MetaNet):
            NgramEngine.loadNgramDictFromMetaNet(allMetaNet,NgramDict,NgramNum)

        return allMetaNet

    @staticmethod
    def loadNgramDictFromChainBlocks(chain_blocks,ngramDict=None,gramNum=2):
        """
        记录字符块之间的二元、三元关系。
        公式说明：N元关系的传统计算公式：已知 “i” 一共出现了2533次,而其后出现 “want” 的情况一共有827次,所以P(want|i)=827/2533≈0.33。
        但由于存在数据稀疏性的问题（主要是样本总数不固定，是一个无限集合，未出现的情况未考虑），导致计算结果非常不准确（与训练数据集有关）
        原方案：总出现次数/总字符块数量，即p=n/m，计算结果为小数
                如果已经存在以前的二元关系，计算公式为：(p0+p1)/2
                这一方案的思路，是“域中存活”，即按有限样本数，出现的即为一个集合，然后计算。
                但这一方案的问题，是最后都会“趋同”，也就是如果训练集足够大，其出现概率会大体一致
        新方案（2018-05-26）：简单粗暴，每出现1次，就加1
        :param chain_blocks: 链式字符块列表[位置，字符，词频，是否元数据]
        :param ngramDict: n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）。
        :param gramNum: 指定进行二元、三元关系计算的“元数”,计算到第n元关系，即对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
                          二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解

        :return:
        """
        if ngramDict is None:
            ngramDict={}

        for cur_chain in chain_blocks:
            i=0
            chain_length=len(cur_chain)
            while i <chain_length-1: # 确保后面至少有一个字符块
                cur_block=cur_chain[i]
                cur_chars=cur_block[1]
                next_chars=None
                # while j<chain_length-1: # 确保后面至少有一个字符块
                #
                next_next_chars=None
                if gramNum==2 and i+1<chain_length:
                    next_block=cur_chain[i+1]
                    next_chars=next_block[1]  # 取得二元关系的字符块

                if gramNum==3 and i+2<chain_length:
                    next_next_block=cur_chain[i+2]
                    next_next_chars=next_next_block[1] # 取得三元关系的字符块
                # 开始记录字符串的N元关系
                NgramEngine.loadNgramDictByWords(cur_chars,next_chars,ngramDict,third = next_next_chars,gramNum=gramNum)

                i+=1

        return ngramDict

    @staticmethod
    def loadNgramDictFromMetaNet(metaNetItem,ngramDict=None,gramNum=2):
        """
        记录字符块之间的二元、三元关系。
        公式说明：N元关系的传统计算公式：已知 “i” 一共出现了2533次,而其后出现 “want” 的情况一共有827次,所以P(want|i)=827/2533≈0.33。
        但由于存在数据稀疏性的问题（主要是样本总数不固定，是一个无限集合，未出现的情况未考虑），导致计算结果非常不准确（与训练数据集有关）
        原方案：总出现次数/总字符块数量，即p=n/m，计算结果为小数
                如果已经存在以前的二元关系，计算公式为：(p0+p1)/2
                这一方案的思路，是“域中存活”，即按有限样本数，出现的即为一个集合，然后计算。
                但这一方案的问题，是最后都会“趋同”，也就是如果训练集足够大，其出现概率会大体一致
        新方案（2018-05-26）：简单粗暴，每出现1次，就加1
        :param chain_blocks: 链式字符块列表[位置，字符，词频，是否元数据]
        :param ngramDict: n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）。
        :param gramNum: 指定进行二元、三元关系计算的“元数”,计算到第n元关系，即对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
                          二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解

        :return:
        """
        if not isinstance(metaNetItem,MetaNet):
            raise Exception("参数错误！metaNetItem类型应为MetaNet")
        if ngramDict is None:
            ngramDict={}

        # 加载ChainItems
        metaNetItem.getChainItems()

        #  开始记录字符串的N元关系
        if gramNum<=2 and len(metaNetItem._s_chain_words)>=2:
            gramNum=2
            cur_chars=metaNetItem._s_chain_words[-2]
            next_chars=metaNetItem._s_chain_words[-1]
            NgramEngine.loadNgramDictByWords(cur_chars,next_chars,ngramDict,third = None,gramNum=gramNum)
        if gramNum>2 and len(metaNetItem._s_chain_words)>=3:
            gramNum=3
            cur_chars=metaNetItem._s_chain_words[-3]
            next_chars=metaNetItem._s_chain_words[-2]
            next_next_chars=metaNetItem._s_chain_words[-1]
            NgramEngine.loadNgramDictByWords(cur_chars,next_chars,ngramDict,third = next_next_chars,gramNum=gramNum)

        return ngramDict
    @staticmethod
    def loadNgramDictByWords(first,second,ngramDict=None,biweight=1.0,triweight=1.0,third=None,gramNum=2):
        """
        开始记录字符串的N元关系
        :param first: 第一个字符串
        :param second: 第二个字符串
        :param ngramDict: N元关系字典
        :param biweight: 二元关系的权重
        :param triweight: 三元关系的权重
        :param third: 第三个字符串
        :param gramNum: 记录的元数
        :return:
        """
        if ngramDict is None:
            ngramDict={}

        if not first or not second:
            return

        ngramRelation=ngramDict.get(first)
        # 二元、三元关系的关联度的计算公式为：总出现次数/总字符块数量，即p=n/m，计算结果为小数
        # 如果已经存在以前的二元关系，计算公式为：(p0+p1)/2
        if ngramRelation is None:
            ngramRelation={}
            ngramDict[first]=ngramRelation
            if gramNum==2 and second:
                ngramRelation[2]={second:biweight} # 二元关系
            if gramNum==3 and second and third:
                # ngramRelation[3]={second:{third:1.0/chain_length}} # 三元关系
                ngramRelation[3]={second:{third:triweight}} # 三元关系
        else:

            if gramNum==2 and second:
                bigram=ngramRelation.get(2) # 二元关系
                if bigram is None:
                    bigram={}
                    ngramRelation[2]=bigram
                # 计算二元关系的关联度
                # bigram.setdefault(second,1.0/chain_length)
                # bigram[second]=(bigram[second]+1.0/chain_length)/2
                if bigram.has_key(second):
                    bigram[second] += biweight
                else:
                    bigram[second]=biweight

            # 计算三元关系的关联度
            if gramNum==3 and second and third:
                trigram=ngramRelation.get(3) # 三元关系
                if trigram is None:
                    trigram={}
                    ngramRelation[3]=trigram
                # trigram.setdefault(second,{third:1.0/chain_length})
                # trigram.setdefault(second,{third:0})
                if trigram.has_key(second) :
                    if trigram[second].has_key(third):
                        # trigram[second][third]=(trigram[second][third]+1.0/chain_length)/2
                        trigram[second][third] += triweight
                    # trigram[second][third]=1.0/chain_length
                    else:
                        trigram[second][third]=triweight
                else:
                    trigram[second]={}
                    trigram[second][third]=triweight


        return ngramDict

    @staticmethod
    def loadNgramDictByMetaChain(metaChain,ngramDict=None,gramNum=2):
        """
        从元数据链加载NgramDic
        :param metaChain:
        :param ngramDict:
        :param gramNum:
        :return:
        """

        if not ngramDict:
            ngramDict={}
        for i in range(len(metaChain)-1): # 确保后面至少有一条
            cur_meta=metaChain[i]
            if isinstance(cur_meta,list): # 如果是一个meta的list，递归循环处理
                NgramEngine.loadNgramDictByMetaChain(cur_meta,ngramDict,gramNum)
                continue
            next_meta=metaChain[i+1]
            if isinstance(next_meta,list): # 如果是一个meta的list，递归循环处理
                NgramEngine.loadNgramDictByMetaChain(next_meta,ngramDict,gramNum)
                continue

            next_next_meta=None
            if i<len(metaChain)-2:
                next_next_meta=metaChain[i+2]
                if isinstance(next_meta,list): # 如果是一个meta的list，递归循环处理
                    NgramEngine.loadNgramDictByMetaChain(next_next_meta,ngramDict,gramNum)
                    next_next_meta=None

            cur_chars=cur_meta.mvalue
            next_chars=next_meta.mvalue
            next_next_chars=None
            if next_next_meta:
                next_next_chars=next_next_meta.mvalue
            # 开始记录其N元关系
            NgramEngine.loadNgramDictByWords(cur_chars,next_chars,ngramDict,third = next_next_chars,gramNum=gramNum)

            i+=1
        return ngramDict




# def loadNgramDictFromNgramItems(ngramItem,ngramDict=None,gramNum=2):
#     # ngramItem=ngramHelper()
#     ngramRelation=ngramDict.get(ngramItem.first)
#     # 二元、三元关系的关联度的计算公式为：总出现次数/总字符块数量，即p=n/m，计算结果为小数
#     # 如果已经存在以前的二元关系，计算公式为：(p0+p1)/2
#     if ngramRelation is None:
#         ngramRelation={}
#         ngramDict[ngramItem.first]=ngramRelation
#         if ngramItem.second:
#             # ngramRelation[2]={next_chars:1.0/chain_length} # 二元关系
#             ngramRelation[2]={ngramItem.second:ngramItem.biweight} # 二元关系
#
#             if gramNum==3 and ngramItem.third:
#                 # ngramRelation[3]={next_chars:{next_next_chars:1.0/chain_length}} # 三元关系
#                 ngramRelation[3]={ngramItem.second:{ngramItem.third:ngramItem.triweight}} # 三元关系
#     else:
#         bigram=ngramRelation.get(2) # 二元关系
#         trigram=ngramRelation.get(3) # 三元关系
#         if ngramItem.second:
#             if bigram is None:
#                 bigram={}
#                 ngramRelation[2]=bigram
#             # 计算二元关系的关联度
#             # bigram.setdefault(next_chars,1.0/chain_length)
#             # bigram[next_chars]=(bigram[next_chars]+1.0/chain_length)/2
#             if bigram.has_key(ngramItem.second):
#                 bigram[ngramItem.second] +=ngramItem.biweight
#             else:
#                 bigram[ngramItem.second]=ngramItem.biweight
#             # 计算三元关系的关联度
#             if gramNum==3 and ngramItem.third:
#                 if trigram is None:
#                     trigram={}
#                     ngramRelation[3]=trigram
#                 # trigram.setdefault(next_chars,{next_next_chars:1.0/chain_length})
#                 # trigram.setdefault(next_chars,{next_next_chars:0})
#                 if not trigram[ngramItem.second].has_key(ngramItem.third):
#                     # trigram[next_chars][next_next_chars]=1.0/chain_length
#                     trigram[ngramItem.second][ngramItem.third]=ngramItem.triweight
#                 else:
#                     # trigram[next_chars][next_next_chars]=(trigram[next_chars][next_next_chars]+1.0/chain_length)/2
#                     trigram[ngramItem.second][ngramItem.third] +=ngramItem.triweight


