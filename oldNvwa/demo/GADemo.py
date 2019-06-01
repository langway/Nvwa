#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project:  demo
Title:    GADemo 
Author:   liuyl 
DateTime: 2014/8/25 14:35 
UpdateLog:
1、liuyl 2014/8/25 Create this File.

遗传算法示例
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import random
import __builtin__

class Gene(object):
    """
    基因基类,在遗传算法中用一个基因来表示群体中的一个个体
    由于基因有不同的表示方法,故抽象出一个基类
    """

    def __init__(self, encode=None, decode=None, fitness=None):
        """
        需要传入基因编码到基因显形的编码和解码算子
        需要传入适应度算子
        """
        self._fitness_operator = fitness
        self._encode_operator = encode
        self._decode_operator = decode
        self.code = []

    def set(self, index, code):
        """
        设置基因编码index位的值
        """
        self.code[index] = code

    def get_value(self):
        """
        获取基因编码的显形(解码)值
        """
        return self._decode_operator(self.code)

    def fitness(self):
        """
        计算基因的适应度
        """
        return self._fitness_operator(self._decode_operator(self.code))

    def print_self(self):
        print("%s  %s" % (self.code, self._decode_operator(self.code)))


class BitGene(Gene):
    """
    二进制基因
    基因的交叉和突变以二进制位为操作对象
    """

    def __init__(self, option):
        """
        需要传入bit_count以设置二进制位数
        """
        super(BitGene, self).__init__(option['encode'], option['decode'], option['fitness'])
        self.code = [random.randint(0, 1) for _ in range(option['bit_count'])]


class FloatGene(Gene):
    """
    浮点值基因
    未使用
    """

    def __init__(self, option):
        super(FloatGene, self).__init__(option['encode'], option['decode'], option['fitness'])
        # self.code = [random.random() for _ in rangeList(option['gene_count'])]


class GeneFactory(object):
    """
    基因工厂,提供generate接口供种群产生新的基因(个体)
    """

    def __init__(self, gene_type, gene_option):
        self._gene_type = gene_type
        self._gene_option = gene_option

    def generate(self):
        return self._gene_type(self._gene_option)


def crossover_bit_fun(gene1, gene2):
    """
    默认二进制基因交叉算子
    获取一个随机点位,两个基因该点位后面的各个二进制位交换
    :param gene1:
    :param gene2:
    :return:
    """
    spot = random.randint(0, len(gene1.code) - 1)
    for i in range(len(gene1.code) - 1, spot - 1, -1):
        temp = gene1.code[i]
        gene1.set(i, gene2.code[i])
        gene2.set(i, temp)


def mutate_bit_fun(gene):
    """
    默认二进制基因突变算子
    获取一个随机点位,该基因编码的该位的值取反
    :param gene:
    :return:
    """
    i = random.randint(0, len(gene.code) - 1)
    gene.code[i] = 1 - gene.code[i]


class Group(object):
    def __init__(self, group_size, gene_factory, fitness, mutate_rate=100, crossover=crossover_bit_fun,
                 mutate=mutate_bit_fun):
        """
        群体,控制种群的进化
        :param group_size: 种群大小(种群中基因个体的数量)
        :param gene_factory: 基因工厂
        :param fitness: 种群适应度算子
        :param mutate_rate: 突变率*1000,默认10%突变率
        :param crossover: 指定交叉算子
        :param mutate: 指定突变算子
        :return:
        """
        self._group_size = group_size
        self._gene_factory = gene_factory
        self._member = [gene_factory.generate() for _ in range(group_size)]
        self._crossover_operator = crossover
        self._mutate_operator = mutate
        self._mutate_rate = mutate_rate
        self._fitness_operator = fitness

    def evolve(self):
        # 计算每个个体在种群的生存环境中的适应度
        print("适应度")
        _fitness = self.do_fitness()
        print(_fitness)
        # 根据适应度 轮盘确定出每个个体的繁衍机会
        print("存活")
        _survive = self.do_select(_fitness)
        random.shuffle(_survive)
        for gene in _survive:
            gene.print_self()
        # 两两配对进行基因交叉
        print("交叉")
        self.do_crossover(_survive)
        for gene in _survive:
            gene.print_self()
        # 每个新基因发生小概率突变
        print("突变")
        self.do_mutate(_survive)
        for gene in _survive:
            gene.print_self()
        # 形成新的种群
        self._member = _survive

    def do_fitness(self):
        """
        种群适应度算子规定了种群生存环境,这里将个体适应度的值根据生存环境的规定映射成一个新的适应度值
        :return:
        """
        return self._fitness_operator(self._member)

    def do_mutate(self, survive):
        for gene in survive:
            if random.randint(1, 1000) < self._mutate_rate:
                self._mutate_operator(gene)

    def do_crossover(self, survive):
        for i in xrange(1, len(survive), 2):
            self._crossover_operator(survive[i - 1], survive[i])

    def do_select(self, fitness):
        """
        模拟自然选择
        通过轮盘的方式确定每个个体的繁衍机会
        :param fitness:
        :return:
        """
        # 将适应度映射成个体繁衍机率(百分比)
        fitness_percent = map(lambda x: int(round(x * 100.0 / reduce(lambda y, z: y + z, fitness))), fitness)
        # 百分比补偿(四舍五入导致整体几率总和不足100时,将缺少的几率补足到最后一个个体)
        fitness_percent[-1] += 100 - sum(fitness_percent)
        # 生成每个个体的繁衍概率的区间
        _threshold, _sum = [], 1
        for fit in fitness_percent:
            if fit != 0:
                _threshold.append([_sum, _sum + fit - 1])
                _sum += fit
            else:
                _threshold.append([-1, -1])
        # 轮盘选取获得繁衍机会的个体,将其加入到"存活"列表中
        _survive = []
        _random = [random.randint(1, 100) for _ in range(len(fitness_percent))]
        for r in _random:
            for (index, threshold) in enumerate(_threshold):
                if threshold[0] <= r <= threshold[1]:
                    child = self._gene_factory.generate()
                    child.code = self._member[index].code[:]
                    _survive.append(child)
        return _survive

    def print_self(self):
        for gene in self._member:
            gene.print_self()


