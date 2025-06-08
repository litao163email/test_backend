#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/23 20:35
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework import serializers

from .models import Project, Interface, TestEnv
from testplans.models import TestStep


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'leader', 'info', 'bugs', 'create_time']   # fields只会包含定义的字段


# obj.a, obj.b obj.c
# obj -> {'a': obj.a, 'b': obj.b, 'c': obj.c}
# obj.a是方法 obj.info
# {'a': obj.a()}  # 如果说某个属性是方法，或可调用对象，那么就执行获取它的返回值
class NestTestStepSerializer(serializers.ModelSerializer):
    """嵌套测试步骤序列化器"""
    class Meta:
        model = TestStep
        fields = ['id', 'title']


class InterfaceSerializer(serializers.ModelSerializer):
    steps = NestTestStepSerializer(source='teststep_set', many=True, read_only=True)

    class Meta:
        model = Interface
        fields ='__all__'


class EnvironmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestEnv
        fields = '__all__'
