#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/14 21:08
# E-mail: litao163email@163.com
# @Author: litao
# 生产环境配置
from datetime import timedelta
from .base import *

print('生产环境')
DEBUG = False

ALLOWED_HOSTS = ['*']  # 允许的ip和域名
# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'easytest',
        'USER': 'root',
        'PASSWORD': 'pythonvip',
        'HOST': 'mariadb',   # 在docker的网桥中，容器名可以被解析为它的ip地址，这里写容器的名字就可以了
        'PORT': '3306'
    }
}

# jwt配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),  # token过期时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # 刷新token过期时间
}

# cors配置
# 运行所有域名跨域
CORS_ALLOW_ALL_ORIGINS = True

# celery配置

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/7'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/8'
# 配置beat的调度器类
