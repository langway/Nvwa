#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from loongtian.util.common.enum import Enum


class ObjType(Enum):
    """
    nvwa对象类型枚举。
    """
    UNKNOWN = 0

    # ####################################
    #      元数据
    # ####################################
    META_DATA = 1  # 元数据的总类(未分类的元数据类型)
    # MetaData.type属性的对应枚举类，与数据库中定义一致。
    # UNCLASSIFIED_METADATA = 10 # 未分类的元数据类型
    WORD = 11  # 文字类型元数据
    SOUND = 12  # 声音类型元数据
    PICTURE = 13  # 图片类型元数据
    VIDEO = 14  # 影像类型元数据
    FILE = 15  # 文件类型元数据
    NEURON = 16  # 神经网络元数据
    WEB_FILE = 17  # 网络地址类型元数据

    # ####################################
    #      元数据网。
    # ####################################
    META_NET = 2  # 元数据网

    # ####################################
    #      实际对象类型枚举。
    # ####################################
    REAL_OBJECT = 3  # 实际对象的总类（未分类的实际对象类型）
    # UNCLASSIFIED_REALOBJECT = 30 # 未分类的实际对象类型
    EXISTENCE = 30  # 实对象（可以通过感知器感知的实际存在的对象，
    # 例如“爱因斯坦”，“这头牛”，“曹操”,“天安门”可以理解为类的实例。
    # 特别需要注意的是：实对象也可以由虚对象构成，
    # 但需要实对象的值进行填充【这时需要引入值、值域的概念】）
    OBSERVER = 301  # 观察者-观察的知识关联关系

    VIRTUAL = 31  # 虚对象（不可以通过感知器感知的不实际存在的对象，例如“牛”，“人类”,是大脑经过抽象提炼出的对象，可以理解为类）在人类的语言中，大部分为虚对象

    GENERATED_ENTITY = 310  # 根据动作迁移产生的新实体对象，例如：小明的手机是苹果，小明的手机就是新实体，需在存储时进行处理（暂时转换成VIRTUAL对象【待考虑】）
    PLACEHOLDER = 311  # 占位符类型实际对象，模式生成中使用
    # 用户管理部分
    USER = 312  # 作为用户的实际对象
    ASSISTANT = 313  # 用户的个人助理

    LINEAR_EXE_MEANING_VALUE = 390  # 意义的值（女娲系统的意义的值只能有一个实际对象，或为一个表示集合的实际对象！）
    CONJUGATED_EXE_MEANING_VALUE = 391
    CONTEXT_EXE_MEANING_VALUE = 392

    CODE = 4

    EMOTION = 5  # 情感实际对象(预留)

    # ####################################
    #      动作类实际对象类型枚举。其中：Instinct\Action\Modifier为可执行性的实际对象（executable ）
    # ####################################
    ACTION = 6  # 动作类实际对象
    COMMON_ACTION = 60  # 动作类实际对象
    INSTINCT = 61  # 内置实际对象（本能，包括元对象、顶级关系）
    ORIGINAL = 610  # 内置元对象（本能，元对象、元集合、元知识等）
    TOP_RELATION = 611  # 顶级关系（本能，成分、属性、父对象等）

    INNER_OPERATION = 62  # 女娲系统内部操作对象 用来连接外部对象与内部代码

    # ####################################
    #      知识链。
    # ####################################
    # 知识对象（实际对象链）类型枚举。
    KNOWLEDGE = 7  # 真正的知识\实际对象链（不作为模式或意义的知识链）
    # REAL_KNOWLEDGE = 40

    LINEAR_EXE_INFO = 71  # 作为可执行信息（模式和意义）的知识链（里面有placeholder）。RealObject的模式（kid）,当RealObject为动词或修限词时。
    CONJUGATED_EXE_INFO = 72  # 作为线性结构的可执行信息（模式和意义）的知识链（里面有placeholder）。
    CONTEXT_EXE_INFO = 73  # 作为上下文结构的可执行信息（模式和意义）的知识链（里面有placeholder）。

    # 模式的知识链只有一个。
    # 意义的知识链（应该看做集合，每个元素看做一步，哪怕只有一个元素）
    # 意义对应的每一步知识链:step1-step2...
    # 每一步知识链的的转换模式（一个状态集合，可以有多个状态转换）：status1,status2...
    # 2018-12-14 leon：不再区分模式和意义，因为有可能会复用。
    # 例如：p1-抬手，在 小明-抬手形成的模式中，就是模式，在小明-打-小丽中，就是意义
    # PATTERN = 41 # 作为模式的知识链
    # MEANING = 42  # 作为意义的知识链（应该看做集合，每个元素看做一步，哪怕只有一个元素）。RealObject的含义（意义为）（rid），当RealObject为动词或修限词时时。
    # MEANING_STEP = 421  # 意义对应的每一步知识链:step1-step2...
    # MEANING_STATUS = 422  # 每一步知识链的的转换模式（一个状态集合，可以有多个状态转换）：status1,status2...

    # COLLECTION = 5  # 集合对象类型
    # DOMAIN = 0x0400

    # ####################################
    #      分层对象。
    # ####################################
    LAYER = 9  # 分层对象类型，例如：MetaData-RealObject


    @staticmethod
    def getSubTypes(type, level=2):
        """
        取得当前类型的子类型，例如：元数据的子类型包括文字、声音等。
        :param type:
        :return:
        """
        sub_types = []
        for attr_value, attr_name in ObjType._value_name_dict.items():
            for i in range(1, level + 1):
                if type * (10 ** i) <= attr_value <= type * (10 ** i) + 9 ** int(i * '1'):
                    sub_types.append(attr_value)

        sub_types.sort()
        return sub_types

    @staticmethod
    def getParentType(type, level=2):
        """
        取得当前类型的最顶层类型，例如：文字、声音等的最顶层类型为元数据。
        :param type:
        :return:
        """
        parent_types = []
        for i in range(1, level + 1):
            parent_type=type // (10 ** i)
            if parent_type>0:
                parent_types.append(parent_type)

        parent_types.sort()
        return parent_types


    @staticmethod
    def isUnknown(type):
        """
        是否是未知的对象类型
        :param type:
        :return:
        """
        if type == ObjType.UNKNOWN:
            return True
        if ObjType._value_name_dict.get(type):
            return False
        return True

    @staticmethod
    def isMetaData(type):
        """
        是否是元数据的总类(未分类的元数据类型)
        :param type:
        :return:
        """
        return type == ObjType.META_DATA or \
               (ObjType.META_DATA * 10 <= type <= ObjType.META_DATA * 10 + 9)

    @staticmethod
    def isWord(type):
        """
        是否是文字类型元数据
        :param type:
        :return:
        """
        return type == ObjType.WORD

    @staticmethod
    def isSound(type):
        """
        是否是声音类型元数据
        :param type:
        :return:
        """
        return type == ObjType.SOUND

    @staticmethod
    def isPicture(type):
        """
        是否是图片类型元数据
        :param type:
        :return:
        """
        return type == ObjType.PICTURE

    @staticmethod
    def isVideo(type):
        """
        是否是影像类型元数据
        :param type:
        :return:
        """
        return type == ObjType.VIDEO

    @staticmethod
    def isFile(type):
        """
        是否是文件类型元数据
        :param type:
        :return:
        """
        return type == ObjType.FILE

    @staticmethod
    def isNeuron(type):
        """
        是否是神经网络元数据
        :param type:
        :return:
        """
        return type == ObjType.NEURON

    @staticmethod
    def isWebFile(type):
        """
        是否是网络地址类型元数据
        :param type:
        :return:
        """
        return type == ObjType.WEB_FILE

    @staticmethod
    def isMetaNet(type):
        """
        是否是元数据网
        :param type:
        :return:
        """
        return type == ObjType.META_NET

    @staticmethod
    def isRealObject(type):
        """
        是否是实际对象的总类（未分类的实际对象类型）
        :param type:
        :return:
        """
        return type == ObjType.REAL_OBJECT or \
               (ObjType.REAL_OBJECT * 10 <= type <= ObjType.REAL_OBJECT * 10 + 9) or \
               (ObjType.REAL_OBJECT * 100 <= type <= ObjType.REAL_OBJECT * 100 + 99)

    @staticmethod
    def isExistence(type):
        """
        是否是实对象（可以通过感知器感知的实际存在的对象，例如“爱因斯坦”，“这头牛”，“王阳明”,可以理解为类的实例）
        :param type:
        :return:
        """
        return type == ObjType.EXISTENCE

    @staticmethod
    def isVirtual(type):
        """
        是否是虚对象（不可以通过感知器感知的不实际存在的对象，
        例如“牛”，“人类”,是大脑经过抽象提炼出的对象，可以理解为类）
        在人类的语言中，大部分为虚对象
        :param type:
        :return:
        """
        return type == ObjType.VIRTUAL or \
               (ObjType.VIRTUAL * 10 <= type <= ObjType.VIRTUAL * 10 + 9)

    @staticmethod
    def isAction(type):
        """
        是否是动作类实际对象
        :param type:
        :return:
        """
        return type == ObjType.ACTION or \
               (ObjType.ACTION * 10 <= type <= ObjType.ACTION * 10 + 9) or \
               (ObjType.ACTION * 100 <= type <= ObjType.ACTION * 100 + 99)

    # @staticmethod
    # def isMotify(type):
    #     """
    #     是否是修限类实际对象（目前未使用）
    #     :param type:
    #     :return:
    #     """
    #     return type == ObjType.MOTIFIER

    # @staticmethod
    # def isTopRelation(type):
    #     return type==RealObjectType.TOP_RELATION

    @staticmethod
    def isInstinct(type):
        """
        是否是内置实际对象（本能，包括顶级关系）
        :param type:
        :return:
        """
        return type == ObjType.INSTINCT or \
               (ObjType.INSTINCT * 10 <= type <= ObjType.INSTINCT * 10 + 9)

    @staticmethod
    def isExecutable(type):
        """
        是否是可执行性的实际对象（包括Instinct/Action/Modifier）
        :param type:
        :return:
        """
        return ObjType.isInstinct(type) or \
               ObjType.isAction(type)
        # type == ObjType.MOTIFIER  # or type==ObjType.KNOWLEDGE

    @staticmethod
    def isPlaceHolder(type):
        """
        是否是占位符类型实际对象，模式生成中使用
        :param type:
        :return:
        """
        return type == ObjType.PLACEHOLDER

    @staticmethod
    def isGeneratedEntity(type):
        """
        是否是根据动作迁移产生的新实体对象，例如：小明的手机是苹果，小明的手机就是新实体，需在存储时进行处理（暂时转换成VIRTUAL对象【待考虑】）
        :param type:
        :return:
        """
        return type == ObjType.GENERATED_ENTITY

    @staticmethod
    def isUser(type):
        """
        是否是作为用户的实际对象
        :param type:
        :return:
        """
        return type == ObjType.USER

    @staticmethod
    def isAssistant(type):
        """
        是否是用户的个人助理
        :param type:
        :return:
        """
        return type == ObjType.ASSISTANT

    @staticmethod
    def isCode(type):
        """
        是否是代码对象类型
        :param type:
        :return:
        """
        return type == ObjType.CODE

    @staticmethod
    def isInnerOperation(type):
        """
        是否是真正的知识\实际对象链（不作为模式或意义的知识链）
        :param type:
        :return:
        """
        return type == ObjType.INNER_OPERATION

    @staticmethod
    def isKnowledge(type):
        """
        是否是真正的知识\实际对象链（不作为模式或意义的知识链）
        :param type:
        :return:
        """
        return type == ObjType.KNOWLEDGE or (type >= ObjType.KNOWLEDGE * 10 and type <= ObjType.KNOWLEDGE * 10 + 9)

    @staticmethod
    def isExeInfo(type):
        """
        是否是作为模式的知识链。RealObject的模式（kid）,当RealObject为动词或修限词时。
        :param type:
        :return:
        """
        return type == ObjType.LINEAR_EXE_INFO

    # @staticmethod
    # def isMeaning(type):
    #     """
    #     是否是作为意义的知识链。RealObject的含义（意义为）（kid），当RealObject为动词或修限词时时。
    #     :param type:
    #     :return:
    #     """
    #     return type == ObjType.MEANING # or (type >= 421 and type <= 422)

    @staticmethod
    def isLayer(type):
        """
        是否是分层对象类型，例如：MetaData-RealObject
        :param type:
        :return:
        """
        return type == ObjType.LAYER

    @staticmethod
    def isObserver(type):
        """
        是否是观察者对象类型，例如：Observer-RealObject
        :param type:
        :return:
        """
        return type == ObjType.OBSERVER


    @staticmethod
    def isInstance(type, parent_type):
        """
        判断一个对象类型是否是父对象类型或其的子类型
        :param type:
        :param parent_type:
        :return:
        """
        if type == parent_type:
            return True
        sub_types = ObjType.getSubTypes(parent_type, level=2)
        if sub_types and type in sub_types:
            return True
        return False


