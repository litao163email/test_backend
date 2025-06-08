#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/14 21:08
# E-mail: litao163email@163.com
# @Author: litao
from datetime import timedelta

from .base import *

# 开发环境
print('开发环境')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'easytest1',
        'USER': 'litaom50.',
        'PASSWORD': 'Mm5201314.',
        'HOST': '106.52.179.105',
        'PORT': '3306'
    }
}

# jwt配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # token过期时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # 刷新token过期时间
}

# cors配置
# 运行所有域名跨域
CORS_ALLOW_ALL_ORIGINS = True

# celery配置


CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
