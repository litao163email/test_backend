#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/30 20:09
# E-mail: litao163email@163.com
# @Author: litao
from celery import shared_task
from apitestengine.core.cases import run_test
# from test_backend.celery import app
from projects.models import TestEnv
from testplans.models import TestScene, TestPlan
from testplans.serializers import TestStepRetrieveSerializer
from reports.models import Record, Report
from reports.serializers import RecordSerializer


@shared_task
def add(x, y):
    return x + y

"""

测试数据的结构
[
    {"Cases": [
        {}, # 用例
        {}
    ]}, # 测试套件，场景
]
环境配置数据的结构
config = {
        'ENV': {
            'host': '',
            'headers': {},
            'some': 'value'
        },              # 环境变量    
        'DB': [],        # 数据库配置
        'global_func': ''   # 全局函数
    }

"""


def __get_env_config(env, debug=True):
    """获取环境配置信息"""
    # 如果是调试环境，需要把调试的全局变量也要加载到环境配置中
    var = {**env.global_variable, **env.debug_global_variable} if debug else env.global_variable
    ENV = {
        'host': env.host,
        'headers': env.headers,
        **var
    }

    config = {
        'ENV': ENV,  # 环境变量
        'DB': env.db,  # 数据库配置
        'global_func': env.global_func  # 全局函数
    }
    return config


def run_test_step(case, env_id):
    """执行单条测试步骤"""
    # 获取运行环境
    env = TestEnv.objects.get(id=env_id)

    config = __get_env_config(env)
    # 执行用例
    res, debug_var = run_test(case_data=[{"Cases": [case]}], env_config=config, debug=True)
    # 获取结果
    result = res['results'][0]['cases'][0]
    # 保存调试模式下的环境变量
    env.debug_global_variable = debug_var
    env.save()
    return result


def run_test_scene(pk, env_id):
    """执行测试场景"""
    # 获取环境配置
    env = TestEnv.objects.get(pk=env_id)
    config = __get_env_config(env, debug=True)
    # 获取测试数据
    scene = TestScene.objects.get(pk=pk)
    # 获取套件下的所有的scenedata，并且以sort字段进行排序
    scene_steps = scene.scenedata_set.all().order_by('sort')  # 套件下的所有的scenedata

    # data = []
    # for item in scene_steps:
    #     data.append(TestStepRetrieveSerializer(item.step).data)  # 序列化测试步骤
    test_data = {
        'name': scene.name,  # 套件的名字
        'Cases': [TestStepRetrieveSerializer(item.step).data for item in scene_steps] #
    }
    # 运行用例
    res, debub_var = run_test(case_data=[test_data], env_config=config, debug=True)
    # 保存debug模式的环境变量
    env.debug_global_variable = debub_var
    env.save()
    return res['results'][0]


@shared_task
def run_test_plan(pk, env_id, record_id, tester):
    """执行测试计划"""
    # 获取运行环境
    env = TestEnv.objects.get(pk=env_id)
    config = __get_env_config(env, debug=False)
    # 构造测试数据
    plan = TestPlan.objects.get(pk=pk)
    scenes = plan.scenes.all()
    test_data = [
        {
            'name': scene.name,  # 套件的名字
            'Cases': [TestStepRetrieveSerializer(item.step).data for item in scene.scenedata_set.all().order_by('sort')]  #
        } for scene in scenes
    ]
    # 执行测试任务
    res = run_test(case_data=test_data, env_config=config, debug=False)
    # 保存运行结果
    record = Record.objects.get(pk=record_id)

    record.all = res.get('all', 0)
    record.success = res.get('success', 0)
    record.fail = res.get('fail', 0)
    record.error = res.get('error', 0)
    record.pass_rate = '{:.2f}'.format(res.get('success', 0)*100 / res.get('all', 0)) if res.get('all', 0) else '0'
    record.status = '执行完毕'
    record.save()
    # 保存报告
    # 添加信息
    res['plan'] = pk
    res['test_env'] = env_id
    res['tester'] = tester
    Report.objects.create(info=res, record=record)
    # return RecordSerializer(record).data


@shared_task
def run_crontab_test_plan(pk, env_id, tester):
    """
    定时执行测试计划
    :param pk:
    :param env_id:
    :param tester:
    :return:
    """
    # 获取运行环境
    env = TestEnv.objects.get(pk=env_id)
    config = __get_env_config(env, debug=False)
    # 构造测试数据
    plan = TestPlan.objects.get(pk=pk)
    scenes = plan.scenes.all()
    test_data = [
        {
            'name': scene.name,  # 套件的名字
            'Cases': [TestStepRetrieveSerializer(item.step).data for item in scene.scenedata_set.all().order_by('sort')]
            #
        } for scene in scenes
    ]
    # 执行测试任务
    res = run_test(case_data=test_data, env_config=config, debug=False)
    # 保存运行结果
    # 创建测试记录
    record = Record.objects.create(
        plan=plan,
        tester=tester,
        test_env=env,
        all=res.get('all', 0),
        success=res.get('success', 0),
        fail=res.get('fail', 0),
        error=res.get('error', 0),
        pass_rate='{:.2f}'.format(res.get('success', 0)*100 / res.get('all', 0)) if res.get('all', 0) else '0',
        status='执行完毕'
    )

    # 保存报告
    # 添加信息
    res['plan'] = pk
    res['test_env'] = env_id
    res['tester'] = tester
    Report.objects.create(info=res, record=record)
