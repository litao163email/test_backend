#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 21:14
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework.routers import DefaultRouter

from . import views

route = DefaultRouter()
route.register('test_steps', views.TestStepViewSet)
route.register('upload', views.UploadFileViewSet)
route.register('test_scenes', views.TestSceneViewSet)
route.register('test_scene_steps', views.TestSceneStepViewSet)
route.register('test_plans', views.TestPlanViewSet)
route.register('crontab_tasks', views.CrontabTaskViewSet)


urlpatterns = route.urls
