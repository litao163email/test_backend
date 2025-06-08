import re

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def validate_mobile(value):
    if not re.match(r'1[3-9]\d{9}',  value):
        raise ValidationError('手机号码格式不正确')


class User(AbstractUser):
    """
    自定义用户模型
    增加一个mobile字段
    """
    mobile = models.CharField('手机号码', max_length=11, unique=True, null=True, blank=True,
                              error_messages={'unique': '手机号码已注册'}, validators=[validate_mobile])

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    REQUIRED_FIELDS = ['mobile']  # 通过createsuperuser管理命令创建用户时，将提示输入mobile字段


