from django.contrib import admin
from users.models import *
# Register your models here.
admin.site.register(User,app_name='用户管理')
