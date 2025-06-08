#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/1 21:49
# E-mail: litao163email@163.com
# @Author: litao
from rest_framework.routers import DefaultRouter

from .views import RecordViewSet

route = DefaultRouter()
route.register('records', RecordViewSet)

urlpatterns = route.urls
