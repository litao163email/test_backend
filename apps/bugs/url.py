#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/4 20:55
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework.routers import DefaultRouter

from . import views

route = DefaultRouter()
route.register('bugs', views.BugViewSet)
route.register('blogs', views.BugHandleViewSet)

urlpatterns = route.urls
