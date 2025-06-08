#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/4 20:21
# E-mail: litao163email@163.com
# @Author: litao
from django_filters import rest_framework as filters

from .models import Record


class RecordFilterSet(filters.FilterSet):
    """测试记录过滤器"""
    project = filters.NumberFilter(field_name='plan__project')
    env = filters.NumberFilter(field_name='test_env')

    class Meta:
        model = Record
        fields = ['plan', 'project', 'env']
