#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'

import copy

import networkx as nx
from pprint import pprint as pt
import matplotlib.pyplot as plt

"""
多叉树
参考：python实现 多叉树 寻找最短路径 - 稀里糊涂林老冷 - 博客园
https://www.cnblogs.com/Lin-Yi/p/7780777.html

"""


class Node(object):
    """
    节点数据结构
    """

    def __init__(self, name=None, value=None):
        """
        初始化一个节点
        :param name:
        :param value:
        """
        self.name = name
        self.value = value  # 节点值
        self.children = []  # 子节点列表
        self.can_repeat=False # 子节点可以重复，例如：A-B,A-B

        self.count = 0
        self.root = Node("tree_root_name")
        self.is_node_exist = False
        self.search_result_parent = None
        self.search_result_children = []

    def add_child(self, node):
        '''
        增加节点
        '''
        if not self.can_repeat:
            if self.check_node_exists(self, node):
                # 判断增加的节点是否原先就存在
                print('Error: Node %s has already existed!' % node.name)
                print('*' * 30)

        self.children.append(node)
        # print('Add node:%s sucessfully!' % node.name)
        # print('*' * 30)


    def search(self, node):
        '''
        检索节点
        打印出其父节点的name以及其下一层所有子节点的name
        '''
        self.is_node_exist = False
        self.check_node_exists(
            self.root, node)
        if self.is_node_exist:
            # 若需要检索的节点存在，返回其父节点以及所有子节点
            print("%s's parent:" % node.name)
            pt(self.search_result_parent)
            print("%s's children:" % node.name)
            pt(self.search_result_children)
            print('*' * 30)
        else:
            # 若检索的节点不存在树中
            print("Error: Node %s doesn't exist!" % node.name)
            print('*' * 30)

    def delete(self, node):
        '''
        删除节点
        '''
        self.is_node_exist = False
        self.check_node_exists(
            self.root, node)
        if not self.is_node_exist:
            print("Error: Node %s doesn't exist!" % node.name)
            print('*' * 30)
        else:
            print('Delete node %s sucessfully!' % node.name)
            print('*' * 30)

    def modify(self, node, new_parent=None):
        '''
        修改节点的父节点
        '''
        self.is_node_exist = False
        self.check_node_exists(
            self.root, node)
        if not self.is_node_exist:
            # 判断需要修改的节点是否原先就存在
            print("Error: Node %s doesn't exist!" % node.name)
            print('*' * 30)
        else:
            if new_parent == None:
                # 如果new_parent为None，则默认其父节点为root节点
                self.is_node_exist = False
                self.check_node_exists(
                    self.root, node)
                root_children = self.root.children
                root_children.append(node)
                self.root.children = root_children
                print('Modify node:%s sucessfully!' % node.name)
                print('*' * 30)
            else:
                # 否则检查需要修改的节点的父节点是否存在
                self.is_node_exist = False
                self.check_node_exists(
                    self.root, new_parent)
                if self.is_node_exist:
                    # 若父节点存在
                    self.is_node_exist = False
                    self.check_node_exists(
                        self.root, node)
                    self._add(new_parent.name, node, self.root)
                    print('Modify node:%s sucessfully!' % node.name)
                    print('*' * 30)
                else:
                    # 若父节点不存在
                    print("Error: Parent node %s doesn't exist!" %
                          new_parent.name)
                    print('*' * 30)

    def show_tree(self):
        '''
        利用networkx转换成图结构，方便结合matplotlib将树画出来
        '''
        G = nx.Graph()
        self.to_graph_recursion(self.root, G)
        nx.draw(G, with_labels=True)
        plt.show()

    def to_graph_recursion(self, tree, G):
        '''
        将节点加入到图中
        '''
        G.add_node(tree.name)
        for child in tree.children:
            G.add_nodes_from([tree.name, child.name])
            G.add_edge(tree.name, child.name)
            self.to_graph_recursion(child, G)

    @staticmethod
    def check_node_exists(parent, child):
        '''
        parent:需要判断是否存在node节点的树
        child:需要判断的节点
        search:当检索到该节点时是否返回该节点的父节点和所有子节点
        if_del:当检索到该节点时是否删除该节点
        '''
        name = child.name
        if name == parent.name:
            return True

        for child in parent.children:
            if child.name == name: 
                return True
            
        return False

    def _add(self, parent, node, tree):
        '''
        增加节点时使用的递归函数
        '''
        if parent == tree.name:
            tree.children.append(node)
            return 1
        for child in tree.children:
            if child.name == parent:
                children_list = child.children
                children_list.append(node)
                child.children = children_list
                break
            else:
                self._add(parent, node, child)




