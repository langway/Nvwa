"""
线性输入（字符串、list）模式处理的帮助类
"""
__author__ = 'Leon'

from collections import Sized
# import heapq


def createDoubleFrequancyDict(iterable_objs: list,
                              unknowns_tolerate_dgree=1.0,
                              filters: list = None,
                              key_connector: str = None,
                              divideByTotalLength=False):
    """
    根据输入的线性序列，创建双字-频率字典（在调用前应使用segmentWithStopMarksAndNumbersAndEnglish进行处理，得到的是应该是中文串、数字串、英文串）
    :param iterable_objs: 元数据字符串（List），形式为：[元数据字符串,是否需要先学习]
    :return:doubleFrequancyDict,total_length
    """
    doubleFrequancyDict = {}

    # 检查参数
    if not iterable_objs:  # 如果没有元输入，直接返回
        return doubleFrequancyDict, 0

    total_length = 0
    for iterable_obj in iterable_objs:
        # 这里应该是中文、数字串、英文串分开的
        doubleFrequancyDict, length = __createDoubleFrequancyDictByIterableObj(iterable_obj,
                                                                               doubleFrequancyDict,
                                                                               filters=filters,
                                                                               key_connector=key_connector)
        total_length += length

    if divideByTotalLength:
        # 这里需要计算其占总字数的比率，作为最后取得的词频，其计算公式为：
        # 总出现次数*字数/总字数
        for key, freq in doubleFrequancyDict.items():
            freq = freq * unknowns_tolerate_dgree / total_length
            doubleFrequancyDict[key] = freq

    return doubleFrequancyDict, total_length


def __createDoubleFrequancyDictByIterableObj(iterable_obj,
                                             doubleFrequancyDict: dict,
                                             filters: list,
                                             key_connector: str = None):
    """
    根据输入的线性序列，创建双字-频率字典
    :param iterable_obj:线性序列(这里应该是中文、数字串、英文串分开的)
    :param stopMarks:
    :param doubleFrequancyDict:
    :param stopMarkLevel:
    :param keepStopMark:是否保留分割的标点
    :return:doubleFrequancyDict,length
    """
    if doubleFrequancyDict is None:
        doubleFrequancyDict = {}
    if not isinstance(iterable_obj, str) and not isinstance(iterable_obj, Sized):
        return doubleFrequancyDict, 0
    length = len(iterable_obj)
    for i in range(length - 1):
        cur_obj = iterable_obj[i]
        next_obj = iterable_obj[i + 1]


        # 过滤掉数字、空格、需要忽略的首字（例如：的）、标点符号，在理解过程中，将优先处理数字
        if not __is_filtered(cur_obj, next_obj, filters):
            continue

        if key_connector:
            key = str(cur_obj) + key_connector + str(next_obj)
        else:
            key = str(cur_obj) + str(next_obj)

        if key in doubleFrequancyDict:
            doubleFrequancyDict[key] += 1.0
        else:
            doubleFrequancyDict[key] = 1.0

    return doubleFrequancyDict, length


def __is_filtered(cur_obj, next_obj, filters):
    if not filters:
        return True
    for filter in filters:
        if filter(cur_obj) and filter(next_obj):  # 只要有一个能够通过滤器，就算通过
            return True

    return False


def getThresholdContinuousBlocks(doubleFrequancyDict, topNum: int = 3):
    """
    从DoubleFrequancyDict根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取），包括：独立成字符块的阀值，连续连接成词的阀值。
    :param doubleFrequancyDict:
    :return:
    """
    li = list(doubleFrequancyDict.values())
    li.sort(reverse=True)
    if len(li) < topNum:
        return li[-1]
    else:
        return li[topNum - 1]

    # max_num_list = list(map(li.index, heapq.nlargest(3, li)))
    # print(max_num_list)


