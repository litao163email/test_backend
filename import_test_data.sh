#!/bin/bash

# 导入测试数据脚本
# 用途：将test_data.sql导入到MySQL数据库

echo "=========================================="
echo "  导入测试数据到MySQL数据库"
echo "=========================================="

# MySQL路径（根据实际情况调整）
MYSQL_BIN="/usr/local/mysql/bin/mysql"

# 检查MySQL是否存在
if [ ! -f "$MYSQL_BIN" ]; then
    echo "❌ 错误: 未找到MySQL客户端"
    echo "请检查MySQL安装路径，或修改脚本中的MYSQL_BIN变量"
    exit 1
fi

# 数据库配置（根据实际情况修改）
DB_NAME="easytest1"
DB_USER="root"

# SQL文件路径
SQL_FILE="$(dirname "$0")/test_data.sql"

# 检查SQL文件是否存在
if [ ! -f "$SQL_FILE" ]; then
    echo "❌ 错误: 未找到SQL文件: $SQL_FILE"
    exit 1
fi

echo "数据库: $DB_NAME"
echo "SQL文件: $SQL_FILE"
echo ""
read -p "请输入MySQL密码: " -s DB_PASSWORD
echo ""

# 导入SQL文件
echo "正在导入数据..."
$MYSQL_BIN -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$SQL_FILE"

if [ $? -eq 0 ]; then
    echo "✓ 数据导入成功！"
else
    echo "❌ 数据导入失败，请检查："
    echo "   1. 数据库是否存在"
    echo "   2. 用户名和密码是否正确"
    echo "   3. SQL文件是否有语法错误"
    exit 1
fi

