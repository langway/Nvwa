#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'


class GeneralCharacter(object):
    """
    整个系统的通用性格。
    女娲AI的个性设置，例如：对事物的激活度（决定联想力等）、遗忘程度等
    :rawParam
    构造函数参数说明
    :attribute
    对象属性说明
    """
    def __init__(self):
        # 从DoubleFrequancyDict根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取），包括：独立成字符块的阀值，连续连接成词的阀值。
        # MetaDataExtractThreshold_SingleBlock =0.09 # 从DoubleFrequancyDict根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取），随着理解的元数据的增多，其阀值应该逐渐增加
        # 从metaNet根据阀值和元输入的位置提取元数据（可能有多个）的频率阀值（超过该阀值才提取）
        self.MetaDataExtractThreshold_ContinuousBlocks = 0.15

        # 指定进行二元、三元关系计算的“元数”,对匹配出来的字符块链进行排序，目前使用邻接匹配法——ngram，
        # 二元字符块（bigram）相当于有向图（为丁字形结构特例），三元字符块（trigram）及以上相当于丁字型结构的分解
        self.GramNum = 2

        # 所有女娲系统内部操作使用的对象的初始权重
        self.System_Obj_Weight = 1000000.0

        self.Original_Link_Weight = 0.02  # 所有两两关联的对象之间的初始权重（例如Layer、MetaData-RealObject等）

        self.Inner_Thinking_Link_Weight = 1.0 # todo 内部思考的对象建立起的权重，是否应该比外部输入建立的初始权重大，待思考。
        self.Inner_Instinct_Link_Weight = self.Inner_Thinking_Link_Weight * 10.0 # 系统内部关于直觉思考时建立的权重

        self.Unknowns_Tolerate_Dgree = 0.999 # 对陌生事物的容忍度，由女娲的性格进行控制(尽量在0.98-1.0之间微调)

        self.Misunderstood_Rethink_Depth = 8 # 避免无限制思考一个理解不了的输入，要考虑重新思考的次数

        self.Search=GeneralCharacter._Search() # 关于数据库查找的参数
        self.Humor = GeneralCharacter._Humor() # 女娲系统对幽默参数的定义。
        self.RecognizedRatio = GeneralCharacter._RecognizedRatio() # 用来计算实际对象已被识别的比率
        self.Association = GeneralCharacter._Association() # 对一个实际对象进行联想的参数

    class _Search(object):
        """
        关于数据库查找的参数
        """
        def __init__(self):
            """
            关于数据库查找的参数
            """
            self.Knowledge_Forwards_Depth = 3  # 向前查找知识链的层深，数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长
            self.Knowledge_Backwards_Depth = 3  # 向后查找知识链的层深，数值越大，查找到的知识链越多，但需要处理的也越多，系统耗时越长

    class _Humor():
        """
        女娲系统对幽默参数的定义。
        """

        """
        nvwa系统对幽默的定义为：
            幽默，是指一种超出了正常处理范围和处理结果，但又对Myself的情感没有伤害或威胁的评估结果。
        主要包括以下几个方面:
        1、字符串分词层面。例如：输入：用“如果”造句，回答：汽水不如果汁营养。/假如果汁不好喝就不要喝。你输入：南京市长江大桥，如果系统将低概率分词结果进行处理，就可能反馈“江大桥是谁？”
        2、语义层面。
            （1）meta到realobject选择。例如：输入：苹果很好吃，回答：手机怎么能吃？
            （2）realobject的构成错误。例如：苹果的颜色蓝黄相间。孩子：我的尾巴受伤了。我的其中一只左脚受伤了。人没有尾巴，人只有一只脚，所以会产生幽默效果。
            （3）上下文的导出错误（不一致）。例如：如果我拼命学习，努力考试，那么我的人生还有什么意义？！
        3、语用层面：小明一下跳了5000米高！
        4、语境层面
            （1）语境不一致。例如：输入：请你用况且造句。回答：一列火车经过，况且况且况且况且……。本来的语境：况且产生的递进层面的众多情境，回答的语境：火车声音产生的情境
            （2）接着错误语境，而进一步产生符合语境逻辑的下文。例如：孩子：我的尾巴受伤了。爸爸：爸爸帮你吹吹，吹吹就不疼了！
            （3）文化导致的语境不一致。例如：输入：问候你老母！（侮辱语境）/我想和你母亲上床！（侮辱语境） 外国人：谢谢！（交际语境）/ 哦，不行，我妈妈虽然年轻时候很漂亮，但现在已经80了（构成语境）
        更多请参考《\doc\joke\笑话参考.docx》
        再如：南京市长江大桥：
        南京市 长江大桥
        南京 市长 江大桥
          解构的程度不一样，引起的幽默感觉就不一样
        """
        def __init__(self):
            """
            女娲系统对幽默参数的定义。
            """
            self.MetaChainSelectionDeepth = 2 # 字符串分词后选择拼接的深度，深度越深，错误可能性越高，幽默程度越高，但不像人的感觉越高
            self.MetaRealSelectionDeepth = 3 # 从meta到realobject选择深度

    class _RecognizedRatio():
        """
        用来计算实际对象已被识别的比率
        :remarks:
        如果已经有父对象（除original_object之外）+10.0，n个乘n
        有构成（顶级关系） +5.0 ，n个乘n
        无构成，但有关联 与其他对象关联+1.0，n个乘n；被其他对象关联+0.5，n个乘n
        """
        def __init__(self):
            """
            用来计算实际对象已被识别的比率
            """
            self.Has_Parent_Ratio = 10.0
            self.toprelation_ratio = 5.0
            self.link_others_ratio = 1.0
            self.other_links_ratio = 0.5

    class _Association():
        """
        对一个实际对象进行联想的参数
        """
        def __init__(self):
            """
            对一个实际对象进行联想的参数
            """
            self.Real_Constituent_Depth =5 # 构成方面的联想深度。实际对象1-构成1-实际对象2-构成3...，
            self.Knowledge_Search_Depth = 5 # 知识链的后链的联想搜索深度 第一层：[牛-有] 第二层：[牛-有-腿]，[牛-有-头]...

Character=GeneralCharacter()

class PersonalCharacter(GeneralCharacter):
    """
    每个用户个人助理大脑的单独性格(个性化性格)
    """

    def __init__(self,brain):
        """
        每个用户个人助理大脑的单独性格
        :param brain:
        """
        super(PersonalCharacter,self).__init__()

        self.brain=brain

    def init(self):
        """
        加载个性化性格
        :return:
        """
