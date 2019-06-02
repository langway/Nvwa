#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文本处理的帮助类
"""
__author__ = 'Leon'
from loongtian.nvwa.engines.ngramEngine import NgramEngine
from loongtian.nvwa.engines.segmentedResult import *
from loongtian.util.helper import stringHelper

# 需要忽略的组词开始字符
IgnorChars = [u"的"]
num_base = 0.1

def segmentWithStopMarks(rawInput, stopMarks, stopMarkLevel=3, keepStopMark=True):
    """
    取得根据标点符号分解出的句子。
    :param rawInput:输入的字符串。
    :param stopMarks: 标点符号的字典，包括0：段落标记:1：句子间标点符号:2：句子内标点符号
                      格式为：{标点符号:[标点符号类别,词频]}
    :param stopMarkLevel: 按标点符号的划分级别（0：段落级别，1：段落级别+句子级别，2：段落级别+句子级别+句内级别）。
    :param keepStopMark: 是否保留分割的标点（默认为True）
    :param StopMarksRexPattern: 已经加载的分解句子所需的标点符号正则pattern。
    :return:
    """
    # 检查参数
    if rawInput is None or len(rawInput) == 0:
        return []

    # 这里需要单独处理一个标点或字符的情况（无需分割）
    if len(rawInput) == 1:
        # if rawInput in StopMarks:
        return [rawInput]

    # return __segmentWithStopMarks_rex(rawInput,stopMarks, stopMarkLevel, keepStopMark,StopMarksRexPattern)
    return __segmentWithStopMarks(rawInput, stopMarks, stopMarkLevel, keepStopMark)


def __segmentWithStopMarks(rawInput, stopMarks, stopMarkLevel=3, keepStopMark=True):
    """
    按逐个标点符号分解输入
    :param rawInput:
    :param stopMarks:
    :param stopMarkLevel:
    :param keepStopMark:
    :param StopMarksRexPattern:
    :return:
    """
    splits = []
    i = 0
    if stopMarkLevel < 0:
        stopMarkLevel = 0

    cur_chars = u""
    while i < len(rawInput):
        cur_char = rawInput[i]
        if cur_char in stopMarks and stopMarks[cur_char][0] <= stopMarkLevel:
            # 特殊处理小数点（跟英文句号区分）
            is_radix_point = False
            if cur_char == u'.':
                if i > 0:
                    backward_char = rawInput[i - 1]
                    if stringHelper.is_number(backward_char):
                        forward_char = rawInput[i + 1]
                        if stringHelper.is_number(forward_char):
                            is_radix_point = True
            if not is_radix_point:  # 只有不是小数点，才可能是英文的句号
                if cur_chars:
                    splits.append(cur_chars)
                if keepStopMark:
                    splits.append(cur_char)
                cur_chars = u""
                i += 1
                continue

        cur_chars += cur_char
        i += 1
        if i == len(rawInput) and not cur_chars == u"":
            splits.append(cur_chars)

    return splits


def segmentWithNumbers(rawInput):
    """
    将输入字符串与数字分开
    :param rawInput:
    :return:
    """
    splits = []
    i = 0

    cur_chars = u""
    length = len(rawInput)
    while i < length:
        cur_char = rawInput[i]
        if stringHelper.is_number(cur_char):  # 如果是数字
            if not cur_chars == u"":
                splits.append(cur_chars)
                cur_chars = u""
            cur_chars += cur_char
            j = i + 1
            if j == length:  # 如果已经是最后一个了，直接停机
                break
            while j < len(rawInput):
                next_char = rawInput[j]
                if stringHelper.is_number(next_char):
                    cur_chars += next_char
                    i = j
                else:
                    splits.append(cur_chars)
                    cur_chars = u""
                    i = j
                    break
                j += 1

        else:
            cur_chars += cur_char
            if i == len(rawInput) - 1:
                splits.append(cur_chars)

            i += 1

    return splits


def segmentWithStopMarksAndNumbersAndEnglish(rawInput, stopMarks, stopMarkLevel=3, keepStopMark=True,
                                             splitWithSpace=False):
    """
    将输入字符串与标点符号、数字、英文分开
    :param rawInput:
    :param splitWithSpace:是否对空格进行分割
    :return:
    """
    return stringHelper.splitsWithStopMarksAndNumbersAndEnglish(rawInput, stopMarks, stopMarkLevel, keepStopMark,
                                                                splitWithSpace)


def __createSingleFrequancyDict(rawInputs, CachedSingleFrequancyDict=None):
    """
    根据输入的元字符串，创建单字-频率字典
    :param rawInputs:
    :param CachedSingleFrequancyDict:
    :return:_singleFrequancyDict,total_length
    """

    _singleFrequancyDict = {}

    if not CachedSingleFrequancyDict is None:
        _singleFrequancyDict = CachedSingleFrequancyDict

    # 检查参数
    if not rawInputs or len(rawInputs) == 0:  # 如果没有元输入，直接返回
        return _singleFrequancyDict, 0

    total_length = 0
    for rawInput in rawInputs:
        for c in rawInput:
            if c in _singleFrequancyDict:
                _singleFrequancyDict[c] += 1.0
            else:
                _singleFrequancyDict[c] = 1.0
        total_length += len(rawInput)

    return _singleFrequancyDict, total_length

    pass


def createDoubleFrequancyDict2(rawInputs, unknowns_tolerate_dgree=1.0):
    """
    根据输入的元字符串，创建双字-频率字典（在调用前应使用segmentWithStopMarksAndNumbersAndEnglish进行处理，得到的是应该是中文串、数字串、英文串）
    :param rawInputs: 元数据字符串（List），形式为：[元数据字符串,是否需要先学习]
    :param unknowns_tolerate_dgree: 对陌生事物的容忍度，由女娲的性格进行控制
    :return:doubleFrequancyDict,total_length
    """
    # 这里需要计算其占总字数的比率，作为最后取得的词频，其计算公式为：
    # tf = 总出现次数 * 对陌生事物的容忍度/总字数
    # idf = log(总输入句子数/出现某词的句子数,10) 底数是10
    # 词频= tf * idf
    # 这里引入的 对陌生事物的容忍度，由女娲的性格进行控制

    # 检查参数
    if rawInputs is None or not isinstance(rawInputs, list) or len(rawInputs) == 0:
        return None, 0

    doubleFrequancyDict = {}

    # 检查参数
    if not rawInputs or len(rawInputs) == 0:  # 如果没有元输入，直接返回
        return doubleFrequancyDict, 0

    total_length = 0
    doubleFrequancyDict_in_rawInputs = {}
    word_apperence_in_others_dict ={}
    for rawinput in rawInputs:
        # 这里应该是中文、数字串、英文串已经被分开的

        doubleFrequancyDict, length, doubleFrequancyDict_in_rawInput = __createDoubleFrequancyDictByRawInput2(rawinput,
                                                                                                             doubleFrequancyDict)
        doubleFrequancyDict_in_rawInputs[rawinput] = doubleFrequancyDict_in_rawInput
        total_length += length

    import math
    # 这里需要计算其占总字数的比率，作为最后取得的词频，其计算公式为：
    # tf = 单句总出现次数 * 对陌生事物的容忍度/单句总字数
    # idf = log((总输入句子数+1 )/出现某词的句子数,10) 底数是10，之所以+0.1，是避免出现idf=0的情况出现
    # 词频= tf * idf
    # 这里引入的 对陌生事物的容忍度，由女娲的性格进行控制

    # 0、总输入句子数
    # 去掉单字符、数字、标点符号等干扰
    rawinpt_num = len(rawInputs) + 0.1
    for rawinput in rawInputs:
        if len(rawinput) == 1:
            rawinpt_num -= 1
            continue
        elif stringHelper.is_number(rawinput):
            rawinpt_num -= 1
            continue
        elif stringHelper.is_stopmark(rawinput):
            rawinpt_num -= 1
            continue
    for rawinput, doubleFrequancyDict_in_rawInput in doubleFrequancyDict_in_rawInputs.items():
        for word, freq in doubleFrequancyDict_in_rawInput.items():
            tf = freq * unknowns_tolerate_dgree / len(rawinput)
            word_in_rawiput_num = 0
            for other_rawinput, other_doubleFrequancyDict_in_rawInput in doubleFrequancyDict_in_rawInputs.items():
                if word in other_doubleFrequancyDict_in_rawInput:
                    word_in_rawiput_num += 1

            idf = math.log( rawinpt_num/ (word_in_rawiput_num + num_base), 10)

            if not isinstance(word,str):
                word=stringHelper.converStringToUnicode(word)
            doubleFrequancyDict[word] = tf * idf

    return doubleFrequancyDict, total_length


def createDoubleFrequancyDict(rawInputs,unknowns_tolerate_dgree =1.0):
    """
    根据输入的元字符串，创建双字-频率字典（在调用前应使用segmentWithStopMarksAndNumbersAndEnglish进行处理，得到的是应该是中文串、数字串、英文串）
    :param rawInputs: 元数据字符串（List），形式为：[元数据字符串,是否需要先学习]
    :return:doubleFrequancyDict,total_length
    """
    # 检查参数
    if rawInputs is None or not isinstance(rawInputs, list) or len(rawInputs) == 0:
        return None, 0

    doubleFrequancyDict = {}

    # 检查参数
    if not rawInputs or len(rawInputs) == 0:  # 如果没有元输入，直接返回
        return doubleFrequancyDict, 0

    total_length = 0
    for rawinput in rawInputs:
        # 这里应该是中文、数字串、英文串分开的
        doubleFrequancyDict, length = __createDoubleFrequancyDictByRawInput(rawinput, doubleFrequancyDict)
        total_length += length

    # 这里需要计算其占总字数的比率，作为最后取得的词频，其计算公式为：
    # 总出现次数*字数/总字数
    for word, freq in doubleFrequancyDict.items():
        freq = freq * unknowns_tolerate_dgree / total_length
        doubleFrequancyDict[word] = freq

    return doubleFrequancyDict, total_length


def __createDoubleFrequancyDictByRawInput(rawInput,
                                          doubleFrequancyDict):
    """
    根据输入的元输入字符串，创建双字-频率字典
    :param rawInput:元输入字符串(这里应该是中文、数字串、英文串分开的)
    :param stopMarks:
    :param doubleFrequancyDict:
    :param stopMarkLevel:
    :param keepStopMark:是否保留分割的标点
    :return:doubleFrequancyDict,length
    """
    if doubleFrequancyDict is None:
        doubleFrequancyDict = {}

    # 2、根据字符串的的类型进行相应处理。包括：
    # 标点符号
    # 纯中文
    # 纯英文
    # 纯数字
    # OTHER=9 # 其他

    # 0、如果是标点符号，不进行处理，继续下一个，标点符号不参与总频率计算
    if rawInput in stringHelper.StopMarks:
        return doubleFrequancyDict, 0
    if stringHelper.is_all_alphabet(rawInput):  # 如果是英文（包含空格、标点等）
        engs = rawInput.split(u" ")  # 使用空格分割英文
        for eng in engs:
            if eng == u"" or eng == u" ":
                continue
            # 过滤掉前后的标点符号
            if len(eng) > 0:
                while eng[0] in stringHelper.StopMarks:
                    eng = eng[1::]
                while eng[-1] in stringHelper.StopMarks:
                    eng = eng[:-1:]

            # 过滤掉数字、空格、需要忽略的首字（例如：的）、标点符号，在理解过程中，将优先处理数字
            if stringHelper.is_number(eng) or eng in IgnorChars:
                continue
            if eng in doubleFrequancyDict:
                doubleFrequancyDict[eng] += 1.0
            else:
                doubleFrequancyDict[eng] = 1.0

        return doubleFrequancyDict, len(engs)
    elif stringHelper.is_all_chinese(rawInput):  # 如果是汉字（包含空格、标点等）

        length = len(rawInput)
        for i in range(length - 1):
            cur_char = rawInput[i]
            # 过滤掉数字、空格、需要忽略的首字（例如：的）、标点符号，在理解过程中，将优先处理数字
            if stringHelper.is_number(cur_char) or stringHelper.is_space(
                    cur_char) or cur_char in IgnorChars or cur_char in stringHelper.StopMarks:
                continue
            next_char = rawInput[i + 1]
            if stringHelper.is_number(next_char) or next_char in stringHelper.StopMarks:
                continue
            key = cur_char + next_char
            key = key.strip()  # 过滤掉空格
            if key == u"":
                continue
            if key in doubleFrequancyDict:
                doubleFrequancyDict[key] += 1.0
            else:
                doubleFrequancyDict[key] = 1.0


        return doubleFrequancyDict, length
    else:  # 数字串、其他不处理（目前未考虑阿拉伯文等）
        # todo 目前未考虑阿拉伯文等
        return doubleFrequancyDict, 0


def __createDoubleFrequancyDictByRawInput2(rawInput,
                                          doubleFrequancyDict):
    """
    根据输入的元输入字符串，创建双字-频率字典
    :param rawInput:元输入字符串(这里应该是中文、数字串、英文串分开的)
    :param stopMarks:
    :param doubleFrequancyDict:
    :param stopMarkLevel:
    :param keepStopMark:是否保留分割的标点
    :return:doubleFrequancyDict,length
    """
    if doubleFrequancyDict is None:
        doubleFrequancyDict = {}

    # 2、根据字符串的的类型进行相应处理。包括：
    # 标点符号
    # 纯中文
    # 纯英文
    # 纯数字
    # OTHER=9 # 其他
    doubleFrequancyDict_in_rawInput = {}
    # 0、如果是标点符号，不进行处理，继续下一个，标点符号不参与总频率计算
    if rawInput in stringHelper.StopMarks:
        return doubleFrequancyDict, 0, doubleFrequancyDict_in_rawInput
    if stringHelper.is_all_alphabet(rawInput):  # 如果是英文（包含空格、标点等）
        engs = rawInput.split(u" ")  # 使用空格分割英文
        for eng in engs:
            if eng == u"" or eng == u" ":
                continue
            # 过滤掉前后的标点符号
            if len(eng) > 0:
                while eng[0] in stringHelper.StopMarks:
                    eng = eng[1::]
                while eng[-1] in stringHelper.StopMarks:
                    eng = eng[:-1:]

            # 过滤掉数字、空格、需要忽略的首字（例如：的）、标点符号，在理解过程中，将优先处理数字
            if stringHelper.is_number(eng) or eng in IgnorChars:
                continue
            if eng in doubleFrequancyDict:
                doubleFrequancyDict[eng] += 1.0
            else:
                doubleFrequancyDict[eng] = 1.0
            if eng in doubleFrequancyDict_in_rawInput:
                doubleFrequancyDict_in_rawInput[eng] += 1.0
            else:
                doubleFrequancyDict_in_rawInput[eng] = 1.0
        return doubleFrequancyDict, len(engs), doubleFrequancyDict_in_rawInput
    elif stringHelper.is_all_chinese(rawInput):  # 如果是汉字（包含空格、标点等）

        length = len(rawInput)
        for i in range(length - 1):
            cur_char = rawInput[i]
            # 过滤掉数字、空格、需要忽略的首字（例如：的）、标点符号，在理解过程中，将优先处理数字
            if stringHelper.is_number(cur_char) or stringHelper.is_space(
                    cur_char) or cur_char in IgnorChars or cur_char in stringHelper.StopMarks:
                continue
            next_char = rawInput[i + 1]
            if stringHelper.is_number(next_char) or next_char in stringHelper.StopMarks:
                continue
            key = cur_char + next_char
            key = key.strip()  # 过滤掉空格
            if key == u"":
                continue
            if key in doubleFrequancyDict:
                doubleFrequancyDict[key] += 1.0
            else:
                doubleFrequancyDict[key] = 1.0

            if key in doubleFrequancyDict_in_rawInput:
                doubleFrequancyDict_in_rawInput[key] += 1.0
            else:
                doubleFrequancyDict_in_rawInput[key] = 1.0
        return doubleFrequancyDict, length, doubleFrequancyDict_in_rawInput
    else:  # 数字串、其他不处理（目前未考虑阿拉伯文等）
        # todo 目前未考虑阿拉伯文等
        return doubleFrequancyDict, 0, doubleFrequancyDict_in_rawInput


    pass  # def __createDoubleFrequancyDictByRawInput(rawInput,doubleFrequancyDict=None):


def extractRawMetaData(rawInputs, doubleFrequancyDict, threshold_ContinuousBlocks, CachedRawMetas=None, segment=False):
    """
    根据元输入，从metaNet根据阀值和元输入的位置提取元数据（可能有多个）
    :param rawInputs: 元输入，用以查找其关键字出现位置
    :param doubleFrequancyDict: 元数据网及其原始输入的长度，其格式为：({字符串:频率},total_length)
    :param threshold_ContinuousBlocks: 提取元数据的频率阀值（超过该阀值才提取），连续连接成词的阀值。
    :param segment:是否直接分割字符串。
    :return:1、WordFrequncyDict：最终取得的元数据，其格式为{元输入（字符串）:词频（平均值）}
             2、segmentedBlocks：最终取得的元数据匹配分割后的根据词频连接的输入字符串（字符块），格式为：
                {"北京举办新年音乐会真棒":[["北京举办",0,False],["新年音乐会",4,True],["真棒",9,False]]}
                含义为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}
    """
    # 检查参数
    if rawInputs is None or not isinstance(rawInputs, list):
        return
    if not doubleFrequancyDict:
        return None

    candidates_continuous = {}  # 连续连接成词的备选词列表，其格式为：{字符串:频率（平均值）}

    for k, v in doubleFrequancyDict.items():
        if v >= threshold_ContinuousBlocks:  # 连续连接成词的阀值判断其频率，如果频率高于阀值，添加到备选列表
            candidates_continuous[k] = v
    if len(candidates_continuous) == 0:  # 如果没有备选词列表
        return candidates_continuous, {}

    # 取得包含备选词的所有字符串，
    # 格式为{"新年音乐会中的音乐很动听":["音乐",2,8],["乐会",3,6],["音乐",7,8]}
    # 其含义为：关键字，起始位置，词频
    segmentedBlocks = []  # 最终取得的元数据匹配分割后的根据词频连接的输入字符串（字符块），格式为：
    new_rawMetas = {}  # 最终取得的元数据（单词字符串的形式）,其格式为{元输入（字符串）:词频（平均值）}
    for rawinput in rawInputs:
        rawinput = rawinput.strip()
        if rawinput == u"":
            continue

        segmentedInput = []  # 分解后的结果

        if stringHelper.is_all_alphabet(rawinput):  # 特殊处理英文
            has_key = False
            if rawinput in candidates_continuous:
                new_rawMetas[rawinput] = candidates_continuous[rawinput]
                has_key = True
            if segment:
                segmentedInput.append([rawinput, 0, has_key])
                # 添加到最终结果
                segmentedBlocks.append((rawinput, segmentedInput))
            continue

        word_position_frequency = __getWordPosition(candidates_continuous, rawinput)

        # {"北京举办新年音乐会":[["北京举办新年",0,False],["音乐会",6,True]]}
        # 含义为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}
        # 取得前后关联的两个词，输入：北京举办新年音乐会，结果["音乐会",6,7]，6为起始位置，7为所有匹配词（音乐+乐会）的词频
        connectedWords = __getConnectedWords(word_position_frequency)
        if not len(connectedWords) > 0:
            continue
        curIndex = 0

        for word, position, frequncy in connectedWords:
            # 如果是完整输入，相当于未识别，继续下一个
            if word == rawinput.strip():
                continue
            if not word in new_rawMetas:  # 这里面的frequncey只需要计算一次（其他循环都是相同的），所以不用考虑已经有该元数据的情况
                new_rawMetas[word] = frequncy

            # 取得输入字符串中包含的所有根据元数据分割后得到的字符串及其位置、是否是元数据
            # 结果为：{"北京举办新年音乐会":[["北京举办新年",0,False],["音乐会",6,True]]}
            # （格式为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}）
            if position > curIndex:
                if segment:
                    segmentedInput.append([rawinput[curIndex:position], curIndex, False])
                    segmentedInput.append([rawinput[position:position + len(word)], position, True])
                curIndex = position + len(word)
            elif position == curIndex:
                if segment:
                    segmentedInput.append([rawinput[position:position + len(word)], position, True])
                curIndex = position + len(word)
            else:
                raise Exception("位置给定错误！当前元数据：{0}，当前位置：{1}".format(word, str(position)))
        if segment:
            # 最后可能还会有尾巴，收秋
            if curIndex < len(rawinput):
                segmentedInput.append([rawinput[curIndex:len(rawinput)], curIndex, False])
            # 添加到最终结果
            segmentedBlocks.append((rawinput, segmentedInput))

    # # 【不再考虑】这里要避免将所有元输入直接作为元词块（一个重复的词块都没有）
    # for rawinput in rawInputs:
    #     segmentedBlock=segmentedBlocks.get(rawinput)
    #     if segmentedBlock and len(segmentedBlock)==1 and segmentedBlock[0][0]==rawinput:
    #         # 更改分割后的结果为：未识别
    #         segmentedBlock[0][2]=False
    #         return None,segmentedBlocks

    # 考虑到"音乐"+"乐会"的频率是叠加的，最后还需更新CachedRawMetas的实际频率
    if not CachedRawMetas is None:  # 如果要保存到当前已加载的元数据字典，添加
        for word, frequncy in new_rawMetas.items():
            if not frequncy:
                continue  # 如果freq为0，或是小于0，过滤掉（避免掉频）
            old_freq = CachedRawMetas.get(word)
            if old_freq:
                frequncy = frequncy + old_freq  # 2018-6-30 目前的方案为单纯累加，否则会出现前面已经非常高了，后面进来一个，突然下降。
                # (frequncy + old_freq)/2# 计算公式为：这里需要对其频率进行累加
            CachedRawMetas[word] = frequncy

    return new_rawMetas, segmentedBlocks

    # pass  def extractRawMetaData(doubleFrequancyDict,thresholds,referenceInputs):


def __getWordPosition(candidateWords, rawInput):
    """
    查找输入的字符串列表中所有包含某一字符串的字符串（提取元数据使用）
    :param candidateWords: 某一关键词的字符串
    :param rawInputs: 输入的字符串列表
    :return:当输入关键词"音乐"时，会产生的格式为{"新年音乐会中的音乐很动听":["音乐",2,8],["乐会",3,6],["音乐",7,8]}
    其含义为：关键字，起始位置，词频
    """
    word_position_frequency_list = []
    if stringHelper.is_all_alphabet(rawInput):  # 特殊处理英文
        splits = segmentWithStopMarksAndNumbersAndEnglish(rawInput, stopMarks=None, splitWithSpace=True)
        for i in range(len(splits)):
            key = splits[i]
            if key in candidateWords:
                word_position_frequency_list.append([key, i, candidateWords[key]])
            else:
                word_position_frequency_list.append([key, i, -1.0])

    else:
        for i in range(len(rawInput) - 1):
            key = rawInput[i:i + 2]
            if key in candidateWords:
                word_position_frequency_list.append([key, i, candidateWords[key]])

    return word_position_frequency_list
    pass  # def __getWordPositions(candidateWords, rawInputs):


def __getConnectedWords(word_position_frequency_list):
    """
    根据词频和顺序链接字符串（提取元数据使用）。
    :param word_position_frequency_list:
    :return:输入：北京举办新年音乐会，结果["新年音乐会",4,17]，4为起始位置，17为所有匹配词（新年+年音+音乐+乐会）的词频
    """
    proceed = []
    result = []
    length = len(word_position_frequency_list)
    for i in range(length):
        if proceed.__contains__(i):
            continue
        word, position, frequency = word_position_frequency_list[i]

        frequncy_num = 1
        for j in range(i + 1, length):
            if proceed.__contains__(j):
                continue
            nextword, nextposition, nextfrequency = word_position_frequency_list[j]

            if nextposition - position == j - i:  # 如果两者是相连的
                word += nextword[1]
                frequency += nextfrequency
                proceed.append(j)
                frequncy_num += 1

        # 前后相连的n个词块的共同频率的计算公式为：
        # （前词块频率+后词块频率）/n
        frequency = frequency / frequncy_num
        result.append([word, position, frequency])  # 添加到结果
        proceed.append(i)  # 标记为已处理

    return result


def loadChainCharFrequncyMetaDict(rawMetas, CachedChainCharMetaDict=None):
    """
    加载字符链字典。
    将{元输入：词频}的字典，转换成以每个字符作为索引，[True/False,meta,frequncy,{...}]为值，建立一个字典。
    :param WordFrequncyDict:{元输入：词频}的字典
    :param CachedChainCharMetaDict:已经加载的ChainCharMetaDict字典（默认为工作记忆区（WorkingMemory）中的ChainCharMetaDict）
    :return:以每个字符作为索引，[True/False,meta,frequncy,{...}]为值的字典，含义为：
    [是否字符块末尾，元字符串，频率，{后续子串字典}]
    例如：
    ddd={
        u"中":[False,"中",0.0,
            {u"央":[True,u"中央",5.4,{}],
            u"国":[True,u"中国",8.6,
                {u"人":[True,u"中国人",6.2,
                    {u"好":[True,u"中国人好",3.2,{}],
                    u"民":[True,u"中国人民",5.2,
                        {u"解":[False,None,0.0,
                            {u"放":[False,None,0.0,
                                {u"军":[True,u"中国人民解放军",6.2,{}]}]}],
                        u"法":[False,None,0.0,
                            {u"院":[True,u"中国人民法院",6.2,{}]}]}]}]}]}]}
    WordFrequncyDict={u"中国人民解放军":5.0,u"中国人民法院":5.0,u"中国人民":5.0,u"中国人好":5.0,u"中国人":5.0,u"中国":5.0,u"中央":5.0,}
    """

    if not CachedChainCharMetaDict is None:  # 如果给定了要保存到当前已加载的字符链字典字典
        cur_dict = CachedChainCharMetaDict
    else:
        cur_dict = {}

    if rawMetas is None or not isinstance(rawMetas, dict) or len(rawMetas) == 0:
        return cur_dict

    for mvalue, frequcy in rawMetas.items():
        # 从0开始嵌套循环以完成后续字符的索引
        __generateNextWordsDict(mvalue, frequcy, 0, cur_dict)

    return cur_dict


def __generateNextWordsDict(mvalue, frequcy, position, curDic):
    """
    嵌套循环（递归）以完成后续字符的索引（加载字符链字典使用）
    :param mvalue: 元输入
    :param frequcy : 词频
    :param position: 当前位置
    :param curDic: 当前正在使用的字典
    :return:以每个字符作为索引，[True/False,meta,frequncy,{...}]为值的字典，含义为：
    [是否字符块末尾，元字符串，频率，{后续子串字典}]
    """

    cur_char = mvalue[position]  # 取当前字符串

    cur_Child = curDic.get(cur_char, None)  # 查找是否有该字符的索引
    if cur_Child is None:  # 如果没有，创建，并添加到字典
        cur_Child = [False, cur_char, 0.0, {}]  # 如果是单字符，将在下一步进行更改，这里不进行判断
        curDic.setdefault(cur_char, cur_Child)

    if position == len(mvalue) - 1:  # 如果当前字符已经在最后一个，将尾部标识改为True，并记录该词，并返回
        cur_Child[0] = True
        cur_Child[1] = mvalue
        old_freq = cur_Child[2]

        if isinstance(old_freq, float):
            if isinstance(frequcy, float):
                if old_freq <= 0 or frequcy <= 0:  # 如果任一freq为0，或是小于0，过滤掉（不除以2，避免掉频）
                    frequcy = max(old_freq, frequcy)
                else:
                    frequcy = (old_freq + frequcy) / 2
            else:
                frequcy = float(old_freq)
        cur_Child[2] = frequcy
        return

    position += 1  # 增加位置计数器

    # 如果有后续字符（没到尾部），嵌套循环（递归）以完成后续字符的索引
    __generateNextWordsDict(mvalue, frequcy, position, cur_Child[3])


def segmentInputsWithChainCharMetaDict(rawInputs,
                                       chainChar_MetaDict,
                                       stopMarks=None,
                                       threshold_ContinuousBlocks=None,
                                       maxMatch=False,
                                       stopMarkLevel=3,
                                       keepStopMark=True,
                                       ngramDict=None,
                                       gramNum=2,
                                       splitWithStopMarksAndNumbersAndEnglish=True,
                                       memory=None):
    """
    根据元数据分割输入字符串（列表）。metaInputs必须是unicode编码
    :param rawInputs: 输入的字符串（列表），必须是unicode编码，格式为：[输入待处理的字符串，是否需要先学习]
    :param chainChar_MetaDict: （元组）链式元数据字典+元数据字典。以每个字符作为索引，[True/False,meta,frequncy,{...}]为值的字典，含义为：
    [是否字符块末尾，元数据字符串，频率，{后续子串字典}]
    :param ngramDict: n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）。
    :param gramNum: 指定进行二元、三元关系计算的“元数”,对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
                      二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解
    :param stopMarks: 标点符号的字典。
    :param maxMatch: 是否最大匹配，默认为True，系统只输出一条结果，如果设置为False，系统将输出全部结果。
    :param stopMarkLevel: 按标点符号的划分级别（0：段落级别，1：段落级别+句子级别，2：段落级别+句子级别+句内级别）。
    :param keepStopMark: 是否保留分割的标点。
    :return:以输入的字符串为键，以分隔后的字符块链列表为值的字典。
    """
    segments = SegmentedResults()  # 最终的结果
    if not rawInputs or not isinstance(rawInputs, list):
        return segments
    if not chainChar_MetaDict:
        return segments

    for rawInput in rawInputs:  # 循环，并把每句的分割列表添加到结果中
        _segmentedResult = segmentInputWithChainCharMetaDict(rawInput,
                                                             chainChar_MetaDict, stopMarks,
                                                             threshold_ContinuousBlocks,
                                                             maxMatch, stopMarkLevel,
                                                             keepStopMark, ngramDict, gramNum,
                                                             splitWithStopMarksAndNumbersAndEnglish,
                                                             memory=memory)
        if not _segmentedResult is None:
            segments.append(_segmentedResult)

    return segments


def segmentInputWithChainCharMetaDict(rawInput,
                                      chainCharMetaDict,
                                      stopMarks=None,
                                      threshold_ContinuousBlocks=None,
                                      maxMatch=False,
                                      stopMarkLevel=3,
                                      keepStopMark=True,
                                      ngramDict=None,
                                      gramNum=2,
                                      splitWithStopMarksAndNumbersAndEnglish=True,
                                      filterSingle=True,
                                      resegmentWithUnknowns=True,memory=None):
    """
    根据元数据分割输入字符串（列表）-根据链接字符词典进行匹配（有两种：最长顺序匹配、全部最可能匹配）。
    分解的顺序为：
    一、处理段落（todo：可能会以词频的方式处理）
    二、按标点符号分解句子（todo：可能会以词频的方式处理）
    三、匹配及分解
        （一）最长顺序匹配
        （二）全部最可能匹配
        1、所有词的匹配
        2、删除不可能（按天然连接顺序）
        3、取得链表
        4、按可能性排序
    :param rawInput: 输入的字符串，metaInput必须是unicode编码
    :param chainChar_MetaDict: （元组）链式元数据字典+元数据字典。以每个字符作为索引，[True/False,meta,frequncy,{...}]为值的字典，含义为：
    [是否字符块末尾，元数据字符串，频率，{后续子串字典}]
    :param ngramDict: n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）。
    :param gramNum: 指定进行二元、三元关系计算的“元数”,对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
                      二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解:param stopMarks: 标点符号的字典。
    :param maxMatch: 是否最大匹配，默认为True，系统只输出一条结果，如果设置为False，系统将输出全部结果。
    :param processInputsToMetas: 是否将输入的字符串转换为元数据
    :param stopMarkLevel: 按标点符号的划分级别（0：段落级别，1：段落级别+句子级别，2：段落级别+句子级别+句内级别）。
    :param keepStopMark: 是否保留分割的标点。
    :param filterSingle: 是否应该过滤掉单字词（在初分阶段应该过滤，但如果使用未知元数据对其他元数据再次精分，应该使用）
    :return:以输入的字符串为键，以分隔后的字符块链列表为值的字典。
    """
    if not rawInput:
        return None
    if not isinstance(rawInput, str):
        raise AttributeError("元输入必须是string类型！" + str(rawInput))
    rawInput = rawInput.strip()
    if rawInput == u"" or len(rawInput) == 0:
        return SegmentedResult.createSingleWordResult(rawInput, 0, True, 1.0)

    # # 0、先期处理段落及标点符号
    # splitByExecutable= segmentWithStopMarks(rawInput,stopMarks)
    # if len(splitByExecutable) > 1:  # 如果包含数字、英文、标点符号
    #     return segmentInputsWithChainCharMetaDict(splitByExecutable, chainCharMetaDict,stopMarks,threshold_ContinuousBlocks,maxMatch,stopMarkLevel ,keepStopMark,ngramDict,gramNum)

    # 1、提取标点，将标点、数字串、英文与字符串分开
    if splitWithStopMarksAndNumbersAndEnglish:
        splits = segmentWithStopMarksAndNumbersAndEnglish(rawInput, stopMarks)
        if len(splits) > 1:  # 如果包含数字、英文、标点符号
            segments = segmentInputsWithChainCharMetaDict(splits, chainCharMetaDict, stopMarks,
                                                          threshold_ContinuousBlocks, maxMatch, stopMarkLevel,
                                                          keepStopMark, ngramDict, gramNum, False)
            segments.rawInput = rawInput
            return segments

    # 2、如果是数字、标点符号，不再进行分割，直接返回结果
    if stringHelper.is_number(rawInput) or stringHelper.is_stopmark(rawInput):
        return SegmentedResult.createSingleWordResult(rawInput, 0, True, 1.0)

    elif len(rawInput) == 1:  # 处理单字
        cur_block_info = chainCharMetaDict.get(rawInput)
        is_meta = False
        freq = -1.0
        if cur_block_info:
            is_meta = cur_block_info[0]
            freq = cur_block_info[2]

        return SegmentedResult.createSingleWordResult(rawInput, 0, is_meta, freq)

    # 3、如果是英文，进行分割，然后返回结果
    elif stringHelper.is_all_alphabet(rawInput):
        cur_chain = BlockChain()
        _segmentedResult = SegmentedResult(rawInput)
        _segmentedResult.bigramResult.append(cur_chain)

        eng_strs = rawInput.split(u" ")  # 使用空格分割英文
        i = 0
        for eng_str in eng_strs:
            cur_dict = chainCharMetaDict
            j = 0
            cur_meta_info = None
            for eng_char in eng_str:  # 对chainCharMetaDict进行完全遍历，找到完全匹配的元数据信息
                if eng_char in cur_dict:
                    cur_meta_info = cur_dict.get(eng_char)
                    if cur_meta_info:
                        cur_dict = cur_meta_info[3]
                        j += 1
                    else:
                        break

            if cur_meta_info and j == len(eng_str):  # 找到了完全匹配的单词
                # 格式为：[字符串,位置,词频，是否元数据]
                cur_block = Block(eng_str, i, True, cur_meta_info[2])
            else:  # 未能完成全部字符串的遍历，说明未找到该单词
                # 格式为：[位置,字符串,词频，是否元数据]
                cur_block = Block(eng_str,i,  False, -1.0)
            cur_chain.chain.append(cur_block)

            i += 1

        return _segmentedResult

    # 4、现在这里肯定是单句（单字）了，匹配及分解
    if maxMatch:  # 最长顺序匹配
        return __segmentInputByMaxMatch(rawInput, chainCharMetaDict, 0, 0, resegmentWithUnknowns=resegmentWithUnknowns)
    else:  # 全部最可能匹配（目前使用）
        return __segmentInputByAll(rawInput, chainCharMetaDict, ngramDict, gramNum, filterSingle,
                                   resegmentWithUnknowns=resegmentWithUnknowns,memory=memory)


def __segmentInputByAll(rawInput,
                        chainChar_MetaDict,
                        ngramDict=None,
                        gramNum=2,
                        filterSingle=True,
                        resegmentWithUnknowns=True,
                        memory=None):
    """
    [核心程序]根据元数据分割输入字符串（列表）-根据链接字符词典进行匹配（全部最可能匹配）
    :param rawInput:输入的字符串（列表），meta必须是unicode编码
    :param chainCharMetaDict:以每个字符作为索引，[True/False,{...},meta,frequncy]为值的字典，含义为：
    [是否字符块末尾，{后续子串字典}，元数据字符串，频率]
    :param ngramDict: n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）。
    :param gramNum: 指定进行二元、三元关系计算的“元数”,对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
                      二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解
    :param filterSingle: 是否应该过滤掉单字词（在初分阶段应该过滤，但如果使用未知元数据对其他元数据再次精分，应该使用）
    :return:所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
                  [
                  [["音乐会",0,True,8.5],["很好",3,False,-1.0]]
                  [["音乐",0,True,3.2],["会",2,False,-1.0],["很好",3,False,-1.0]]
                  ]
                  每条记录的格式应为：[[word,i,True/False,frequncy]]其含义为：[匹配到的单词，起始位置,是否元数据，频率]的列表
                  如果不是元数据，默认频率为-1.0
                  中国人民法院有司法权中央"可以分解为下面的possibleMetas
    possibleMetas=[
        [[0,u"中国人民法院",5.5,True],[0,u"中国人民",7.0,True],[0,u"中国人",8.5,True],[0,u"中国",9.8,True],],
        [[1,u"国人",4.0,True],],
        [[2,u"人民",8.1,True],[2,u"人民法院",4.3,True],],
        [[3,u"民法",6.3,True],[3,u"民法院",3.2,True],],
        [[4,u"法院",8.7,True],],
        [[6,u"有司",2.4,True],[6,u"有",9.9,True],],
        [[7,u"司法权",6.4,True],[7,u"司法",8.5,True],],
        [[8,u"法权",2.5,True],],
        [[10,u"中央",8.0,True],],
    ]
    拼接为线性字符块，如：
    chainBlocks=[
        [[u"中国人民法院",5.5,True,0],[u"有司",2.4,True,6],[u"法权",2.5,True,8],[u"中央",8.0,True,10],],
        [[u"中国人民法院",5.5,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人民法院",5.5,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],[u"中央",8.0,True],],
        [[u"中国人民",7.0,True],[u"法院",8.7,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国人民",7.0,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人民",7.0,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法院",3.2,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法院",3.2,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法院",3.2,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法",6.3,True],[u"院",-1.0,False],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法",6.3,True],[u"院",-1.0,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法",6.3,True],[u"院",-1.0,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民法院",4.3,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民法院",4.3,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民法院",4.3,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民",8.1,True],[u"法院",8.7,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民",8.1,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民",8.1,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
    ]
    含义为：
    [分出的字符块，词频，是否元数据，起始位置]
    """
    # 全部最可能匹配
    #     1、所有词的匹配
    #     2、取得链表（删除不可能，按天然连接顺序）
    #     3、按可能性排序
    #     4、
    # segmentedResult=[] # 所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
    # [
    # [["音乐会",0,True,8.5],["很好",3,False,-1.0]]
    # [["音乐",0,True,3.2],["会",2,False,-1.0],["很好",3,False,-1.0]]
    # ]
    # 每条记录的格式应为：[[word,i,True/False,frequncy]]其含义为：[匹配到的单词，起始位置,是否元数据，频率]的列表
    # 如果不是元数据，默认频率为-1.0

    # 1、根据元数据字典匹配所有的可能的元数据，所有词的匹配（为避免过多匹配，过滤单字词、数字）
    possibleMetas = __getAllPossibleMetas(rawInput, chainChar_MetaDict, filterSingle)

    if not possibleMetas: # 如果没有匹配的元数据，可能是由于过滤单字词导致的
        possibleMetas = __getAllPossibleMetas(rawInput, chainChar_MetaDict, filterSingle=False)
    # 2、根据所有的可能的元数据取得链表
    chain_blocks = __getChainBlocksWithPossibleMetas(possibleMetas, 0)

    if not chain_blocks:
        # 这种情况是真的不识别了
        return SegmentedResult.createSingleWordResult(rawInput, 0, False, -1.0)

    # 3、如果有未识别，整合到一起（这时要检查单字符，如果存在，替换现有频率、是否已知等参数，直接整合在一起，）
    integrated_chain_blocks, unknowns_dict = __getIntegratedChainBlocks(rawInput, chain_blocks, chainChar_MetaDict,getUnknownSingleWord=True)

    if resegmentWithUnknowns and unknowns_dict:
        resegmented_chain_blocks_with_unknowns = __resegmentChainBlocksWithUnknowns(integrated_chain_blocks, unknowns_dict,memory)
        if resegmented_chain_blocks_with_unknowns:
            integrated_chain_blocks = []
            for resegmented_chain_block_with_unknowns in resegmented_chain_blocks_with_unknowns:  # 只拆一层
                for resegmented_chain_with_unknowns in resegmented_chain_block_with_unknowns:
                    integrated_chain_blocks.append(resegmented_chain_with_unknowns)

    # 4、去除重复的
    cleaned_chain_blocks = __cleanDuplicatedChainBlocks(integrated_chain_blocks, rawInput)

    # 5、记录字符块之间的二元、三元关系
    NgramEngine.loadNgramDictFromChainBlocks(cleaned_chain_blocks, ngramDict)

    # 6、按词频、二元（三元）关系可能性排序
    # 传统的可能性（路径L的概率[路径依赖]）计算公式为：
    # 【二元】P(L) = P(w2|w1) * P(w3|w2) * P(w4|w3) *……* P(wk|w(k-1))*P(w1) * P(w2) * P(w3)…… * P(wk)
    # 【三元】P(L) = P(w3|w1w2) * P(w4|w3w2) * P(w5|w4w3) *……* P(wk|w(k-2)w(k-1))*P(w1) * P(w2) * P(w3)…… * P(wk)
    # 这里考虑以下几点：
    # 当前元数的可能性，应与该元数关系的可能性正相关，与该元数所包含字符块的可能性之和正相关，而不应仅仅是乘积关系
    # 而各字符链的可能性之间的关系，应该是累加的
    # 如果全部已知，还应增加可能性
    # 同时，这种概率还与词块的长度正相关，实际词频应该为：词块词频*词块长度
    # 所以，这里将上述公式修改为：
    # 【二元】P(L) = P(w2|w1) * （P(w1)*len(w1) + P(w2)*len(w2)） +
    #                P(w3|w2) * （P(w2)*len(w2) + P(w3)*len(w3)）+ …… +
    #                P(wk|w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1))
    # 【三元】P(L) = P(w3|w1w2) * （P(w1)*len(w1) + P(w2)*len(w1)+ P(w3)*len(w3)） +
    #                P(w4|w2w3) * （P(w2)*len(w2) + P(w3)*len(w3)+ P(w4)*len(w4)）+ …… +
    #                P(wk|w(k-2)w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)+P(w(k-2)*len(wk-2))
    # 另外，要避免分词多反而造成可能性大的情况，所以要对可能性进行加权平均
    # 【二元】P(L) = (P(w2|w1) * （P(w1)*len(w1) + P(w2)*len(w2)） +
    #                P(w3|w2) * （P(w2)*len(w2) + P(w3)*len(w3)）+ …… +
    #                P(wk|w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)))/(k-1)
    # 【三元】P(L) = P(w3|w1w2) * （P(w1)*len(w1) + P(w2)*len(w1)+ P(w3)*len(w3)） +
    #                P(w4|w2w3) * （P(w2)*len(w2) + P(w3)*len(w3)+ P(w4)*len(w4)）+ …… +
    #                P(wk|w(k-2)w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)+P(w(k-2)*len(wk-2))/(k-2)
    _segmentedResult = __sortSegmentedResultByNgram(rawInput, cleaned_chain_blocks, ngramDict, gramNum)

    # 返回结果
    return _segmentedResult


def __getAllPossibleMetas(rawInput, chainCharMetaDict, filterSingle=True):
    """
    根据元数据字典匹配所有的可能的元数据（为避免过多匹配，过滤单字词）
    :param rawInput:
    :param chainCharMetaDict:
    :param filterSingle: 是否应该过滤掉单字词（在初分阶段应该过滤，但如果使用未知元数据对其他元数据再次精分，应该使用）
    :return:[起始位置，该起始位置所有匹配的结果([匹配的词块，频率，是否词块])]
    "中国人民法院系红旗有司法权中央"可以分解为：
    possibleMetas=[
        [0,[[u"中国人民法院",5.5,True],[u"中国人民",7.0,True],[u"中国人",8.5,True],[u"中国",9.8,True],]],
        [1,[[u"国人",4.0,True],]],
        [2,[[u"人民",8.1,True],[u"人民法院",4.3,True],]],
        [3,[[u"民法",6.3,True],[u"民法院",3.2,True],]],
        [4,[[u"法院",8.7,True],]],
        [9,[[u"有司",2.4,True],]],
        [10,[[u"司法权",6.4,True],[u"司法",8.5,True],]],
        [11,[[u"法权",2.5,True],]],
        [13,[[u"中央",8.0,True],]],
    ]
    """
    if not isinstance(chainCharMetaDict, dict):
        return

    possibleMetas = []

    # 2、取得字符串的类型。包括：
    # PURE_CHINESE=0 # 纯中文
    # PURE_ENGLISH=1 # 纯英文
    # PURE_NUMBERS=2 # 纯数字
    # CHINESE_ENGLISH=3 # 中英文混合
    # CHINESE_NUMBERS=4 # 中文数字混合
    # ENGLISH_NUMBERS=5 # 英文数字混合
    # CHINESE_ENGLISH_NUMBERS=6 # 中文英文数字混合
    # OTHER=9 # 其他
    for i in range(len(rawInput)):
        cur_meta_input = rawInput[i:]
        currentBlocks = []
        __getCurrentBlocksFromChainCharMetaDict(cur_meta_input, 0, chainCharMetaDict, currentBlocks, filterSingle)
        # cur_char_in_list = False
        blockList = []
        for block in currentBlocks[::-1]:  # 根据最大匹配需要，这里进行倒序处理
            # 格式为：[位置,字符串,词频，是否元数据]
            blockList.append([i, block[1], block[2], block[0]])
        if len(blockList):
            possibleMetas.append(blockList)

    return possibleMetas


def __getIntersectMetas(possibleMeta, possibleMetas):
    """
    取得相交的元数据，例如：国人-人民，有司-司法，有司-司法权，中间有相交的部分
    :param possibleMetas:
    :return:
    """
    result = {}

    for positionedMeta in possibleMeta:
        start = positionedMeta[0]
        end = start + len(positionedMeta[1]) - 1
        next_start = start + 1
        intersect_list = []
        while next_start <= end:
            next_possibleMeta = __getPossibleMetasByCharPos(possibleMetas, next_start)
            next_start += 1
            if next_possibleMeta:
                for metaInfo in next_possibleMeta:
                    next_end = metaInfo[0] + len(metaInfo[1]) - 1
                    if next_end > end:
                        intersect = [positionedMeta, metaInfo]
                        intersect_list.append(intersect)
        if len(intersect_list):
            result[positionedMeta[1]] = intersect_list

    return result


def __getCurrentBlocksFromChainCharMetaDict(currentMetaInput, cur_position, curDict, currentBlocks, filterSingle=False):
    """
    取得元输入中最长匹配的链接字符块的路径。
    :param currentMetaInput:
    :param cur_position:
    :param curDict:
    :param currentBlocks:
    :param filterSingle: 是否应该过滤掉单字词（在初分阶段应该过滤，但如果使用未知元数据对其他元数据再次精分，应该使用）
    :return:
    """
    if cur_position == len(currentMetaInput):  # 如果已经是最后一个了，直接返回
        return

    cur_char = currentMetaInput[cur_position]
    cur_Child = curDict.get(cur_char)

    if cur_Child is None:  # 未登录词
        return

    # 这里过滤掉非元数据及单个字符
    if cur_Child[0] == True:
        if len(cur_Child[1]) == 1 and filterSingle:  # 根据最大匹配原则，如果能够跟后面的不成词，就不过滤
            try:
                next_char = currentMetaInput[cur_position + 1]  # 有可能取不到导致错误
                next_child = cur_Child[3].get(next_char)
                if next_child:
                    if filterSingle:
                        if len(cur_Child[1]) > 1:  # or len(currentMetaInput)==1:
                            currentBlocks.append(cur_Child)
                else:
                    currentBlocks.append(cur_Child)
            except:
                pass
        else:
            currentBlocks.append(cur_Child)

    # nextChar = currentMetaInput[cur_position + 1]
    curDict = cur_Child[3]
    if curDict:
        __getCurrentBlocksFromChainCharMetaDict(currentMetaInput, cur_position + 1, curDict, currentBlocks,
                                                filterSingle)


def __getChainBlocksWithPossibleMetas(possibleMetas, cur_position):
    """
    根据所有的可能的元数据取得链表
    :param possibleMetas: 可能的元数据
    :param cur_position: 当前所在位置
    :param intersectMetas : 两两相交的原数据
    :return:
    """
    if len(possibleMetas) == 0:
        return None

    cur_chain_Blocks = []
    if cur_position > possibleMetas[-1][0][0]:  # 已经是最后一个，直接返回
        return cur_chain_Blocks

    # 取得当前位置（或距离最近的下一个匹配出来的元数据）
    cur_possibleMeta_list = __getNextPossibleMetasByCharPos(possibleMetas, cur_position)

    if not cur_possibleMeta_list:
        return

    for cur_possibleMeta in cur_possibleMeta_list:
        next_position = cur_possibleMeta[0] + len(cur_possibleMeta[1])
        # if cur_possibleMeta[1]==u"有":
        #     iii=1
        next_chain_Blocks = __getChainBlocksWithPossibleMetas(possibleMetas, next_position)
        if next_chain_Blocks:  # 如果有后续的，逐条添加
            for next_chain_Block_list in next_chain_Blocks:
                cur_chain_Block = [cur_possibleMeta]
                cur_chain_Block.extend(next_chain_Block_list)
                cur_chain_Blocks.append(cur_chain_Block)

        else:  # 已经没有后续的了，直接添加一条
            cur_chain_Block = [cur_possibleMeta]
            cur_chain_Blocks.append(cur_chain_Block)

        pass

    # 取得相交的元数据，例如：国人-人民，有司-司法，有司-司法权，中间有相交的部分
    intersect_chain_Blocks = __getIntersectMetas(cur_possibleMeta_list, possibleMetas)
    if len(intersect_chain_Blocks) > 0:
        for cur_possibleMeta in cur_possibleMeta_list:

            cur_intersect_chain_Blocks = intersect_chain_Blocks.get(cur_possibleMeta[1])
            if cur_intersect_chain_Blocks:
                for cur_intersect_chain_Block in cur_intersect_chain_Blocks:
                    cur_meta = cur_intersect_chain_Block[1]
                    next_chain_Blocks = __getChainBlocksWithPossibleMetas(possibleMetas, cur_meta[0] + len(cur_meta[1]))

                    if next_chain_Blocks:  # 如果有后续的，逐条添加
                        for next_chain_Block_list in next_chain_Blocks:
                            cur_chain_Block = [cur_meta]
                            cur_chain_Block.extend(next_chain_Block_list)
                            cur_chain_Blocks.append(cur_chain_Block)

                    else:  # 已经没有后续的了，直接添加一条
                        cur_chain_Block = [cur_meta]
                        cur_chain_Blocks.append(cur_chain_Block)

                pass

    return cur_chain_Blocks


def __getNextPossibleMetasByCharPos(possibleMetas, cur_pos):
    """
    取得下一个位置的元数据列表（可能不是当前位置，而是大于等于当前位置）（包括与下一个位置相交的其他元数据）
    :param possibleMetas:
    :param cur_pos:
    :return:
    """

    for possibleMeta_list in possibleMetas:
        nextPos = possibleMeta_list[0][0]
        if nextPos >= cur_pos:
            return possibleMeta_list
    return None


def __getPossibleMetasByCharPos(possibleMetas, cur_pos):
    """
    取得当前位置的元数据列表
    :param possibleMetas:
    :param cur_pos:
    :return:
    """
    for possibleMeta_list in possibleMetas:
        if possibleMeta_list[0][0] == cur_pos:
            return possibleMeta_list
    return None


def __getIntegratedChainBlocks(rawInput,
                               chain_blocks,
                               chainChar_MetaDict,
                               getUnknownSingleWord=True):
    """
    如果有未识别，整合到一起
    :param rawInput:
    :param chain_blocks: 链式字符块列表
    :param chainChar_MetaDict:
    :param getUnknownSingleWord: 由于可能有单字，但已被过滤掉了，成为了未识别元字符、需要使用chainChar_MetaDict的结果进行替换
    :return:
    """
    integrated_chain_blocks = []
    unknowns = {}

    index =0
    for cur_chain_block in chain_blocks:
        cur_integrated_chain_block = []
        cur_unknowns = {}
        i = 0
        while i < len(cur_chain_block):
            # 看前一个与当前词块之间是否存在“缝隙”，如果存在缝隙，如果存在，添加之
            cur_meta_info = cur_chain_block[i]
            backward_meta_info = None
            if i == 0:
                backward_meta_info = [0, u"", -1, False]
            else:
                backward_meta_info = cur_chain_block[i - 1]
            unknown_meta_info = __getUnknownMetaInfo(rawInput, backward_meta_info[0] + len(backward_meta_info[1]),
                                                     cur_meta_info[0])
            if unknown_meta_info:
                is_known_as_single_word = False
                if getUnknownSingleWord:
                    # 由于可能有单字，但已被过滤掉了，成为了未识别元字符、使用chainChar_MetaDict的结果进行替换
                    cur_last_chars = unknown_meta_info[1]
                    if len(cur_last_chars) == 1:
                        cur_last_chain_char_meta_dict = chainChar_MetaDict.get(cur_last_chars)
                        # 如果找到了，对其数据进行替换
                        if cur_last_chain_char_meta_dict and cur_last_chain_char_meta_dict[0] == True:
                            unknown_meta_info[2] = cur_last_chain_char_meta_dict[2]  # 频率
                            unknown_meta_info[3] = cur_last_chain_char_meta_dict[0]  # 是否元数据
                            is_known_as_single_word = True
                cur_integrated_chain_block.append(unknown_meta_info)
                if not is_known_as_single_word:
                    cur_unknowns[i]=unknown_meta_info
            # 将当前元数据词块添加到结果
            cur_integrated_chain_block.append(cur_meta_info)

            i += 1

        # 最后添加最后一个已知字符块之后的未知字符（也可能没有）
        last_meta_info = cur_chain_block[-1]
        last_unknown_meta_info = __getUnknownMetaInfo(rawInput, last_meta_info[0] + len(last_meta_info[1]),
                                                      len(rawInput))
        if last_unknown_meta_info:
            # 由于可能有单字，但已被过滤掉了，成为了未识别元字符、使用chainChar_MetaDict的结果进行替换
            cur_last_chars = last_unknown_meta_info[1]
            if len(cur_last_chars) == 1:
                cur_last_chain_char_meta_dict = chainChar_MetaDict.get(cur_last_chars)
                if cur_last_chain_char_meta_dict and cur_last_chain_char_meta_dict[0] == True:
                    last_unknown_meta_info[2] = cur_last_chain_char_meta_dict[2]  # 频率
                    last_unknown_meta_info[3] = cur_last_chain_char_meta_dict[0]  # 是否元数据
            cur_integrated_chain_block.append(last_unknown_meta_info)
            cur_unknowns[i] =last_unknown_meta_info

        integrated_chain_blocks.append(cur_integrated_chain_block)
        if cur_unknowns:
            unknowns[index]=cur_unknowns

        index+=1

    return integrated_chain_blocks, unknowns


def __getUnknownMetaInfo(rawInput, start, end):
    """
    看前一个与当前词块之间是否存在“缝隙”，如果存在缝隙，如果存在，添加之
    :param rawInput:
    :param start:
    :param end:
    :return:
    """
    try:
        unknown_str = rawInput[start:end]
        if unknown_str and not unknown_str == u"":
            return [start, unknown_str, -1.0, False]
    except:
        return None


def __appendCurBlockCopyOrReplaceWithPossibleMeta(cur_block_copy, possibleMetas, integrated_chain_block):
    """
    【不再使用】对连续未识别整合而成的字符块进行重新识别，将其中已识别的元数据进行替换
    :param cur_block_copy:
    :param possibleMetas: 可能的元数据
    :param integrated_chain_block:
    :return:
    """
    cur_possibleMeta_list = possibleMetas[cur_block_copy[0]]
    recognized = False
    for cur_possibleMeta in cur_possibleMeta_list:
        if cur_possibleMeta[1] == cur_block_copy[1]:
            recognized = True
            integrated_chain_block.append(cur_possibleMeta)
            break

    if not recognized:
        integrated_chain_block.append(cur_block_copy)


def __cleanDuplicatedChainBlocks(chain_blocks, metaInput):
    """
    在链式字符块列表中，根据相同的元输入，删除重复的（子元素结构为[位置，元输入，频率，是否元数据]的列表）
    :param chain_blocks: 链式字符块列表
    :return:
    """
    removeIndexs = []
    for i in range(len(chain_blocks)):
        if removeIndexs.__contains__(i):
            i += 1
            continue

        cur_block = chain_blocks[i]
        j = i + 1
        while j < len(chain_blocks):
            if removeIndexs.__contains__(j):
                j += 1
                continue
            next_block = chain_blocks[j]
            if __isChainBlockEqual(cur_block, next_block):
                removeIndexs.append(j)
            j += 1
        i += 1

    cleaned_chain_blocks = []
    i = 0
    for chain_block in chain_blocks:
        if removeIndexs.__contains__(i):
            i += 1
            continue
        # if len(chain_block)==1 and chain_block[0][1]==metaInput and chain_block[0][3]==False: # 这里过滤掉整个一个句子都未能识别的情况
        #     i+=1
        #     continue
        cleaned_chain_blocks.append(chain_block)
        i += 1

    return cleaned_chain_blocks


def __resegmentChainBlocksWithUnknowns(chain_blocks, unknowns_dict,memory=None):
    """
    进一步使用其他已分出来的未知元数据重新处理已经分割出来的结果。
    :param cleaned_chain_blocks:
    :param unknowns_dict:
    :return:
    """
    import copy
    resegmented_chain_blocks = copy.copy(chain_blocks)  # 复制一个
    for i,cur_unknowns_dict in unknowns_dict.items():
        if not cur_unknowns_dict:  # 如果没有未知的，继续下一个
            continue
        cur_resegmented_chain_block = resegmented_chain_blocks[i]
        for j,cur_unknown in cur_unknowns_dict.items():

            # 如果只有一个字符(无需再分)，直接略过
            if len(cur_unknown[1]) == 1:
                continue

            other_unknown_list = []
            for k,other_unknown in cur_unknowns_dict.items():  # 找到其他的未知元数据（不能用自身分割自身）
                if j == k:
                    continue

                if not other_unknown[1] == cur_unknown[1] and \
                        cur_unknown[1].find(other_unknown[1]) >= 0:  # 排除自身，并且能够找到（否则无法进一步分割）
                    other_unknown_list.append(other_unknown)

            _resegmented_unknown_meta_chains = None
            if other_unknown_list:  # 如果能够进行进一步分割，使用未知数据再分割之，否则保持不变
                _chainCharMetaDict = {}
                for other_unknown in other_unknown_list:
                    loadChainCharFrequncyMetaDict({other_unknown[1]: other_unknown[3]}, _chainCharMetaDict)

                _ngramDict = {}

                cur_segment_result = segmentInputWithChainCharMetaDict(cur_unknown[1],
                                                                       chainCharMetaDict=_chainCharMetaDict,
                                                                       ngramDict=_ngramDict, filterSingle=False,
                                                                       resegmentWithUnknowns=False,
                                                                       memory=memory)

                if cur_segment_result:
                    _resegmented_unknown_meta_chains = ResegmentedUnknownMetaChains()  # 肯定是全部未识别的
                    while True:
                        cur_meta_data_chain = getCurMetaChainBySegmentResult(cur_segment_result,memory=memory)
                        if not cur_meta_data_chain:
                            break
                        cur_meta_chain = ResegmentedUnknownMetaChain()
                        x = 0
                        for cur_meta_data in cur_meta_data_chain[1]:
                            cur_meta_chain.append(
                                [cur_unknown[0] + x, cur_meta_data.mvalue, cur_meta_data.weight, False])
                            x += 1
                        _resegmented_unknown_meta_chains.append(cur_meta_chain)  # 取中间实际的meta_chain

            if _resegmented_unknown_meta_chains:  # 如果对当前未知字符串进行了进一步分割，处理之
                # 取得与当前未知对象位置一致的chain_block
                cur_pos = 0
                cur_resegmented_chain = None
                for temp_resegmented_chain in cur_resegmented_chain_block:
                    if temp_resegmented_chain[0] == cur_unknown[0]:
                        cur_resegmented_chain = temp_resegmented_chain
                        break
                    cur_pos += 1
                if cur_resegmented_chain:
                    resegmented_chain_blocks[i][cur_pos] = _resegmented_unknown_meta_chains

        # 对原有的元素进行装箱处理（非ResegmentedUnknownMetaChains类型）
        for y in range(len(cur_resegmented_chain_block)):
            if not isinstance(cur_resegmented_chain_block[y], ResegmentedUnknownMetaChains):
                cur_resegmented_chain_block[y] = [cur_resegmented_chain_block[y]]

    final_resegmented_chain_blocks = []
    import itertools
    i=0
    for resegmented_chain_block in resegmented_chain_blocks:
        if not i in unknowns_dict: # 全部已知，装箱，添加后直接返回
            final_resegmented_chain_blocks.append([resegmented_chain_block])
            i+=1
            continue

        cur_final_resegmented_chain_block = []
        # 拆箱
        for cur_final_resegmented_chain in itertools.product(*resegmented_chain_block,repeat=1):
            # 将ResegmentedUnknownMetaChain进一步拆箱
            extended_final_resegmented = []
            for cur_final_resegmented_obj in cur_final_resegmented_chain:
                if isinstance(cur_final_resegmented_obj, ResegmentedUnknownMetaChain):
                    extended_final_resegmented.extend(cur_final_resegmented_obj)
                else:
                    extended_final_resegmented.append(cur_final_resegmented_obj)
            cur_final_resegmented_chain_block.append(extended_final_resegmented)
        final_resegmented_chain_blocks.append(cur_final_resegmented_chain_block)
        i += 1

    return final_resegmented_chain_blocks

    # for i in range(len(unknowns_dict)):
    #     cur_meta = meta_chain[i]
    #
    #     # 只有元数据，并且非单字符才需要用其他未识别的元数据进一步分割处理
    #     if not isinstance(cur_meta, MetaData) or not len(cur_meta.mvalue) > 1:
    #         continue
    #
    #     # 进一步使用其他已分出来的未知元数据重新处理meta
    #     unknown_metas = []
    #     for j in metas_level_result.unknown_metas_index:  # 找到其他的未知元数据（不能用自身分割自身）
    #         if i == j:
    #             continue
    #         other_meta = metas_level_result.meta_chain[j]
    #         if isinstance(other_meta, MetaData):  # 只有元数据，才能成为进一步分割的依据。
    #             if not other_meta.mvalue == cur_meta.mvalue and \
    #                     cur_meta.mvalue.find(other_meta.mvalue) >= 0:  # 排除自身，并且能够找到（否则无法进一步分割）
    #                 unknown_metas.append(other_meta)
    #     if unknown_metas:  # 如果能够进行进一步分割，使用未知元数据再分割之，否则保持不变
    #         _resegmented_unknown_meta_chains = metaDataHelper.segmentWithUnknownMetas(
    #             cur_meta, unknown_metas)
    #         if _resegmented_unknown_meta_chains:
    #             if len(_resegmented_unknown_meta_chains) == 1:  # 扒皮
    #                 _resegmented_unknown_meta_chains = _resegmented_unknown_meta_chains[0]
    #             if not isinstance(_resegmented_unknown_meta_chains, list):
    #                 metas_level_result.meta_chain[i] = _resegmented_unknown_meta_chains
    #             else:
    #                 metas_level_result.meta_chain[i] = _resegmented_unknown_meta_chains[0]
    #                 k = 1
    #                 while k < len(_resegmented_unknown_meta_chains):
    #                     metas_level_result.meta_chain.insert(i + k, _resegmented_unknown_meta_chains[k])
    #                     k += 1

    pass


def loadNgramDictFromMetaNet():
    raise NotImplemented
    pass


def __sortSegmentedResultByNgram(rawInput, chain_blocks, ngramDict, gramNum=2):
    """
    对匹配出来的字符块链进行排序，使用邻接匹配法——ngram，进行计算
    :param chain_blocks: 字符块链
    :param ngramDict: n元丁字型结构的字符块链表（数据库存储丁字型结构，用的时候加载）。
                      ngram，二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解。
    :param gramNum: 指定进行二元、三元关系计算的“元数”,对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
                      二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解
    :return:传统的可能性（路径L的概率[路径依赖]）计算公式为：
            【二元】P(L) = P(w2|w1) * P(w3|w2) * P(w4|w3) *……* P(wk|w(k-1))*P(w1) * P(w2) * P(w3)…… * P(wk)
            【三元】P(L) = P(w3|w1w2) * P(w4|w3w2) * P(w5|w4w3) *……* P(wk|w(k-2)w(k-1))*P(w1) * P(w2) * P(w3)…… * P(wk)
            这里考虑以下几点：
            当前元数的可能性，应与该元数关系的可能性正相关，与该元数所包含字符块的可能性之和正相关，而不应仅仅是乘积关系
            而各字符链的可能性之间的关系，应该是累加的
            同时，这种概率还与词块的长度正相关，实际词频应该为：词块词频*词块长度的加权值
            所以，这里将上述公式修改为：
            【二元】P(L) = P(w2|w1) * （P(w1)*len(w1) + P(w2)*len(w2)）/ (len(w1)+len(w2))+
                           P(w3|w2) * （P(w2)*len(w2) + P(w3)*len(w3)）/ (len(w2)+len(w3))+ …… +
                           P(wk|w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1))/ (len(wk)+len(wk-1))
            【三元】P(L) = P(w3|w1w2) * （P(w1)*len(w1) + P(w2)*len(w1)+ P(w3)*len(w3)）/ (len(w1)+len(w2)+len(w3)) +
                           P(w4|w2w3) * （P(w2)*len(w2) + P(w3)*len(w3)+ P(w4)*len(w4)）/ (len(w2)+len(w3)+len(w4))+ …… +
                           P(wk|w(k-2)w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)+P(w(k-2)*len(wk-2))/ (len(wk)+len(wk-1)len(wk-2))
            另外，要避免分词多反而造成可能性大的情况，所以要对可能性进行加权平均
            【二元】P(L) = P(w2|w1) * （P(w1)*len(w1) + P(w2)*len(w2)）/ (len(w1)+len(w2))+
                           P(w3|w2) * （P(w2)*len(w2) + P(w3)*len(w3)）/ (len(w2)+len(w3))+ …… +
                           P(wk|w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1))/ (len(wk)+len(wk-1))
                           /(k-1)
            【三元】P(L) = P(w3|w1w2) * （P(w1)*len(w1) + P(w2)*len(w1)+ P(w3)*len(w3)）/ (len(w1)+len(w2)+len(w3)) +
                           P(w4|w2w3) * （P(w2)*len(w2) + P(w3)*len(w3)+ P(w4)*len(w4)）/ (len(w2)+len(w3)+len(w4))+ …… +
                           P(wk|w(k-2)w(k-1))* (P(wk)*len(wk)+P(w(k-1)*len(wk-1)+P(w(k-2)*len(wk-2))/ (len(wk)+len(wk-1)len(wk-2))
                           /(k-2)
    """
    # # 如果只有一个字符块，直接返回
    # if len(chain_blocks) ==1:
    #     return chain_blocks

    calcBigram = False  # 是否需要计算二元关系
    calcTrigram = False  # 是否需要计算三元关系

    if gramNum <= 2:
        calcBigram = True
    if gramNum >= 3:
        calcBigram = True
        calcTrigram = True

    _segmentedResult = SegmentedResult(rawInput)


    # chain_block_bigram_probability=[] # 二元关系可能性的计算结果，其子元素格式为：[当前字符块链,二元关系的可能性]，例如：[cur_chain_block,cur_bi_probability]
    # chain_block_trigram_probability=[] # 三元关系可能性的计算结果，其子元素格式为：[当前字符块链,三元关系的可能性]，例如：[cur_chain_block,cur_tri_probability]
    for cur_chain_block in chain_blocks:
        cur_block_chain = __get_block_chain(cur_chain_block)

        chain_length = len(cur_chain_block)
        if chain_length == 1:  # 如果只有一个字符块，不需要查找n元关系，添加到结果，继续下一个
            total_probability_ratio = __get_total_probability_ratio(cur_chain_block, num_base)
            cur_block_chain.probability = cur_chain_block[0][2] * total_probability_ratio *10
            _segmentedResult.bigramResult.append(cur_block_chain)
            continue

        cur_bi_probability = 0.0
        cur_tri_probability = 0.0
        i = 0

        while i < chain_length - 1:  # 这里-1，是要保证存在后续的字符块
            cur_block = cur_chain_block[i]
            ngram = ngramDict.get(cur_block[1])
            if ngram:
                next_block = cur_chain_block.__getitem__(i + 1)
                bifrequncy = 1.0
                if calcBigram:  # 如果需要计算二元关系
                    bigram = ngram.get(2)
                    if bigram:
                        bifrequncy = bigram.get(next_block[1])
                    if not bifrequncy:
                        bifrequncy = 1.0 / chain_length

                    cur_bi_probability += bifrequncy * (cur_block[2] * (len(cur_block[1]) ** 2) + next_block[2] * (
                            len(next_block[1]) ** 2))  # /(len(cur_block[1])+len(next_block[1]))

                if calcTrigram:  # 如果需要计算三元关系
                    trigram = ngram.get(3)
                    cur_chain_block = []
                    next_next_block = cur_chain_block.__getitem__(i + 2)
                    trifrequncy = 1.0
                    if trigram and next_next_block:
                        biDict = trigram.get(next_block[1])
                        if biDict:
                            trifrequncy = biDict.get(next_next_block[1])
                            if not trifrequncy:
                                trifrequncy = 1.0

                    cur_tri_probability += trifrequncy * (
                            cur_block[2] * (len(cur_block[1]) ** 3) + next_block[2] * (len(next_block[1]) ** 3) +
                            next_next_block[2] * (len(
                        next_next_block[1]) ** 3))  # /(len(cur_block[1])+len(next_block[1])+len(next_next_block[1]))

            i += 1

        total_probability_ratio=__get_total_probability_ratio(cur_chain_block,num_base)

        if calcBigram:
            cur_bi_probability*=total_probability_ratio
            cur_block_chain.probability = cur_bi_probability  # /(len(cur_chain_block)) # 这里要避免分词多反而造成可能性大的情况，所以要对可能性进行加权平均
            _segmentedResult.bigramResult.append(cur_block_chain)

        if calcTrigram:
            cur_tri_probability *= total_probability_ratio
            cur_block_chain.probability = cur_tri_probability  # /(len(cur_tri_probability))
            _segmentedResult.trigramResult.append(cur_block_chain)

    # 根据计算出来的可能性进行排序
    # 二元关系可能性结果排序
    if calcBigram:
        _segmentedResult.sortBigramResult()
    # 三元关系可能性结果排序
    if calcTrigram:
        _segmentedResult.sortTrigramResult()

    return _segmentedResult

def __get_total_probability_ratio(cur_chain_block,known_num_base):
    known_num = 0
    for cur_block in cur_chain_block:
        if cur_block[3] == True:
            known_num += 1
    # 取得已知/所有的占比，加底数，防止出现0
    total_probability_ratio = (known_num + known_num_base) / (len(cur_chain_block) + known_num_base)

    if known_num == len(cur_chain_block):
        total_probability_ratio *= 100 #

    return total_probability_ratio





def __get_block_chain(chain_block):
    block_chain = BlockChain()
    for block in chain_block:
        cur_block = Block(block[1], block[0], block[3], block[2])
        block_chain.chain.append(cur_block)
    return block_chain


def __isChainBlockEqual(cur_block, next_block):
    """
    【不再使用】判断两个子元素结构为[位置，元输入，频率，是否元数据]的列表是否相同
    :param cur_block:
    :param next_block:
    :return:
    """

    if not len(cur_block) == len(next_block):
        return False
    for i in range(len(cur_block)):
        cur_item = cur_block[i]
        next_item = next_block[i]
        if not cur_item[0] == next_item[0] and not cur_item[1] == next_item[1]:
            return False
    return True


#
# def __getNextPossibleMeta():
"""
***********************************************************
以下方法为分词的其他方法（例如：首字匹配法），不建议使用
***********************************************************
"""


def getStopMarksRexPattern(stopMarks, stopMarkLevel=3, StopMarksRexPattern=None):
    """
    【不建议使用】
    取得分解句子所需的标点符号正则pattern（弃用）。
    :param stopMarks: 标点符号的字典，包括0：段落标记:1：句子间标点符号:2：句子内标点符号
                      格式为：{标点符号:[标点符号类别,词频]}
    :param stopMarkLevel: 按标点符号的划分级别（0：段落级别，1：段落级别+句子级别，2：段落级别+句子级别+句内级别）。
    :return:
    """
    if stopMarkLevel > 2:  # 如果超过2，直接设为2：段落级别+句子级别+句内级别
        stopMarkLevel = 2
    # 查看是否已经完成了正则pattern的拼接，如果是，直接返回
    if StopMarksRexPattern and stopMarkLevel in StopMarksRexPattern:
        return StopMarksRexPattern[stopMarkLevel]

    pattern = u""
    is_first = True
    for stopMark, detail in stopMarks.items():
        cur_levlel = detail[0]  # 当前需要取得的标点符号的级别
        if is_first == True:
            if cur_levlel <= stopMarkLevel:
                pattern += stopMark
                is_first = False
        else:
            if cur_levlel <= stopMarkLevel:
                pattern += u"|" + stopMark

    if not StopMarksRexPattern is None:
        StopMarksRexPattern[stopMarkLevel] = pattern

    return pattern


def __segmentWithStopMarks_rex(metaInput, stopMarks, stopMarkLevel=3, keepStopMark=True, StopMarksRexPattern=None):
    """
    【不建议使用】使用正则按标点符号分解输入
    :param metaInput:
    :param stopMarks:
    :param stopMarkLevel:
    :param keepStopMark:
    :param StopMarksRexPattern:
    :return:
    """
    pattern = getStopMarksRexPattern(stopMarks, stopMarkLevel, StopMarksRexPattern)

    import re
    # metaInput=u"习近平强调，中国将坚持改革开放.坚持走和平发展道路...努力推动构建以合作共赢为核心的新型国际关系，打造人类命运共同体!维护和完善以联合国为中心的现行国际体系和秩序。作为最大发展中国家和最大发达国家、世界前两大经济体，中美两国对促进世界和平、稳定、繁荣负有更加重要的责任，应该合作、可以合作的领域十分广阔。中美共同利益远远大于分歧，中美合作可以办成许多有利于两国和世界的大事。同时，双方应该在尊重彼此核心利益和重大关切基础上，通过对话协商积极寻求解决彼此间的分歧，或以建设性方式管控敏感问题，避免误解误判和矛盾升级，防止中美合作大局受到大的干扰。中方愿同美方加强沟通，聚焦合作，增进互信，一道努力构建新型大国关系，实现不冲突不对抗、相互尊重、合作共赢。"
    splits = re.split(pattern, metaInput)

    if splits is None:  # todo 这里需要测试一下单独一个标点的输入情况
        return []

    if keepStopMark:  # 如果保留分割的标点，将标点添加到分割后的列表
        i = 0
        postion = 0
        removeList = []  # 正则分割句子后，会有很多不符合要求的，例如None或空字符串，加入待删除列表
        while i < len(splits):

            sentence = splits[i]
            if sentence is None or len(sentence) == 0:
                removeList.append(i)

            postion += len(sentence)
            stopMark = metaInput[postion:postion + 1]
            splits.insert(i + 1, stopMark)
            postion += 1  # 再向后移一位（标点符号之后）
            i += 2  # 由于已经插入了一个标点，所以位置要加2

        # 由于上面是i+=2结束的循环，可能已经跳过了对最后一个是否合格的检查，这里需要检查最后一个是否合格
        sentence = splits[len(splits) - 1]
        if sentence is None or len(sentence) == 0:
            removeList.append(len(splits) - 1)

        # 删除不合格的
        removedNum = 0
        for pos in removeList:
            del splits[pos - removedNum]
            removedNum += 1

    return splits


def segmentInputsWithFirstCharMetaDict(metaInputs, firstCharMetaDict, maxMatch=True):
    """
    【不建议使用】根据元数据分割输入字符串（列表）-根据首字母进行匹配（有两种：最长顺序匹配、全部匹配）。
    :param metaInputs: 输入的字符串（列表），metaInputs必须是unicode编码
    :param firstCharMetaDict: 首字符元数据字典。以首字符作为索引，所有元数据（按长度倒序排列）的列表为值。
    :param maxMatch: 是否最大匹配，默认为True，系统只输出一条结果，如果设置为False，系统将输出全部结果。
    :return:
    """
    segments = {}
    for metaInput in metaInputs:

        segment = segmentInputWithFirstCharMetaDict(metaInput, firstCharMetaDict, maxMatch)
        if not segment is None:
            segments[metaInput] = segment

    return segments


def loadFirstCharMetaDict(rawMetas, CachedFirstCharMetaDict=None):
    """
    【不建议使用】
    将{元输入：词频}的字典，转换成以首字符作为索引，所有元数据（按长度倒序排列）的列表为值，建立一个字典或将其添加到CachedFirstCharMetaDict。
    :param WordFrequncyDict:{元输入：词频}的字典
    :return:以首字符作为索引，所有元数据（按长度倒序排列）的列表为值，建立的字典
    """
    if CachedFirstCharMetaDict is None:
        __dict = {}
    else:
        __dict = CachedFirstCharMetaDict

    for raw_meta_chars, frequcy in rawMetas.items():
        first_char = raw_meta_chars[0]
        if not first_char in __dict:
            __dict.setdefault(first_char, [])
            __dict[first_char].append(raw_meta_chars)
        else:
            if not raw_meta_chars in __dict[first_char]:
                __dict[first_char].append(raw_meta_chars)

    # 按词的长度倒序排列
    # 倒序提取，这样可以避免从头查到尾，如果没有对应的元数据，而导致的多次查询问题。
    for first_char, words in __dict.items():
        __dict[first_char] = sorted(words, key=lambda x: len(x), reverse=True)

    return __dict


def __getChainBlocksWithDescartes(metaInput, possibleMetas):
    """
    【不建议使用】以笛卡尔乘积的方式取得链式字符块。（当遇到较长文本时会遇到速度等问题，弃用）
    :param possibleMetas:
    :return:中国人民法院有司法权中央"可以分解为下面的possibleMetas
    possibleMetas=[
        [[0,u"中国人民法院",5.5,True],[0,u"中国人民",7.0,True],[0,u"中国人",8.5,True],[0,u"中国",9.8,True],],
        [[1,u"国人",4.0,True],],
        [[2,u"人民",8.1,True],[2,u"人民法院",4.3,True],],
        [[3,u"民法",6.3,True],[3,u"民法院",3.2,True],],
        [[4,u"法院",8.7,True],],
        [[6,u"有司",2.4,True],[6,u"有",9.9,True],],
        [[7,u"司法权",6.4,True],[7,u"司法",8.5,True],],
        [[8,u"法权",2.5,True],],
        [[10,u"中央",8.0,True],],
    ]
    拼接为线性字符块，如：
    chainBlocks=[
        [[u"中国人民法院",5.5,True,0],[u"有司",2.4,True,6],[u"法权",2.5,True,8],[u"中央",8.0,True,10],],
        [[u"中国人民法院",5.5,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人民法院",5.5,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],[u"中央",8.0,True],],
        [[u"中国人民",7.0,True],[u"法院",8.7,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国人民",7.0,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人民",7.0,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法院",3.2,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法院",3.2,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法院",3.2,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法",6.3,True],[u"院",-1.0,False],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法",6.3,True],[u"院",-1.0,False],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国人",8.5,True],[u"民法",6.3,True],[u"院",-1.0,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民法院",4.3,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民法院",4.3,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民法院",4.3,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民",8.1,True],[u"法院",8.7,True],[u"有司",2.4,True],[u"法权",2.5,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民",8.1,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法权",6.4,True],[u"中央",8.0,True],],
        [[u"中国",9.8,True],[u"人民",8.1,True],[u"法院",8.7,True],[u"有",-1.0,False],[u"司法",8.5,True],[u"权",-1.0,False],,[u"中央",8.0,True],],
    ]
    含义为：
    [分出的字符块，词频，是否元数据，起始位置]
    """
    chainBlocks = []
    # cur_chainBlocks=__getChainBlocksWithPossibleMetas(possibleMetas,0,metaInput)
    # chainBlocks.extend(cur_chainBlocks)
    import itertools
    descartes = itertools.product(*possibleMetas)

    descartesList = []

    for cur_block in descartes:
        l = list(cur_block)
        descartesList.append(l)

    # total = 0
    for item in descartesList:
        # if total == 6:
        #     aaa = 9
        i = 0
        while i < len(item):
            cur_block = item[i]
            cur_chars = cur_block[1]
            cur_start_position = cur_block[0]
            cur_end_position = cur_start_position + len(cur_chars) - 1
            j = i + 1
            while j < len(item):
                next_block = item[j]
                j += 1
                next_chars = next_block[1]
                next_start_position = next_block[0]
                next_end_position = next_start_position + len(next_chars) - 1
                if next_start_position > cur_end_position:  # 如果位置超出当前块，直接跳出
                    break
                if __blockIntersected(cur_start_position, cur_end_position, next_start_position,
                                      next_end_position):  # 如果是包含
                    item.remove(next_block)
                    j -= 1

            i += 1
        # total += 1

    removeIndexs = []
    # 删除重复的（子元素结构为[位置，元输入，频率，是否元数据]的列表）
    for i in range(len(descartesList)):
        if removeIndexs.__contains__(i):
            i += 1
            continue

        cur_block = descartesList[i]
        j = i + 1
        while j < len(descartesList):
            if removeIndexs.__contains__(j):
                j += 1
                continue
            next_block = descartesList[j]
            if __isChainBlockEqual(cur_block, next_block):
                removeIndexs.append(j)
            j += 1
        i += 1

    cleanedList = []
    i = 0
    for item in descartesList:
        if not removeIndexs.__contains__(i):
            cleanedList.append(item)
        i += 1

    return chainBlocks


def __blockIntersected(cur_start_position, cur_end_position, next_start_position, next_end_position):
    """
    【不建议使用】判断两个字符块是否有交叉重叠或包含关系
    :param cur_start_position:
    :param cur_end_position:
    :param next_start_position:
    :param next_end_position:
    :return:
    """
    if next_start_position >= cur_start_position and next_end_position <= cur_end_position:
        return True
    if cur_end_position >= next_start_position and cur_end_position <= next_end_position:
        return True
    return False


def __fillChainBlocks(currentMetaInput, chainCharMetaDict, unknownBlock, filterSingle=True):
    """
    【不建议使用】
    :param currentMetaInput:
    :param chainCharMetaDict:
    :param unknownBlock:
    :param filterSingle: 是否应该过滤掉单字词（在初分阶段应该过滤，但如果使用未知元数据对其他元数据再次精分，应该使用）
    :return:
    """
    resultDict = {}
    if currentMetaInput == u"":
        return resultDict
    currentBlocks = []

    __getCurrentBlocksFromChainCharMetaDict(currentMetaInput, 0, chainCharMetaDict, currentBlocks, filterSingle)
    if len(currentBlocks) == 0:
        # 这里的情况是首字符已知，但与第二个字符相连就是未知，例如：法，已知“法院、法律”，但“法权”未知
        # 这里的处理方式，是将两者添加到unknownBlock
        unknownBlock += getUnknownBlock(currentMetaInput, 0, chainCharMetaDict)
        position = len(unknownBlock)
        nextDict = __fillChainBlocks(currentMetaInput[position:], chainCharMetaDict, u"")

        resultDict.setdefault(unknownBlock, [0.0, False, nextDict])
    else:
        for block in currentBlocks:
            position = len(block[1])
            nextDict = __fillChainBlocks(currentMetaInput[position:], chainCharMetaDict, unknownBlock)
            # if len(nextDict) == 0:
            #     pass
            resultDict.setdefault(block[1], [block[2], block[0], nextDict])

    return resultDict


def getUnknownBlock(currentMetaInput, cur_pos, curDict):
    """
    【不再使用】
    :param currentMetaInput:
    :param cur_pos:
    :param curDict:
    :return:
    """
    unknownBlock = u""
    while cur_pos < len(currentMetaInput):  # 继续往后查不识别的
        cur_char = currentMetaInput[cur_pos]
        cur_child = curDict.get(cur_char)
        if cur_child and cur_pos + 1 < len(currentMetaInput):
            next_char = currentMetaInput[cur_pos + 1]
            if next_char in cur_child[3]:
                break
        unknownBlock += cur_char
        cur_pos += 1
    return unknownBlock


def __loopForChainBlocks(metaInput, cur_position, unknownBlock, curDict, chainCharMetaDict):
    """
    【不再使用】
    :param metaInput:
    :param cur_position:
    :param unknownBlock:
    :param curDict:
    :param chainCharMetaDict:
    :return:
    """
    resultDict = {}
    if cur_position < len(metaInput) - 1:  # resovledtodo（已解决） 这理应考虑一个字符的情况
        cur_char = metaInput[cur_position]

        cur_Child = curDict.get(cur_char)

        if cur_Child is None:  # 这说明未找到该字符及以该字符为索引的后续信息，直接作为未知字符块处理
            unknownBlock += cur_char
            cur_position += 1
            if cur_position == len(metaInput):  # 如果已经是最后一个字符了，直接添加，然后结束循环
                resultDict[unknownBlock] = [0.0, False, {}]
                return resultDict
            curDict = chainCharMetaDict
            return resultDict

        # 深度遍历子字符块
        nextChar = metaInput[cur_position + 1]
        nextDict = cur_Child[3]
        curDict = nextDict
        next_Child = nextDict.get(nextChar)
        # 如果是完整的元数据，添加到resultDict
        if len(next_Child[3]) == 0 or next_Child[3] is None:  # 如果后续没有相关的字符了,停机，迭代查询到最近的上级meta
            resultDict[cur_Child[1]] = [next_Child[2], True, {}]
        else:
            # 深度遍历子字符块
            nextChildDict = __loopForChainBlocks(metaInput, cur_position + 1, unknownBlock, curDict,
                                                 chainCharMetaDict)

            resultDict[next_Child[1]] = [next_Child[2], True, nextChildDict]

    return resultDict

    # if cur_position==len(metaInput)-1:# 如果已经是最后一个字符了，直接将该字符的相关信息（位置、是否是元数据、词频等）添加，然后结束循环
    #     unknownBlock+=cur_char
    #     segmentedResult.append([unknownBlock,cur_position,cur_Child[0],cur_Child[2]])
    #     break
    #
    # if not unknownBlock ==u"": #如果查到了目前的字符有索引，需要将以前的未知块加入分解结果，并清空
    #     lastResult= segmentedResult[len(segmentedResult)-1]
    #     if lastResult[2]==False:
    #         lastResult[0]+=unknownBlock
    #     else:
    #         segmentedResult.append([unknownBlock,cur_position-len(unknownBlock),False,0.0])
    #     unknownBlock=u""
    #     continue


def __segmentInputByMaxMatch(rawInput, chainCharMetaDict, start, end, resegmentWithUnknowns=True):
    """
    根据元数据分割输入字符串（列表）-根据链接字符词典进行匹配（最长顺序匹配）
    :param rawInput:输入的字符串（列表），metaInputs必须是unicode编码
    :param chainCharMetaDict:以每个字符作为索引，[True/False,{...},meta,frequncy]为值的字典，含义为：
    [是否字符块末尾，{后续子串字典}，元数据字符串，频率]
    :return:所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
                  [
                  [["音乐会",0,True,8.5],["很好",3,False,0.0]]
                  [["音乐",0,True,3.2],["会",2,False,0.0],["很好",3,False,0.0]]
                  ]
                  每条记录的格式应为：[[word,i,True/False,frequncy]]其含义为：[匹配到的单词，起始位置,是否元数据，频率]的列表
                  如果不是元数据，默认频率为0.0
    """

    segmentedResult = []  # 所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
    # [
    # [["音乐会",0,True,8.5],["很好",3,False,0.0]]
    # [["音乐",0,True,3.2],["会",2,False,0.0],["很好",3,False,0.0]]
    # ]
    # 每条记录的格式应为：[[word,i,True/False,frequncy]]其含义为：[匹配到的单词，起始位置,是否元数据，频率]的列表
    # 如果不是元数据，默认频率为0.0
    curDict = chainCharMetaDict  # curDict主要用于逐渐进行的查找，不能删除
    cur_char = rawInput[start]
    cur_chain_block = curDict.get(cur_char)

    if cur_chain_block:
        curDict = cur_chain_block[3]
        next_char = rawInput[start + 1]
        next_chain_block = curDict.get(next_char)

        pass


def __segmentInputByMaxMatch2(rawInput, chainCharMetaDict):
    """
    根据元数据分割输入字符串（列表）-根据链接字符词典进行匹配（最长顺序匹配）
    :param rawInput:输入的字符串（列表），metaInputs必须是unicode编码
    :param chainCharMetaDict:以每个字符作为索引，[True/False,{...},meta,frequncy]为值的字典，含义为：
    [是否字符块末尾，{后续子串字典}，元数据字符串，频率]
    :return:所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
                  [
                  [["音乐会",0,True,8.5],["很好",3,False,0.0]]
                  [["音乐",0,True,3.2],["会",2,False,0.0],["很好",3,False,0.0]]
                  ]
                  每条记录的格式应为：[[word,i,True/False,frequncy]]其含义为：[匹配到的单词，起始位置,是否元数据，频率]的列表
                  如果不是元数据，默认频率为0.0
    """

    segmentedResult = []  # 所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
    # [
    # [["音乐会",0,True,8.5],["很好",3,False,0.0]]
    # [["音乐",0,True,3.2],["会",2,False,0.0],["很好",3,False,0.0]]
    # ]
    # 每条记录的格式应为：[[word,i,True/False,frequncy]]其含义为：[匹配到的单词，起始位置,是否元数据，频率]的列表
    # 如果不是元数据，默认频率为0.0
    curDict = chainCharMetaDict  # curDict主要用于逐渐进行的查找，不能删除
    childPath = []  # 用来记录子字符字典的路径
    unknownBlock = u""  # 未知块，用来记录处理未建立索引的字符块
    i = 0

    chain_blocks = []

    while i < len(rawInput):  # resovledtodo（已解决） 这理应考虑一个字符的情况
        cur_char = rawInput[i]
        cur_Child = curDict.get(cur_char)
        if cur_Child is None:  # 这说明未找到该字符及以该字符为索引的后续信息，直接作为未知字符块处理
            unknownBlock += cur_char
            i += 1
            if i == len(rawInput):  # 如果已经是最后一个字符了，直接添加，然后结束循环
                segmentedResult.append([unknownBlock, i - len(unknownBlock), False, 0.0])
                break
            curDict = chainCharMetaDict
            continue

        if i == len(rawInput) - 1:  # 如果已经是最后一个字符了，直接将该字符的相关信息（位置、是否是元数据、词频等）添加，然后结束循环
            unknownBlock += cur_char
            segmentedResult.append([unknownBlock, i, cur_Child[0], cur_Child[2]])
            break

        if not unknownBlock == u"":  # 如果查到了目前的字符有索引，需要将以前的未知块加入分解结果，并清空
            if len(segmentedResult) == 0:
                segmentedResult.append([unknownBlock, 0, False, 0.0])
            else:
                lastResult = segmentedResult[len(segmentedResult) - 1]
                if lastResult[2] == False:
                    lastResult[0] += unknownBlock
                else:
                    segmentedResult.append([unknownBlock, i - len(unknownBlock), False, 0.0])
            unknownBlock = u""
            continue

        childPath.append(cur_Child)
        nextChar = rawInput[i + 1]
        nextDict = cur_Child[3]
        curDict = nextDict
        next_Child = nextDict.get(nextChar)
        if next_Child is None:  # 如果在cur_char的索引下，没有找到下一个字的索引，说明这两个字符都是未知的，
            unknownBlock += cur_char
            i += 1
            curDict = chainCharMetaDict
        elif len(next_Child[3]) == 0 or next_Child[3] is None:  # 如果后续没有相关的字符了,停机，迭代查询到最近的上级meta
            childPath.append(next_Child)
            upperChild = __getUpperMeta(childPath)
            upper_chars = upperChild[1]
            segmentedResult.append([upper_chars, i + 2 - len(upper_chars), upperChild[0], upperChild[2], []])

            # 取得有交叉的元数据，例如：有司-法权，中的“有司”，与“司法权”相交
            intersect_chars = upper_chars[1:]
            # intersectMeta=

            curDict = chainCharMetaDict
            i += 2  # 跳到当前位置的下两个（下一个已经处理过了）
            childPath = []
        else:
            i += 1

    return segmentedResult


def __getUpperMeta(childPath):
    """
    迭代查询到最近的上级meta
    :param childPath:
    :return:
    """
    for i in range(0, len(childPath))[::-1]:
        cur_Child = childPath[i]
        if cur_Child[0] == True:
            return cur_Child


def segmentInputWithFirstCharMetaDict(metaInput, firstCharMetaDict, maxMatch=True):
    """
    【不建议使用】根据元数据分割输入字符串。
    :param metaInput:输入字符串。metaInput必须是unicode编码
    :param firstCharMetaDict:首字符元数据字典。以首字符作为索引，所有元数据（按长度倒序排列）的列表为值。
    :param maxMatch: 是否最大匹配，默认为True，系统只输出一条结果，如果设置为False，系统将输出全部结果。
    :return:分割后的结果。
    """
    if not metaInput:
        return []
    # results = []
    # i = 0
    # while i < len(metaInput):
    #     first_char = metaInput[i]
    #     matched_words = __match_word_with_firstChar(first_char, i, metaInput,firstCharMetaDict,maxMatch)
    #     results.append(matched_words)
    #     if maxMatch: # 为True，这里只对最大匹配的结果进行处理
    #         # matched_words的格式应为：[[word,i,True/False]]其含义为：[匹配到的单词，位置,是否元数据]的列表
    #         i += len(matched_words[0][0])
    #     else:
    #         i += len(matched_words)
    # return results
    segmentedResult = []  # 所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
    # [
    # [["音乐会",0,True],["很好",3,False]]
    # [["音乐",0,True],["会",2,False],["很好",3,False]]
    # ]
    # 每条记录的格式应为：[[word,i,True/False]]其含义为：[匹配到的单词，位置,是否元数据]的列表

    segmented_linked_words = []
    __match_word_with_firstChar(segmentedResult, segmented_linked_words, 0, metaInput,
                                firstCharMetaDict, maxMatch)

    return segmentedResult

    pass


def __match_word_with_firstChar(segmentedResult, currentLinkedWords, i, input, firstCharMetaDict, maxMatch=True):
    """
    【不建议使用】根据当前位置进行分词，ascii的直接读取连续字符，中文的读取词库
    :param segmentedResult: 所有分割出的字符串连接列表，例如："音乐会很好"，会分割出下面两条结果：
                 # [
                 # [["音乐会",0,True],["很好",3,False]]
                 # [["音乐",0,True],["会",2,False],["很好",3,False]]
                 # ]
                 # 每条记录的格式应为：[[word,i,True/False]]其含义为：[匹配到的单词，位置,是否元数据]的列表
    :param currentLinkedWords:当前分解出的相互连接的一串字符串
    :param first_char:首字符
    :param i:当前位置
    :param input:输入字符串
    :param firstCharMetaDict:元数据字典。以首字符作为索引，所有元数据（按长度倒序排列）的列表为值。
    :param maxMatch: 是否最大匹配，默认为True，系统只输出一条结果，如果设置为False，系统将输出全部结果。
    :return:格式应为：[[word,i,True/False]]其含义为：[匹配到的单词，位置，是否元数据]的列表，如果maxMatch=True，结果只有一条
    """
    first_char = input[i]
    if i == len(input) - 1:  # 如果是最后一个字符，直接添加，并返回。因为是单字，所以肯定会有metaData
        currentLinkedWords.append([first_char, i, True])
        return

    if not first_char in firstCharMetaDict:
        curChar = first_char
        import string
        if first_char in string.ascii_letters:
            curChar = __match_ascii(i, input)
        if currentLinkedWords is None:
            currentLinkedWords = [[curChar, i, False]]
        else:
            currentLinkedWords.append([curChar, i, False])

        # 接着处理后面的字符
        n = i + len(curChar)
        __match_word_with_firstChar(segmentedResult, currentLinkedWords, n, input, firstCharMetaDict,
                                    maxMatch)
        if i == 0:  # 如果是第一条记录，直接添加到结果
            segmentedResult.append(currentLinkedWords)

    words = firstCharMetaDict.get(first_char)
    if words:
        for word in words:
            if input[i:i + len(word)] == word:
                if currentLinkedWords is None:
                    currentLinkedWords = [[word, i, True]]
                else:
                    currentLinkedWords.append([word, i, True])

                # 接着处理后面的字符
                n = i + len(word)
                if n < len(input):  # 如果后面有字符，继续处理
                    __match_word_with_firstChar(segmentedResult, currentLinkedWords, n, input,
                                                firstCharMetaDict, maxMatch)

                if i == 0:  # 如果是第一条记录，直接添加到结果
                    segmentedResult.append(currentLinkedWords)
                if maxMatch:  # 为True，系统只输出一条结果，直接返回
                    return

    # pass  def __match_word_with_firstChar(segmentedResult,currentLinkedWords,first_char, i , input,firstCharMetaDict,maxMatch=True):


def __match_ascii(i, input):
    """
    【不建议使用】返回连续的英文字母，数字，符号
    :param i:
    :param input:
    :return:
    """
    import string
    result = ''
    for i in range(i, len(input)):
        if not input[i] in string.ascii_letters:
            break
        result += input[i]
    return result


def getCurMetaChainBySegmentResult(segmentResult, ngram=2,memory=None):
    """
    根据当前的分割的结果创建元数据链（由于分割结果可能有多个，所以在处理时一条条调用，直到“理解”为止）
    :param segmentResult:
    :return:
    """

    if not isinstance(segmentResult, SegmentedResult):
        return None
    if ngram <= 2:  # 一条条调用
        cur_block_chain = segmentResult.getCurBigramBlockChain()
    else:
        cur_block_chain = segmentResult.getCurTrigramBlockChain()
    if not cur_block_chain:
        return None

    meta_chain = []
    unknown_metas_index = []
    i = 0
    from loongtian.nvwa.models.metaData import MetaData

    for cur_block in cur_block_chain.chain:
        # 判断是否是标点符号、数字、字母
        # if stringHelper.is_stopmark(cur_block.word) or \
        #         stringHelper.is_number(cur_block.word) or \
        #         stringHelper.is_all_alphabet(cur_block.word):
        #     cur_meta = MetaData(mvalue=cur_block.word, recognized=True).create()
        #     meta_chain.append(cur_meta)
        # elif cur_block.isMeta:
        cur_meta = None
        if cur_block.isMeta:
            if memory:
                cur_meta =memory.getMetaByMvalueInMemory(cur_block.word)# 取得内存之中的元数据
            if not cur_meta:
                cur_meta = MetaData.retrieveByMvalue(cur_block.word)  # 取得数据库之中的元数据
            if not cur_meta:
                # 未识别的字符串：
                # 记录到内存，不应该创建到数据库
                cur_meta = MetaData(mvalue=cur_block.word, recognized=False,memory=memory).create(recordInDB=False)
        else:  # 未识别的字符串：
            # 记录到内存，不应该创建到数据库
            cur_meta = MetaData(mvalue=cur_block.word, recognized=False,memory=memory).create(recordInDB=False)

        # 记录
        meta_chain.append(cur_meta)
        if not cur_meta.recognized:
            unknown_metas_index.append(i)

        i += 1

    return (segmentResult.rawInput, meta_chain, unknown_metas_index)


def segmentWithUnknownMetas(meta, unknown_metas,memory=None):
    """
    使用已分出来的未知元数据进一步处理meta
    例如：牛有腿意义为牛组件为腿，初分出 牛有腿-意义为-牛-组件-腿，
    再次重分，分为：牛-有-腿-意义为-牛-组件-腿
    :param meta:
    :param unknown_metas:
    :return:
    """
    _chainCharMetaDict = {}
    for unknown_meta in unknown_metas:
        loadChainCharFrequncyMetaDict({unknown_meta.mvalue: unknown_meta.weight}, _chainCharMetaDict)

    _ngramDict = {}

    cur_segment_result = segmentInputWithChainCharMetaDict(meta.mvalue,
                                                           chainCharMetaDict=_chainCharMetaDict,
                                                           ngramDict=_ngramDict,
                                                           filterSingle=False,
                                                           memory=memory)

    if cur_segment_result:
        _unknown_meta_chains = ResegmentedUnknownMetaChains()  # 肯定是全部未识别的
        while True:
            cur_meta_chain = getCurMetaChainBySegmentResult(cur_segment_result)
            if not cur_meta_chain:
                break
            _unknown_meta_chains.append(cur_meta_chain[1])  # 取中间实际的meta_chain
        return _unknown_meta_chains


class ResegmentedUnknownMetaChain(list):
    """
    将未识别的meta.mvalue使用其他未识别的meta重分之后，生成的meta_chain
    """


class ResegmentedUnknownMetaChains(list):
    """
    将未识别的meta.mvalue使用其他未识别的meta重分之后，生成的meta_chain
    """
