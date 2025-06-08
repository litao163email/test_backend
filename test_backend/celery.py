#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/6 20:38
# E-mail: litao163email@163.com
# @Author: litao
import os
from celery import Celery

# 设置django的配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_backend.settings')

app = Celery('test_backend')

# 设置celery的配置来源
# 从django项目的配置文件中获取celery的配置
# from django.conf import settings
app.config_from_object('django.conf:settings', namespace='CELERY')
# 配置文件中以CELERY开头的配置会被读取

# 为了应用可以复用
# 调用自动发现任务的方法，注册所有已经在应用中定义的任务
app.autodiscover_tasks()
