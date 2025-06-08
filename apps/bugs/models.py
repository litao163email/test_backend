from django.db import models


class Bug(models.Model):
    CHOICES = [
        ('未处理', '未处理'),
        ('处理中', '处理中'),
        ('处理完', '处理完'),
        ('无效bug', '无效bug'),
    ]
    # 项目
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, help_text='项目id', verbose_name='项目id')
    # 接口
    interface = models.ForeignKey('projects.Interface', on_delete=models.CASCADE, help_text='接口', verbose_name='接口')
    # bug描述
    desc = models.TextField('bug描述', max_length=3000, blank=True)
    # bug基本信息（请求头 请求体 请求方式  响应结果）
    info = models.JSONField('测试报告', default=dict, blank=True)
    # bug状态（待提交，已提交  处理中  关闭  无效bug）
    status = models.CharField('状态', help_text='bug状态', max_length=40, choices=CHOICES, default='1')
    user = models.CharField('提交者', help_text='提交者', max_length=40, default='', blank=True)
    create_time = models.DateTimeField('创建时间', help_text='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'tb_bug'
        verbose_name = 'bug表'
        verbose_name_plural = verbose_name


class BugHandle(models.Model):
    """bug处理记录表"""

    bug = models.ForeignKey('Bug', on_delete=models.CASCADE, help_text='bug ID', verbose_name='bug ID')
    handle = models.CharField('处理操作', max_length=20, blank=True)
    update_user = models.CharField('更新用户', max_length=20, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'tb_bug_handle'
        verbose_name = "bug操作记录表"
        verbose_name_plural = verbose_name
