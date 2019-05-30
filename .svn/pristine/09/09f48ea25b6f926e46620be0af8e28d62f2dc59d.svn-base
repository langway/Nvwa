#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
import numpy
# import Levenshtein

# 比较常用的几种计算Levenshtein distance的函数，
# 其中函数(1)为调用数学工具包Numpy， 函数(2)和(1)算法类似，都是采用DP, (3)来自wiki(4)是直接调用python的第三方库Levenshtein

def levenshtein1(source, target):
    if len(source) < len(target):
        return levenshtein1(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = numpy.array(tuple(source))
    target = numpy.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = numpy.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = numpy.minimum(
                current_row[1:],
                numpy.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = numpy.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]


def levenshtein2(s1, s2):
    if len(s1) < len(s2):
        return levenshtein2(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def levenshtein3(s, t):
        """ From Wikipedia article; Iterative with two matrix rows. """
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(t)]


# @fn_timer
# def calllevenshtein4(s,t,n):
#     for i in range(n):
#         Levenshtein.distance(s,t)

import numpy as np


"""
s1:
    String A = m, String B = n
s2:
"""
# initial
# A, B string
strA = "kitten"#"bcdabab"
strB = "sitting" #"cbacbaaba"
m = len(strA)
n = len(strB)

matrix = np.array([[0 for i in range(m + 1)] for i in range(m + 1)])
ans = [float('Inf') for i in range(m + 1)]

pos = 0
MAX = 0

while MAX <= m - pos:
    posA = pos
    LCS = 1
    lowerB = 0
    while posA < m and lowerB < n:
        upperB = n - 1
        posB = lowerB
        while posB <= upperB and strA[posA] != strB[posB]:
            posB = posB + 1
        if posB <= upperB:
            lowerB = posB
        else:
            break
        matrix[LCS - 1, posA] = lowerB + 1
        if lowerB == -1:
            LCS = LCS - 1
        MAX = max(MAX, LCS)
        if matrix[LCS - 1, posA] < ans[posA - pos]:
            ans[posA - pos] = matrix[LCS - 1, posA]
        LCS = LCS + 1
        posA = posA + 1
    pos = pos + 1


print(matrix)
print(ans)


if __name__ == "__main__":
    n = 50000
    a = 'abddcdefdgbd22svb'
    b = 'bcdefg34rdyvdfsd'
    from loongtian.util import fn_timer
    @fn_timer
    def calllevenshtein1(s,t,n):
        for i in range(n):
            levenshtein3(s,t)

    @fn_timer
    def calllevenshtein2(s,t,n):
        for i in range(n):
            levenshtein3(s,t)

    @fn_timer
    def calllevenshtein3(s,t,n):
        for i in range(n):
            levenshtein3(s,t)

    # calllevenshtein1(a, b, n)
    # calllevenshtein2(a, b, n)
    # calllevenshtein3(a, b, n)
    # calllevenshtein4(a, b, n)
