#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from loongtian.nvwa.engines.groupEngine import GroupEngine

from loongtian.nvwa.models.enum import ObjType
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.models.realObject import RealObject

class TestGroupEngine(TestCase):
    def setUp(self):
        print ("----setUp----")
        self.groupEngine=GroupEngine(None)
        # self.data = [
        #     {"mvalue":"小明", "relatedRealObjs":[ # self.meta01
        #         {"remark":"<名称代词>小明"}
        #     ]},
        #     {"mvalue":"打", "frequency":80, "relatedRealObjs":[ # self.meta02
        #         {"pattern":"{0}打{1}", "meaning":"{0}手拿{A};{A}快速接触{1};{1}痛",
        #             "weight":0.2, "remark":"<动作>打"},
        #         {"weight":0.8, "remark":"<名词>打"}
        #     ]},
        #     {"mvalue":"小丽", "relatedRealObjs":[ # self.meta03
        #         {"remark":"<名称代词>小丽"}
        #     ]},
        #     {"mvalue":"的", "frequency":100, "relatedRealObjs":[ # self.meta04
        #         {"pattern":"{0}的{1}", "meaning":"{1}归属{0};",
        #             "weight":0.2, "remark":"<归属>的"},
        #         {"pattern":"{0}的{1}", "meaning":"{1}被修限{0};",
        #             "weight":0.3, "remark":"<修限>的"},
        #         {"weight":0.5, "remark":"<名词>的"}
        #     ]},
        #     {"mvalue":"弟弟", "relatedRealObjs":[ # self.meta05
        #         {"remark":"<关系名词>弟弟"}
        #     ]},
        #     {"mvalue":"买", "relatedRealObjs":[ # self.meta06
        #         {"pattern":"{0}买{1}", "meaning":"{1}归属{A};{1}归属{0};",
        #             "weight":0.2, "remark":"<归属>买"},
        #         {"weight":0.5, "remark":"<名词>买"}
        #     ]},
        #     {"mvalue":"新", "frequency":30, "relatedRealObjs":[ # self.meta07
        #         {"pattern":"{?}:新{0}", "meaning":"{?}父对象{0};{0}状态新;return {?};",
        #             "weight":0.2, "remark":"<状态>新"},
        #         {"weight":0.5, "remark":"<名词>新"}
        #     ]},
        #     {"mvalue":"衣服", "relatedRealObjs":[ # self.meta08
        #         {"remark":"<名词>衣服"}
        #     ]},
        #     {"mvalue":"中国", "relatedRealObjs":[ # self.meta09
        #         {"remark":"<国名>中国"}
        #     ]},
        #     {"mvalue":"人", "relatedRealObjs":[ # self.meta10
        #         {"remark":"<名词>人"}
        #     ]},
        #     {"mvalue":"跑", "frequency":50, "relatedRealObjs":[ # self.meta11
        #         {"pattern":"{0}跑", "meaning":"{0}位置状态改变",
        #             "weight":0.2, "remark":"<位置状态>跑"},
        #         {"weight":0.5, "remark":"<名词>跑"}
        #     ]},
        #     {"mvalue":"了", "frequency":500, "relatedRealObjs":[ # self.meta12
        #         {"pattern":"{0}了", "meaning":"return {0};",
        #             "weight":0.2, "remark":"<助词>了"}
        #     ]},
        #     {"mvalue":"日本", "relatedRealObjs":[ # self.meta13
        #         {"remark":"<国名>日本"}
        #     ]},
        #     {"mvalue":"人民", "relatedRealObjs":[ # self.meta14
        #         {"remark":"<名词>人民"}
        #     ]},
        #     {"mvalue":"银行", "relatedRealObjs":[ # self.meta15
        #         {"remark":"<名词>银行"}
        #     ]},
        #     {"mvalue":"到", "frequency":60, "relatedRealObjs":[ # self.meta16
        #         {"pattern":"{0}到{1}", "meaning":"{0}位置状态改变为{1}",
        #             "weight":0.2, "remark":"<位置状态>到"},
        #         {"weight":0.5, "remark":"<名词>到"}
        #     ]},
        #     {"mvalue":"取", "frequency":40, "relatedRealObjs":[ # self.meta17
        #         {"pattern":"{0}取{1}", "meaning":"{0}拿走{1}",
        #             "weight":0.2, "remark":"<动作>取"},
        #         {"weight":0.5, "remark":"<名词>取"}
        #     ]},
        #     {"mvalue":"钱", "relatedRealObjs":[ # self.meta18
        #         {"remark":"<名词>钱"}
        #     ]}
        # ]
        # i = 0
        # for meta in self.data:
        #     i += 1
        #     exec("self.meta%02d = MetaData(mvalue = '%s')" % (i, meta["mvalue"]))
        #     if meta.has_key("frequency"):
        #         exec("self.meta%02d.frequency = %d" % (i, meta["frequency"]))
        #     exec("self.meta%02d.create()" % i)
        #     j = 0
        #     for real in meta["relatedRealObjs"]:
        #         j += 1
        #         exec("r%02d%d = RealObject(remark='%s')" % (i, j, real["remark"]))
        #         if real.has_key("pattern"):
        #             exec("r%02d%d.pattern = '%s'" % (i, j, real["pattern"]))
        #         if real.has_key("meaning"):
        #             exec("r%02d%d.meaning = '%s'" % (i, j, real["meaning"]))
        #         if real.has_key("weight"):
        #             exec("r%02d%d.weight = %f" % (i, j, real["weight"]))
        #         exec("r%02d%d.create()" % (i, j))
        #         exec("self.meta%02d.addRelatedRealObject(r%02d%d)" % (i, i, j))
    #
    # def testGroupByMeta(self):
    #     print("----testGroupByMeta----")
    #     group1 = GroupEngine.groupByMeta(
    #         [self.meta09, self.meta14, self.meta15]
    #     )
    #     print("[中国, 人民, 银行]:<%s>" % group1)
    #     group2 = GroupEngine.groupByMeta(
    #         [self.meta01, self.meta16, self.meta09, self.meta14, self.meta15, self.meta17, self.meta18, self.meta06, self.meta07, self.meta08]
    #     )
    #     print("[小明, 到, 中国, 人民, 银行, 取, 钱, 买, 新, 衣服]:<%s>" % group2)
    #     group3 = GroupEngine.groupByMeta(
    #         [self.meta01, self.meta02, self.meta03, self.meta04, self.meta05]
    #     )
    #     print("[小明, 打, 小丽, 的, 弟弟]:<%s>" % group3)
    #     group4 = GroupEngine.groupByMeta(
    #         [self.meta09, self.meta10, self.meta02, self.meta11, self.meta12, self.meta13, self.meta10]
    #     )
    #     print("[中国, 人, 打, 跑, 了, 日本, 人]:<%s>" % group4)


    def tearDown(self):
        print("----tearDown----")
