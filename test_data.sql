-- ========================================
-- 接口自动化测试平台 - 测试数据SQL脚本
-- ========================================
-- 使用说明：
-- 1. 请先确保已运行数据库迁移（python manage.py migrate）
-- 2. 执行此SQL脚本前，请根据实际情况修改用户ID和项目ID
-- 3. 建议在测试环境执行，不要在生产环境执行
-- ========================================

-- 1. 创建测试用户（如果不存在）
-- 注意：这里假设已通过Django创建了用户，ID为1
-- 如果需要创建新用户，请使用：python manage.py createsuperuser

-- 2. 插入项目数据
INSERT INTO `tb_project` (`name`, `leader`, `create_time`) VALUES
('电商平台项目', '张三', NOW()),
('移动端APP项目', '李四', NOW()),
('后台管理系统', '王五', NOW()),
('API网关服务', '赵六', NOW())
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 获取插入的项目ID（假设项目ID为1-4）
SET @project_id_1 = (SELECT id FROM tb_project WHERE name = '电商平台项目' LIMIT 1);
SET @project_id_2 = (SELECT id FROM tb_project WHERE name = '移动端APP项目' LIMIT 1);
SET @project_id_3 = (SELECT id FROM tb_project WHERE name = '后台管理系统' LIMIT 1);
SET @project_id_4 = (SELECT id FROM tb_project WHERE name = 'API网关服务' LIMIT 1);

-- 3. 插入测试环境数据
-- 注意：数据库配置格式必须包含 name、type 和 config 字段
-- 数据库密码需要与 Django settings/dev.py 中的配置一致：test5201314
INSERT INTO `tb_test_env` (`name`, `project_id`, `host`, `global_variable`, `debug_global_variable`, `db`, `headers`, `global_func`) VALUES
('开发环境', @project_id_1, 'http://dev.example.com', '{"base_url": "http://dev.example.com", "env": "dev"}', '{"debug": true}', '[{"name": "dev_db", "type": "mysql", "config": {"host": "127.0.0.1", "port": 3306, "user": "root", "password": "test5201314", "database": "easytest1"}}]', '{"Content-Type": "application/json"}', '"""自定义全局工具函数\n============================\n"""\nfrom apitestengine.core.tools import *'),
('测试环境', @project_id_1, 'http://test.example.com', '{"base_url": "http://test.example.com", "env": "test"}', '{"debug": false}', '[{"name": "test_db", "type": "mysql", "config": {"host": "127.0.0.1", "port": 3306, "user": "root", "password": "test5201314", "database": "easytest1"}}]', '{"Content-Type": "application/json", "Authorization": "Bearer token123"}', '"""自定义全局工具函数\n============================\n"""\nfrom apitestengine.core.tools import *'),
('生产环境', @project_id_1, 'http://prod.example.com', '{"base_url": "http://prod.example.com", "env": "prod"}', '{"debug": false}', '[]', '{"Content-Type": "application/json", "Authorization": "Bearer prod_token"}', '"""自定义全局工具函数\n============================\n"""\nfrom apitestengine.core.tools import *'),
('开发环境', @project_id_2, 'http://dev-app.example.com', '{"base_url": "http://dev-app.example.com", "env": "dev"}', '{"debug": true}', '[]', '{"Content-Type": "application/json"}', '"""自定义全局工具函数\n============================\n"""\nfrom apitestengine.core.tools import *')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 获取环境ID
SET @env_id_1 = (SELECT id FROM tb_test_env WHERE name = '开发环境' AND project_id = @project_id_1 LIMIT 1);
SET @env_id_2 = (SELECT id FROM tb_test_env WHERE name = '测试环境' AND project_id = @project_id_1 LIMIT 1);
SET @env_id_3 = (SELECT id FROM tb_test_env WHERE name = '生产环境' AND project_id = @project_id_1 LIMIT 1);
SET @env_id_4 = (SELECT id FROM tb_test_env WHERE name = '开发环境' AND project_id = @project_id_2 LIMIT 1);

