#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/14 21:07
# E-mail: litao163email@163.com
# @Author: litao
import os

if os.environ.get('ENV') == 'production':
    # 生产环境
    from .pro import *
else:
    # 开发环境
    from .dev import *
