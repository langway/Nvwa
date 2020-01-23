#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

from unittest import TestCase
from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.runtime.reals import AdminUser
from loongtian.util.tasks.runnable import run
from loongtian.nvwa.organs.brain import Brain


class TestBrain(TestCase):

    def setUp(self):
        print("----setUp----")
        from loongtian.nvwa.organs.centralManager import CentralManager
        CentralManager._cleanDB(wait_for_command=True)
        self.brain = Brain()
        # self.brain._cleanDB()
        self.brain.init()
        run(self.brain)

    def testCreateMeaningPattern(self):
        print("——testCreateMeaningPattern——")

        #############################
        # 牛有腿
        #############################
        self.meta_niu = MetaData(mvalue="牛", memory=self.brain.MemoryCentral).create()
        self.meta_you = MetaData(mvalue="有", memory=self.brain.MemoryCentral).create()
        self.meta_tui = MetaData(mvalue="腿", memory=self.brain.MemoryCentral).create()
        self.real_niu = RealObject.createRealByMeta(self.meta_niu, realType=ObjType.VIRTUAL)
        self.real_you = RealObject.createRealByMeta(self.meta_you, realType=ObjType.COMMON_ACTION)
        self.real_tui = RealObject.createRealByMeta(self.meta_tui, realType=ObjType.VIRTUAL)

        pattern_objs = [self.real_niu, self.real_you, self.real_tui]
        # todo 应替换为Workflow
        meaning_objs = [  # meaning对应的knowledge知识链
            [  # steps：knowledge知识链的每一步的转换模式（可以有多个状态转换）
                [self.real_niu, self.brain.MemoryCentral.Instincts.instinct_component, self.real_tui],
                # status：knowledge知识链每一步中包含的每一个状态knowledge
            ],
        ]

        # # 测试分组1、没有任何可执行信息
        # grouped_reals_list, execute_sequence = self.brain.ThinkingCentral.GroupEngine.groupRealChain(pattern_objs)
        # print (grouped_reals_list)

        # pattern_knowledge=Knowledge.createKnowledgeByRealChain(pattern_objs,understood_ratio = 1.0)
        # meaning_knowledge=Knowledge.createKnowledgeByRealChain(meaning_objs,understood_ratio = 1.0)
        # 生成模式
        pattern_knowledge, meaning_knowledge = self.brain.ThinkingCentral.ModelingEngine.createExcutionInfo(
            self.real_you,
            pattern_objs,
            meaning_objs,
        )

        # 迁移模式
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 马有尾巴
        #############################
        self.meta_ma = MetaData(mvalue="马", memory=self.brain.MemoryCentral).create()
        self.real_ma = RealObject.createRealByMeta(self.meta_ma, realType=ObjType.VIRTUAL)
        self.meta_weiba = MetaData(mvalue="尾巴", memory=self.brain.MemoryCentral).create()
        self.real_weiba = RealObject.createRealByMeta(self.meta_weiba, realType=ObjType.VIRTUAL)

        pattern_objs = [self.real_ma, self.real_you, self.real_weiba]
        # 迁移模式
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 小明打小丽
        #############################
        self.meta_xiaoming = MetaData(mvalue="小明", memory=self.brain.MemoryCentral).create()
        self.meta_da = MetaData(mvalue="打", memory=self.brain.MemoryCentral).create()
        self.meta_xiaoli = MetaData(mvalue="小丽", memory=self.brain.MemoryCentral).create()

        self.meta_shouluo = MetaData(mvalue="手落", memory=self.brain.MemoryCentral).create()
        self.meta_taishou = MetaData(mvalue="抬手", memory=self.brain.MemoryCentral).create()

        self.meta_shouteng = MetaData(mvalue="手疼", memory=self.brain.MemoryCentral).create()
        self.meta_ku = MetaData(mvalue="哭", memory=self.brain.MemoryCentral).create()

        self.meta_xiaoliang = MetaData(mvalue="小亮", memory=self.brain.MemoryCentral).create()
        self.meta_xiaohong = MetaData(mvalue="小红", memory=self.brain.MemoryCentral).create()

        self.real_xiaoming = RealObject.createRealByMeta(self.meta_xiaoming, realType=ObjType.VIRTUAL)
        self.real_da = RealObject.createRealByMeta(self.meta_da, realType=ObjType.COMMON_ACTION)
        self.real_xiaoli = RealObject.createRealByMeta(self.meta_xiaoli, realType=ObjType.VIRTUAL)
        self.real_shouteng = RealObject.createRealByMeta(self.meta_shouteng, realType=ObjType.VIRTUAL)

        self.real_taishou = RealObject.createRealByMeta(self.meta_taishou, realType=ObjType.VIRTUAL)
        self.real_shouluo = RealObject.createRealByMeta(self.meta_shouluo, realType=ObjType.VIRTUAL)

        self.real_ku = RealObject.createRealByMeta(self.meta_ku, realType=ObjType.VIRTUAL)
        self.real_xiaoliang = RealObject.createRealByMeta(self.meta_xiaoliang, realType=ObjType.VIRTUAL)
        self.real_xiaohong = RealObject.createRealByMeta(self.meta_xiaohong, realType=ObjType.VIRTUAL)

        self.meta_pao = MetaData(mvalue="跑", memory=self.brain.MemoryCentral).create()
        self.real_pao = RealObject.createRealByMeta(self.meta_pao, realType=ObjType.VIRTUAL)

        pattern_objs = [self.real_xiaoming, self.real_da, self.real_xiaoli]
        # meaning_objs = [  # meaning对应的knowledge知识链
        #     [  # steps：knowledge知识链的每一步的转换模式（可以有多个状态转换）
        #         [self.real_xiaoming, self.real_shouteng],[self.real_xiaoli,self.real_ku],
        #         # status：knowledge知识链每一步中包含的每一个状态knowledge
        #     ],
        # ]
        meaning_objs = [  # meaning对应的knowledge知识链
            [  # steps：knowledge知识链的每一步的转换模式（可以有多个状态转换）
                [self.real_xiaoming, self.real_taishou], [self.real_xiaoming, self.real_shouluo],
                [self.real_xiaoming, self.real_shouteng], [self.real_xiaoli, self.real_ku],
                # status：knowledge知识链每一步中包含的每一个状态knowledge
            ],
        ]

        # 生成模式
        pattern_knowledge, meaning_knowledge = self.brain.ThinkingCentral.ModelingEngine.createExcutionInfo(
            self.real_da,
            pattern_objs,
            meaning_objs,
        )

        # 迁移模式（小明 打 小丽）
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 小明 打 小丽（再次生第一种模式，应该使用原有的）
        #############################
        # 生成模式
        pattern_knowledge, meaning_knowledge = self.brain.ThinkingCentral.ModelingEngine.createExcutionInfo(
            self.real_da,
            pattern_objs,
            meaning_objs,
        )

        # 输出结果
        self.brain.logThinkResult(str(meaning_knowledge), None)

        #############################
        # 小亮 打 小红
        #############################
        pattern_objs = [self.real_xiaoliang, self.real_da, self.real_xiaohong]

        # 迁移模式
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 小明 打 小丽（第二种模式）
        #############################
        pattern_objs = [self.real_xiaoming, self.real_da, self.real_xiaoli]

        meaning_objs = [  # meaning对应的knowledge知识链
            [  # steps：knowledge知识链的每一步的转换模式（可以有多个状态转换）
                [self.real_xiaoming, self.real_taishou], [self.real_xiaoming, self.real_shouluo],
                [self.real_xiaoming, self.real_shouteng], [self.real_xiaoli, self.real_pao],
                # status：knowledge知识链每一步中包含的每一个状态knowledge
            ],
        ]

        # 生成模式
        pattern_knowledge, meaning_knowledge = self.brain.ThinkingCentral.ModelingEngine.createExcutionInfo(
            self.real_da,
            pattern_objs,
            meaning_objs,
        )

        # 迁移模式（小明 打 小丽）
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 小明跑
        #############################

        self.meta_taiqi = MetaData(mvalue="抬起", memory=self.brain.MemoryCentral).create()
        self.real_taiqi = RealObject.createRealByMeta(self.meta_taiqi, realType=ObjType.VIRTUAL)

        self.meta_luoxia = MetaData(mvalue="落下", memory=self.brain.MemoryCentral).create()
        self.real_luoxia = RealObject.createRealByMeta(self.meta_luoxia, realType=ObjType.VIRTUAL)

        self.meta_dengdi = MetaData(mvalue="蹬地", memory=self.brain.MemoryCentral).create()
        self.real_dengdi = RealObject.createRealByMeta(self.meta_dengdi, realType=ObjType.VIRTUAL)

        pattern_objs = [self.real_xiaoming, self.real_pao]
        meaning_objs = [  # meaning对应的knowledge知识链  # 这里应考虑集合的元素循环的问题
            [  # steps：knowledge知识链的每一步的转换模式（可以有多个状态转换）
                [self.real_xiaoming, self.real_tui, self.real_taiqi],
                [self.real_xiaoming, self.real_tui, self.real_luoxia],
                [self.real_xiaoming, self.real_tui, self.real_dengdi],
                # status：knowledge知识链每一步中包含的每一个状态knowledge
            ],
        ]

        # 生成模式
        pattern_knowledge, meaning_knowledge = self.brain.ThinkingCentral.ModelingEngine.createExcutionInfo(
            self.real_pao,
            pattern_objs,
            meaning_objs,
        )

        # 迁移模式（小明 跑）
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 马 跑
        #############################
        pattern_objs = [self.real_ma, self.real_pao]
        # 迁移模式（马 跑）
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 牛 跑
        #############################
        pattern_objs = [self.real_niu, self.real_pao]
        # 迁移模式（牛 跑）
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

        #############################
        # 小亮 跑
        #############################
        pattern_objs = [self.real_xiaoliang, self.real_pao]
        # 迁移模式（小亮 跑）
        result = self.brain.ThinkingCentral.TransitionEngine.transitByAction(pattern_objs, pattern_knowledge,
                                                                             meaning_knowledge)

        # 输出结果
        self.brain.logThinkResult(str(pattern_objs), str(result))

    def testMeaning(self):
        print("——testMeaning——")

        # 对话演示：
        # 输入：牛有腿
        # nvwa：我不懂“牛有腿”
        # 输入：牛有腿意义牛组件为腿
        # nvwa：知道了
        # 输入：牛有腿
        # nvwa：牛组件为腿
        # 输入：牛有什么
        # nvwa：腿

        # ########################################
        # 测试单对象部分
        # ########################################
        # self.brain.PerceptionCentral.receive("牛")  # 应该什么都不知道
        # self.brain.PerceptionCentral.receive("牛")  # 这回知道牛了（字符），也知道是什么实际对象了
        #
        # self.brain.PerceptionCentral.receive("组件")  # 肯定知道组件，应该输出需要上下文

        meta = MetaData(mvalue="天数",
                        memory=self.brain.MemoryCentral).create()
        # 测试单行短语
        self.brain.PerceptionCentral.receive("1年天数365天。")  # 肯定知道组件，应该输出需要上下文
        # 测试单行单句
        self.brain.PerceptionCentral.receive("1年天数365天。")  # 肯定知道组件，应该输出需要上下文

        self.brain.PerceptionCentral.receive("小明说：“1年天数365天”。6 june有24小时,数字8.96。")  # 肯定知道组件，应该输出需要上下文

        # ########################################
        # 测试两个对象部分（简单构成）
        # ########################################
        # self.brain.PerceptionCentral.receive("牛跑")  # 跑仍然不知道
        self.brain.PerceptionCentral.receive("牛组件")  # 应该等待下文
        self.brain.PerceptionCentral.receive("马组件")  # 不知道马，还应该等待下文
        self.brain.PerceptionCentral.receive("组件腿")  # 不知道腿，应该等待上文

        # ########################################
        # 测试简单构成
        # ########################################
        self.brain.PerceptionCentral.receive("牛组件腿")  # 不知道腿，应该能够理解
        self.brain.PerceptionCentral.receive("牛组件腿")  # 再输入一次，应该能够匹配

        self.brain.PerceptionCentral.receive("马组件腿")  # 不知道马、腿，应该能够理解
        self.brain.PerceptionCentral.receive("牛组件头马父对象动物")  # 测试由理解的片段判断的全理解
        self.brain.PerceptionCentral.receive("牛组件腿属性黄色")  # 测试简单构成的冲突解决
        # ########################################
        # 测试“意义”
        # ########################################
        # 测试“意义”的自解释
        self.brain.PerceptionCentral.receive("牛组件腿意义牛组件腿")

        # 单步骤迁移
        self.brain.PerceptionCentral.receive("牛有腿")
        # 期望结果：生成"有（组件为）"的模式，问出 "牛"，"腿"是什么。
        self.brain.PerceptionCentral.receive("牛有腿意义牛组件腿")  # 上文的取得
        # self.brain.PerceptionCentral.receive("牛组件腿意义牛有腿")  # 测试下文的取得（用完后注释掉）

        self.brain.PerceptionCentral.receive("牛有尾巴")  # 测试“有”已经被生成
        self.brain.PerceptionCentral.receive("牛有角")  # 测试“有”已经被生成

        self.brain.PerceptionCentral.receive("李明是人类")  # 完全没理解
        self.brain.PerceptionCentral.receive("李明是人类意义李明父对象人类")  # 测试“是”已经被生成
        self.brain.PerceptionCentral.receive("李明是人类")  # 完全理解

        self.brain.PerceptionCentral.receive("牛是动物意义牛父对象动物")  # 测试重新生成“是”，内部判断模式、意义是否一致
        self.brain.PerceptionCentral.receive("马是动物马有腿")
        self.brain.PerceptionCentral.receive("牛是动物")
        self.brain.PerceptionCentral.receive("猫是动物")
        self.brain.PerceptionCentral.receive("苹果是水果")

        # 测试生成不一样的模式、意义
        # 例如“是”
        # 生成"有（所属物为）"的模式，问出 "马云"，"钱"是什么。
        self.brain.PerceptionCentral.receive("小丽有钱")
        self.brain.PerceptionCentral.receive("小丽有钱意义小丽所属物钱")  # 这时建立的是所属物的意义
        self.brain.PerceptionCentral.receive("小丽有钱")
        self.brain.PerceptionCentral.receive("小明有手机")

        self.brain.PerceptionCentral.receive("苹果是红色")  # 这时建立的是父对象的意义
        self.brain.PerceptionCentral.receive("苹果是红色意义苹果属性红色")
        self.brain.PerceptionCentral.receive("马是动物")  # 这时应该有两个意义
        self.brain.PerceptionCentral.receive("苹果是水果")  # 这时应该有两个意义

        # 测试简单问答
        self.brain.PerceptionCentral.receive("牛有")  # 正向查询
        self.brain.PerceptionCentral.receive("什么是")  # 反向查询

        self.brain.PerceptionCentral.receive("牛有什么")  # 正向查询
        self.brain.PerceptionCentral.receive("牛是什么")

        self.brain.PerceptionCentral.receive("什么是水果")  # 反向查询
        self.brain.PerceptionCentral.receive("香蕉是水果")  # 新增
        self.brain.PerceptionCentral.receive("什么是水果")  # 再次反向查询
        self.brain.PerceptionCentral.receive("李明是什么")
        self.brain.PerceptionCentral.receive("什么是动物")  # 反向查询

        # 测试其他线性范式（复杂动作）的生成
        self.brain.PerceptionCentral.receive("小明打小丽")
        self.brain.PerceptionCentral.receive("小明打小丽意义小明抬手小明手落小丽哭")
        self.brain.PerceptionCentral.receive("小亮打小红")

        self.brain.PerceptionCentral.receive("小明跑")
        self.brain.PerceptionCentral.receive("小明跑意义小明抬腿小明腿蹬地小明移动")
        self.brain.PerceptionCentral.receive("小亮跑")

        # 测试基于生成对象的线性范式的生成
        # “的”的模式-生成并返回新对象，意义左右有相同的部分
        self.brain.PerceptionCentral.receive("小明的手机")
        self.brain.PerceptionCentral.receive("小明的手机意义小明的手机是手机小明有小明的手机")

        self.brain.PerceptionCentral.receive("小亮的玩具")

        self.brain.PerceptionCentral.receive("四是数字")
        self.brain.PerceptionCentral.receive("数量是名词")

        self.brain.PerceptionCentral.receive("四头牛")
        self.brain.PerceptionCentral.receive("四头牛意义四头牛是集合四头牛元素是牛四头牛数量四")
        # todo 这里应区分实体的“头”（例如：牛有头）和做成动作的“头”-例如：“四头牛”

        self.brain.PerceptionCentral.receive("五头牛")

        # 测试动词交联

        # 测试动词的分组：[马,有,[是,人类]],[[马,有],是,人类]
        self.brain.PerceptionCentral.receive("马有是人类")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("马是有是人类")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("马是有是人类是对的")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("马有腿是人类")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("马有是人类苹果是水果")

        # 测试两个动词的前后关联
        self.brain.PerceptionCentral.receive("因为是单词")
        self.brain.PerceptionCentral.receive("所以是单词")

        self.brain.PerceptionCentral.receive("下雨了是单词")
        self.brain.PerceptionCentral.receive("湿了是单词")
        self.brain.PerceptionCentral.receive("因为下雨了所以地面湿了")  # 测试
        self.brain.PerceptionCentral.receive("因为下雨了所以地面湿了意义前面下雨了后面地面湿了下雨了地面就湿了")  # 测试

        self.brain.PerceptionCentral.receive("因为下雨了所以地面湿了")  # 测试
        self.brain.PerceptionCentral.receive("因为什么所以地面湿了")  # 测试

        self.brain.PerceptionCentral.receive("太阳是单词")
        self.brain.PerceptionCentral.receive("升起了是单词")
        self.brain.PerceptionCentral.receive("天是单词")
        self.brain.PerceptionCentral.receive("亮了是单词")
        self.brain.PerceptionCentral.receive("因为太阳升起了所以天亮了")  # 测试

        self.brain.PerceptionCentral.receive("因为太阳升起了所以什么")  # 测试

        # 作为集合进行思考
        self.brain.PerceptionCentral.receive("组件属性")
        self.brain.PerceptionCentral.receive("组件属性父对象")
        self.brain.PerceptionCentral.receive("组件属性父对象成分")
        self.brain.PerceptionCentral.receive("组件属性牛父对象成分")

        # 测试线性输入的集合
        self.brain.PerceptionCentral.receive("马是动物")
        self.brain.PerceptionCentral.receive("牛是动物")
        self.brain.PerceptionCentral.receive("羊是动物")
        self.brain.PerceptionCentral.receive("马牛羊")

        self.brain.PerceptionCentral.receive("跑是动作")
        self.brain.PerceptionCentral.receive("跳是动作")
        self.brain.PerceptionCentral.receive("蹲是动作")
        self.brain.PerceptionCentral.receive("跑跳蹲")

        # 测试连名词
        self.brain.PerceptionCentral.receive("四是数字")
        self.brain.PerceptionCentral.receive("五是数字")
        self.brain.PerceptionCentral.receive("六是数字")
        self.brain.PerceptionCentral.receive("四五六")

        # 连名词修限
        self.brain.PerceptionCentral.receive("中国是国家")
        self.brain.PerceptionCentral.receive("人民是名词")
        self.brain.PerceptionCentral.receive("银行是名词")
        self.brain.PerceptionCentral.receive("中国人民银行")
        self.brain.PerceptionCentral.receive("中国人民银行是银行")

        # 同一性
        # 逻辑思维的基本规律有同一律，矛盾律，排中律和充足理由律。
        self.brain.PerceptionCentral.receive("牛就是牛")
        self.brain.PerceptionCentral.receive("牛就是牛意义牛同一于牛")
        self.brain.PerceptionCentral.receive("四就是4意义四同一于4")
        self.brain.PerceptionCentral.receive("苹果就是apple")

        self.brain.PerceptionCentral.receive("牛不是马意义牛不同一于马")



    def testLinearPattern(self):
        print("——testLinearPattern——")
        # 目前发现的线性pattern包括：
        # 1、修限型
        # （1）R1-...Rn，例如：中国人民银行
        # （2）A1A2，例如：跑了
        # （3）A1A2R1，例如：跑是动作，跑了一圈
        # （4）R1A1A2，例如：动作包含跑
        # 2、集合型（一般为同一父对象）
        # （1）R1-...Rn，例如：四五六七
        # （2）A1A2...An，例如：跑跳蹲
        from loongtian.nvwa.runtime.pattern import LinearPattern
        self.brain.PerceptionCentral.receive("牛是动物意义牛父对象动物")  # 测试重新生成“是”，内部判断模式、意义是否一致
        self.brain.PerceptionCentral.receive("四是数字")
        self.brain.PerceptionCentral.receive("五是数字")
        self.brain.PerceptionCentral.receive("六是数字")

        # 生不成实际对象类型模式
        self.brain.ThinkingCentral.PatternEngine.extractObjTypePattern(["四五六"])
        self.brain.PerceptionCentral.receive("一是数字")
        self.brain.PerceptionCentral.receive("二是数字")
        self.brain.PerceptionCentral.receive("三是数字")

        # 生成实际对象类型模式
        self.brain.ThinkingCentral.PatternEngine.extractObjTypePattern(["四五六","一二三","四五六"])

        # 生成实际对象父对象模式
        self.brain.ThinkingCentral.PatternEngine.extractParentPattern("四五六")

        # 生成对应的操作方法模式
        self.brain.ThinkingCentral.PatternEngine.extractParentPattern("四五六意义四五六是集合四五六有四四五六有五四五六有六四五六元素是数字四五六数量三")

    def testCollectionMeaning(self):
        print("——testCollectionMeaning——")

        # 清空内存
        self.brain.MemoryCentral.flush()

        self.brain.PerceptionCentral.receive("四是数字意义为四父对象数字")

        self.brain.PerceptionCentral.receive("四是数字")
        self.brain.PerceptionCentral.receive("五是数字")
        self.brain.PerceptionCentral.receive("六是数字")
        self.brain.PerceptionCentral.receive("集合1是集合")
        self.brain.PerceptionCentral.receive("四属于四五六意义四五六组件四")

    def testLogicalMeaning(self):
        print("——testLogicalMeaning——")

        # 清空内存
        self.brain.MemoryCentral.flush()

        self.brain.PerceptionCentral.receive("苹果是水果")
        self.brain.PerceptionCentral.receive("苹果不是动物")
        self.brain.PerceptionCentral.receive("苹果不是动物意义非苹果父对象动物")

    def testContextMeaning(self):
        print("——testContextMeaning——")

        # 清空内存
        self.brain.MemoryCentral.flush()

        # 三位一体：存储的，问的，应该回答的

        self.brain.PerceptionCentral.receive("牛有腿意义牛组件腿")  # 生成有
        self.brain.PerceptionCentral.receive("牛有腿")
        self.brain.PerceptionCentral.receive("牛有角")
        self.brain.PerceptionCentral.receive("牛有尾巴")
        # 上下文输入生成范式
        self.brain.PerceptionCentral.receive("&:牛有腿吗@:有")
        self.brain.PerceptionCentral.receive("&:牛有角吗@:有")
        self.brain.PerceptionCentral.receive("牛有尾巴吗")  # 回答：有

        self.brain.PerceptionCentral.receive("&:牛有手吗@:没有")
        self.brain.PerceptionCentral.receive("&:牛有爪子吗@:没有")
        self.brain.PerceptionCentral.receive("牛有翅膀吗")  # 回答：没有

        self.brain.PerceptionCentral.receive("牛是动物意义牛父对象动物")
        self.brain.PerceptionCentral.receive("一是数字")
        self.brain.PerceptionCentral.receive("二是数字")
        self.brain.PerceptionCentral.receive("三是数字")
        self.brain.PerceptionCentral.receive("四是数字")
        self.brain.PerceptionCentral.receive("一二三四是集合")
        self.brain.PerceptionCentral.receive("&:一下一个什么@:二")
        self.brain.PerceptionCentral.receive("&:二下一个什么@:三")
        self.brain.PerceptionCentral.receive("三下一个什么")  # 回答：四
        self.brain.PerceptionCentral.receive("&:二上一个什么@:一")
        self.brain.PerceptionCentral.receive("&:三上一个什么@:二")
        self.brain.PerceptionCentral.receive("四上一个什么")  # 回答：三

        self.brain.PerceptionCentral.receive("马有烙上的印记，牛没有")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("跑是动词")  # 测试两个看似动作但实际一个动作，互相打架

        self.brain.PerceptionCentral.receive("牛有长毛的腿意义牛组件腿腿长毛")

        # 测试标点符号的分组
        # 期望结果：生成"有（所属物为）"的模式，问出 "马云"，"钱"是什么。
        self.brain.PerceptionCentral.receive("马云有钱意义马云所属物很多钱")
        # 多步骤迁移
        self.brain.PerceptionCentral.receive("小明打小丽意义小明抬手，小明手落到小丽身上，然后小明手疼，小丽哭。")
