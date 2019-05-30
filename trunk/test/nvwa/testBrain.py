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
        print ("----setUp----")
        from loongtian.nvwa.organs.centralManager import CentralManager
        CentralManager._cleanDB(wait_for_command=True)
        self.brain = Brain()
        # self.brain._cleanDB()
        self.brain.init()
        run(self.brain)

    def testCreatePattern(self):
        print("——testCreatePattern——")

        #############################
        # 牛有腿
        #############################
        self.meta_niu = MetaData(mvalue=u"牛",memory=self.brain.MemoryCentral).create()
        self.meta_you = MetaData(mvalue=u"有",memory=self.brain.MemoryCentral).create()
        self.meta_tui = MetaData(mvalue=u"腿",memory=self.brain.MemoryCentral).create()
        self.real_niu = RealObject.createRealByMeta(self.meta_niu, realType=ObjType.VIRTUAL)
        self.real_you = RealObject.createRealByMeta(self.meta_you, realType=ObjType.ACTION)
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
        self.meta_ma = MetaData(mvalue=u"马",memory=self.brain.MemoryCentral).create()
        self.real_ma = RealObject.createRealByMeta(self.meta_ma, realType=ObjType.VIRTUAL)
        self.meta_weiba = MetaData(mvalue=u"尾巴",memory=self.brain.MemoryCentral).create()
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
        self.meta_xiaoming = MetaData(mvalue=u"小明",memory=self.brain.MemoryCentral).create()
        self.meta_da = MetaData(mvalue=u"打",memory=self.brain.MemoryCentral).create()
        self.meta_xiaoli = MetaData(mvalue=u"小丽",memory=self.brain.MemoryCentral).create()

        self.meta_shouluo = MetaData(mvalue=u"手落",memory=self.brain.MemoryCentral).create()
        self.meta_taishou = MetaData(mvalue=u"抬手",memory=self.brain.MemoryCentral).create()

        self.meta_shouteng = MetaData(mvalue=u"手疼",memory=self.brain.MemoryCentral).create()
        self.meta_ku = MetaData(mvalue=u"哭",memory=self.brain.MemoryCentral).create()

        self.meta_xiaoliang = MetaData(mvalue=u"小亮",memory=self.brain.MemoryCentral).create()
        self.meta_xiaohong = MetaData(mvalue=u"小红",memory=self.brain.MemoryCentral).create()

        self.real_xiaoming = RealObject.createRealByMeta(self.meta_xiaoming, realType=ObjType.VIRTUAL)
        self.real_da = RealObject.createRealByMeta(self.meta_da, realType=ObjType.ACTION)
        self.real_xiaoli = RealObject.createRealByMeta(self.meta_xiaoli, realType=ObjType.VIRTUAL)
        self.real_shouteng = RealObject.createRealByMeta(self.meta_shouteng, realType=ObjType.VIRTUAL)

        self.real_taishou = RealObject.createRealByMeta(self.meta_taishou, realType=ObjType.VIRTUAL)
        self.real_shouluo = RealObject.createRealByMeta(self.meta_shouluo, realType=ObjType.VIRTUAL)

        self.real_ku = RealObject.createRealByMeta(self.meta_ku, realType=ObjType.VIRTUAL)
        self.real_xiaoliang = RealObject.createRealByMeta(self.meta_xiaoliang, realType=ObjType.VIRTUAL)
        self.real_xiaohong = RealObject.createRealByMeta(self.meta_xiaohong, realType=ObjType.VIRTUAL)

        self.meta_pao = MetaData(mvalue=u"跑",memory=self.brain.MemoryCentral).create()
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

        self.meta_taiqi = MetaData(mvalue=u"抬起",memory=self.brain.MemoryCentral).create()
        self.real_taiqi = RealObject.createRealByMeta(self.meta_taiqi, realType=ObjType.VIRTUAL)

        self.meta_luoxia = MetaData(mvalue=u"落下",memory=self.brain.MemoryCentral).create()
        self.real_luoxia = RealObject.createRealByMeta(self.meta_luoxia, realType=ObjType.VIRTUAL)

        self.meta_dengdi = MetaData(mvalue=u"蹬地",memory=self.brain.MemoryCentral).create()
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
        # 输入：牛有腿？
        # nvwa：对

        # ########################################
        # 测试单对象部分
        # ########################################
        self.brain.PerceptionCentral.receive("牛")  # 应该什么都不知道
        self.brain.PerceptionCentral.receive("牛")  # 这回知道牛了（字符），也知道是什么实际对象了

        self.brain.PerceptionCentral.receive("组件")  # 肯定知道组件，应该输出需要上下文

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
        self.brain.PerceptionCentral.receive("猫是动物")
        self.brain.PerceptionCentral.receive("苹果是水果")

        self.brain.PerceptionCentral.receive("牛有什么") # 正向查询
        self.brain.PerceptionCentral.receive("牛是什么")

        self.brain.PerceptionCentral.receive("什么是水果") # 反向查询
        self.brain.PerceptionCentral.receive("香蕉是水果") # 新增
        self.brain.PerceptionCentral.receive("什么是水果") # 再次反向查询
        self.brain.PerceptionCentral.receive("李明是什么")

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

        # 测试其他线性范式的生成
        self.brain.PerceptionCentral.receive("小明打小丽")
        self.brain.PerceptionCentral.receive("小明打小丽意义小明抬手小明手落小丽哭")
        self.brain.PerceptionCentral.receive("小亮打小红")

        self.brain.PerceptionCentral.receive("小明跑")
        self.brain.PerceptionCentral.receive("小明跑意义小明抬腿小明腿蹬地小明移动")
        self.brain.PerceptionCentral.receive("小亮跑")


        # 测试非线性范式的生成
        # “的”的模式-生成并返回新对象，意义左右有相同的部分
        self.brain.PerceptionCentral.receive("小明的手机")
        self.brain.PerceptionCentral.receive("小明的手机意义小明的手机是手机小明有小明的手机")

        self.brain.PerceptionCentral.receive("小亮的玩具")

        self.brain.PerceptionCentral.receive("四是数字")
        self.brain.PerceptionCentral.receive("数量是名词")

        self.brain.PerceptionCentral.receive("四头牛")
        self.brain.PerceptionCentral.receive("四头牛意义四头牛是集合四头牛元素是牛四头牛数量四")

        self.brain.PerceptionCentral.receive("五头牛")

        self.brain.PerceptionCentral.receive("中华人民共和国")
        self.brain.PerceptionCentral.receive("中华人民共和国意义中华人民共和国是共和国中华人民共和国名称中华人民共和国")

        # 测试动词交联
        self.brain.PerceptionCentral.receive("组件属性")
        self.brain.PerceptionCentral.receive("组件属性父对象")
        self.brain.PerceptionCentral.receive("组件属性父对象成分")
        self.brain.PerceptionCentral.receive("组件属性牛父对象成分")

        # 测试动词的分组：[马,有,[是,人类]],[[马,有],是,人类]
        self.brain.PerceptionCentral.receive("马有是人类")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("马有是人类苹果是水果")
        self.brain.PerceptionCentral.receive("马是有是人类")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("马是有是人类是对的")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("马有腿是人类")  # 测试两个看似动作但实际一个动作，互相打架

        # 测试线性输入的集合
        self.brain.PerceptionCentral.receive("马是动物")
        self.brain.PerceptionCentral.receive("牛是动物")
        self.brain.PerceptionCentral.receive("羊是动物")
        self.brain.PerceptionCentral.receive("马牛羊")

        self.brain.PerceptionCentral.receive("跑是动作")
        self.brain.PerceptionCentral.receive("跳是动作")
        self.brain.PerceptionCentral.receive("蹲是动作")
        self.brain.PerceptionCentral.receive("跑跳蹲")

        # 测试简单问答
        self.brain.PerceptionCentral.receive("牛有腿")
        self.brain.PerceptionCentral.receive("牛有角")
        self.brain.PerceptionCentral.receive("牛有尾巴")
        self.brain.PerceptionCentral.receive("牛有什么")

        self.brain.PerceptionCentral.receive("马是动物")
        self.brain.PerceptionCentral.receive("马是什么")
        self.brain.PerceptionCentral.receive("牛是动物")
        self.brain.PerceptionCentral.receive("什么是动物")


        # 测试两个动词的前后关联
        self.brain.PerceptionCentral.receive("因为下雨了所以地面湿了")  # 测试
        self.brain.PerceptionCentral.receive("因为下雨了所以地面湿了意义前面下雨了后面地面湿了下雨了地面就湿了")  # 测试

        self.brain.PerceptionCentral.receive("马有烙上的印记，牛没有")  # 测试两个看似动作但实际一个动作，互相打架
        self.brain.PerceptionCentral.receive("跑是动词")  # 测试两个看似动作但实际一个动作，互相打架

        self.brain.PerceptionCentral.receive("牛有长毛的腿意义牛组件腿腿长毛")

        # 测试标点符号的分组
        # 期望结果：生成"有（所属物为）"的模式，问出 "马云"，"钱"是什么。
        self.brain.PerceptionCentral.receive("马云有钱意义马云所属物很多钱")
        # 多步骤迁移
        self.brain.PerceptionCentral.receive("小明打小丽意义小明抬手，小明手落到小丽身上，然后小明手疼，小丽哭。")