ObjType = ObjType()


class LayerDirection(Enum):
    """
    方向（上层、下层）
    """
    UNKNOWN = 0
    UPPER = 1
    LOWER = 2
    BOTH = 3  # 全方向


LayerDirection = LayerDirection()


class DBValueType(Enum):
    """
    数据库数据类型（对应postgre）
    """
    # ######################
    # 数值数据类型
    # ######################
    smallint = 11  # 存储整数，小范围	2字节	-32768 至 +32767
    integer = 12  # 存储整数。使用这个类型可存储典型的整数	4字节	-2147483648 至 +2147483647
    bigint = 13  # 存储整数，大范围。	8字节	-9223372036854775808 至 9223372036854775807
    decimal = 14  # 用户指定的精度，精确	变量	小数点前最多为131072个数字; 小数点后最多为16383个数字。
    numeric = 15  # 用户指定的精度，精确	变量	小数点前最多为131072个数字; 小数点后最多为16383个数字。
    real = 16  # 可变精度，不精确	4字节	6位数字精度
    double = 17  # 可变精度，不精确	8字节	15位数字精度
    serial = 18  # 序列号类型 自动递增整数	4字节	1 至 2147483647
    bigserial = 19  # 序列号类型 大的自动递增整数	8字节	1 至 9223372036854775807

    # ######################
    # 字符串数据类型
    # ######################
    char_size = 21  # 这里size是要存储的字符数。固定长度字符串，右边的空格填充到相等大小的字符。
    character = 22  # 这里size是要存储的字符数。 固定长度字符串。 右边的空格填充到相等大小的字符。
    varchar = 23  # 这里size是要存储的字符数。 可变长度字符串。
    character_varying = 24  # 这里size是要存储的字符数。 可变长度字符串。
    text = 25  # 可变长度字符串。
    # ######################
    # 日期/时间数据类型
    # ######################
    timestamp = 31  # 日期和时间(无时区)	8字节	4713 bc	294276 ad	1微秒/14位数
    timestamp_with_zone = 32  # 包括日期和时间，带时区	8字节	4713 bc	294276 ad
    date = 33  # 日期(没有时间)	4字节	4713 bc	5874897 ad	1微秒/14位数
    time = 34  # 时间(无日期)	8字节	00:00:00	24:00:00	1微秒/14位数
    time_with_zone = 35  # 仅限时间，带时区	12字节	00:00:00+1459	24:00:00-1459	1微秒/14位数
    interval = 36  # 时间间隔	12字节	-178000000年	178000000年	1微秒/14位数
    # ######################
    # 布尔类型
    # ######################
    boolean = 41  # 它指定true或false的状态。	1字节
    # ######################
    # 货币类型
    # ######################
    money = 51  # 货币金额 8 字节 - 92233720368547758.08 至 + 92233720368547758.07
    # ######################
    # 几何类型
    # ######################
    point = 61  # 16字节	在一个平面上的点	(x,y)
    line = 62  # 32字节	无限线(未完全实现)	((x1,y1),(x2,y2))
    lseg = 63  # 32字节	平面中的有限线段	((x1,y1),(x2,y2))
    box = 64  # 32字节	矩形框	((x1,y1),(x2,y2))
    path = 65  # 16+16n字节	封闭路径(类似于多边形)	((x1,y1),…)
    polygon = 66  # 40+16n字节	多边形(类似于封闭路径)	((x1,y1),…)
    circle = 67  # 24字节	圆	<(x，y)，r>(中心点和半径)

    # ######################
    # 数据类型
    # ######################
    bit = 71  # 定长位串
    bit_varying = 72  # 变长位串
    bytea = 73  # 二进制数据（"字节数组"）

    # ######################
    # 文档级别的数据类型
    # ######################
    tsquery = 81  # 全文检索查询
    tsvector = 82  # 全文检索文档
    txid_snapshot = 83  # 用户级别事务ID快照
    uuid = 84  # 通用唯一标识符 PostgreSQL还接受下面几种格式，其中的十六进制位可以是大写的：
    # （1）A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11
    # （2）{a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11}
    # （3）a0eebc999c0b4ef8bb6d6bb9bd380a11
    xml = 85  # XML数据

    # ######################
    # 网络地址数据类型
    # ######################
    cidr = 91  # IPv4或者IPv6  网络地址
    inet = 92  # IPv4 或者 IPv6 网络地址
    macaddr = 93  # MAC地址

DBValueType=DBValueType()

class WhereRelation(Enum):
    """
    查询参数(条件)之间的关系（and/or）
    """
    AND = 0
    OR = 1

WhereRelation=WhereRelation()
