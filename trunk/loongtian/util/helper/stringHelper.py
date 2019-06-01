#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'leon'

import math
import re
import hashlib
from loongtian.util.common.enum import Enum


"""
标点符号字典，包括0：段落标记、1：整句子间标点符号、2：短语间标点符号、3：短语内标点符号
格式为：{标点符号:[标点符号类别,词频]}
"""
StopMarks = {
     # paragraphMarks段落标记
        u"\r\n":[0, 8.8],
        u"\n": [0,6.5],
        u"\r": [0,3.3],
        # u"\t":[0,2.0],
    # sentence_punctuation句子间标点符号，是句子结束
        u".": [1,9.2],
        u";": [1,9.2],
        u"?": [1,9.2],
        u"…": [1,9.2],
        u"!": [1,9.2],
        u"。": [1,9.2],
        u"；": [1,9.2],
        u"！": [1,9.2],
        u"？": [1,9.2],
        u"……": [1,9.2],
    # short_punctuation短语间标点符号，不是句子结束
        u",": [2,8.8],
        u":": [2,8.8],
        u"...": [2,8.8],
        u"，": [2,8.8],
        u"：": [2,8.8],
        # u" ": [2,8.8], # 空格
    # inshort_punctuation短语间标点符号，不是短语结束
        u"+": [3,8.8],
        u"-": [3,8.8],
        u"|": [3,8.8],
        u"/": [3,8.8],
        u"\\": [3,8.8],
        u"'": [3,8.8],
        u"\"": [3,8.8],
        u"<": [3,8.8],
        u">": [3,8.8],
        u"[": [3,8.8],
        u"]": [3,8.8],
        u"{": [3,8.8],
        u"}": [3,8.8],
        u"@": [3,8.8],
        u"#": [3,8.8],
        u"$": [3,8.8],
        u"%": [3,8.8],
        u"^": [3,8.8],
        u"&": [3,8.8],
        u"*": [3,8.8],
        u"(": [3,8.8],
        u")": [3,8.8],
        u"~": [3,8.8],
        u"`": [3,8.8],
        u"‘": [3,8.8],
        u"’": [3,8.8],
        u"“": [3,8.8],
        u"”": [3,8.8],
        u"／": [3,8.8],
        u"～": [3,8.8],
        u"＠": [3,8.8],
        u"＃": [3,8.8],
        u"￥": [3,8.8],
        u"％": [3,8.8],
        u"＆": [3,8.8],
        u"×": [3,8.8],
        u"（": [3,8.8],
        u"）": [3,8.8],
        u"【": [3,8.8],
        u"】": [3,8.8],
        u"｛": [3,8.8],
        u"｝": [3,8.8],
        u"｜": [3,8.8],
        u"、": [3,8.8],
        u"《": [3,8.8],
        u"》": [3,8.8],
        u"——": [3,8.8],
}


class StringNullOrEmptyException(Exception):
    """
    对象非字符串或是空白的错误类。
    """
    pass

class StringTypeEnum(Enum):
    """
    字符串的类型。包括：
    PURE_CHINESE=0 # 纯中文
    PURE_ENGLISH=1 # 纯英文
    PURE_NUMBERS=2 # 纯数字
    CHINESE_ENGLISH=3 # 中英文混合
    CHINESE_NUMBERS=4 # 中文数字混合
    ENGLISH_NUMBERS=5 # 英文数字混合
    CHINESE_ENGLISH_NUMBERS=6 # 中文英文数字混合
    OTHER=9 # 其他
    """
    PURE_CHINESE=0 # 纯中文
    PURE_ENGLISH=1 # 纯英文
    PURE_NUMBERS=2 # 纯数字
    CHINESE_ENGLISH=3 # 中英文混合
    CHINESE_NUMBERS=4 # 中文数字混合
    ENGLISH_NUMBERS=5 # 英文数字混合
    CHINESE_ENGLISH_NUMBERS=6 # 中文英文数字混合
    OTHER=9 # 其他

StringTypeEnum=StringTypeEnum()

Numbers = [0,1,2,3,4,5,6,7,8,9] # 阿拉伯数字

# 罗马数字
RomanNumbers = {
    # 个位数举例
    'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,
    # 十位数举例
      'X':10,'XL':40,'L':50,'XC':90,
    # 百位数举例
    'C':100,'CD':400,'D':500,'CM':900,'M':1000
}

