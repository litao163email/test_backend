from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Record
from .serializers import RecordSerializer, ReportSerializer
from .filters import RecordFilterSet


class RecordViewSet(ReadOnlyModelViewSet):
    """测试记录视图集"""
    queryset = Record.objects.all().order_by('-create_time')
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated, ]
    filterset_class = RecordFilterSet    # 设置过滤器类

    @action(methods=['get'], detail=True)
    def report(self, request, pk, format=None):
        # 1. 拿到对象
        obj = self.get_object()  # obj是谁？

        # 2. 序列化
        serializer = ReportSerializer(obj.report)
        # 3. 返回响应
        return Response(serializer.data)


    # filterset_fields = ['project', 'plan', 'env']  # 这里的字段，只能是模型的字段
    # 过滤 project, plan, env

    # def get_queryset(self):
    #     queryset = Record.objects.all()
    #     # 获取参数
    #     plan = self.request.query_params.get('plan')
    #     if plan:
    #         queryset = queryset.filter(plan=plan)
    #
    #     env = self.request.query_params.get('env')
    #     if env:
    #         queryset = queryset.filter(test_env=env)
    #
    #     project = self.request.query_params.get('project')
    #     if project:
    #         queryset = queryset.filter(plan__project=project)
    #     return queryset

