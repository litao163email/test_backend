import os
from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action

from .models import TestStep, UploadFile, TestScene, SceneData, TestPlan, CrontabTask
from .serializers import (TestStepSerializer, TestStepRetrieveSerializer,
                          UploadFieldSerializer, TestSceneSerializer,
                          TestSceneStepSerializer, TestPlanSerializer,
                          CrontabTaskSerializer)
from .tasks import run_test_step, run_test_scene, run_test_plan
from reports.serializers import RecordSerializer


class TestStepViewSet(ModelViewSet):
    queryset = TestStep.objects.all()
    serializer_class = TestStepSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """实现查看详情时，使用不同的序列化器类"""
        if self.action == 'retrieve':
            return TestStepRetrieveSerializer
        return super().get_serializer_class()

    @action(methods=['post'], detail=False)
    def run(self, request):
        # 1. 获取测试数据
        case = request.data.get('data')
        env_id = request.data.get('env')
        if not (case and env_id):
            return Response({'msg': '请求参数env,data必填', 'data': None}, status=400)
        # 2. 执行测试步骤
        res = run_test_step(case, env_id)
        # 3. 返回响应
        return Response(res)


class UploadFileViewSet(ModelViewSet):
    """文件上传"""
    queryset = UploadFile.objects.all()
    serializer_class = UploadFieldSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """重写perform_create,在创建对象时还要做额外的操作"""
        # 获取文件的大小和文件名，以及构造info字段数据
        size = self.request.data['file'].size
        name = self.request.data['file'].name
        # 去掉文件名中的空格
        name = name.replace(' ', '')
        self.request.data['file'].name = name
        file_type = self.request.data['file'].content_type
        path = str(settings.MEDIA_ROOT / name)
        info = [name, path, file_type]
        # 限制同名文件名
        if os.path.isfile(path):
            raise ValidationError('上传失败，同名文件已存在！')
        # 限制一下大小
        if size > 1024 * 300:
            raise ValidationError('上传失败， 文件大小不能超过300kb')

        # 保存文件
        serializer.save(info=info)

    def perform_destroy(self, instance):
        """复写perform_destroy 保证删除文件"""
        os.remove(instance.file.path)
        instance.delete()


class TestSceneViewSet(ModelViewSet):
    """测试场景视图集"""
    queryset = TestScene.objects.all()
    serializer_class = TestSceneSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'testplan']

    @action(methods=['post'], detail=True)
    def run(self, request, pk):
        # 获取前端传递参数
        env_id = request.data.get('env')
        res = run_test_scene(pk, env_id)
        return Response(res)


class TestSceneStepViewSet(ModelViewSet):
    """测试场景步骤视图集"""
    queryset = SceneData.objects.all()
    serializer_class = TestSceneStepSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['scene']

    # action 默认生成的url，使用方法名
    # /test_scene_steps/order/  detail = False
    # /test_scene_steps/pk/order/  detail = True
    # 如果设置了 url_path = 'aaa'
    # /test_scene_steps/aaa/  detail = False
    # /test_scene_steps/pk/aaa/  detail = True

    @action(methods=['put'], detail=False)
    def order(self, request):
        # 先获取前端传递的数据
        for item in request.data:
            # 获取对象
            obj = SceneData.objects.get(pk=item['id'])
            obj.sort = item['sort']
            obj.save()

        return Response(request.data)


class TestPlanViewSet(ModelViewSet):
    """测试计划视图集"""
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', ]

    @action(methods=['post'], detail=True)
    def run(self, request, pk):
        """
        运行测试计划
        """
        # 1. 获取参数
        env_id = request.data.get('env')
        # 创建测试记录
        serializer = RecordSerializer(data={
            'test_env': env_id,
            'plan': pk,
            'status': "执行中",
            'tester': request.user.username
        })
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        tester = request.user.username
        # 同步执行测试计划
        res = run_test_plan(pk, env_id, record.id, tester)
        return Response(res)

        # 异步执行
        # run_test_plan.delay(pk, env_id, record.id, tester)
        # return Response({"message":"执行成功！"})
        # return Response(serializer.data)


class CrontabTaskViewSet(ModelViewSet):
    queryset = CrontabTask.objects.all()
    serializer_class = CrontabTaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'plan']

    # 创建时需要把当前用户填入tester字段
    def perform_create(self, serializer):
        serializer.save(tester=self.request.user.username)
