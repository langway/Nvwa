
from loongtian.util.tasks.runnable import run
from loongtian.nvwa.organs.brain import Brain
from loongtian.nvwa.tools.cidian import xml_cidian_to_sql_postgresql,jieba_cidian_to_sql_postgresql
def fillupData():
    """
    将数据填充到数据库中（todo 目前只完成metadata）
    :return:
    """
    from loongtian.nvwa.organs.centralManager import CentralManager
    CentralManager._cleanDB(wait_for_command=True)
    _brain = Brain()
    _brain.init()
    # run(_brain)

    xml_cidian_to_sql_postgresql.start()

    jieba_cidian_to_sql_postgresql.start()

if __name__ == '__main__':
    fillupData()
