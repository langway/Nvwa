#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.nvwa.engines.engineBase import ThinkEngineBase
from loongtian.util.log import logger
from loongtian.nvwa.engines import patternHelper
from loongtian.nvwa.runtime.pattern import LinearPattern
from loongtian.util.common.generics import GenericsList


class PatternEngine(ThinkEngineBase):
    """
    模板引擎。
    """

    def __init__(self, thinkingCentral):
        """
        模板引擎。
        :param thinkingCentral:
        """
        super(PatternEngine, self).__init__(thinkingCentral)

    def createLinearPattern(self, reals):
        """
        根据实际对象列表创建线性模式。
        :param reals:
        :return:
        :remark:目前发现的线性pattern包括：
        1、修限型
        （1）R1-...Rn，例如：中国人民银行
        （2）A1R2，例如：说话
        （3）A1A2，例如：跑了、开关、伟大
        （4）A1A2A3，例如：打跑了
        （5）A1A2R1，例如：跑是动作，跑了一圈
        （6）R1A1A2，例如：动作包含跑，牛能叫

        2、集合型（一般为同一父对象）
        （1）R1-...Rn，例如：四五六七、苹果橘子香蕉
        （2）A1A2...An，例如：跑跳蹲
        具体生成的pattern格式为：
        {R1:[False,{operation1:frequncy,...},]}
        """

    def createObjTypeDoubleFrequancyDict(self, objTypesList: list,
                                         unknowns_tolerate_dgree=1.0,
                                         filters: list = None,
                                         key_connector: str = None,
                                         divideByTotalLength=False):
        """

        :param objTypesList: 元输入字符串（List），形式为：[[元输入字符串,是否需要先学习]]
        :param unknowns_tolerate_dgree: 对陌生事物的容忍度，由女娲的性格进行控制
        :param filters:
        :param key_connector:
        :return: doubleFrequancyDict,total_length
        """
        doubleFrequancyDict, total_length = patternHelper.createDoubleFrequancyDict(
            objTypesList,
            unknowns_tolerate_dgree=unknowns_tolerate_dgree,
            filters=filters,
            key_connector=key_connector,
            divideByTotalLength=divideByTotalLength)  # ,self.DoubleFrequancyDict) # 不再将现有的DoubleFrequancyDict传入，以便计算单次输入提取的元数据。

        return doubleFrequancyDict, total_length

    def extractObjTypePattern(self,
                              objTypesList: list,
                              unknowns_tolerate_dgree=1.0,
                              key_connector: str = None):
        """
        根据元输入，从单双字-频率字典提取元词块（可能有多个）（传入self.WordFrequncyDict）
        规则：双字-频率字典根据阀值和元输入的位置，1、如果连续词块超过指定阀值，即将其进行拼接；2、如果备选词块在元输入中独立存在，也进行提取
        :rawParam rawInputs: 元输入，用以查找其关键字出现位置
        :return:1、WordFrequncyDict：最终取得的元数据，其格式为{元输入（字符串）:词频（平均值）}
             2、segmentedBlocks：最终取得的元数据匹配分割后的根据词频连接的输入字符串（字符块），格式为：
                {"北京举办新年音乐会真棒":[["北京举办新年",0,False],["音乐会",6,True],["真棒!",9,False]]}
                含义为：{输入字符串:[第n个分割后得到的字符串,起始位置,是否是元数据]}
        """

        # 1、根据双字-频率字典提取元词块（可能有多个）（传入self.WordFrequncyDict）
        doubleFrequancyDict, length = self.createObjTypeDoubleFrequancyDict(objTypesList,
                                                                            unknowns_tolerate_dgree=unknowns_tolerate_dgree,
                                                                            filters=filters,
                                                                            key_connector=key_connector)
        if not doubleFrequancyDict:
            return None

        threshold_ContinuousBlocks = patternHelper.getThresholdContinuousBlocks(doubleFrequancyDict)
        str_new_objtype_patterns = patternHelper.extractPattern(objTypesList,
                                                                doubleFrequancyDict,
                                                                threshold_ContinuousBlocks,
                                                                key_connector=None)

        new_objtype_patterns = {}
        for str_new_objtype_pattern, freq in str_new_objtype_patterns.items():
            str_obj_types = str_new_objtype_pattern.split(key_connector)
            obj_types = GenericsList(int)
            for str_obj_type in str_obj_types:
                obj_types.append(int(str_obj_type))
            objtype_pattern = LinearPattern(obj_types)
            new_objtype_patterns[objtype_pattern] = freq
        return new_objtype_patterns

    def extractParentPattern(self, reals, unknowns_tolerate_dgree=1.0):
        """
        提取所有实际对象父对象的模式
        :param reals:
        :param unknowns_tolerate_dgree:
        :return:
        """

    # 梁启超的儿子的太太的情人的父亲
    # 下一代搜索引擎即将来临：知识图谱的用户体验报告_36氪
    # https://36kr.com/p/205737.html
    # 亚马逊、谷歌“火拼”语音助手，谁能笑到最后？ | 雷锋网
    # https://www.leiphone.com/news/201901/XWVQsPjUQWSB5SNu.html
    # 1、已知：牛-组件-腿
    #    输入：牛有腿吗？
    #    应该的输出：有

    #    输入：牛有翅膀吗？
    #    应该的输出：没有
    #    生成范式：吗?---{系统已知:有,系统未知:没有}

    # 2、已知：1的下一个是2，2的上一个是1，2的下一个是3
    #    输入：3的上一个是？
    #    应该的输出：2
    #    输入：3的下一个是？
    #    应该的输出：不知道
    #    生成范式：上一个是---{{0}的下一个是{1}，{1}的上一个是{0}}

    # 3、已知：牛有腿，牛能跑，马有腿
    #    输入：马能跑？
    #    应该的输出：能
    #    输入：兔子能跑？
    #    应该的输出：不知道
    #    生成范式：能{{0}有腿，{0}能跑}

    # 4、已知：r1-父对象-集合，r1-组件-[a,b,c],r1-数量-3
    #    输入：r2-父对象-集合，r2-组件-[a,b,c,d],r2-数量-?
    #    应该的输出：4
    #    生成范式：数量？{}

    # 5、创建集合
    # 输入：有一个集合
    # 应该的输出：r-父对象-集合

    # 输入：有一个集合[a,b,c,d]
    # 应该的输出：r-父对象-集合，k1:r-组件-a，k2:r-组件-b，k3:r-组件-c，k4:r-组件-d，k1-k2-k3-k4

    # 输入：动物的集合
    # 应该的输出：r-父对象-集合，r-组件-[牛,鸟,狗...]
    # 牛-父对象-动物...
    # 系统需定义每次取几个、最多实验取（循环）几次以可以停机

    # 6、集合的循环
    # 输入：循环[a,b,c,d]3次
    # 应该的输出：[[a,b,c,d],[a,b,c,d],[a,b,c,d]]
    # 输入：循环[a,b,c,d]
    # 应该的输出：[[a,b,c,d],[a,b,c,d],[a,b,c,d],……]

    # 7、逻辑“非”
    # 逻辑非
    # 例如：牛 不 能 飞
    # 鸟 能 飞,飞机 能 飞
    # A = {鸟,飞机}
    # 牛 ∉ A
    # 输入：鸵鸟不能飞
    # 应该的输出：集合-鸟:[鸵鸟,集合-能飞的鸟:[麻雀,乌鸦,……]]
    # 应该的输出：集合 - Original_Object:[鸵鸟, 集合 - 能飞的Original_Object:[麻雀, 乌鸦,飞机……]]
    # 输入：马没有翅膀
    # 应该的输出：集合-动物/Original_Object:[马,集合-有翅膀的动物/Original_Object:[麻雀,乌鸦,鸵鸟……]]

    # 8、逻辑“与”

    # 9、逻辑“或”

    # 10、数量词
    # 输入：两头牛
    # 应该的输出：[r1,r2] ,r1-父对象-牛，r2-父对象-牛

    # 值域
    # 水果的颜色
    # 我的衣服
    # 我的东西
    # 苹果的属性

    # 叫做什么 叫做-什么 叫（谁？）做什么

    # 如果...那么
