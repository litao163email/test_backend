# 测试数据SQL脚本使用说明

## 文件说明

`test_data.sql` - 包含所有表的测试数据插入SQL语句

## 使用方法

### 方法一：使用导入脚本（推荐）

```bash
cd test_backend
./import_test_data.sh
```

脚本会自动检测MySQL路径并导入数据。

### 方法二：使用MySQL命令行（完整路径）

如果 `mysql` 命令找不到，请使用完整路径：

```bash
# 方式1：直接导入
cd test_backend
/usr/local/mysql/bin/mysql -u root -p easytest1 < test_data.sql

# 方式2：登录后执行
/usr/local/mysql/bin/mysql -u root -p
USE easytest1;
source /Users/litao/project_testdemo/test_backend/test_data.sql;
```

**注意**：如果您的MySQL安装在其他路径，请替换 `/usr/local/mysql/bin/mysql` 为实际路径。

### 方法三：添加MySQL到PATH（永久解决）

将MySQL的bin目录添加到PATH环境变量：

```bash
# 编辑 ~/.zshrc 或 ~/.bash_profile
echo 'export PATH="/usr/local/mysql/bin:$PATH"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 验证
mysql --version
```

添加PATH后，就可以直接使用 `mysql` 命令了。

### 方法四：在Django shell中执行（不推荐，复杂）

```bash
cd test_backend
DJANGO_SETTINGS_MODULE=test_backend.settings.dev python3 manage.py shell
```

然后在shell中：
```python
from django.db import connection

with open('test_data.sql', 'r', encoding='utf-8') as f:
    sql = f.read()
    
# 执行SQL
with connection.cursor() as cursor:
    # 由于SQL中包含变量，需要分段执行
    # 或者直接使用MySQL客户端执行
    pass
```

**建议**：直接使用MySQL客户端执行SQL文件，因为SQL中使用了MySQL变量（@变量名），在Django ORM中无法直接执行。

## 包含的测试数据

### 1. 项目数据 (4个)
- 电商平台项目
- 移动端APP项目
- 后台管理系统
- API网关服务

### 2. 测试环境数据 (4个)
- 开发环境
- 测试环境
- 生产环境

### 3. 接口数据 (12个)
- 用户登录、注册、信息查询等
- 商品列表、详情
- 订单创建、查询
- 支付接口
- 短信发送等

### 4. 测试步骤数据 (7个)
- 登录成功/失败用例
- 注册新用户
- 获取用户信息
- 查询商品列表
- 创建订单成功/失败用例

### 5. 测试场景数据 (6个)
- 用户登录流程
- 用户注册流程
- 商品浏览流程
- 订单创建流程
- 完整购物流程
- 接口冒烟测试

### 6. 测试计划数据 (4个)
- 每日回归测试
- 版本发布测试
- 接口冒烟测试
- 性能测试计划

### 7. 运行记录数据 (4条)
- 包含不同状态的执行记录
- 成功、失败、错误用例统计

### 8. 测试报告数据 (2条)
- 详细的测试报告JSON数据

### 9. Bug数据 (4条)
- 不同状态的Bug记录
- 未处理、处理中、处理完、无效bug

### 10. Bug处理记录 (4条)
- Bug的操作历史记录

### 11. 定时任务数据 (3条)
- 不同类型的定时任务配置

## 注意事项

1. **执行顺序**：SQL脚本已经按照依赖关系排序，请按顺序执行
2. **ON DUPLICATE KEY UPDATE**：使用了该语法避免重复插入，但请确保表中有唯一约束
3. **变量使用**：SQL中使用了MySQL变量（@变量名）来保存ID，确保MySQL版本支持
4. **JSON字段**：JSON字段使用了JSON格式字符串，确保MySQL版本支持JSON类型（5.7+）
5. **时间字段**：使用了NOW()函数，请根据实际情况调整

## 验证数据

执行完SQL后，可以使用以下SQL验证数据：

```sql
-- 查看各表数据量
SELECT '项目' as table_name, COUNT(*) as count FROM tb_project
UNION ALL
SELECT '测试环境', COUNT(*) FROM tb_test_env
UNION ALL
SELECT '接口', COUNT(*) FROM tb_interface
UNION ALL
SELECT '测试步骤', COUNT(*) FROM tb_test_step
UNION ALL
SELECT '测试场景', COUNT(*) FROM tb_test_scene
UNION ALL
SELECT '测试计划', COUNT(*) FROM tb_test_plan
UNION ALL
SELECT '运行记录', COUNT(*) FROM tb_record
UNION ALL
SELECT 'Bug', COUNT(*) FROM tb_bug;
```

## 清理测试数据

如果需要清理测试数据，可以执行：

```sql
-- 注意：请谨慎执行，会删除所有测试数据
DELETE FROM tb_bug_handle;
DELETE FROM tb_bug;
DELETE FROM tb_report;
DELETE FROM tb_record;
DELETE FROM tb_crontab_task;
DELETE FROM tb_test_plan_scenes;
DELETE FROM tb_scene_data;
DELETE FROM tb_test_scene;
DELETE FROM tb_test_step;
DELETE FROM tb_interface;
DELETE FROM tb_test_env;
DELETE FROM tb_test_plan;
DELETE FROM tb_project;
```

或者使用Django管理命令：

```bash
python3 manage.py flush  # 清空所有数据（包括用户数据）
```

## 常见问题

### 1. 执行时报错：变量未定义
- 确保按照顺序执行SQL语句
- 检查是否有表不存在的情况

### 2. JSON字段插入失败
- 确保MySQL版本 >= 5.7
- 检查JSON格式是否正确

### 3. 外键约束错误
- 确保先插入主表数据（如项目），再插入关联表数据（如接口）

### 4. 重复插入错误
- SQL中使用了ON DUPLICATE KEY UPDATE，但如果表中没有唯一约束，可以移除该语句

