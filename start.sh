#!/bin/bash

# 后端启动脚本
# 用途：一键启动 Django 开发服务器

echo "=========================================="
echo "  接口自动化测试平台 - 后端启动脚本"
echo "=========================================="

# 进入项目目录
cd "$(dirname "$0")"

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3.7+"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"

# 检查依赖是否安装
echo ""
echo "检查依赖..."
if ! python3 -c "import django" 2>/dev/null; then
    echo "⚠️  检测到依赖未安装，正在安装..."
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请检查网络连接和 Python 环境"
        exit 1
    fi
    echo "✓ 依赖安装完成"
else
    echo "✓ 依赖已安装"
fi

# 检查数据库连接（可选）
echo ""
echo "检查数据库配置..."
# 这里可以添加数据库连接检查逻辑

# 运行数据库迁移（如果需要）
echo ""
read -p "是否需要运行数据库迁移？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在运行数据库迁移..."
    DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py migrate
    if [ $? -ne 0 ]; then
        echo "⚠️  数据库迁移失败，但将继续启动服务器"
    else
        echo "✓ 数据库迁移完成"
    fi
fi

# 启动开发服务器
echo ""
echo "=========================================="
echo "  正在启动 Django 开发服务器..."
echo "  访问地址: http://localhost:8000"
echo "  管理后台: http://localhost:8000/admin/"
echo "  API文档:  http://localhost:8000/swagger/"
echo "=========================================="
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py runserver