-- 4. 插入接口数据
INSERT INTO `tb_interface` (`name`, `project_id`, `url`, `method`, `type`) VALUES
('用户登录', @project_id_1, '/api/users/login/', 'POST', '1'),
('用户注册', @project_id_1, '/api/users/register/', 'POST', '1'),
('获取用户信息', @project_id_1, '/api/users/info/', 'GET', '1'),
('更新用户信息', @project_id_1, '/api/users/update/', 'PUT', '1'),
('商品列表', @project_id_1, '/api/products/', 'GET', '1'),
('商品详情', @project_id_1, '/api/products/{id}/', 'GET', '1'),
('创建订单', @project_id_1, '/api/orders/', 'POST', '1'),
('订单列表', @project_id_1, '/api/orders/', 'GET', '1'),
('支付接口', @project_id_1, '/api/payment/pay/', 'POST', '2'),
('短信发送', @project_id_2, '/api/sms/send/', 'POST', '2'),
('文件上传', @project_id_2, '/api/files/upload/', 'POST', '1'),
('数据统计', @project_id_3, '/api/stats/', 'GET', '1')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 获取接口ID
SET @interface_id_1 = (SELECT id FROM tb_interface WHERE name = '用户登录' AND project_id = @project_id_1 LIMIT 1);
SET @interface_id_2 = (SELECT id FROM tb_interface WHERE name = '用户注册' AND project_id = @project_id_1 LIMIT 1);
SET @interface_id_3 = (SELECT id FROM tb_interface WHERE name = '获取用户信息' AND project_id = @project_id_1 LIMIT 1);
SET @interface_id_4 = (SELECT id FROM tb_interface WHERE name = '商品列表' AND project_id = @project_id_1 LIMIT 1);
SET @interface_id_5 = (SELECT id FROM tb_interface WHERE name = '创建订单' AND project_id = @project_id_1 LIMIT 1);

-- 5. 插入测试步骤数据
INSERT INTO `tb_test_step` (`title`, `interface_id`, `request`, `headers`, `file`, `setup_script`, `teardown_script`) VALUES
('登录成功用例', @interface_id_1, '{"username": "testuser", "password": "123456"}', '{"Content-Type": "application/json"}', '[]', '# 前置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\n', '# 后置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# response:响应对象response \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\n'),
('登录失败用例-密码错误', @interface_id_1, '{"username": "testuser", "password": "wrong"}', '{"Content-Type": "application/json"}', '[]', '# 前置脚本\n', '# 后置脚本\n'),
('注册新用户', @interface_id_2, '{"username": "newuser", "password": "123456", "mobile": "13800138000"}', '{"Content-Type": "application/json"}', '[]', '# 前置脚本\n', '# 后置脚本\n'),
('获取用户信息-正常', @interface_id_3, '{}', '{"Content-Type": "application/json", "Authorization": "Bearer token123"}', '[]', '# 前置脚本\n', '# 后置脚本\n'),
('查询商品列表', @interface_id_4, '{"page": 1, "page_size": 10, "category": "electronics"}', '{"Content-Type": "application/json"}', '[]', '# 前置脚本\n', '# 后置脚本\n'),
('创建订单-成功', @interface_id_5, '{"product_id": 1, "quantity": 2, "address": "北京市朝阳区"}', '{"Content-Type": "application/json", "Authorization": "Bearer token123"}', '[]', '# 前置脚本\n', '# 后置脚本\n'),
('创建订单-库存不足', @interface_id_5, '{"product_id": 999, "quantity": 1000, "address": "北京市朝阳区"}', '{"Content-Type": "application/json", "Authorization": "Bearer token123"}', '[]', '# 前置脚本\n', '# 后置脚本\n')
ON DUPLICATE KEY UPDATE `title`=`title`;

-- 获取测试步骤ID
SET @step_id_1 = (SELECT id FROM tb_test_step WHERE title = '登录成功用例' LIMIT 1);
SET @step_id_2 = (SELECT id FROM tb_test_step WHERE title = '登录失败用例-密码错误' LIMIT 1);
SET @step_id_3 = (SELECT id FROM tb_test_step WHERE title = '注册新用户' LIMIT 1);
SET @step_id_4 = (SELECT id FROM tb_test_step WHERE title = '获取用户信息-正常' LIMIT 1);
SET @step_id_5 = (SELECT id FROM tb_test_step WHERE title = '查询商品列表' LIMIT 1);
SET @step_id_6 = (SELECT id FROM tb_test_step WHERE title = '创建订单-成功' LIMIT 1);
SET @step_id_7 = (SELECT id FROM tb_test_step WHERE title = '创建订单-库存不足' LIMIT 1);

-- 6. 插入测试场景数据
INSERT INTO `tb_test_scene` (`name`, `project_id`) VALUES
('用户登录流程', @project_id_1),
('用户注册流程', @project_id_1),
('商品浏览流程', @project_id_1),
('订单创建流程', @project_id_1),
('完整购物流程', @project_id_1),
('接口冒烟测试', @project_id_2)
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 获取测试场景ID
SET @scene_id_1 = (SELECT id FROM tb_test_scene WHERE name = '用户登录流程' AND project_id = @project_id_1 LIMIT 1);
SET @scene_id_2 = (SELECT id FROM tb_test_scene WHERE name = '用户注册流程' AND project_id = @project_id_1 LIMIT 1);
SET @scene_id_3 = (SELECT id FROM tb_test_scene WHERE name = '商品浏览流程' AND project_id = @project_id_1 LIMIT 1);
SET @scene_id_4 = (SELECT id FROM tb_test_scene WHERE name = '订单创建流程' AND project_id = @project_id_1 LIMIT 1);
SET @scene_id_5 = (SELECT id FROM tb_test_scene WHERE name = '完整购物流程' AND project_id = @project_id_1 LIMIT 1);

