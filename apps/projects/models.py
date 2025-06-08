from django.db import models

from reports.models import Record
from bugs.models import Bug


class Project(models.Model):
    """项目表"""
    name = models.CharField('项目名', max_length=20, help_text='项目名称')
    leader = models.CharField('负责人', max_length=20, help_text='负责人名称')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'tb_project'
        verbose_name = '项目表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def info(self):
        """统计项目信息"""
        return [
            {'name': '执行环境', 'value': self.test_envs.count()},
            {'name': '测试场景', 'value': self.test_scenes.count()},
            {'name': '测试计划', 'value': self.test_plans.count()},
            {'name': '接口数量', 'value': self.interfaces.count()},
            {'name': '定时任务', 'value': self.crontab_tasks.count()},
            {'name': '执行记录', 'value': Record.objects.filter(plan__project=self).count()}
        ]

    def bugs(self):
        """统计bug信息"""
        return [
            {'name': '未处理bug', 'value': self.bug_set.filter(status='未处理').count()},
            {'name': '处理中bug', 'value': self.bug_set.filter(status='处理中').count()},
            {'name': '处理完bug', 'value': self.bug_set.filter(status='处理完').count()},
            {'name': '无效bug', 'value': self.bug_set.filter(status='无效bug').count()},
        ]


class TestEnv(models.Model):
    """测试环境表"""

    GLOBAL_FUNC_TEXT = '''"""
自定义全局工具函数
============================
"""
from apitestengine.core.tools import *'''

    name = models.CharField('环境名称', max_length=20, help_text='测试环境名称')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目', help_text='项目id',
                                related_name='test_envs')
    global_variable = models.JSONField('全局变量', default=dict, null=True, blank=True)
    debug_global_variable = models.JSONField('debug模式全局变量', default=dict, null=True, blank=True)
    host = models.CharField('base_url地址', max_length=100, null=True, blank=True)
    db = models.JSONField('数据库配置', default=list, null=True, blank=True)
    headers = models.JSONField('全局请求头', default=dict, null=True, blank=True)
    global_func = models.TextField('全局函数', default=GLOBAL_FUNC_TEXT, null=True, blank=True)

    class Meta:
        db_table = 'tb_test_env'
        verbose_name = '测试环境表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Interface(models.Model):
    """接口模型"""
    TYPE_CHOICES = [
        ('1', '项目接口'),
        ('2', '三方接口')
    ]

    name = models.CharField('接口名称', max_length=20)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目', help_text='项目id',
                                related_name='interfaces')
    url = models.CharField('接口地址', max_length=200, help_text='接口地址，url')
    method = models.CharField('请求方法', max_length=20, help_text='http请求方法')
    type = models.CharField('接口类型', choices=TYPE_CHOICES, default='1', max_length=10)

    class Meta:
        db_table = 'tb_interface'
        verbose_name = '接口表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.url








