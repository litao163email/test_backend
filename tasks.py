#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/4 22:00
# E-mail: litao163email@163.com
# @Author: litao
import time
from celery import Celery
from celery.schedules import crontab
# 实例化应用
# redis url 格式 redis://:password@hostname:port/db_number
app = Celery('tasks',
             broker='redis://127.0.0.1:6379/7',
             # backend='redis://:pythonvip@47.112.233.130:5100/8'
             )
# 设置时区
app.conf.timezone = 'Asia/Shanghai'


#添加定时任务
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每10秒调用一次
    sender.add_periodic_task(10, add.s(1, 2), name='add every 10')

    # 具体某个时间
    sender.add_periodic_task(crontab(hour=21, minute=53, day_of_week=5), hello.s(), name='周五21:53分执行')


# 定义任务
@app.task
def add(x, y):
    # time.sleep(10)
    print(f'x+y={x+y}')
    # return x+y

@app.task
def hello():
    print('Hello world!')

