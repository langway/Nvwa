#!/usr/bin/env python
# coding: utf-8
import os
import uuid
from bs4 import BeautifulSoup
import psycopg2
from loongtian.util.helper import stringHelper,fileHelper

conn = psycopg2.connect(database="nvwa", user="postgres", password="123456qaz", host="localhost", port="5432")
cur = conn.cursor()
tbl_metadata = "\"tbl_metaData\""
valuesHasStopMark = []
valuesHasNumber = []


def xmlCiDianToSql():
    """

    """
    path_r = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'newDict.xml')

    lines = fileHelper.read(path_r)

    path_w = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'sql_r_cidian.txt')
    file_w = open(path_w, 'w',encoding='utf8')
    path_w_n = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'sql_m_cidian.txt')
    file_w_n = open(path_w_n, 'w',encoding='utf8')
    detail_url = BeautifulSoup(lines,features="lxml").findAll('d')  # 整个单字，包括字、词
    for du in detail_url:
        tag_a = du.find('a')  # 字
        tag_z = du.find('z')  # 繁体
        tag_y = du.find('y')  # 发音

        remark = getExplanation(du)
        pronunciation = ""
        if tag_y:
            pronunciation = tag_y.text

        # 单字部分
        if not tag_a.find('p'):
            mvalue = tag_a.text
            u_id = str(uuid.uuid1()).replace("-", "")
            insertOrUpdateMetaData(mvalue, u_id, pronunciation, remark, file_w, file_w_n)

        # 繁体字部分
        if tag_z and not tag_z.find('p'):
            mvalue = tag_z.text
            u_id = str(uuid.uuid1()).replace("-", "")
            insertOrUpdateMetaData(mvalue, u_id, pronunciation, remark, file_w, file_w_n)

        #
        tag_j = du.findAll('j')
        for tj in tag_j:
            tag_b = tj.find('b')
            if not tag_b:
                continue

            u_id = str(uuid.uuid1()).replace("-", "")
            mvalue = tag_b.text
            # if mvalue=="阿鼻":
            #     a=0
            tag_z = tj.find('z')  # 繁体
            tag_y = tj.find('y')  # 发音
            remark = getExplanation(tj)
            if tag_y:
                pronunciation = tag_y.text

            insertOrUpdateMetaData(mvalue, u_id, pronunciation, remark, file_w, file_w_n)

        conn.commit()
    cur.close()
    conn.close()


def getExplanation(tag):
    tag_x_list = tag.findAll('x')  # 含义 可能有多个
    remark = ""
    if tag_x_list:
        for tag_x in tag_x_list:
            if not tag_x.parent == tag:
                continue
            remark += tag_x.__str__()
    return remark


from loongtian.nvwa.organs.character import Character
from loongtian.nvwa.models.enum import ObjType

def insertOrUpdateMetaData(mvalue, u_id, pronunciation, remark, file_w, file_w_n):
    # if pronunciation.find("'")>=0:
    #     pronunciation=pronunciation.replace("'","\\'")
    #     # remark=remark.replace("'","\'")

    if hasStopMark(mvalue):
        valuesHasStopMark.append(mvalue)
    elif hasNumber(mvalue):
        valuesHasNumber.append(mvalue)
    else:
        cur.execute("select * from %s where mvalue=\'%s\'" % (tbl_metadata, mvalue))
        rows = cur.fetchall()
        if rows.__len__() == 0:
            # sql = """INSERT INTO %s (id, type, mvalue, pronunciation,remark, weight) VALUES ('%s', 100, '%s', '%s','%s', 0.02);\n"""\
            #           %(tbl_metadata,u_id, mvalue,pronunciation, remark)
            sql = """INSERT INTO {0} (id, type, mvalue, remark, weight,recognized) VALUES ('{1}',{2} , '{3}', '{4}',{5},{6});\n""" \
                  .format(tbl_metadata, u_id,ObjType.WORD, mvalue, remark, Character.Original_Link_Weight,True)
            cur.execute(sql)
            file_w.write(sql)
            print(sql)
        else:
            if rows[0][11] and remark:
                if rows[0][11].find(remark):
                    return
                remark = rows[0][11] + '\n' + remark
            if remark:
                # sql = """UPDATE %s SET remark='%s',pronunciation='%s' WHERE id='%s';\n"""%(tbl_metadata,remark,pronunciation, rows[0][0])
                sql = """UPDATE %s SET remark='%s' WHERE id='%s';\n""" % (tbl_metadata, remark, rows[0][0])
                cur.execute(sql)
                file_w_n.write(sql)
                print(sql)


def hasStopMark(value):
    mvalue = value
    if mvalue == u'一…一…':
        a = 0
    for c in mvalue:
        if c in stringHelper.StopMarks:
            return True
    return False


def hasNumber(mvalue):
    if stringHelper.contain_num(mvalue):
        return True
    return False


def start():
    xmlCiDianToSql()
    print(valuesHasStopMark)
    print(valuesHasNumber)

    from loongtian.util.helper import fileHelper

    path_ = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'valuesHasStopMark_cidian.txt')
    fileHelper.writeLines(path_, valuesHasStopMark)

    path_ = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'valuesHasNumber_cidian.txt')
    fileHelper.writeLines(path_, valuesHasNumber)

    print('------------test_chidian_xml_to_sql------------')


if __name__ == '__main__':
    start()
