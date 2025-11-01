# 接口自动化测试平台 - 后端

基于 Django + Django REST Framework 开发的接口自动化测试平台后端服务。

## 技术栈

- Python 3.7+
- Django 3.2.13
- Django REST Framework 3.14.0
- PyMySQL 1.0.2（MySQL 数据库驱动）
- Celery 5.2.7（异步任务处理）
- Redis（Celery 消息队列）
- MySQL（数据库）

## 快速开始

### 环境要求

- Python 3.7 或更高版本
- MySQL 5.7+ 或 MySQL 8.0+
- Redis（可选，如果使用 Celery 异步任务）

### 安装依赖

```bash
cd test_backend
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**注意**：在 macOS 上使用 PyMySQL 替代 mysqlclient，避免编译问题。

### 数据库配置

1. 创建 MySQL 数据库：
```sql
CREATE DATABASE easytest1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改数据库配置（`test_backend/settings/dev.py`）：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'easytest1',        # 数据库名
        'USER': 'root',              # 数据库用户名
        'PASSWORD': 'test5201314',    # 数据库密码
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

### 数据库迁移

```bash
# 生成迁移文件
python3 manage.py makemigrations --settings=test_backend.settings.dev

# 执行迁移
python3 manage.py migrate --settings=test_backend.settings.dev
```

### 启动开发服务器

#### 方式一：使用启动脚本（推荐）

```bash
cd test_backend
./start.sh
```

启动脚本会自动：
- 检查 Python 环境
- 检查并安装依赖
- 可选执行数据库迁移
- 启动开发服务器

#### 方式二：手动启动

```bash
cd test_backend
DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py runserver
```

### 访问地址

启动成功后，可通过以下地址访问：

- **API 服务**: http://localhost:8000
- **管理后台**: http://localhost:8000/admin/
- **Swagger 文档**: http://localhost:8000/swagger/
- **ReDoc 文档**: http://localhost:8000/redoc/

## 项目结构

```
test_backend/
├── apps/                    # 应用目录
│   ├── users/               # 用户模块
│   ├── projects/            # 项目模块
│   ├── testplans/           # 测试计划模块
│   ├── reports/             # 报告模块
│   └── bugs/                # Bug管理模块
├── apitestengine/           # API 测试引擎
├── test_backend/            # 项目配置
│   ├── settings/            # 设置文件
│   │   ├── base.py          # 基础配置
│   │   ├── dev.py           # 开发环境配置
│   │   └── pro.py           # 生产环境配置
│   └── urls.py              # URL 路由配置
├── manage.py                # Django 管理脚本
├── requirements.txt         # 项目依赖
└── start.sh                 # 启动脚本
```

## 常用命令

### Django 管理命令

```bash
# 创建超级用户
DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py createsuperuser

# 启动开发服务器
DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py runserver

# 运行测试
DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py test

# 检查项目配置
DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py check
```

### Celery 任务（可选）

如果使用 Celery 异步任务，需要启动 Celery Worker：

```bash
# 启动 Celery Worker
celery -A test_backend worker -l info

# 启动 Celery Beat（定时任务）
celery -A test_backend beat -l info
```

## 环境配置

### 开发环境

使用 `dev.py` 配置文件：
- 数据库：本地 MySQL
- 调试模式：开启
- 允许所有域名跨域

### 生产环境

使用 `pro.py` 配置文件，需要：
- 配置生产数据库
- 关闭调试模式
- 配置允许的主机列表
- 配置静态文件服务

## 依赖说明

### 主要依赖

- **Django**: Web 框架
- **djangorestframework**: REST API 框架
- **django-simpleui**: Django Admin 美化
- **pymysql**: MySQL 数据库驱动（macOS 推荐）
- **celery**: 异步任务队列
- **redis**: 消息队列后端
- **drf-yasg**: API 文档生成

### 特殊说明

- **PyMySQL vs mysqlclient**: 在 macOS 上使用 PyMySQL 避免编译问题
- **importlib-metadata**: 需要版本 < 5.0，与 celery 5.2.7 兼容

## 故障排除

### 1. 数据库连接失败

- 检查 MySQL 服务是否启动
- 检查数据库配置是否正确
- 确认数据库用户权限

### 2. Celery 导入错误

如果遇到 `ImportError: cannot import name 'Celery'`，执行：

```bash
pip3 install "importlib-metadata<5.0"
```

### 3. 端口占用

如果 8000 端口被占用，可以指定其他端口：

```bash
python3 manage.py runserver 8001
```

## 开发建议

1. **使用虚拟环境**：建议使用 `venv` 或 `virtualenv` 管理 Python 依赖
2. **代码规范**：遵循 PEP 8 Python 编码规范
3. **API 文档**：修改 API 后及时更新 Swagger 文档
4. **测试覆盖**：编写单元测试和集成测试

## 许可证

查看 LICENSE 文件了解详情。

