#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新建python文件
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'


def find_structure_variable2(queue, structure, **kwd):
    """
    指定一个严格结构和2个变量,查找符合此结构且满足变量的各自结构限定的两个变量间的所有组合
    :param queue: 关系表
    :param structure: 严格的结构
    :param kwd: 两个变量的占位符及限定结构
    :return:
    """
    # 评估变量,按最小化记录提取的策略进行排序
    vars = evaluate_variable(kwd)
    # 仅有2个变量,则第一个为能够最小化记录提取的变量,找出符合该变量的限定结构的所有记录的key
    first_values = select_whole_structure_restrict(queue, vars[0]['key'], vars[0]['value'])
    # 根据上面求得的第一个变量的所有可能值按照结构推导出所有可能的两个变量的值的对应关系
    not_finish_links = deduce_whole_structure_restrict(queue, structure, vars[0]['key'], first_values)
    # 根据另一变量的限定结构最后筛选出最终结果
    second_values = filter_whole_structure_restrict(
        queue, set([link[1] for link in not_finish_links]), vars[1]['key'], vars[1]['value'])
    finish_links = filter(lambda link: link[1] in second_values, not_finish_links)
    return [var['key'] for var in vars], finish_links


def deduce_whole_structure_restrict(queue, structure, placeholder, values):
    """

    :param queue:
    :param structure:
    :param origin:
    :return:
    """
    result_links = []

    first_structure_records = [{'key': str(structure.index(item)), 'value': item}
                               for item in structure if item['end'] == placeholder or item['start'] == placeholder]
    start_restrict = first_structure_records[0]['value']['end'] == placeholder
    for value in values:
        if not start_restrict:
            links = deduce_normal_order(queue, structure, placeholder, value)
        else:
            links = deduce_reverse_order(queue, structure, placeholder, value)
        result_links.extend([[value, link] for link in links])
    return result_links


def deduce_normal_order(queue, structure, placeholder, value):
    first_structure_record = [{'key': str(structure.index(item)), 'value': item}
                              for item in structure if item['start'] == placeholder][0]
    records = select_whole_start_end_restrict(queue, value, first_structure_record['value']['end'])
    keys = [x['key'] for x in records]
    while True:
        next_placeholder = str(structure.index(first_structure_record['value']))
        next_structure_records = [{'key': str(structure.index(item)), 'value': item}
                                  for item in structure if item['start'] == next_placeholder]
        try:
            next_end_value = int(next_structure_records[0]['value']['end'])
        except:
            values = [record['value']['end'] for record in select_whole_start_restrict(queue, keys)]
            return values
        next_keys = []
        for key in keys:
            next_keys.extend(select_whole_start_end_restrict(queue, key, next_end_value))
        keys = next_keys


def deduce_reverse_order(queue, structure, placeholder, value):
    records = select_whole_end_restrict(queue, [value])
    first_structure_record = [{'key': str(structure.index(item)), 'value': item}
                              for item in structure if item['end'] == placeholder][0]

    keys = [x['value']['start'] for x in records]
    index = int(first_structure_record['value']['start'])
    while True:
        structure_record = structure[index]
        records = select_whole_keys_restrict(queue, keys)
        keys = [x['value']['start'] for x in records if x['value']['end'] == structure_record['end']]
        try:
            index = int(structure_record['start'])
        except:
            break
    return keys


def evaluate_variable(kwd):
    """
    评估变量及其限定条件,按能够最大化筛除无关记忆的顺序排列
    暂时以条件组合的记录条数为评判依据
    :param kwd: 变量及其限定条件
    :return: 一个列表 列表项为{'key':变量名,'value':限定条件}
    """
    li = [{'key': key, 'value': kwd[key]} for key in kwd.keys()]
    li.sort(key=lambda x: len(x['value']), reverse=True)
    return li


