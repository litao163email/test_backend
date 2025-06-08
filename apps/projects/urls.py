#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/23 20:37
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework.routers import DefaultRouter

from . import views


route = DefaultRouter()
route.register('projects', views.ProjectViewSet)
route.register('interfaces', views.InterfaceViewSet)
route.register('test_envs', views.TestEnvViewSet)


urlpatterns = route.urls

