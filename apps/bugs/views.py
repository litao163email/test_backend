from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Bug, BugHandle
from .serializer import BugSerializer, BugHandleSerializer


class BugViewSet(ModelViewSet):
    queryset = Bug.objects.all().order_by('-create_time')
    serializer_class = BugSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'interface']

    # bug的操作日志，应该是在bug创建，修改状态时产生的
    def perform_create(self, serializer):
        bug = serializer.save()
        # 添加bug提交的操作日志
        BugHandle.objects.create(
            bug=bug,
            handle=f'提交bug，状态为【{bug.status}】',
            update_user=self.request.user.username
        )

    def perform_update(self, serializer):
        bug = serializer.save()
        # 添加bug状态修改的操作日志
        BugHandle.objects.create(
            bug=bug,
            handle=f'处理bug，状态为【{bug.status}】',
            update_user=self.request.user.username
        )


class BugHandleViewSet(ReadOnlyModelViewSet):
    queryset = BugHandle.objects.all()
    serializer_class = BugHandleSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['bug', ]
