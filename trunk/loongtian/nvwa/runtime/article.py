__author__ = 'Leon'

from loongtian.util.common.enum import Enum
from loongtian.util.helper import stringHelper
from loongtian.nvwa.runtime.sequencedObjs import SequencedObjs, SequencedObj


class DialogDirection(Enum):
    """
    对话类的方向枚举。
    """
    Input = 0
    Output = 1


DialogDirection = DialogDirection()


class StrContent(SequencedObj):
    """
    各种级别的字符串包装类（包括文章、段落、句子、短句、短语）
    """

    def __init__(self, rawInput: str, parent, userid=None, dialogDirection=DialogDirection.Input):
        """
        各种级别的字符串包装类（包括文章、段落、句子、短句、短语）
        :param rawInput:子级字符串
        :param parent: 父对象
        :param userid: 进行输入/输出的用户id
        :param dialogDirection: 输入/输出的方向
        """
        if not rawInput:
            raise Exception("必须提供子级字符串！")
        super(StrContent, self).__init__(containedObj=rawInput)

        self.parent = parent  # 父对象

        self.userid = userid
        self.dialogDirection = dialogDirection

        self.thinkResult = None  # 当前级别的字符串的思考结果，供thinkCentral/mind调用


class _StrStructure(StrContent):
    """
    各种级别的字符串包装类（包括文章、段落、句子、短句、短语）
    """

    def __init__(self, rawInput: str,
                 parent,
                 subContentType: type,
                 stopMarkLevel=stringHelper.StopMarkLevel.paragraph,
                 splitWholeAlphabet=False,
                 splitWholeNumber=False,
                 userid=None,
                 dialogDirection=DialogDirection.Input):
        """
        文章级别的完整的字符串输入
        :param rawInput: 子级字符串
        :param parent: 父对象
        :param subContentType: 子级字符串包装类类型
        :param stopMarkLevel: 子级字符串包装类序列
        :param splitWholeAlphabet: 是否对子级字符串中的字母进行着整体分割
        :param splitWholeNumber: 是否对子级字符串中的数字进行着整体分割
        """
        super(_StrStructure, self).__init__(rawInput=rawInput, parent=parent, userid=userid,
                                            dialogDirection=dialogDirection)

        if not subContentType:  # 子级字符串包装类类型
            raise Exception("必须提供子级字符串包装类类型！")
        self._subContentType = subContentType
        self._subContents = None  # SequencedObjs([subContentType]) # 子级字符串包装类序列

        self._stopMarkLevel = stopMarkLevel  # 子级字符串的分割标点符号
        self._splitWholeAlphabet = splitWholeAlphabet  # 是否对子级字符串中的字母进行着整体分割
        self._splitWholeNumber = splitWholeNumber  # 是否对子级字符串中的数字进行着整体分割

    def _getSubContents(self, forceRestructure=False):
        """
        取得下一级别的字符串（包装类）
        :param: 强制更新结构
        :return:
        """
        if self._subContents and len(self._subContents) > 0 and not forceRestructure:
            return self._subContents

        self._subContents = SequencedObjs([self._subContentType])
        if self.containedObj is None:
            return self._subContents

        level_freq_stopMarks, level_stopMarks = stringHelper.getLeveledStopMarks()
        stopMarks = level_stopMarks[self._stopMarkLevel]

        splits = stringHelper.splitWithStopMarksAndNumbersAndEnglish(
            self.containedObj,
            stopMarks,
            splitWholeAlphabet=self._splitWholeAlphabet,
            splitWholeNumber=self._splitWholeNumber
        )

        # 生成句子，如果后面的是分割标点符号，合并至前一个
        i = 0
        while i < len(splits):
            cur_split = splits[i]

            if not cur_split:
                i += 1
                continue
            next_split_is_stopmark = False
            next_split = None
            if i < len(splits) - 1:
                next_split = splits[i + 1]
                if next_split and next_split in stopMarks:
                    next_split_is_stopmark = True

            new_subContent = self._subContentType(rawInput=cur_split, parent=self, userid=self.userid,
                                                  dialogDirection=self.dialogDirection)
            if hasattr(new_subContent, "_getSubContents"):
                new_subContent._getSubContents()
            if next_split_is_stopmark and hasattr(new_subContent, "_subContentType"):
                new_subContent.containedObj += next_split

                new_grandsonContent = new_subContent._subContentType(rawInput=next_split, parent=new_subContent,
                                                                     userid=self.userid,
                                                                     dialogDirection=self.dialogDirection)
                if hasattr(new_grandsonContent, "_getSubContents"):
                    new_grandsonContent._getSubContents()
                new_subContent._subContents.add(new_grandsonContent)
                i += 2
            else:
                i += 1
            self._subContents.add(new_subContent)

        return self._subContents

    def getRealContent(self):
        """
        取得实际的内容。
        :return:
        :remark:可能输入的中只有一个词、短语或句子，这时无需遍历，直接返回当前级别的包装类。
        """
        self._getSubContents()
        if len(self._subContents) == 0:
            return None
        elif len(self._subContents) == 1:
            if hasattr(self._subContents[0], "getRealContent"):
                return self._subContents[0].getRealContent()
            else:
                return self._subContents[0]
        else:
            return self

    def getFirstInShortPhrase(self):
        """
        取得当前级别内第一个需要处理的短语。
        :return:
        """
        sub_content = self.getRealContent()
        return self.__getFirstInShortPhrase(sub_content)

    def __getFirstInShortPhrase(self, sub_content):
        """
        递归取得当前级别内第一个需要处理的短语。
        :return:
        """
        if isinstance(sub_content, InShortPhrase):
            return sub_content

        if hasattr(sub_content,"_subContents") and sub_content._subContents:
            return self.__getFirstInShortPhrase(sub_content._subContents[0])
        return None


