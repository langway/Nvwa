
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from loongtian.nvwa.managers.dialogsManager import DialogsManager,Dialog
from loongtian.nvwa.models.realObject import RealObject


class TestDialogsManager(TestCase):
    def setUp(self):
        print("----setUp----")
        self.DialogsManager=DialogsManager()

        self.dialog_niu=Dialog()
        self.dialog_ma = Dialog()
        self.dialog_yang = Dialog()
        self.dialog_xihongshi = Dialog()

        self.DialogsManager.add(self.dialog_niu)
        self.DialogsManager.add(self.dialog_ma)
        self.DialogsManager.add(self.dialog_yang)
        self.DialogsManager.add(self.dialog_xihongshi)

        real_niu = RealObject(remark="牛")
        real_ma = RealObject(remark="马")
        real_yang = RealObject(remark="羊")
        real_jiao = RealObject(remark="角")
        real_tui = RealObject(remark="腿")
        real_weiba = RealObject(remark="尾巴")
        real_xihongshi = RealObject(remark="西红柿")
        real_hongse = RealObject(remark="红色")

        self.dialog_niu.subjects.extend([real_niu,real_jiao,real_tui,real_weiba])
        self.dialog_ma.subjects.extend([real_ma, real_tui, real_weiba])
        self.dialog_yang.subjects.extend([real_yang, real_jiao, real_tui, real_weiba])
        self.dialog_xihongshi.subjects.extend([real_xihongshi,real_hongse])

    def testGetDialogBySubjects(self):
        print("----testGetDialogBySubjects----")

        dialogsBySubjects=self.DialogsManager.getRelatedDialogsBySubjects(self.dialog_niu.subjects)
        print(dialogsBySubjects)

        dialogsBySubjects=self.DialogsManager.getRelatedDialogsBySubjects(self.dialog_ma.subjects)
        print(dialogsBySubjects)

        dialogsBySubjects = self.DialogsManager.getRelatedDialogsBySubjects(self.dialog_yang.subjects)
        print(dialogsBySubjects)

        dialogsBySubjects = self.DialogsManager.getRelatedDialogsBySubjects(self.dialog_xihongshi.subjects)
        print(dialogsBySubjects)

    def tearDown(self):
        print("----tearDown----")