from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Project, Interface, TestEnv
from .serializers import (
    ProjectSerializer, ProjectDetailSerializer, InterfaceSerializer,
    EnvironmentSerializer
)


class ProjectViewSet(ModelViewSet):
    """
    测试项目视图集
    list:
    返回项目列表
    retrieve:
    返回项目详情
    create:
    创建项目
    update:
    修改项目
    destroy:
    删除项目
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    # 当获取项目详情时，使用ProjectDetailSerializer
    # 可以通过复写方法get_serializer_class来实现
    # 视图集有一个属性，叫action，它的值就是
    # list, retrieve, create, update, destroy分别和对应的请求对应
    def get_serializer_class(self):
        if self.action == 'retrieve':
            # 说明当前请求是详情
            return ProjectDetailSerializer
        return super().get_serializer_class()


class InterfaceViewSet(ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', ]

    # # 复写方法get_queryset实现过滤
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # 过滤
    #     # 获取参数
    #     project = self.request.query_params.get('project')
    #     if project:
    #         queryset = queryset.filter(project=project)
    #
    #     return queryset

class TestEnvViewSet(ModelViewSet):
    queryset = TestEnv.objects.all()
    serializer_class = EnvironmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', ]

    # # 复写方法get_queryset实现过滤
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # 过滤
    #     # 获取参数
    #     project = self.request.query_params.get('project')
    #     if project:
    #         queryset = queryset.filter(project=project)
    #
    #     return queryset

