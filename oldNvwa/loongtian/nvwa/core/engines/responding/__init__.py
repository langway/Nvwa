#!/usr/bin/env python
# coding: utf-8
""" responding
应答
"""
import language
__author__ = 'Liuyl'
__all__ = {"respond"}


def respond(frag):
    return language.respond(frag)

if __name__ == '__main__':
    import doctest

    doctest.testmod()