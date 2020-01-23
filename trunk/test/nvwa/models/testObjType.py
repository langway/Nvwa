

from unittest import TestCase
from loongtian.nvwa.models.enum import ObjType
class TestObjType(TestCase):
    def setUp(self):
        print("----setUp----")


    def testGetSubTypes(self):
        print("----testGetSubTypes----")
        self.assertEqual(ObjType.getSubTypes(ObjType.ACTION),
                         [ObjType.COMMON_ACTION,
                          ObjType.INSTINCT,
                          ])

        self.assertEqual(ObjType.getSubTypes(ObjType.REAL_OBJECT),
                         [ObjType.EXISTENCE,
                          ObjType.VIRTUAL,
                          ])

        self.assertEqual(ObjType.getSubTypes(ObjType.INSTINCT),
                         [ObjType.ORIGINAL,
                          ObjType.TOP_RELATION,
                          ObjType.INNER_OPERATION
                          ])



    def testGetTopType(self):
        print("----testGetTopType----")
        self.assertEqual(ObjType.getParentType(ObjType.COMMON_ACTION),
                         [ObjType.ACTION,
                          ])
        self.assertEqual(ObjType.getParentType(ObjType.PLACEHOLDER,level=2),
                         [ObjType.REAL_OBJECT,
                          ObjType.VIRTUAL
                          ])

    def tearDown(self):
        print("----tearDown----")