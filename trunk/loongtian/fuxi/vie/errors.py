#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Leon'
"""
错误处理
"""
from flask import render_template
from loongtian.fuxi import main


@main.app_errorhandler(404)
def page_not_found(e):
    """
    404错误处理
    :param e:
    :return:
    """
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
