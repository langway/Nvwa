#/usr/bin/python
# coding: utf-8

"""
数据库操作帮助类
"""
__author__ = 'leon'
import pymongo

connection=pymongo.MongoClient()#.Connection('10.32.38.50',27017)

#选择myblog库
db=connection.myblog

# 使用users集合
collection=db.users

#添加命令如下：

# 添加单条数据到集合中
user = {"name":"xiaoxu","age":"23"}
collection.insert(user)     #添加数据
collection.save(user)      #添加数据

#同时添加多条数据到集合中
users=[{"name":"xiaoxu","age":"23"},{"name":"xiaoli","age":"20"}]
collection.insert(users)    #添加数据
collection.save(users)      #添加数据

#删除命令如下：
collection.remove({"name":"xiaoxu"})


#修改命令如下：
collection.update({"name":"xiaoli"})


#查询命令如下：

#查询单条记录
print (collection.find_one())

#查询所有记录
for data in collection.find():
    print (data)

#查询此集合中数据条数
print (collection.count())

#简单参数查询
for data in collection.find({"name":"1"}):
    print (data)

#使用find_one获取一条记录
print (collection.find_one({"name":"1"}))