def extractPattern(iterable_objs: list,
                   doubleFrequancyDict,
                   threshold_ContinuousBlocks,
                   key_connector: str = None):
    """
    根据元输入，从metaNet根据阀值和元输入的位置提取元数据（可能有多个）
    :param iterable_objs: 元输入，用以查找其关键字出现位置
    :param doubleFrequancyDict: 元数据网及其原始输入的长度，其格式为：({字符串:频率},total_length)
    :param threshold_ContinuousBlocks: 提取元数据的频率阀值（超过该阀值才提取），连续连接成词的阀值。
    :param should_segment:是否直接分割字符串。
    :return:1、WordFrequncyDict：最终取得的元数据，其格式为{元输入（字符串）:词频（平均值）}
             2、segmentedBlocks：最终取得的元数据匹配分割后的根据词频连接的输入字符串（字符块），格式为：
                {"北京举办新年音乐会真棒":[["北京举办",0,False],["新年音乐会",4,True],["真棒",9,False]]}
                含义为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}
    """
    # 检查参数
    if iterable_objs is None or not isinstance(iterable_objs, list):
        return
    if not doubleFrequancyDict:
        return None

    candidates_continuous = {}  # 连续连接成词的备选词列表，其格式为：{字符串:频率（平均值）}

    for k, v in doubleFrequancyDict.items():
        if v >= threshold_ContinuousBlocks:  # 连续连接成词的阀值判断其频率，如果频率高于阀值，添加到备选列表
            candidates_continuous[k] = v
    if len(candidates_continuous) == 0:  # 如果没有备选词列表
        return candidates_continuous

    # 取得包含备选词的所有字符串，
    # 格式为{"新年音乐会中的音乐很动听":["音乐",2,8],["乐会",3,6],["音乐",7,8]}
    # 其含义为：关键字，起始位置，词频
    new_patterns = {}  # 最终取得的元数据（单词字符串的形式）,其格式为{元输入（字符串）:词频（平均值）}

    for iterable_obj in iterable_objs:
        if not isinstance(iterable_obj,str):
            str_obj = ""
            for item in iterable_obj:
                if str_obj == "":
                    str_obj=str(item)
                    continue
                if key_connector:
                    str_obj += key_connector + str(item)
                else:
                    str_obj += str(item)
        else:
            str_obj=iterable_obj

        str_obj = str_obj.strip()
        if not str_obj:
            continue

        word_position_frequency = __getWordPosition(candidates_continuous, str_obj,key_connector)

        if not word_position_frequency:
            continue
        # {"北京举办新年音乐会":[["北京举办新年",0,False],["音乐会",6,True]]}
        # 含义为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}
        # 取得前后关联的两个词，输入：北京举办新年音乐会，结果["音乐会",6,7]，6为起始位置，7为所有匹配词（音乐+乐会）的词频
        connectedWords = __getConnectedWords(word_position_frequency,key_connector)
        if not connectedWords:
            continue
        curIndex = 0

        for word, position, frequncy in connectedWords:
            # 如果是完整输入，相当于未识别，继续下一个
            if word == str_obj.strip():
                continue
            if not word in new_patterns:  # 这里面的frequncey只需要计算一次（其他循环都是相同的），所以不用考虑已经有该元数据的情况
                new_patterns[word] = frequncy

            # 取得输入字符串中包含的所有根据元数据分割后得到的字符串及其位置、是否是元数据
            # 结果为：{"北京举办新年音乐会":[["北京举办新年",0,False],["音乐会",6,True]]}
            # （格式为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}）
            if position >= curIndex:
                curIndex = position + len(word)
                if key_connector:
                    curIndex -= len(key_connector)
            else:
                raise Exception("位置给定错误！当前元数据：{0}，当前位置：{1}".format(word, str(position)))

    # # 【不再考虑】这里要避免将所有元输入直接作为元词块（一个重复的词块都没有）
    # for rawinput in rawInputs:
    #     segmentedBlock=segmentedBlocks.get(rawinput)
    #     if segmentedBlock and len(segmentedBlock)==1 and segmentedBlock[0][0]==rawinput:
    #         # 更改分割后的结果为：未识别
    #         segmentedBlock[0][2]=False
    #         return None,segmentedBlocks

    return new_patterns

    # pass  def extractRawMetaData(doubleFrequancyDict,thresholds,referenceInputs):


def __getWordPosition(candidateWords, rawInput,key_connector: str = None):
    """
    查找输入的字符串列表中所有包含某一字符串的字符串（提取元数据使用）
    :param candidateWords: 某一关键词的字符串
    :param rawInputs: 输入的字符串列表
    :return:当输入关键词"音乐"时，会产生的格式为{"新年音乐会中的音乐很动听":["音乐",2,8],["乐会",3,6],["音乐",7,8]}
    其含义为：关键字，起始位置，词频
    """
    word_position_frequency_list = []

    for i in range(len(rawInput) - 1):
        end=i + 2
        if key_connector:
            end+=len(key_connector)
        key = rawInput[i:end]
        if key in candidateWords:
            word_position_frequency_list.append([key, i, candidateWords[key]])

    return word_position_frequency_list
    # def __getWordPositions(candidateWords, rawInputs):


def __getConnectedWords(word_position_frequency_list,key_connector: str = None):
    """
    根据词频和顺序链接字符串（提取元数据使用）。
    :param word_position_frequency_list:
    :return:输入：北京举办新年音乐会，结果["新年音乐会",4,17]，4为起始位置，17为所有匹配词（新年+年音+音乐+乐会）的词频
    """
    proceed = []
    result = []
    length = len(word_position_frequency_list)
    for i in range(length):
        if i in proceed:
            continue
        word, position, frequency = word_position_frequency_list[i]

        frequncy_num = 1
        for j in range(i + 1, length):
            if j in proceed:
                continue
            nextword, nextposition, nextfrequency = word_position_frequency_list[j]

            if key_connector:
                connector_length=len(key_connector)
            else:
                connector_length=0
            if nextposition - position-connector_length == j - i:  # 如果两者是相连的
                word += nextword[1:2+connector_length]
                frequency += nextfrequency
                proceed.append(j)
                frequncy_num += 1

        # 前后相连的n个词块的共同频率的计算公式为：
        # （前词块频率+后词块频率）/n
        frequency = frequency / frequncy_num
        result.append([word, position, frequency])  # 添加到结果
        proceed.append(i)  # 标记为已处理

    return result