# 希腊字母
GreekAlphabet={
    u"Α":u"alpha",
    u"Β":u"beta",
    u"Γ":u"gamma",
    u"Δ":u"delta",
    u"Ε":u"epsilon",
    u"Ζ":u"zeta",
    u"Η":u"eta",
    u"Θ":u"theta",
    u"Ι":u"iota",
    u"Κ":u"kappa",
    u"Λ":u"lambda",
    u"Μ":u"mu",
    u"α":u"alpha",
    u"β":u"beta",
    u"γ":u"gamma",
    u"δ":u"delta",
    u"ε":u"epsilon",
    u"ζ":u"zeta",
    u"η":u"eta",
    u"θ":u"theta",
    u"ι ℩":u"iota",
    u"κ":u"kappa",
    u"λ":u"lambda",
    u"μ":u"mu",
    u"Ν":u"nu",
    u"Ξ":u"xi",
    u"Ο":u"omicron",
    u"Π":u"pi",
    u"Ρ":u"rho",
    u"Σ":u"sigma",
    u"Τ":u"tau",
    u"Υ":u"upsilon",
    u"Φ":u"phi",
    u"Χ":u"chi",
    u"Ψ":u"psi",
    u"Ω":u"omega",
    u"ν":u"nu",
    u"ξ":u"xi",
    u"ο":u"omicron",
    u"π":u"pi",
    u"ρ":u"rho",
    u"σ":u"sigma",
    u"τ":u"tau",
    u"υ":u"upsilon",
    u"φ":u"phi",
    u"χ":u"chi",
    u"ψ":u"psi",
    u"ω":u"omega",

}

def checkStringNullOrEmpty(content,raiseException=True):
    if isStringNullOrEmpty(content):
        if raiseException:
            raise StringNullOrEmptyException("输入的对象非字符串或字符串为空！请检查输入:" +str(content))
    # else:
    #     # return False
    #     pass


def isStringNullOrEmpty(content):
    """
    判断一个对象是否是字符串或是空白
    :rawParam content:输入对象
    :return:
    """
    if content is None:
        return True

    if isinstance(content, str) and content=="":
        return True

    else:
        return False


def isNotAStringOrStringEmpty(content):
    """
    <id></id>
    <ObjectType>Action</ObjectType>
    <Relation>处理方法</Relation>
    <MetaData>判断<arg>1</arg>是否是字符串或是空白;Is <arg>1</arg> Not A String Or String Empty</MetaData>
    <Postion>1</Postion>
    <Args>
        <Arg>
            <id></id>
            <ObjectType>RealObject</ObjectType>
            <Relation></Relation>
            <Postion>2</Postion>
            <MetaData>内容;content</MetaData>
        <Arg>
    </Args>
    <Return></Return>
    <Remark>Postion:用来存放与当前对象的位置关系，例如-1就是在当前对象前面(默认为1)</Remark>
    """
    return not isStringNullOrEmpty(content)

    pass#def isNotAStringOrStringEmpty(content):

def converUnicodeToString(u):
    try:
        u=u.encode("utf-8")
    except:
        try:
            u= u.encode('raw_unicode_escape')
        except:
            u=None

    return u

def converStringToUnicode(s):
    try:
        s=s.decode("utf-8")
    except:
        try:
            s= s.decode('raw_unicode_escape')
        except:
            s=None

    return s


def convert_hex_to_string(hex):
    try:
        return hex.decode("gbk")
    except:
        return None

def convertToNumber(s):
    """
    将一个全数字的字符串转化成数字（float、int类型）
    :param s:
    :return:
    """
    if isStringNullOrEmpty(s):
        return None
    #试着进行float、int类型等数字类型的转换
    if s.isdigit():
        return int(s)
    elif is_float(s):
        return float(s)

    # elif isKexue(s):
    #     raise NotImplementedError('科学计数法判断尚未实现！')
    #     return float(s)
    # elif isFushu(s):
    #     raise NotImplementedError('复数计数法判断尚未实现！')
    #     return float(s)

    return None

def is_float(str):
    """
    判断一个字符串是否是float
    :rawParam str:
    :return:
    """
    pattern= '^[-+]?[0-9]+\.[0-9]+$ ' #'^([0-9]*.[0-9]+)?$'
    # 将正则表达式编译成Pattern对象
    pattern = re.compile(pattern, re.S)
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    _matched = pattern.findall(str)
    if _matched is None or len(_matched )==0 :
        return False

    if str==_matched[0]:
        return True

    return False

def is_chinese(ustr):
    """
    判断一个unicode是否是汉字
    :param ustr:
    :return:
    """
    for uchar in ustr:
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            continue
        else:
            return False # 只要有一个不是，就返回
    return True

