import pymysql

# 使用 PyMySQL 替代 mysqlclient
pymysql.install_as_MySQLdb()

from .celery import app as celery_app

__all__ = ('celery_app', )
