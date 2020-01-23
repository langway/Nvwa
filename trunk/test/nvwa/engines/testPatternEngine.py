from unittest import TestCase
from loongtian.nvwa.organs.brain import Brain
from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.centrals.memoryCentral import MemoryCentral
from loongtian.nvwa.models.enum import ObjType

__author__ = 'Leon'


class TestPatternEngine(TestCase):
    def setUp(self):
        print ("----setUp----")

        self.brain = Brain()
        self.ThinkingCentral = self.brain.ThinkingCentral
        self.PatternEngine = self.ThinkingCentral.PatternEngine

        self.obj_types = [
            [ObjType.REAL_OBJECT, ObjType.REAL_OBJECT, ObjType.REAL_OBJECT],
            [ObjType.REAL_OBJECT, ObjType.ACTION, ObjType.REAL_OBJECT],
            [ObjType.REAL_OBJECT, ObjType.REAL_OBJECT, ObjType.REAL_OBJECT, ObjType.ACTION],
            [ObjType.ACTION, ObjType.ACTION, ObjType.REAL_OBJECT],
        ]


    def testCreateDoubleFrequancyDict(self):
        """
        测试创建元输入双字-频率字典
        :return:
        """
        print ("----testCreateDoubleFrequancyDict----")
        # 多输入
        doubleFrequancyDict1, length = self.PatternEngine.createObjTypeDoubleFrequancyDict(self.obj_types,key_connector="_")
        print(doubleFrequancyDict1)

    def testExtractObjTypePattern(self):
        """
        测试根据元输入，从双字-频率字典提取元词块（可能有多个）（传入self.WordFrequncyDict）
        :return:
        """
        print("----testExtractObjTypePattern----")
        objTypePattern=self.PatternEngine.extractObjTypePattern(self.obj_types,key_connector="_")
        print(objTypePattern)


