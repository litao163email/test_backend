#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/16 20:54
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import User

class AccessToToken:
    def validate(self, attrs):
        """复写validate方法，实现更换access键为token"""
        attrs = super().validate(attrs)
        # 修改access为token
        attrs['token'] = attrs.pop('access')
        return attrs


class LoginSerializer(AccessToToken, TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # 添加数据
        data['username'] = self.user.username
        data['id'] = self.user.id
        data['msg'] = '登录成功'
        return data


class RefreshSerializer(AccessToToken, TokenRefreshSerializer):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(label='确认密码', write_only=True, min_length=6, max_length=20,
                                             error_messages={
                                                 'min_length': '仅允许6-20个字符的密码',
                                                 'max_length': '仅允许6-20个字符的密码',
                                             })

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'mobile')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的密码',
                    'max_length': '仅允许5-20个字符的密码',
                }

            },
            'password': {
                'label': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的密码',
                    'max_length': '仅允许6-20个字符的密码',
                }
            }
        }

    def validate_password_confirm(self, value):
        """校验密码和确认密码是否相等"""
        if value != self.initial_data['password']:
            raise serializers.ValidationError('两次输入的密码不一致！')
        return value

    # def validate(self, attrs):
    #     if attrs.get('password') != attrs.get('password_confirm'):
    #         raise serializers.ValidationError('两次输入的密码不一致！')
    #     return attrs

    def create(self, validated_data):
        """因为password_confirm字段在创建用户时要删掉，所以复写create"""
        validated_data.pop('password_confirm')
        # 注意调用create_user方法来创建用户，它会对密码进行加密
        return User.objects.create_user(**validated_data)