# 初始化一颗测试二叉树
def init():
    '''
    初始化一颗测试二叉树:
            A
        B   C   D
      EFG       HIJ
    '''
    root = Node(value='A')
    B = Node(value='B')
    root.add_child(B)
    root.add_child(Node(value='C'))
    D = Node(value='D')
    root.add_child(D)
    B.add_child(Node(value='E'))
    B.add_child(Node(value='F'))
    B.add_child(Node(value='G'))
    D.add_child(Node(value='H'))
    D.add_child(Node(value='I'))
    D.add_child(Node(value='J'))
    return root


# 深度优先查找 返回从根节点到目标节点的路径
def deep_first_search(cur, val, path=None):
    if not path:
        path = []
    path.append(cur.value)  # 当前节点值添加路径列表
    if cur.value == val:  # 如果找到目标 返回路径列表
        return path

    if cur.children == []:  # 如果没有孩子列表 就 返回 no 回溯标记
        return 'no'

    for node in cur.children:  # 对孩子列表里的每个孩子 进行递归
        t_path = copy.deepcopy(path)  # 深拷贝当前路径列表
        res = deep_first_search(node, val, t_path)
        if res == 'no':  # 如果返回no，说明找到头 没找到  利用临时路径继续找下一个孩子节点
            continue
        else:
            return res  # 如果返回的不是no 说明 找到了路径

    return 'no'  # 如果所有孩子都没找到 则 回溯


# 获取最短路径 传入两个节点值，返回结果
# 多叉树的最短路径：
#
# 思想：
#     传入start 和 end 两个 目标值
#     1 找到从根节点到目标节点的路径
#     2 从所在路径，寻找最近的公共祖先节点，
#     3 对最近公共祖先根节点 拼接路径
def get_shortest_path(start, end):
    # 分别获取 从根节点 到start 和end 的路径列表，如果没有目标节点 就返回no
    path1 = deep_first_search(root, start, [])
    path2 = deep_first_search(root, end, [])
    if path1 == 'no' or path2 == 'no':
        return '无穷大', '无节点'
    # 对两个路径 从尾巴开始向头 找到最近的公共根节点，合并根节点
    len1, len2 = len(path1), len(path2)
    for i in range(len1 - 1, -1, -1):
        if path1[i] in path2:
            index = path2.index(path1[i])
            path2 = path2[index:]
            path1 = path1[-1:i:-1]
            break
    res = path1 + path2
    length = len(res)
    path = '->'.join(res)
    return '%s:%s' % (length, path)


# 主函数、程序入口
if __name__ == '__main__':
    root = init()
    res = get_shortest_path('F', 'I')
    print(res)


class MultiTree(Node):
    '''
    树的操作：
    增、删、改、查
    '''

def main():
    T = MultiTree('tree')
    A = Node('A')
    B = Node('B')
    C = Node('C')
    D = Node('D')
    E = Node('E')
    N = Node('N')
    G = Node('G')
    T.add_child(A)
    T.add_child(D)
    T.add_child(B, A)
    T.add_child(C, A)
    T.add_child(E, C)
    T.add_child(Node('F'))
    T.add_child(G)
    T.add_child(Node('H'), G)
    T.add_child(A)
    T.add_child(C)
    T.add_child(D)
    T.search(A)
    T.delete(A)
    # T.add(TreeNode('I'), N)
    T.add_child(A)
    T.modify(A, G)
    T.show_tree()


if __name__ == '__main__':
    main()
