#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/16 20:50
# E-mail: litao163email@163.com
# @Author: litao
from django.urls import path

from . import views

urlpatterns = [
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.RefreshView.as_view(), name='token_refresh'),
    path('users/register/', views.UserRegisterView.as_view(), name='register')
]
