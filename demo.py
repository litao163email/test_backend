#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/14 21:41
# E-mail: litao163email@163.com
# @Author: litao
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_backend.settings')
django.setup()

from testplans.models import TestScene
from testplans.serializers import TestSceneStepSerializer, TestStepRetrieveSerializer
scene = TestScene.objects.get(pk=1)

scene_steps = scene.scenedata_set.all().order_by('sort')  # 套件下的所有的scenedata
for item in scene_steps:
    print(item.sort, item.step.title)
data = []
for item in scene_steps:
    data.append(TestStepRetrieveSerializer(item.step).data)
    # data.append({
    #     'id': item.step.id,
    #     'title': item.step.title,
    #     'request': item.step.request
    #
    # })

print(data[0])

"""
{
  "id": 1,
  "title": "登录成功",
  "request": {
    "json": {
      "username": "litao",
      "password": "123456"
    },
    "data": null,
    "params": {
      "key": "value"
    }
  },
  "headers": {
    "customer": "somevalue"
  },
  "file": [],
  "setup_script": "# 前置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\nprint('我是前置脚本----------------------------------')",
  "teardown_script": "# 后置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# response:响应对象response \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\n# 断言响应状态码\n# 断言http状态码 \n# Demo:断言http状态码是否为200  \ntest.assertion(\"相等\",200,response.status_code)\n# 设置全局变量 \ntest.save_global_variable(\"token\",response.json()['token'])",
  "interface": {
    "url": "/users/login/",
    "method": "POST"
  }
}
"""
test_data = {
    'name': scene.name,  # 套件的名字
    'Cases': data
}