class Article(_StrStructure):
    """
    文章级别的完整的字符串输入
    """

    def __init__(self, rawInput: str,
                 userid=None,
                 dialogDirection=DialogDirection.Input):
        """
        文章级别的完整的字符串输入
        :param rawInput:
        """
        super(Article, self).__init__(rawInput,
                                      parent=None,
                                      subContentType=Paragraph,
                                      stopMarkLevel=stringHelper.StopMarkLevel.paragraph,
                                      splitWholeAlphabet=False,
                                      splitWholeNumber=False,
                                      userid=userid, dialogDirection=dialogDirection)

    def getParagraphs(self):
        """
        取得段落级别的字符串（包装类）
        :return:
        """
        return self._getSubContents()


class Paragraph(_StrStructure):
    """
    段落级别的字符串输入
    """

    def __init__(self, rawInput: str, parent: Article,
                 userid=None,
                 dialogDirection=DialogDirection.Input):
        """
        段落级别的完整的字符串输入
        :param rawInput:
        """
        super(Paragraph, self).__init__(rawInput,
                                        parent=parent,
                                        subContentType=Sentence,
                                        stopMarkLevel=stringHelper.StopMarkLevel.sentence,
                                        splitWholeAlphabet=False,
                                        splitWholeNumber=False,
                                        userid=userid, dialogDirection=dialogDirection)

    def getSentences(self):
        """
        取得句子级别的字符串（包装类）
        :return:
        """
        return self._getSubContents()


class Sentence(_StrStructure):
    """
    句子级别的字符串输入
    """

    def __init__(self, rawInput: str, parent: Paragraph,
                 userid=None,
                 dialogDirection=DialogDirection.Input):
        """
        句子级别的完整的字符串输入
        :param rawInput:
        """
        super(Sentence, self).__init__(rawInput,
                                       parent=parent,
                                       subContentType=ShortPhrase,
                                       stopMarkLevel=stringHelper.StopMarkLevel.short,
                                       splitWholeAlphabet=False,
                                       splitWholeNumber=False,
                                       userid=userid, dialogDirection=dialogDirection)

    def getShortPhrases(self):
        """
        取得短句级别的字符串（包装类）
        :return:
        """
        return self._getSubContents()


class ShortPhrase(_StrStructure):
    """
    短句级别的字符串输入
    """

    def __init__(self, rawInput: str, parent: Sentence,
                 userid=None,
                 dialogDirection=DialogDirection.Input):
        """
        短句级别的完整的字符串输入
        :param rawInput:
        """
        super(ShortPhrase, self).__init__(rawInput,
                                          parent=parent,
                                          subContentType=InShortPhrase,
                                          stopMarkLevel=stringHelper.StopMarkLevel.inshort,
                                          splitWholeAlphabet=True,
                                          splitWholeNumber=True,
                                          userid=userid, dialogDirection=dialogDirection)

    def getInShortPhrases(self):
        """
        取得短语级别的字符串（包装类）
        :return:
        """
        return self._getSubContents()


class InShortPhrase(StrContent):
    """
    短语级别的字符串输入
    """

    def __init__(self, rawInput: str,
                 parent: ShortPhrase,
                 userid=None,
                 dialogDirection=DialogDirection.Input):
        """
        短语级别的完整的字符串输入
        :param rawInput: 子级字符串
        :param parent: 父对象
        :param userid: 进行输入/输出的用户id
        :param dialogDirection: 输入/输出的方向
        """
        super(InShortPhrase, self).__init__(rawInput=rawInput, parent=parent, userid=userid,
                                            dialogDirection=dialogDirection)

        self.segmentedResult = None

    def getFirstInShortPhrase(self):
        """
        取得当前级别内第一个需要处理的短语。
        :return:
        """
        return self
