#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/4 20:52
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework import serializers

from .models import Bug, BugHandle


class BugSerializer(serializers.ModelSerializer):
    """bug序列化器"""

    interface_url = serializers.CharField(source='interface.url', read_only=True)

    class Meta:
        model = Bug
        fields = '__all__'


class BugHandleSerializer(serializers.ModelSerializer):
    """bug跟踪记录序列化器"""

    class Meta:
        model = BugHandle
        fields = '__all__'


