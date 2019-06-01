#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from loongtian.nvwa.bof.collection import Collection, CollectionModeEnum
from loongtian.nvwa.models.enum import ObjType



class TestCollection(TestCase):
    def setUp(self):
        print ("----setUp----")
        type = ObjType.ACTION | ObjType.COLLECTION
        self.data = [
            {"mvalue":"甲", "relatedRealObjs":[ # self.meta01
                {"remark":"<名词>甲", 'type': type} # self.r011
            ]},
            {"mvalue":"乙", "relatedRealObjs":[ # self.meta02
                {"remark":"<名词>乙", 'type': type} # self.r021
            ]},
            {"mvalue":"丙", "relatedRealObjs":[ # self.meta03
                {"remark":"<名词>丙", 'type': type} # self.r031
            ]},
            {"mvalue":"丁", "relatedRealObjs":[ # self.meta04
                {"remark":"<名词>丁", 'type': type} # self.r041
            ]},
            {"mvalue":"如果", "relatedRealObjs":[ # self.meta05
                {"remark":"<名词>如果", 'type': type} # self.r051
            ]},
            {"mvalue":"那么", "relatedRealObjs":[ # self.meta06
                {"remark":"<名词>那么", 'type': type} # self.r061
            ]},
            {"mvalue":"首先", "relatedRealObjs":[ # self.meta07
                {"remark":"<名词>首先", 'type': type} # self.r071
            ]},
            {"mvalue":"其次", "relatedRealObjs":[ # self.meta08
                {"remark":"<名词>其次", 'type': type} # self.r081
            ]},
            {"mvalue":"再次", "relatedRealObjs":[ # self.meta09
                {"remark":"<名词>再次", 'type': type} # self.r091
            ]},
            {"mvalue":"最后", "relatedRealObjs":[ # self.meta10
                {"remark":"<名词>最后", 'type': type} # self.r101
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

    def testSaveCollection(self):
        print ("----testSaveCollection----")
        Collection([self.r011, self.r021, self.r031, self.r041], CollectionModeEnum.HEADCLOSE).save()
        # print "Chain1<%s> = [[['甲', '乙'], '丙'], '丁']" % self.chain1.id
        # Collection([self.r071, self.r081, self.r091, self.r101], CollectionModeEnum.HEADTAILCLOSE).save()
        # Collection([self.r051, self.r061], CollectionModeEnum.ALLCLOSE).save()
        # print "Chain1<%s> = ['如果', '那么']" % self.chain1.id

    def tearDown(self):
        print ("----tearDown----")