def test_2_args():
    """
    用于演示推导出二元多项式的最大值
    :return:
    """
    # 目标函数 x^2+y^2
    target_fun = lambda value: value[0] ** 2 + value[1] ** 2

    # 5 --> [1,0,1]
    encode_sub_fun = lambda value: map(lambda x: int(x), ("00000" + bin(value)[2:])[-5:])
    print("encode_sub_fun(5):")
    print(encode_sub_fun(5))

    # [5,3] --> [1,0,1,0,1,1]
    encode_fun = lambda value: encode_sub_fun(value[0]) + encode_sub_fun(value[1])
    print("encode_fun([5,3]):")
    print(encode_fun([5, 3]))

    # [1,0,1,0,1,1] --> [5,3]
    decode_fun = lambda code: [int('0b' + reduce(lambda x, y: str(x) + str(y), code[0:len(code) / 2]), 2),
                               int('0b' + reduce(lambda x, y: str(x) + str(y), code[len(code) / 2:]), 2)]
    print("decode_fun([1,0,1,0,1,1]):")
    print(decode_fun([1, 0, 1, 0, 1, 1]))
    fitness_fun = target_fun

    # 群体适应度算子
    def group_fitness_fun(genes):
        """
        为了使群体中最不适应的个体被快速淘汰,将群体中所有个体的适应度都减去最不适应个体的适应度
        :param genes:
        :return:
        """
        _fitness = [gene.fitness() for gene in genes]
        # 这里加了1,是的当群体中所有基因都相同时,适应度不会被全部置为0
        _fitness = [fit - min(_fitness) + 1 for fit in _fitness]
        return _fitness

    gene_factory = GeneFactory(BitGene,
                               {"bit_count": 10,
                                "encode": encode_fun,
                                "decode": decode_fun,
                                "fitness": fitness_fun})

    group = Group(10, gene_factory, fitness=group_fitness_fun)
    print("初始种群")
    group.print_self()

    for _ in range(30):
        group.evolve()


def test_1_args():
    """
    用于演示推导出一元多项式的最大值
    :return:
    """
    # 目标函数 -x^2+78x
    target_fun = lambda value: value * 78 - value ** 2
    # 基因编码算子 5 --> [1,0,1]
    encode_fun = lambda value: map(lambda x: int(x), ("000000" + bin(value)[2:])[-6:])
    print("encode_fun(5):")
    print(encode_fun(5))

    # 基因解码算子 [1,0,1] --> [5]
    decode_fun = lambda code: int('0b' + reduce(lambda x, y: str(x) + str(y), code), 2)
    print("decode_fun([1,0,1]):")
    print(decode_fun([1, 0, 1]))

    # 个体适应度算子用目标函数代替
    fitness_fun = target_fun

    # 群体适应度算子
    def group_fitness_fun(genes):
        """
        为了使群体中最不适应的个体被快速淘汰,将群体中所有个体的适应度都减去最不适应个体的适应度
        :param genes:
        :return:
        """
        _fitness = [gene.fitness() for gene in genes]
        # 这里加了1,是的当群体中所有基因都相同时,适应度不会被全部置为0
        _fitness = [fit - min(_fitness) + 1 for fit in _fitness]
        return _fitness

    # 定义基因工厂
    gene_factory = GeneFactory(BitGene,
                               {"bit_count": 6,
                                "encode": encode_fun,
                                "decode": decode_fun,
                                "fitness": fitness_fun})

    # 定义群体
    group = Group(10, gene_factory, fitness=group_fitness_fun)
    print("初始种群")
    group.print_self()

    # 开始进化
    for _ in range(100):
        group.evolve()


if __name__ == '__main__':
    test_1_args()