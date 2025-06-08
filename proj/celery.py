#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/6 20:11
# E-mail: litao163email@163.com
# @Author: litao
from celery import Celery

app = Celery('proj',
             broker='redis://127.0.0.1:6379/7',
             backend='redis://127.0.0.1:6379/8',
             include=['proj.tasks']
             )

# 做些配置
app.conf.update(
    result_expires=10000,    # 结果过期时间
)
