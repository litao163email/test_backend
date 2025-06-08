from django.contrib import admin
from testplans.models import *
# Register your models here.
admin.site.register(TestStep)
admin.site.register(TestScene)
admin.site.register(SceneData)
admin.site.register(TestPlan)
admin.site.register(UploadFile)
admin.site.register(CrontabTask)

