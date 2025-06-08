import json

from django.db import models, transaction
from django.core.exceptions import ValidationError

from django_celery_beat.models import PeriodicTask, CrontabSchedule

SETUP_SCRIPT = """# 前置脚本(python):
# global_tools:全局工具函数
# data:用例数据 
# env: 局部环境
# ENV: 全局环境
# db: 数据库操作对象
"""

TEARDOWN_SCRIPT = """# 后置脚本(python):
# global_tools:全局工具函数
# data:用例数据 
# response:响应对象response 
# env: 局部环境
# ENV: 全局环境
# db: 数据库操作对象
"""


class TestStep(models.Model):
    """测试步骤/测试用例"""
    title = models.CharField('用例名称', max_length=200)
    interface = models.ForeignKey('projects.Interface', on_delete=models.CASCADE, verbose_name='所属接口')
    request = models.JSONField('请求参数', default=dict, blank=True)
    headers = models.JSONField('请求头', default=dict, blank=True)
    file = models.JSONField('上传文件参数', default=list, blank=True)
    setup_script = models.TextField('前置脚本', default=SETUP_SCRIPT, blank=True)
    teardown_script = models.TextField('后置脚本', default=TEARDOWN_SCRIPT, blank=True)

    class Meta:
        db_table = 'tb_test_step'
        verbose_name = '测试步骤表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class TestScene(models.Model):
    """测试场景/测试套件"""
    name = models.CharField('测试场景名', max_length=50)
    project = models.ForeignKey('projects.Project', verbose_name='所属项目', on_delete=models.PROTECT,
                                related_name='test_scenes')
    steps = models.ManyToManyField('TestStep', verbose_name='步骤', through='SceneData', help_text='包含的测试步骤')

    class Meta:
        db_table = 'tb_test_scene'
        verbose_name = '测试场景'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SceneData(models.Model):
    """场景/套件数据，自定义第三张表"""
    scene = models.ForeignKey('TestScene', verbose_name='场景', on_delete=models.PROTECT)
    step = models.ForeignKey('TestStep', verbose_name='步骤', on_delete=models.PROTECT)
    sort = models.IntegerField('执行顺序', blank=True, default=0)

    class Meta:
        db_table = 'tb_scene_data'
        verbose_name = '场景步骤'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class TestPlan(models.Model):
    """测试计划模型"""
    name = models.CharField('计划名称', max_length=100)
    project = models.ForeignKey('projects.Project', on_delete=models.PROTECT, verbose_name='所属项目',
                                related_name='test_plans')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    scenes = models.ManyToManyField('TestScene', verbose_name='测试场景', help_text='包含的测试场景', blank=True)

    class Meta:
        db_table = 'tb_test_plan'
        verbose_name = '测试计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UploadFile(models.Model):
    """上传文件"""
    file = models.FileField('文件', help_text='文件')  # 它只保存文件在服务器上的路径
    info = models.JSONField('数据', help_text='数据', default=list, blank=True)

    def __str__(self):
        return self.file.name

    class Meta:
        db_table = 'tb_upload_file'
        verbose_name = '上传文件'
        verbose_name_plural = verbose_name


class CrontabTask(models.Model):
    """定时任务表"""
    name = models.CharField('任务名称', max_length=120)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, verbose_name='所属项目', related_name='crontab_tasks')
    plan = models.ForeignKey('TestPlan', verbose_name='执行计划', on_delete=models.PROTECT)
    env = models.ForeignKey('projects.TestEnv', verbose_name='测试环境', on_delete=models.PROTECT)
    rule = models.CharField('定时规则', max_length=80, default='* * * * *')
    tester = models.CharField('测试员', max_length=20, blank=True, null=True)
    status = models.BooleanField('是否开启', default=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'tb_crontab_task'
        verbose_name = '定时任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 当创建一个CrontabTask的对象时，需要同步创建一个PeriodicTask对象
    # 当修改一个CrontabTask的对象时，需要同步修改对应的PeriodicTask对象
    # 当删除一个CrontabTask的对象时，需要同步删除对应的PeriodicTask对象
    # 可以再两个地方去实现
    # 1. 在视图中
    # 2. 在模型中

    def save(self, *args, **kwargs):
        """同步创建或修改对应的PeriodicTask"""
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
                # 创建或这更新PeriodicTask
                self.create_or_update_periodic_task()
        except:
            raise ValidationError('创建定时任务失败!请稍后尝试！')

    def delete(self, *args, **kwargs):
        """同步删除对应的PeriodicTask"""
        try:
            with transaction.atomic():
                self.delete_periodic_task()  # 这个一定要写在前面
                super().delete(*args, **kwargs)  # 因为执行了这个行代码后，self.id=None了

        except:
            raise ValidationError('删除定时任务失败！请稍后尝试！')

    def create_or_update_periodic_task(self):
        """创建或者修改一个定时任务"""
        queryset = PeriodicTask.objects.filter(name=self.id)
        kwargs = json.dumps({"pk": self.plan.id, "env_id": self.env.id, "tester": self.tester})
        if queryset:
            # 更新
            periodic_task = queryset.first()
            periodic_task.crontab = self.get_crontab()
            periodic_task.enabled = self.status
            periodic_task.kwargs = kwargs
            periodic_task.save()
        else:
            PeriodicTask.objects.create(
                name=self.id,  # 使用我们项目中的CrontabTask的id作为PeriodicTask的名字,
                task='testplans.tasks.run_crontab_test_plan',
                crontab=self.get_crontab(),
                kwargs=kwargs,
                enabled=self.status
            )

    def delete_periodic_task(self):
        """删除一个定时任务"""
        queryset = PeriodicTask.objects.filter(name=self.id)
        if queryset:
            queryset.first().delete()

    def get_crontab(self):
        """获取crontab"""
        crontab_list = self.rule.split(' ')  # 33 21 * * *
        crontab_dict = {
            'minute': crontab_list[0],
            'hour': crontab_list[1],
            'day_of_week': crontab_list[2],
            'day_of_month': crontab_list[3],
            'month_of_year': crontab_list[4]
        }
        queryset = CrontabSchedule.objects.filter(**crontab_dict)
        if queryset:
            crontab = queryset.first()
        else:
            crontab = CrontabSchedule.objects.create(**crontab_dict)

        return crontab





