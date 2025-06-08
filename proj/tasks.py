#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/6 20:11
# E-mail: litao163email@163.com
# @Author: litao

from .celery import app

@app.task
def add(x, y):
    print(x+y)
    return x + y

@app.task
def mul(x, y):
    return x * y