def is_all_chinese(ustr):
    """
    判断一个unicode是否是汉字（包含空格、标点等）
    :param ustr:
    :return:
    """
    for uchar in ustr:
        if (uchar >= u'\u4e00' and uchar<=u'\u9fa5') or uchar==u" " or StopMarks.has_key(uchar):
            continue
        else:
            return False # 只要有一个不是，就返回
    return True


def is_stopmark(uchar):
    """
    判断一个unicode字符是否是标点符号
    :param uchar:
    :return:
    """
    return StopMarks.has_key(uchar)

def is_number(ustr):
    """
    判断一个unicode是否是数字
    :param ustr: 可以是一长串数字。
    :return:
    """
    # for uchar in ustr:
    #     if uchar >= u'\u0030' and uchar<=u'\u0039':
    #         pass
    #     else:
    #         return False # 只要有一个不是，就返回
    #
    # return True
    if ustr.isdigit():
        return True
    elif is_float(ustr):
        return True

    return False


def is_alphabet(ustr):
    """
    判断一个unicode是否是英文字母
    :param ustr:
    :return:
    """
    for uchar in ustr:
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            pass
        else:
            return False # 只要有一个不是，就返回
    return True



def is_all_alphabet(ustr):
    """
    判断一个unicode字符串是否是英文字母（可以包含空格、标点）
    :param ustr:
    :return:
    """
    for uchar in ustr:
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or \
                (uchar >= u'\u0061' and uchar<=u'\u007a') or \
                        uchar==u" " or is_stopmark(uchar):
            pass
        else:
            return False # 只要有一个不是，就返回
    return True

def get_string_type(ustr):
    """
    取得字符串类型。包括：
    PURE_CHINESE=0 # 纯中文
    PURE_ENGLISH=1 # 纯英文
    PURE_NUMBERS=2 # 纯数字
    CHINESE_ENGLISH=3 # 中英文混合
    CHINESE_NUMBERS=4 # 中文数字混合
    ENGLISH_NUMBERS=5 # 英文数字混合
    CHINESE_ENGLISH_NUMBERS=6 # 中文英文数字混合
    OTHER=9 # 其他
    :param ustr:
    :return:
    """
    has_chinese=False
    has_english=False
    has_number=False
    for uchar in ustr:
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a') or uchar==u" ":
            has_english=True
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            has_chinese=True
        if ustr.isdigit():
            has_number=True
        if has_english and has_chinese and has_number: # 已经全都有了，直接返回
            return StringTypeEnum.CHINESE_ENGLISH_NUMBERS

    if not has_english:
        if has_chinese :
            if has_number :
                return StringTypeEnum.CHINESE_NUMBERS
            else:
                return StringTypeEnum.PURE_CHINESE
        else:
            if has_number :
                return StringTypeEnum.PURE_NUMBERS
            else:
                return StringTypeEnum.OTHER
    else:
        if has_chinese:
            if has_number :
                return StringTypeEnum.CHINESE_ENGLISH_NUMBERS
            else:
                return StringTypeEnum.CHINESE_ENGLISH
        else:
            if has_number :
                return StringTypeEnum.ENGLISH_NUMBERS
            else:
                return StringTypeEnum.PURE_ENGLISH

    return StringTypeEnum.OTHER


def encodeStringMD5(string=None):
    """
    获取字符串的MD5值
    :return:MD5加密后的字符串
    """

    if string:
        string = hashlib.md5(string.encode("gbk")).hexdigest()
    return string

