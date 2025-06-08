"""test_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated

from drf_yasg.views import get_schema_view as get_s_view
from drf_yasg import openapi

swg_view = get_s_view(
    openapi.Info(
        title='ck15接口自动化测试平台',
        description='一个教学项目',
        default_version='1.0'
    ),
    public=True,
    permission_classes=[IsAuthenticated, ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/', include('rest_framework.urls')),
    path('', include('users.urls')),
    path('', include('projects.urls')),
    path('', include('testplans.urls')),
    path('', include('reports.urls')),
    path('', include('bugs.url')),
    # api文档视图
    path('openapi/', get_schema_view(
        title='ck15接口自动化测试平台',
        description='一个教学项目',
        version='1.0'
    ), name='openapi'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='api/swagger-ui.html',
        extra_context={'schema_url': 'openapi'}
    )),
    path('docs/', include_docs_urls(
        title='ck15接口自动化测试平台',
        description='一个教学项目',
    )),
    # drf_yasg api
    re_path(r'^swagger(?P<format>\.json|\.yml|.yaml)$', swg_view.without_ui(), name='swg-json'),
    re_path(r'^swagger/$', swg_view.with_ui(), name='swg-ui'),
    re_path(r'^redoc/$', swg_view.with_ui('redoc')),
]
