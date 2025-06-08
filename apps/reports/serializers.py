#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/1 21:25
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework import serializers

from .models import Record, Report


class RecordSerializer(serializers.ModelSerializer):
    env_name = serializers.StringRelatedField(source='test_env')
    plan_name = serializers.StringRelatedField(source='plan')

    class Meta:
        model = Record
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