-- 7. 插入场景步骤关联数据
INSERT INTO `tb_scene_data` (`scene_id`, `step_id`, `sort`) VALUES
(@scene_id_1, @step_id_1, 1),
(@scene_id_1, @step_id_2, 2),
(@scene_id_2, @step_id_3, 1),
(@scene_id_3, @step_id_5, 1),
(@scene_id_4, @step_id_6, 1),
(@scene_id_4, @step_id_7, 2),
(@scene_id_5, @step_id_1, 1),
(@scene_id_5, @step_id_5, 2),
(@scene_id_5, @step_id_6, 3)
ON DUPLICATE KEY UPDATE `sort`=`sort`;

-- 8. 插入测试计划数据
INSERT INTO `tb_test_plan` (`name`, `project_id`, `create_time`) VALUES
('每日回归测试', @project_id_1, NOW()),
('版本发布测试', @project_id_1, NOW()),
('接口冒烟测试', @project_id_2, NOW()),
('性能测试计划', @project_id_1, NOW())
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 获取测试计划ID
SET @plan_id_1 = (SELECT id FROM tb_test_plan WHERE name = '每日回归测试' AND project_id = @project_id_1 LIMIT 1);
SET @plan_id_2 = (SELECT id FROM tb_test_plan WHERE name = '版本发布测试' AND project_id = @project_id_1 LIMIT 1);
SET @plan_id_3 = (SELECT id FROM tb_test_plan WHERE name = '接口冒烟测试' AND project_id = @project_id_2 LIMIT 1);

-- 9. 插入测试计划与场景的关联（多对多关系表）
-- Django自动创建的表名：tb_test_plan_scenes
INSERT INTO `tb_test_plan_scenes` (`testplan_id`, `testscene_id`) VALUES
(@plan_id_1, @scene_id_1),
(@plan_id_1, @scene_id_3),
(@plan_id_2, @scene_id_5),
(@plan_id_2, @scene_id_4),
(@plan_id_3, @scene_id_1)
ON DUPLICATE KEY UPDATE `testplan_id`=`testplan_id`;

-- 10. 插入运行记录数据
INSERT INTO `tb_record` (`create_time`, `plan_id`, `all`, `success`, `fail`, `error`, `pass_rate`, `tester`, `test_env_id`, `status`) VALUES
(NOW() - INTERVAL 1 DAY, @plan_id_1, 50, 45, 3, 2, '90.00%', '张三', @env_id_1, '执行完成'),
(NOW() - INTERVAL 2 DAY, @plan_id_1, 50, 48, 1, 1, '96.00%', '李四', @env_id_2, '执行完成'),
(NOW() - INTERVAL 3 DAY, @plan_id_2, 100, 95, 3, 2, '95.00%', '王五', @env_id_2, '执行完成'),
(NOW() - INTERVAL 1 HOUR, @plan_id_1, 30, 0, 0, 0, '0.00%', '赵六', @env_id_1, '执行中')
ON DUPLICATE KEY UPDATE `all`=`all`;

-- 获取记录ID（按照插入顺序获取，确保每个记录都有对应的报告）
SET @record_id_1 = (SELECT id FROM tb_record WHERE plan_id = @plan_id_1 AND tester = '张三' LIMIT 1);
SET @record_id_2 = (SELECT id FROM tb_record WHERE plan_id = @plan_id_1 AND tester = '李四' LIMIT 1);
SET @record_id_3 = (SELECT id FROM tb_record WHERE plan_id = @plan_id_2 AND tester = '王五' LIMIT 1);
SET @record_id_4 = (SELECT id FROM tb_record WHERE plan_id = @plan_id_1 AND tester = '赵六' LIMIT 1);

-- 11. 插入测试报告数据（为所有记录创建报告）
INSERT INTO `tb_report` (`info`, `record_id`) VALUES
('{"total": 50, "success": 45, "fail": 3, "error": 2, "duration": 120, "details": [{"step": "登录成功用例", "status": "success", "time": 0.5}, {"step": "登录失败用例", "status": "success", "time": 0.3}]}', @record_id_1),
('{"total": 50, "success": 48, "fail": 1, "error": 1, "duration": 110, "details": [{"step": "登录成功用例", "status": "success", "time": 0.4}, {"step": "查询商品列表", "status": "success", "time": 0.6}]}', @record_id_2),
('{"total": 100, "success": 95, "fail": 3, "error": 2, "duration": 300, "details": [{"step": "商品列表", "status": "success", "time": 0.8}, {"step": "创建订单", "status": "fail", "time": 1.2, "error": "库存不足"}]}', @record_id_3),
('{"total": 30, "success": 0, "fail": 0, "error": 0, "duration": 0, "details": [], "status": "执行中"}', @record_id_4)
ON DUPLICATE KEY UPDATE `info`=`info`;