def mailValid(mail):
    """
    邮箱格式验证
    :return:True or False ,验证成功返回True
    """
    isMatch = bool(re.match(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$', mail, re.VERBOSE))
    return isMatch

def phoneValid(phone):
    """
    手机格式验证
    :return:True or False ,验证成功返回True
    """
    isMatch = bool(re.match(r'^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1})|145|147|)+\d{8})$', phone, re.VERBOSE))
    return isMatch

import random, string

def Genjhm(length):
    #随机出数字的个数
    numOfNum = random.randint(1,length-1)
    numOfLetter = length - numOfNum
    #选中numOfNum个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    #选中numOfLetter个字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    #打乱这个组合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    #生成密码
    genPwd = ''.join([i for i in slcChar])
    return genPwd

def is_title(ustr):
    """
    所有单词都是首字母大写
    :param ustr:
    :return:
    """
    return ustr.istitle()

def is_space(ustr):
    """
     str.isspace() 所有字符都是空白字符、\t、\n、\r
    :param ustr:
    :return:
    """
    return  ustr.isspace() # 所有字符都是空白字符、\t、\n、\r

def is_other(ustr):
    """
    判断是否非汉字，数字和英文字符
    :param uchar:
    :return:
    """
    if not (is_chinese(ustr) or is_number(ustr) or is_alphabet(ustr)):
        return True
    else:
        return False

def contain_upper(ustr):
    """
    是否包含大写字母
    :param ustr:
    :return:
    """
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(ustr)
    if match:
        return True
    else:
        return False

def contain_num(ustr):
    """
    是否包含数字
    :param ustr:
    :return:
    """
    pattern = re.compile('[0-9]+')
    match = pattern.findall(ustr)
    if match:
        return True
    else:
        return False

def contain_zh_cn(ustr):
    """
    是否包含汉字
    :param ustr:
    :return:
    """
    for ch in ustr.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    else:
        return False

def contain_lower(ustr):
    """
    是否包含小写字母
    :param ustr:
    :return:
    """
    pattern = re.compile('[a-z]+')
    match = pattern.findall(ustr)
    if match:
        return True
    else:
        return False

def contain_stopMark(value):
    try:
        value=value.decode("utf-8")
        for c in value:
            if StopMarks.has_key(c):
                return True
        return False
    except:
        return False






UNITS = [u"", u"十", u"百", u"千", u"万", u"十", u"百", u"千",
         u"亿", u"十", u"百", u"千",u"万",u"十",u"百",u"千",
         u"兆",u"十", u"百", u"千",u"万",u"十",u"百",u"千",
         u"京",u"十", u"百", u"千",u"万",u"十",u"百",u"千"]
NUMS = [u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"]


UNITS_MONEY = [u"", u"拾", u"佰", u"仟", u"萬", u"拾", u"佰", u"仟",
             u"亿", u"拾", u"佰", u"仟", u"萬", u"拾", u"佰", u"仟",
             u"兆",u"拾", u"佰", u"仟", u"萬", u"拾", u"佰", u"仟",
             u"京",u"拾", u"佰", u"仟", u"萬", u"拾", u"佰", u"仟",]
NUMS_MONEY = [u"零", u"壹", u"贰", u"叁", u"肆", u"伍", u"陆", u"柒", u"捌", u"玖"]

CN_NUM = { # 汉字数字与阿拉伯数字对应的字典
    u'〇': 0,
    u'一': 1,
    u'二': 2,
    u'三': 3,
    u'四': 4,
    u'五': 5,
    u'六': 6,
    u'七': 7,
    u'八': 8,
    u'九': 9,

    u'零': 0,
    u'壹': 1,
    u'贰': 2,
    u'叁': 3,
    u'肆': 4,
    u'伍': 5,
    u'陆': 6,
    u'柒': 7,
    u'捌': 8,
    u'玖': 9,

    u'貮': 2,
    u'两': 2,
    u'俩': 2,
}

NUM_CN = { # 阿拉伯数字与汉字数字对应的字典
    0:u'〇' ,
    1:u'一' ,
    2:u'二' ,
    3:u'三' ,
    4:u'四' ,
    5:u'五' ,
    6:u'六' ,
    7:u'七' ,
    8:u'八' ,
    9:u'九' ,
}


CN_UNIT = {
    u'十': 10,
    u'拾': 10,
    u'百': 100,
    u'佰': 100,
    u'千': 1000,
    u'仟': 1000,
    u'万': 10000,
    u'萬': 10000,
    u'亿': 100000000,
    u'億': 100000000,
    u'兆': 1000000000000,
}


def arabicNumeral_to_chineseNumeral(num):
    """
    阿拉伯数字转汉字数字
    :rawParam num:
    :return:
    """
    num=str(num)
    if not num =="0":
        num = str(num.lstrip(u'0'))
    res = ''

    num= num.split('.') # 分割小数点
    lnum=None
    rnum=None
    if len(num)==2:
        lnum=num[0]
        rnum=num[1]
    elif len(num)==1:
        lnum=num[0]


    # 处理小数点左侧
    if lnum:
        for p in range(len(lnum) - 1, -1, -1):
            r = int(int(lnum) / math.pow(10, p))
            res += NUMS[r % 10] + UNITS[p]

        for (i, j) in [(u'零十', u'零'), (u'零百', u'零'), (u'零千', u'零'),(u'十零', u'十')]:
            res = res.replace(i, j)

        while res.find(u'零零') != -1:
            res = res.replace(u'零零', u'零')

        for (i, j) in [(u'零万', u'万'), (u'零亿', u'亿')]:
            res = res.replace(i, j)

        res = res.replace(u'亿万', u'亿')

        if res.startswith(u'一十'):
            res = res[2:]

        if res!=u'零' and res.endswith(u'零'):
            res = res[:-2]

    if rnum and not rnum==u'零':
        while rnum.endswith(u'零'):
            rnum =rnum.strip(u'零')
        res += u"点"
        for p in range(0,len(rnum)):
            cur_num=int(rnum[p])
            cur_num_cn=NUM_CN.get(cur_num)
            if cur_num_cn:
                res += cur_num_cn
    return res



def arabicNumeral_to_chineseNumeral_Money(num):
    """
    阿拉伯数字转汉字大写数字
    :rawParam num:
    :return:
    """
    num=str(num)

    num = str(num.lstrip(u'0'))
    res = ''

    num= num.split('.') # 分割小数点
    lnum = None
    if len(num)==2:
        lnum=num[0]
        rnum=num[1]
    elif len(num)==1:
        lnum=num[0]


    # 处理小数点左侧
    if lnum:
        for p in range(len(lnum) - 1, -1, -1):
            r = int(int(lnum) / math.pow(10, p))
            res += NUMS_MONEY[r % 10] + UNITS_MONEY[p]

        for (i, j) in [(u'零拾', u'零'), (u'零佰', u'零'), (u'零仟', u'零'),(u'拾零', u'拾')]:
            res = res.replace(i, j)

        while res.find(u'零零') != -1:
            res = res.replace(u'零零', u'零')

        for (i, j) in [(u'零萬', u'萬'), (u'零亿', u'亿')]:
            res = res.replace(i, j)

        res = res.replace(u'亿萬', u'亿')

        if res.startswith(u'壹拾'):
            res = res[2:]

        if res.endswith(u'零'):
            res = res[:-2]

    if rnum:
        while rnum.endswith(u'零'):
            rnum =rnum.strip(u'零')
        res += u"点"
        for p in range(0,len(rnum)):
            cur_num=int(rnum[p])
            cur_num_cn=NUM_CN.get(cur_num)
            if cur_num_cn:
                res += cur_num_cn
    return res


def chineseNumeral_to_arabicNumeral(cn):
    """
    汉字数字转阿拉伯数字
    :rawParam cn:
    :return:
    """
    cn= cn.split(u'点')

    lcn = None
    if len(cn)==2:
        lcn=cn[0]
        rcn=cn[1]
    elif len(cn)==1:
        lcn=cn[0]

    ret=0
    if lcn:
        lcn = list(lcn)
        multi=1

        while lcn:
            cndig = lcn.pop()
            dig = CN_NUM.get(cndig)
            if dig>0:
                dig*=multi
                ret+=dig
                multi*=10
            elif dig ==0:
                ret *=10
                multi*=100
    if rcn:
        rcn = list(rcn)[::-1]
        multi=0.1
        while rcn:
            cndig = rcn.pop()
            dig = CN_NUM.get(cndig)
            if dig>0:
                dig*=multi
                ret+=dig
                multi*=0.1
            elif dig ==0:
                multi*=0.1


    return ret


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                 #半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring


#
# def B2Q(uchar):
#     """半角转全角"""
#     try:
#     inside_code=ord(uchar)
#     if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
#             return uchar
#     if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
#             inside_code=0x3000
#     else:
#             inside_code+=0xfee0
#     return str(inside_code)
#
# def Q2B(uchar):
#     """全角转半角"""
#     inside_code=ord(uchar)
#     if inside_code==0x3000:
#             inside_code=0x0020
#     else:
#             inside_code-=0xfee0
#     if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
#             return uchar
#     return str(inside_code)

# def stringQ2B(ustring):
#     """把字符串全角转半角"""
#     return "".join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return strQ2B(ustring).lower()

def string2List(ustring):
    """将ustring按照中文，字母，数字分开"""
    retList=[]
    utmp=[]
    for uchar in ustring:
        if is_other(uchar):
            if len(utmp)==0:
                continue
            else:
                retList.append("".join(utmp))
                utmp=[]
        else:
            utmp.append(uchar)
    if len(utmp)!=0:
        retList.append("".join(utmp))
    return retList


def split(str,seprators):
    """
    根据seprators（list）分割字符串
    :param str:
    :param seprators:
    :return:
    """
    splits=[]
    if not seprators:
        seprators=[",","+","-","*","/","\\","(",")"]

    w=""
    for c in str:
        if not c in seprators:
            w+=c
        else:
            if not w=="":
                splits.append(w)
                w=""
            splits.append(c)
    if not w=="":
        splits.append(w)

    return splits

def splitsWithStopMarksAndNumbersAndEnglish(rawInput,stopMarks,stopMarkLevel = 3, keepStopMark = True,splitWithSpace=False):
    """
    将输入字符串与标点符号、数字、英文分开
    :param rawInput:
    :param stopMarks: 标点符号的字典，包括0：段落标记:1：句子间标点符号:2：句子内标点符号
                      格式为：{标点符号:[标点符号类别,词频]}
    :param stopMarkLevel: 按标点符号的划分级别（0：段落级别，1：段落级别+句子级别，2：段落级别+句子级别+句内级别）。
    :param keepStopMark: 是否保留分割的标点（默认为True）
    :param splitWithSpace:是否对空格进行分割
    :return:
    """
    splits=[]
    i=0

    cur_chars=u""
    length=len(rawInput)
    while i < length:
        cur_char=rawInput[i]

        if cur_char==u" ": # 如果是空格：
            if splitWithSpace:
                if not cur_chars==u"": # 添加已有的
                    splits.append(cur_chars)
                    cur_chars=u""
                splits.append(cur_char)
                i+=1
                continue
            else:
                cur_chars+=cur_char
                i+=1
                continue

        elif is_alphabet(cur_char): # 如果是英文
            cur_char=strQ2B(cur_char) # 转换成半角
            if not cur_chars==u"": # 添加已有的
                splits.append(cur_chars)
                cur_chars=u""
            cur_chars+=cur_char
            j=i+1
            if j==length: # 如果已经是最后一个了，直接停机
                break
            while j <len(rawInput):
                next_char=rawInput[j]

                if next_char==u" ":
                    if splitWithSpace:
                        splits.append(cur_chars)
                        cur_chars=u""
                        i=j
                        break
                    else:
                        cur_chars+= next_char
                        i=j
                elif is_alphabet(next_char) or next_char==u'’': # 如果后续是英文字母、’，继续合并添加
                   cur_chars+= next_char
                   i=j
                else:
                    splits.append(cur_chars)
                    cur_chars=u""
                    i=j
                    break
                j+=1

        elif is_stopmark(cur_char): # 如果是标点符号
            cur_char=strQ2B(cur_char) # 转换成半角
            if not cur_chars==u"": # 添加已有的
                splits.append(cur_chars)
                cur_chars=u""
            if cur_char==u'’': # 特殊处理英文中的'，例如：it's 需要连接在一起
                before_char=None
                next_char =None
                if i>=1:
                    before_char=rawInput[i-1]
                if i<len(rawInput)-1:
                    next_char=rawInput[i+1]
                before_char_is_number=False
                next_char_is_number=False
                if before_char:
                    if is_alphabet(before_char):
                        before_char_is_number=True
                else:
                    before_char_is_number=True
                if next_char :
                    if is_alphabet(next_char):
                        next_char_is_number=True
                else:
                    next_char_is_number =True

                if before_char_is_number and next_char_is_number:
                    cur_chars+=cur_char
                    i+=1
                    continue
            elif cur_char==u'.': # 特殊处理数字中的.，例如：6.9 需要连接在一起
                before_char=None
                next_char =None
                if i>=1:
                    before_char=rawInput[i-1]
                if i<len(rawInput)-1:
                    next_char=rawInput[i+1]
                before_char_is_number=False
                next_char_is_number=False
                if before_char:
                    if is_number(before_char):
                        before_char_is_number=True
                else:
                    before_char_is_number=True
                if next_char :
                    if is_number(next_char):
                        next_char_is_number=True
                else:
                    next_char_is_number =True

                if before_char_is_number and next_char_is_number:
                    cur_chars+=cur_char
                    i+=1
                    continue

            splits.append(cur_char)
            i+=1
            continue
        elif is_number(cur_char): # 如果是数字
            cur_char=strQ2B(cur_char) # 转换成半角
            if not cur_chars==u"": # 添加已有的
                splits.append(cur_chars)
                cur_chars=u""
            cur_chars+=cur_char
            j=i+1
            if j==length: # 如果已经是最后一个了，直接停机
                break
            while j <len(rawInput):
                next_char=rawInput[j]
                if is_number(next_char): # 如果后续是数字，继续合并添加
                   cur_chars+= next_char
                   i=j
                elif next_char==u".":
                    next_next_char=rawInput[j+1]
                    if is_number(next_next_char): # 如果后续是数字，继续合并添加
                       cur_chars+= next_char
                       i=j
                else:
                    splits.append(cur_chars)
                    cur_chars=u""
                    i=j
                    break
                j+=1

        else:
            cur_chars+=cur_char
            if i==len(rawInput)-1: # 如果是最后一个
                splits.append(cur_chars)

            i+=1

    return splits


# 现实情况下可能并不会把所以的字符统一进行转换，
# 比如中文文章中我们期望将所有出现的字母和数字全部转化成半角，
# 而常见标点符号统一使用全角，上面的转化就不适合了。
FH_SPACE = FHS = ((u"　", u" "),)
FH_NUM = FHN = (
 (u"０", u"0"), (u"１", u"1"), (u"２", u"2"), (u"３", u"3"), (u"４", u"4"),
 (u"５", u"5"), (u"６", u"6"), (u"７", u"7"), (u"８", u"8"), (u"９", u"9"),
)
FH_ALPHA = FHA = (
 (u"ａ", u"a"), (u"ｂ", u"b"), (u"ｃ", u"c"), (u"ｄ", u"d"), (u"ｅ", u"e"),
 (u"ｆ", u"f"), (u"ｇ", u"g"), (u"ｈ", u"h"), (u"ｉ", u"i"), (u"ｊ", u"j"),
 (u"ｋ", u"k"), (u"ｌ", u"l"), (u"ｍ", u"m"), (u"ｎ", u"n"), (u"ｏ", u"o"),
 (u"ｐ", u"p"), (u"ｑ", u"q"), (u"ｒ", u"r"), (u"ｓ", u"s"), (u"ｔ", u"t"),
 (u"ｕ", u"u"), (u"ｖ", u"v"), (u"ｗ", u"w"), (u"ｘ", u"x"), (u"ｙ", u"y"), (u"ｚ", u"z"),
 (u"Ａ", u"A"), (u"Ｂ", u"B"), (u"Ｃ", u"C"), (u"Ｄ", u"D"), (u"Ｅ", u"E"),
 (u"Ｆ", u"F"), (u"Ｇ", u"G"), (u"Ｈ", u"H"), (u"Ｉ", u"I"), (u"Ｊ", u"J"),
 (u"Ｋ", u"K"), (u"Ｌ", u"L"), (u"Ｍ", u"M"), (u"Ｎ", u"N"), (u"Ｏ", u"O"),
 (u"Ｐ", u"P"), (u"Ｑ", u"Q"), (u"Ｒ", u"R"), (u"Ｓ", u"S"), (u"Ｔ", u"T"),
 (u"Ｕ", u"U"), (u"Ｖ", u"V"), (u"Ｗ", u"W"), (u"Ｘ", u"X"), (u"Ｙ", u"Y"), (u"Ｚ", u"Z"),
)
FH_PUNCTUATION = FHP = (
 (u"．", u"."), (u"，", u","), (u"！", u"!"), (u"？", u"?"), (u"”", u'"'),
 (u"'", u"'"), (u"‘", u"`"), (u"＠", u"@"), (u"＿", u"_"), (u"：", u":"),
 (u"；", u";"), (u"＃", u"#"), (u"＄", u"$"), (u"％", u"%"), (u"＆", u"&"),
 (u"（", u"("), (u"）", u")"), (u"‐", u"-"), (u"＝", u"="), (u"＊", u"*"),
 (u"＋", u"+"), (u"－", u"-"), (u"／", u"/"), (u"＜", u"<"), (u"＞", u">"),
 (u"［", u"["), (u"￥", u"\\"), (u"］", u"]"), (u"＾", u"^"), (u"｛", u"{"),
 (u"｜", u"|"), (u"｝", u"}"), (u"～", u"~"),
)
FH_ASCII = HAC = lambda: ((fr, to) for m in (FH_ALPHA, FH_NUM, FH_PUNCTUATION) for fr, to in m)

HF_SPACE = HFS = ((u" ", u"　"),)
HF_NUM = HFN = lambda: ((h, z) for z, h in FH_NUM)
HF_ALPHA = HFA = lambda: ((h, z) for z, h in FH_ALPHA)
HF_PUNCTUATION = HFP = lambda: ((h, z) for z, h in FH_PUNCTUATION)
HF_ASCII = ZAC = lambda: ((h, z) for z, h in FH_ASCII())


def convertHalfAndFull(text, *maps, **ops):
    """ 全角/半角转换
    args:
        text: unicode string need to convert
        maps: conversion maps
        skip: skip out of character. In a tuple or string
        return: converted unicode string
    """

    if "skip" in ops:
        skip = ops["skip"]
        if isinstance(skip, str):
            skip = tuple(skip)

        def replace(text, fr, to):
            return text if fr in skip else text.replace(fr, to)
    else:
        def replace(text, fr, to):
            return text.replace(fr, to)

    for m in maps:
        if callable(m):
            m = m()
        elif isinstance(m, dict):
            m = m.items()
        for fr, to in m:
            text = replace(text, fr, to)
    return text


def difference(str1,str2):
    """
    求两个字符串的差集
    :param str1:
    :param str2:
    :return:
    """
    set1=set(str1)
    set2 = set(str2)
    return set1 - set2


def intersection(str1,str2):
    """
    求两个字符串的交集
    :param str1:
    :param str2:
    :return:
    """
    set1=set(str1)
    set2 = set(str2)
    return set1 & set2

def union(str1,str2):
    """
    求两个字符串的并集
    :param str1:
    :param str2:
    :return:
    """
    set1 = set(str1)
    set2 = set(str2)
    return set1 | set2



if __name__=="__main__":
    #test Q2B and B2Q
    for i in range(0x0020,0x007F):
        print(strQ2B(strB2Q(str(i))),strB2Q(str(i)))

    #test uniform
    ustring=u'中国 人名ａ高频Ａ'
    print(ustring)
    ustring=uniform(ustring)
    print(ustring)
    ret=string2List(ustring)
    print(ret)


    print (convert_hex_to_string(" \xce\xde\xd0\xa7\xb5\xc4\xb4\xb0\xbf\xda\xbe\xe4\xb1\xfa\xa1\xa3"))#('\xce\xde\xd0\xa7\xb5\xc4\xb4\xb0\xbf\xda\xbe\xe4\xb1\xfa\xa1\xa3'))

    print(convert_hex_to_string("%1 ������Ч�� Win32"))
    # print("�ܾ����ʡ�".encode("ascii").encode("utf-8"))
    print(converUnicodeToString("\u0af8\u0af8\u0af8"))

    print (convert_hex_to_string(" \xce\xde\xd0\xa7\xb5\xc4\xb4\xb0\xbf\xda\xbe\xe4\xb1\xfa\xa1\xa3"))#('\xce\xde\xd0\xa7\xb5\xc4\xb4\xb0\xbf\xda\xbe\xe4\xb1\xfa\xa1\xa3'))

    print (converUnicodeToString(" \x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\xed\x00\xe0\xfb\x0ew\xb0\x1d\xd7\x00\x00\x00\x00\x00\x00\x00\xd7\x00\xa0\xf9\x0ew\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x10\xf4s\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00y\x00\x00\x00\x00\x00\x80\xfb\x0ew\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\xec\xfe\x00\x00\x00\x000\x07\xec\xfe\x00\x00\xfc\xfe\x00\x00\xfc\xfe(\x00\xff\xfe\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x9b\x07m\xe8\xff\xff\x00\x00\x10\x00\x00"))#('\xce\xde\xd0\xa7\xb5\xc4\xb4\xb0\xbf\xda\xbe\xe4\xb1\xfa\xa1\xa3'))

    _str=arabicNumeral_to_chineseNumeral("805794852031746820.8906")
    print(_str)
    _num=chineseNumeral_to_arabicNumeral(_str)
    print(_num)

    _str=arabicNumeral_to_chineseNumeral_Money("031046820.7089")
    print(_str)
    _num=chineseNumeral_to_arabicNumeral(_str)
    print(_num)

    text = u"成田空港—【ＪＲ特急成田エクスプレス号・横浜行，2站】—東京—【ＪＲ新幹線はやぶさ号・新青森行,6站 】—新青森—【ＪＲ特急スーパー白鳥号・函館行，4站 】—函館"
    print (convertHalfAndFull(text, FH_ASCII, {u"【": u"[", u"】": u"]", u",": u"，", u".": u"。", u"?": u"？", u"!": u"！"}, spit= "，。？！“”"))


    str1 = "spam"
    str2 = "ham"
    result = intersection(str1,str2)
    print (u"交集：%s" % result)

    result = union(str1, str2)
    print (u"并集：%s" %  result)

    result =difference(str1, str2)
    print (u"差集1：%s" %  result)

    result =difference(str2, str1)
    print (u"差集2：%s" %  result)






