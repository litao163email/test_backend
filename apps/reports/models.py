from django.db import models


class Record(models.Model):
    """运行记录表"""
    create_time = models.DateTimeField('创建时间', help_text='创建时间', auto_now_add=True)
    plan = models.ForeignKey('testplans.TestPlan', verbose_name='执行计划', on_delete=models.PROTECT,
                             related_name='records')
    all = models.IntegerField('用例总数', help_text='用例总数', blank=True, default=0)
    success = models.IntegerField('成功用例', help_text='成功用例', blank=True, default=0)
    fail = models.IntegerField('失败用例', help_text='失败用例', blank=True, default=0)
    error = models.IntegerField('错误用例', help_text='错误用例', blank=True, default=0)
    pass_rate = models.CharField('执行通过率', help_text='执行通过率', max_length=20, blank=True, default=0)
    tester = models.CharField('执行者', help_text='执行者', max_length=20, blank=True)
    test_env = models.ForeignKey('projects.TestEnv', help_text='测试环境', verbose_name='测试环境', on_delete=models.PROTECT)
    status = models.CharField(help_text='执行状态', verbose_name='执行状态', max_length=100)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tb_record'
        verbose_name = '运行记录表'
        verbose_name_plural = verbose_name


class Report(models.Model):
    """测试报告"""
    info = models.JSONField('测试报告', help_text='测试报告详细信息', default=dict, blank=True)
    record = models.OneToOneField('Record', help_text='测试记录', verbose_name='测试记录', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tb_report'
        verbose_name = '报告表'
        verbose_name_plural = verbose_name
