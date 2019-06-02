#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from loongtian.nvwa.models.enum import ObjType
# from loongtian.nvwa.models.instinct import Instinct
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.models.knowledge import Knowledge
from loongtian.nvwa.models.realObject import RealObject
from loongtian.nvwa.models.metaData import MetaData
from loongtian.nvwa.tools.db import DbPools


class TestKnowledgeChain(TestCase):
    def setUp(self):
        print("----setUp----")
        self.data = [
            {"mvalue":"小明", "relatedRealObjs":[ # self.meta01
                {"remark":"<名称代词>小明"} # self.r011
            ]},
            {"mvalue":"给", "frequency":80, "relatedRealObjs":[ # self.meta02
                {"pattern":"{0}给{1}{2}", "meaning":"{0}失去{2};{1}得到{2};", "type":ObjType.ACTION,
                    "weight":0.2, "remark":"<动作>给"}, # self.r021
                {"weight":0.8, "remark":"<名词>给"} # self.r022
            ]},
            {"mvalue":"小丽", "relatedRealObjs":[ # self.meta03
                {"remark":"<名称代词>小丽"}  # self.r031
            ]},
            {"mvalue":"一", "relatedRealObjs":[ # self.meta04
                {"remark":"<数词>一"} # self.r041
            ]},
            {"mvalue":"朵", "relatedRealObjs":[ # self.meta05
                {"remark":"<量词>朵"}] # self.r051
            },
            {"mvalue":"红色", "relatedRealObjs":[ # self.meta06
                {"remark":"<名词>红色"} # self.r061
            ]},
            {"mvalue":"的", "frequency":100, "relatedRealObjs":[ # self.meta07
                {"pattern":"{0}的{1}", "meaning":"{1}归属{0};", "type":ObjType.ACTION,
                    "weight":0.2, "remark":"<归属>的"}, # self.r071
                {"pattern":"{0}的{1}", "meaning":"{1}被修限{0};", "type":ObjType.ACTION,
                    "weight":0.3, "remark":"<修限>的"}, # self.r072
                {"weight":0.5, "remark":"<名词>的"} # self.r073
            ]},
            {"mvalue":"玫瑰", "relatedRealObjs":[ # self.meta08
                {"remark":"<名词>玫瑰"} # self.r081
            ]},
            {"mvalue":"花", "relatedRealObjs":[ # self.meta09
                {"remark":"<名词>花"} # self.r091
            ]},
            {"mvalue":"情人节", "relatedRealObjs":[ # self.meta10
                {"remark":"<名词>情人节"} # self.r101
            ]},
            {"mvalue":"块", "relatedRealObjs":[ # self.meta11
                {"remark":"<量词>块"} # self.r111
            ]},
            {"mvalue":"巧克力", "relatedRealObjs":[ # self.meta12
                {"remark":"<名词>巧克力"} # self.r121
            ]},
            {"mvalue":"生日", "relatedRealObjs":[ # self.meta13
                {"remark":"<名词>生日"} # self.r131
            ]},
            {"mvalue":"小刚", "relatedRealObjs":[ # self.meta14
                {"remark":"<名称代词>小刚"} # self.r141
            ]},
            {"mvalue":"蓝色", "relatedRealObjs":[ # self.meta15
                {"remark":"<名词>蓝色"} # self.r151
            ]},
            {"mvalue":"中国", "relatedRealObjs":[ # self.meta16
                {"remark":"<名词>中国"} # self.r161
            ]},
            {"mvalue":"人民", "relatedRealObjs":[ # self.meta17
                {"remark":"<名词>人民"} # self.r171
            ]},
            {"mvalue":"建设", "relatedRealObjs":[ # self.meta18
                {"remark":"<名词>建设"} # self.r181
            ]},
            {"mvalue":"银行", "relatedRealObjs":[ # self.meta19
                {"remark":"<名词>银行"} # self.r191
            ]},
            {"mvalue":"甲", "relatedRealObjs":[ # self.meta20
                {"remark":"<名词>甲"} # self.r201
            ]},
            {"mvalue":"乙", "relatedRealObjs":[ # self.meta21
                {"remark":"<名词>乙"} # self.r211
            ]}
        ]
        i = 0
        for meta in self.data:
            i += 1
            exec("self.meta%02d = MetaData(mvalue = '%s')" % (i, meta["mvalue"]))
            if "frequency" in meta:
                exec("self.meta%02d.frequency = %d" % (i, meta["frequency"]))
            exec("self.meta%02d = self.meta%02d.create()" % (i, i))
            j = 0
            for real in meta["relatedRealObjs"]:
                j += 1
                exec("self.r%02d%d = RealObject(remark='%s')" % (i, j, real["remark"]))
                if "pattern" in real:
                    exec("self.r%02d%d.pattern = '%s'" % (i, j, real["pattern"]))
                if "meaning" in real:
                    exec("self.r%02d%d.meaning = '%s'" % (i, j, real["meaning"]))
                if "weight" in real:
                    exec("self.r%02d%d.weight = %f" % (i, j, real["weight"]))
                if "type" in real:
                    exec("self.r%02d%d.type = %d" % (i, j, real["type"]))
                exec("self.r%02d%d = self.r%02d%d.create()" % (i, j, i, j))
                exec("self.meta%02d.addRelatedRealObject(self.r%02d%d)" % (i, i, j))
                exec("self.meta%02d.addRelationWithRealObjInDB(self.r%02d%d)" % (i, i, j))

        self.domain1 = Knowledge(self.r101).saveChain()
        print("Domain1<%s> = [情人节]" % self.domain1.id)
        self.domain2 = Knowledge([self.r031, self.r071, self.r131]).saveChain()
        print("Domain2<%s> = [小丽, 的, 生日]" % self.domain2.id)
        self.chain1 = Knowledge(
            [self.r011, self.r021, self.r031,[[self.r041, self.r051], [self.r061, self.r072,[self.r081, self.r091]]]]
        ).saveChain()
        print("Chain1<%s> = [小明, 给, 小丽, [[一, 朵], [红色, 的, [玫瑰, 花]]]]" % self.chain1.id)
        self.chain2 = Knowledge(
            [self.r011, self.r021, self.r031,[[self.r041, self.r111], self.r121]]
        ).saveChain()
        print("Chain2<%s> = [小明, 给, 小丽, [[一, 块], 巧克力]]" % self.chain2.id)
        self.chain3 = Knowledge(
            [self.r011, self.r021, self.r141,[[self.r041, self.r111], self.r121]]
        ).saveChain()
        print("Chain3<%s> = [小明, 给, 小刚, [[一, 块], 巧克力]]" % self.chain3.id)

        self.chain4 = Knowledge(
            [self.r161, [self.r171, [self.r181, self.r191]]]
        ).saveChain()
        print("Chain4<%s> = [中国, [人民，[建设, 银行]]]" % self.chain4.id)

        # Instinct.getAllByInDB(alias= "parent")
        # Instinct.getAllByInDB(alias= "coll")
        self.chain5 = Knowledge(
            [[self.r201, self.r211], self.i221, self.i231]
        ).saveChain()
        print("Chain5<%s> = [['甲', '乙'], '父对象', '集合']" % self.chain5.id)

    def testSaveChain(self):
        print("----testSaveChain----")
        self.assertTrue(isinstance(self.chain1, Knowledge))
        self.assertTrue(isinstance(self.chain2, Knowledge))
        self.assertTrue(isinstance(self.domain1, RealObject))
        self.assertTrue(isinstance(self.domain2, Knowledge))
        self.chain1.addDomain(self.domain1)
        self.chain1.addDomain(self.domain2)
        self.chain1.getAllBackwardsInDB()
        print("{t_graph:%s, domain:%s}" % (self.chain1.id, self.chain1.domains))
        self.chain1.removeDomain(self.domain1)
        self.chain1.removeDomain(self.domain2)
        DbPools["nvwa"].executeSQL("delete from Domain where status = 0")
        self.domain1.addDomainedChain(self.chain1)
        self.domain1.addDomainedChain(self.chain2)
        self.domain1.refreshChains()
        self.assertTrue(len(self.domain1.chains) > 0)
        for id,temp in self.domain1.chains.items():
            print("{doamin:%s, t_graph:%s}" % (self.domain1.id, temp.chain))

    def testFindChain(self):
        print("----testFindChain----")
        find1 = Knowledge(self.r101).findChain()
        print("<%s>:[情人节]" % find1)
        self.assertIsNone(find1)
        find2 = Knowledge([self.r061, self.r072,[self.r081, self.r091]]).findChain()
        print("<%s>:[红色, 的, [玫瑰, 花]]" % find2.id)
        self.assertIsNotNone(find2)
        find3 = Knowledge([[self.r041, self.r051], [self.r081, self.r091]]).findChain()
        print("<%s>:[[一, 朵], [玫瑰, 花]]" % find3)
        self.assertIsNone(find3)

    def testFindHead(self):
        print("----testFindHead----")
        head1 = [self.r011, self.r021, self.r031]
        find1 = Knowledge.findHead(head1)
        Knowledge.forwardToRealObjects(find1)
        self.assertEqual(2, len(find1))
        print("find:[小明, 给, 小丽] ==> %s" % find1)
        head2 = [self.r011, self.r021]
        find2 = Knowledge.findHead(head2)
        Knowledge.forwardToRealObjects(find2)
        self.assertEqual(3, len(find2))
        print("find:[小明, 给] ==> %s" % find2)
        head3 = [self.r031, self.r021]
        find3 = Knowledge.findHead(head3)
        Knowledge.forwardToRealObjects(find3)
        self.assertEqual(0, len(find3))
        print("find:[小丽, 给] ==> %s" % find3)
        head4 = [self.r061]
        find4 = Knowledge.findHead(head4)
        Knowledge.forwardToRealObjects(find4)
        self.assertEqual(1, len(find4))
        print("find:[红色] ==> %s" % find4)

        head5 = [self.r161]
        find5 = Knowledge.findHead(head5)
        Knowledge.forwardToRealObjects(find5)
        self.assertEqual(1, len(find5))
        print("find:[中国] ==> %s" % find5)

        head6 = [self.r161, self.r171]
        find6 = Knowledge.findHead(head6)
        Knowledge.forwardToRealObjects(find6)
        self.assertEqual(1, len(find6))
        print("find:[中国, 人民] ==> %s" % find6)

        head7 = [self.r161, self.r171, self.r181]
        find7 = Knowledge.findHead(head7)
        Knowledge.forwardToRealObjects(find7)
        self.assertEqual(1, len(find7))
        print("find:[中国, 人民，建设] ==> %s" % find7)

        head8 = [self.r171]
        find8 = Knowledge.findHead(head8)
        Knowledge.forwardToRealObjects(find8)
        self.assertEqual(1, len(find8))
        print("find:[人民] ==> %s" % find8)

        head9 = [self.r171, self.r181]
        find9 = Knowledge.findHead(head9)
        Knowledge.forwardToRealObjects(find9)
        self.assertEqual(1, len(find9))
        print("find:[人民， 建设] ==> %s" % find9)

        head10 = [self.r181]
        find10 = Knowledge.findHead(head10)
        Knowledge.forwardToRealObjects(find10)
        self.assertEqual(1, len(find10))
        print("find:[建设] ==> %s" % find10)


    def testFindTail(self):
        print("----testFindTail----")
        self.chainTail = Knowledge(
            [[self.r041, self.r051], [self.r151, self.r072, self.r091]]
        ).saveChain()
        print("ChainTail<%s> = [[一, 朵], [蓝色, 的, 花]]" % self.chainTail.id)
        tail1 = [self.r091]
        find1 = Knowledge.findTail(tail1)
        Knowledge.forwardToRealObjects(find1)
        self.assertEqual(6, len(find1))
        print("find:[花] ==> %s" % find1)
        tail2 = [self.r031]
        find2 = Knowledge.findTail(tail2)
        Knowledge.forwardToRealObjects(find2)
        self.assertEqual(0, len(find2))
        print("find:[小丽] ==> %s" % find2)

        tail3 = [self.r191]
        find3 = Knowledge.findTail(tail3)
        Knowledge.forwardToRealObjects(find3)
        self.assertEqual(3, len(find3))
        print("find:[银行] ==> %s" % find3)

        tail4 = [self.r181, self.r191]
        find4 = Knowledge.findTail(tail4)
        Knowledge.forwardToRealObjects(find4)
        self.assertEqual(3, len(find4))
        print("find:[建设, 银行] ==> %s" % find4)

        tail5 = [self.r171, self.r181, self.r191]
        find5 = Knowledge.findTail(tail5)
        Knowledge.forwardToRealObjects(find5)
        self.assertEqual(2, len(find5))
        print("find:[人民，建设, 银行] ==> %s" % find5)

        tail6 = [self.r161, self.r171, self.r181, self.r191]
        find6 = Knowledge.findTail(tail6)
        Knowledge.forwardToRealObjects(find6)
        self.assertEqual(1, len(find6))
        print("find:[中国，人民，建设, 银行] ==> %s" % find6)


    def testFindHeadAndTail(self):
        print("----testFindHeadAndTail----")
        self.chainHeadTail1 = Knowledge(
            [self.r011, self.r021, self.r031, self.r091]
        ).saveChain()
        print("ChainHeadTail1<%s> = [小明, 给, 小丽, 花]" % self.chainHeadTail1.id)
        self.chainHeadTail2 = Knowledge(
            [self.r011, self.r021, self.r031, [self.r151, self.r072, self.r091]]
        ).saveChain()
        print("ChainHeadTail2<%s> = [小明, 给, 小丽, [蓝色, 的, 花]]" % self.chainHeadTail2.id)
        head1 = [self.r011, self.r021, self.r031]
        tail1 = [self.r091]
        find1 = Knowledge.findHeadAndTail(head1, tail1)
        Knowledge.forwardToRealObjects(find1)
        self.assertEqual(3, len(find1))
        print("find:{head:[小明, 给, 小丽], tail:[花]} ==> %s" % find1)
        head2 = [self.r021, self.r031]
        tail2 = [self.r091]
        find2 = Knowledge.findHeadAndTail(head2, tail2)
        Knowledge.forwardToRealObjects(find2)
        self.assertEqual(0, len(find2))
        print("find:{head:[给, 小丽], tail:[花]} ==> %s" % find2)

        head3 = [self.r161]
        tail3 = [self.r191]
        find3 = Knowledge.findHeadAndTail(head3, tail3)
        Knowledge.forwardToRealObjects(find3)
        self.assertEqual(1, len(find3))
        print("find:{head:[中国], tail:[银行]} ==> %s" % find3)

        head4 = [self.r161, self.r171]
        tail4 = [self.r191]
        find4 = Knowledge.findHeadAndTail(head4, tail4)
        Knowledge.forwardToRealObjects(find4)
        self.assertEqual(1, len(find4))
        print("find:{head:[中国, 人民], tail:[银行]} ==> %s" % find4)

        head5 = [self.r161, self.r171, self.r181]
        tail5 = [self.r191]
        find5 = Knowledge.findHeadAndTail(head5, tail5)
        Knowledge.forwardToRealObjects(find5)
        self.assertEqual(1, len(find5))
        print("find:{head:[中国, 人民, 建设], tail:[银行]} ==> %s" % find5)

        head6 = [self.r171,self.r181]
        tail6 = [self.r191]
        find6 = Knowledge.findHeadAndTail(head6, tail6)
        Knowledge.forwardToRealObjects(find6)
        self.assertEqual(1, len(find6))
        print("find:{head:[人民, 建设], tail:[银行]} ==> %s" % find6)

        head7 = [self.r171]
        tail7 = [self.r181, self.r191]
        find7 = Knowledge.findHeadAndTail(head7, tail7)
        Knowledge.forwardToRealObjects(find7)
        self.assertEqual(1, len(find7))
        print("find:{head:[人民], tail:[建设, 银行]} ==> %s" % find7)

        head8 = [self.r171]
        tail8 = [self.r191]
        find8 = Knowledge.findHeadAndTail(head8, tail8)
        Knowledge.forwardToRealObjects(find8)
        self.assertEqual(1, len(find8))
        print("find:{head:[人民], tail:[银行]} ==> %s" % find8)


    def tearDown(self):
        print("----tearDown----")
