#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/8 20:27
# E-mail: litao163email@163.com
# @Author: litao
import os
from django import setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_backend.settings')
setup()

from django_celery_beat.models import PeriodicTask, CrontabSchedule


# 拿到django-celery-beat的周期任务
p = PeriodicTask.objects.all()[1]
print(p.name)
print(p.task)
print(p.crontab)
print(p.kwargs)

# 通过代码添加一条记录
PeriodicTask.objects.create(
    name='通过代码添加的',
    task='testplans.tasks.run_crontab_test_plan',
    crontab=CrontabSchedule.objects.create(minute=35, hour=20),
    kwargs='{"pk":3, "env_id": 1, "tester": "litao"}'
)
