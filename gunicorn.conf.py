#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/18 21:34
# E-mail: litao163email@163.com
# @Author: litao
import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1  # 配置worker进程为cpu核心的两倍+1
bind = '0.0.0.0:8000'
reload = False  # 调试模式设置为True，每当代码更新时，会自动重启
pidfile = '/tmp/gunicorn.pid'
accesslog = '/app/logs/gunicorn_access.log'
errorlog = '/app/logs/gunicorn_error.log'
