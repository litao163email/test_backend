#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:52
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework import serializers

from .models import TestStep, UploadFile, TestScene, SceneData, TestPlan, CrontabTask
from projects.serializers import InterfaceSerializer


class TestStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestStep
        fields = '__all__'


class TestStepRetrieveSerializer(serializers.ModelSerializer):
    """测试步骤详情序列化器"""
    # interface = InterfaceSerializer()
    class Meta:
        model = TestStep
        fields = '__all__'
        depth = 1


class UploadFieldSerializer(serializers.ModelSerializer):
    """上传文件序列化器"""
    path = serializers.CharField(source='file.path', read_only=True)

    class Meta:
        model = UploadFile
        fields = '__all__'
        extra_kwargs = {'file': {'write_only': True}}


class TestSceneSerializer(serializers.ModelSerializer):
    """测试场景/测试套件序列化器"""
    class Meta:
        model = TestScene
        fields = '__all__'


class NestStepSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class TestSceneStepSerializer(serializers.ModelSerializer):
    """测试场景步骤序列化器"""
    stepInfo = NestStepSerializer(source='step', read_only=True)

    class Meta:
        model = SceneData
        fields = '__all__'


class TestPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestPlan
        fields = '__all__'


class CrontabTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrontabTask
        fields = '__all__'



