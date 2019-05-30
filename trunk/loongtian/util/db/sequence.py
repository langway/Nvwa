#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'CoolSnow'

class Sequence(object):
    """
    序列
    :rawParam
    :attribute
    """

    metaDataSequence = 0
    metaNetSequence = 0
    realObjectSequence = 0
    knowledgeSequence = 0
    instinctSequence = 0
    collectionSequence = 0

    @staticmethod
    def nextMetaData():
        Sequence.metaDataSequence += 1
        return Sequence.metaDataSequence

    @staticmethod
    def nextMetaNet():
        Sequence.metaNetSequence += 1
        return Sequence.metaNetSequence

    @staticmethod
    def nextRealObject():
        Sequence.realObjectSequence += 1
        return Sequence.realObjectSequence

    @staticmethod
    def nextKnowledge():
        Sequence.knowledgeSequence += 1
        return Sequence.knowledgeSequence

    @staticmethod
    def nextCollection():
        Sequence.collectionSequence += 1
        return Sequence.collectionSequence