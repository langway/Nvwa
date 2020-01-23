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


def jiebaCiDianToSql():
    """

    """
    import sys

    python_path = sys.executable
    path_r =  python_path[ 0 : python_path.rfind( os.sep ) ] + "\\Lib\\site-packages\\jieba\\dict.txt"

    lines = fileHelper.readLines(path_r)

    path_w = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'sql_r_jieba.txt')
    file_w = open(path_w, 'w',encoding='utf8')
    path_w_n = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'sql_m_jieba.txt')
    file_w_n = open(path_w_n, 'w',encoding='utf8')

    for line in lines:
        splits=line.split(" ")
        mvalue=splits[0].strip()
        u_id = str(uuid.uuid1()).replace("-", "")
        freq=int(splits[1].strip())

        insertOrUpdateMetaData(mvalue, u_id, freq, file_w, file_w_n)

        conn.commit()
    cur.close()
    conn.close()


from loongtian.nvwa.models.enum import ObjType

def insertOrUpdateMetaData(mvalue, u_id, freq, file_w, file_w_n,
                           insert_valuesHasStopMark=True,
                           insert_valuesHasNumber=True):
    # if pronunciation.find("'")>=0:
    #     pronunciation=pronunciation.replace("'","\\'")
    #     # remark=remark.replace("'","\'")

    if hasStopMark(mvalue):
        valuesHasStopMark.append(mvalue)
        if not insert_valuesHasStopMark:
            return
    if hasNumber(mvalue):
        valuesHasNumber.append(mvalue)
        if not insert_valuesHasNumber:
            return

    cur.execute("select * from %s where mvalue=\'%s\'" % (tbl_metadata, mvalue))
    rows = cur.fetchall()
    if rows.__len__() == 0:
        # sql = """INSERT INTO %s (id, type, mvalue, pronunciation,remark, weight) VALUES ('%s', 100, '%s', '%s','%s', 0.02);\n"""\
        #           %(tbl_metadata,u_id, mvalue,pronunciation, remark)
        sql = """INSERT INTO {0} (id, type, mvalue, remark, weight,recognized) VALUES ('{1}',{2} , '{3}', '{4}',{5},{6});\n""" \
              .format(tbl_metadata, u_id,ObjType.WORD, mvalue, "", freq,True)
        cur.execute(sql)
        file_w.write(sql)
        print(sql)
    else:

        if freq:
            # sql = """UPDATE %s SET remark='%s',pronunciation='%s' WHERE id='%s';\n"""%(tbl_metadata,remark,pronunciation, rows[0][0])
            sql = """UPDATE {0} SET weight={1} WHERE id='{2}';\n""" .format (tbl_metadata, freq, rows[0][0])
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
    jiebaCiDianToSql()
    print(valuesHasStopMark)
    print(valuesHasNumber)

    from loongtian.util.helper import fileHelper

    path_ = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'valuesHasStopMark_jieba.txt')
    fileHelper.writeLines(path_, valuesHasStopMark)

    path_ = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'valuesHasNumber_jieba.txt')
    fileHelper.writeLines(path_, valuesHasNumber)

    print('------------test_jieba_to_sql------------')

if __name__ == '__main__':
    start()
