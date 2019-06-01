#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    const_values 
Author:   fengyh 
DateTime: 2014/9/4 10:45 
UpdateLog:
1、fengyh 2014/9/4 Create this File.


"""

# 常量类实现常量的功能
#
# 该类定义了一个方法__setattr()__，和一个异常ConstError, ConstError类继承
# 自类TypeError. 通过调用类自带的字典__dict__, 判断定义的常量是否包含在字典
# 中。如果字典中包含此变量，将抛出异常，否则，给新创建的常量赋值。
# 最后两行代码的作用是把const类注册到sys.modules这个全局字典中。
class ConstValues:
    class ConstError(TypeError):pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const (%s)" %name
        self.__dict__[name]=value

# fengyh 20150114 暂定初始阈值为50. 总阈值范围为0-100.
ConstValues.threshold_initial_value = 50.0


"""
问题定义：
系统已知“牛组件腿”“桌子组件腿”，输入“羊有腿”时满足什么条件可以抽取为“羊组件腿”？

规则：
1、规则r1：系统已知“牛父对象动物”“羊父对象动物”“牛组件XXX”。类似“XXX父对象动物”且“XXX组件XXX”的出现次数k1。占权重w1。
2、规则r2：系统已知“XXX组件腿”出现次数k2。占权重w2。
3、类比值计算：V = k1*w1+k2*w2
4、V大于类比门槛值T则为类比成功，符合条件。
说明：
1、w1和w2权重总和为1，可设置各规则占比，程序可设置。
2、K1和k2可设置。
3、门槛值T可设置。
"""

# 类比规则参数k1，w1，k2，w2
ConstValues.analogy_rule_weight_w1 = 0.5
ConstValues.analogy_rule_weight_w2 = 0.5
ConstValues.analogy_rule_success_threshold = 2

