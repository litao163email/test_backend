 #!/bin/sh
python manage.py makemigrations
python manage.py migrate
# 因为django的容器启动的时候，mariadb容器肯定启动了，docker-compose中设置了
# 但是mariadb服务不一定启动了，所以这里有可能会失败
# 那么如果这里失败了，直接退出返回非0值，配合容器的restart=always的参数
# 可以让容器自动重启，等待mariadb服务的启动
if [ $? -ne 0 ]
then
  echo "数据库连接失败重启！"
  exit 1
fi

# 创建管理员用户
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('litao', '13888888888', '123456')" | python manage.py shell &> /dev/null

# 启动supervisor
supervisord -c supervisord.conf