-- 12. 插入Bug数据
INSERT INTO `tb_bug` (`project_id`, `interface_id`, `desc`, `info`, `status`, `user`, `create_time`) VALUES
(@project_id_1, @interface_id_5, '创建订单接口在库存不足时返回错误码不一致', '{"request": {"product_id": 999, "quantity": 1000}, "response": {"code": 500, "message": "系统错误"}, "expected": {"code": 400, "message": "库存不足"}}', '未处理', '测试员A', NOW() - INTERVAL 1 DAY),
(@project_id_1, @interface_id_1, '登录接口缺少参数校验，空密码也能登录', '{"request": {"username": "admin", "password": ""}, "response": {"code": 200, "token": "xxx"}}', '处理中', '测试员B', NOW() - INTERVAL 2 DAY),
(@project_id_1, @interface_id_4, '商品列表接口分页参数错误时返回500', '{"request": {"page": -1}, "response": {"code": 500}}', '处理完', '测试员C', NOW() - INTERVAL 3 DAY),
(@project_id_1, @interface_id_3, '获取用户信息接口token过期时间过短', '{"request": {}, "response": {"code": 401, "message": "token expired"}, "duration": 300}', '无效bug', '测试员D', NOW() - INTERVAL 5 DAY)
ON DUPLICATE KEY UPDATE `desc`=`desc`;

-- 获取Bug ID
SET @bug_id_1 = (SELECT id FROM tb_bug WHERE project_id = @project_id_1 AND `desc` LIKE '创建订单接口%' LIMIT 1);
SET @bug_id_2 = (SELECT id FROM tb_bug WHERE project_id = @project_id_1 AND `desc` LIKE '登录接口缺少%' LIMIT 1);

-- 13. 插入Bug处理记录
INSERT INTO `tb_bug_handle` (`bug_id`, `handle`, `update_user`, `create_time`) VALUES
(@bug_id_1, '提交bug', '测试员A', NOW() - INTERVAL 1 DAY),
(@bug_id_2, '开始处理', '开发人员A', NOW() - INTERVAL 2 DAY),
(@bug_id_2, '已修复，待验证', '开发人员A', NOW() - INTERVAL 1 DAY),
(@bug_id_2, '验证通过', '测试员B', NOW() - INTERVAL 12 HOUR)
ON DUPLICATE KEY UPDATE `handle`=`handle`;

-- 14. 插入定时任务数据
-- 注意：CrontabTask会自动创建PeriodicTask，这里只插入基础数据
INSERT INTO `tb_crontab_task` (`name`, `project_id`, `plan_id`, `env_id`, `rule`, `tester`, `status`, `create_time`) VALUES
('每日自动回归测试', @project_id_1, @plan_id_1, @env_id_2, '0 2 * * *', '自动化测试', 1, NOW()),
('每周版本测试', @project_id_1, @plan_id_2, @env_id_2, '0 10 * * 1', '测试团队', 1, NOW()),
('冒烟测试', @project_id_2, @plan_id_3, @env_id_4, '0 9 * * *', '测试员A', 0, NOW())
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 15. 插入上传文件数据（可选，文件路径需要根据实际情况调整）
-- INSERT INTO `tb_upload_file` (`file`, `info`) VALUES
-- ('upload_files/test_data.xlsx', '[{"name": "测试用例1", "data": {"username": "test1"}}, {"name": "测试用例2", "data": {"username": "test2"}}]'),
-- ('upload_files/user_list.csv', '[{"name": "用户1", "mobile": "13800138001"}, {"name": "用户2", "mobile": "13800138002"}]')
-- ON DUPLICATE KEY UPDATE `file`=`file`;

-- ========================================
-- 数据插入完成
-- ========================================
-- 验证数据：
-- SELECT COUNT(*) as project_count FROM tb_project;
-- SELECT COUNT(*) as env_count FROM tb_test_env;
-- SELECT COUNT(*) as interface_count FROM tb_interface;
-- SELECT COUNT(*) as step_count FROM tb_test_step;
-- SELECT COUNT(*) as scene_count FROM tb_test_scene;
-- SELECT COUNT(*) as plan_count FROM tb_test_plan;
-- SELECT COUNT(*) as record_count FROM tb_record;
-- SELECT COUNT(*) as bug_count FROM tb_bug;
-- ========================================