def select_whole_structure_restrict(queue, placeholder, restrict):
    """
    完全限定查找,指定占位符,及仅包含有一个该占位符的结构,查找所有满足该结构的记录id
    待优化:仅从占位符处按顺序树形递归查找,后面需要优化,避免提取出过多记录
    :param queue: 关系表
    :param placeholder: 占位符
    :param restrict: 限定结构
    :return: 所有满足限定结构的记录id
    """
    origin = [{'key': str(restrict.index(item)), 'value': item}
              for item in restrict if item['start'] == placeholder or item['end'] == placeholder][0]
    objects = []
    if origin['value']['start'] == placeholder:
        objects = select_whole_end_restrict(queue, [origin['value']['end']])
    if origin['value']['end'] == placeholder:
        objects = select_whole_start_restrict(queue, [origin['value']['start']])
    filters = [obj['key'] for obj in objects]
    result = filter_whole_structure_restrict(queue, filters, origin['key'], restrict)
    return result


def filter_whole_structure_restrict(queue, filters, placeholder, restrict):
    """
    过滤掉与结构限定不符的记录,树形递归调用
    暂时只考虑了"与"的情况
    :param queue: 关系表
    :param filters: 上一级递归调用传入的用于替换占位符的记录id
    :param placeholder: 占位符
    :param restrict: 限定结构
    :return:
    """
    next_restrict_records = [{'key': str(restrict.index(item)), 'value': item}
                             for item in restrict if item['start'] == placeholder or item['end'] == placeholder]

    result_filters = set(filters)
    for restrict_record in next_restrict_records:
        next_filters = []
        start_restrict = restrict_record['value']['end'] == placeholder
        for filter_key in filters:
            if start_restrict:
                records = select_whole_start_end_restrict(
                    queue, restrict_record['value']['start'], filter_key, inherit=True)
            else:
                records = select_whole_start_end_restrict(
                    queue, filter_key, restrict_record['value']['end'], inherit=True)
            for record in records:
                next_filters.append([filter_key, record['key']])
        sub_filters = filter_whole_structure_restrict(
            queue, [x[1] for x in next_filters], restrict_record['key'], restrict)
        result_filters.union(set([x[0] for x in next_filters if x[1] in sub_filters]))
    return result_filters


def deduce_inherit(queue, child, parent):
    if parent == 0:
        return True
    records = select_whole_keys_restrict(queue, [child])
    while len(records) == 1 and records[0]['value']['end'] != 0:
        if records[0]['value']['end'] == parent:
            return True
        records = select_whole_keys_restrict(queue, [records[0]['value']['end']])
    return False


def select_whole_start_end_restrict(queue, start, end, inherit=False):
    """
    根据start和end值查找所有满足条件的记录
    :param queue: 关系表
    :param start: 给定的start值
    :param end: 给定的end值
    :param inherit: 是否考虑继承,如果查询到的结果的key和start相同,则以该start值为end值进行递归查找
    :return:
    """
    records = filter(lambda item: item['value'] == {'start': start, 'end': end}, queue)
    if inherit:
        if len(records) == 0:
            start_records = select_whole_keys_restrict(queue, [start])
            if len(start_records) == 1:
                if deduce_inherit(queue, start_records[0]['value']['end'], end):
                    return start_records
    return records


def select_whole_keys_restrict(queue, keys):
    return filter(lambda record: record['key'] in set(keys), queue)


def select_whole_start_restrict(queue, starts):
    """
    查询所有start值为给定值记录
    :param queue: 关系表
    :param start: 给定的start值
    :return: 所有start值为给定值记录
    """
    return filter(lambda item: item['value']['start'] in starts, queue)


def select_whole_end_restrict(queue, ends, inherit=False):
    """
    查询所有end值为给定值记录
    :param queue: 关系表
    :param end: 给定的start值
    :param inherit: 是否考虑继承,如果查询到的结果的key和start相同,则以该start值为end值进行递归查找
    :return: 所有end值为给定值记录(inherit=True时包括所有与end值表示的object有间接继承关系的记录)
    """
    records = filter(lambda item: item['value']['end'] in ends, queue)
    if inherit:
        for record in records:
            if record['key'] == record['value']['start']:
                records.extend(select_whole_end_restrict(queue, [record['value']['start']]))
    return records

def select_whole_link(queue, starts, max_deep_count=10):
    pass

if __name__ == '__main__':
    import doctest

    doctest.testmod()
