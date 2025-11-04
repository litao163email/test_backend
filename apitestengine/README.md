# APITestEngine - Unittest 用例执行引擎

## 📖 简介

`apitestengine` 是一个基于 Python `unittest` 框架构建的 API 测试执行引擎，它提供了动态创建测试用例、环境变量管理、数据库支持、前置后置脚本执行等功能，专门用于 API 接口自动化测试。

## 🎯 核心特性

- ✅ **动态创建测试用例**：根据测试数据动态生成测试类和测试方法
- ✅ **环境变量管理**：支持全局变量和临时变量，支持变量引用和替换
- ✅ **数据库支持**：支持 MySQL 数据库连接和操作
- ✅ **前置/后置脚本**：支持用例执行前后的自定义脚本
- ✅ **多线程执行**：支持多线程并发执行测试用例
- ✅ **详细日志记录**：完整的测试执行日志和结果记录
- ✅ **文件上传支持**：支持 multipart/form-data 文件上传
- ✅ **JSONPath 数据提取**：支持从响应中提取数据
- ✅ **正则表达式提取**：支持正则表达式提取数据
- ✅ **自定义工具函数**：支持自定义全局工具函数

## 📁 目录结构

```
apitestengine/
├── core/
│   ├── cases.py      # 核心测试用例类和生成逻辑
│   ├── runner.py     # 测试运行器和结果处理
│   ├── DBClient.py   # 数据库客户端
│   └── tools.py      # 工具函数（随机数据生成、加密等）
└── README.md         # 本文档
```

## 🔧 核心模块说明

### 1. cases.py - 核心测试逻辑

#### BaseEnv - 环境变量类
```python
class BaseEnv(dict):
    """环境变量字典类，支持属性方式访问"""
    pass
```

- 全局环境变量：`ENV` - 所有测试用例共享
- 临时环境变量：`self.env` - 每个测试类独享

#### GenerateCase - 测试用例生成器
```python
class GenerateCase:
    """解析测试数据，动态创建测试用例"""
    
    def data_to_suite(self, datas):
        """根据测试数据生成测试套件"""
        pass
    
    def create_test_class(self, item):
        """动态创建测试类"""
        pass
    
    def create_test_func(self, func, case_):
        """动态创建测试方法"""
        pass
```

**工作原理：**
1. 接收测试数据（JSON 格式）
2. 为每个测试套件动态创建测试类
3. 为每个测试用例动态创建测试方法（方法名：`test_01`, `test_02`...）
4. 将测试类添加到 unittest.TestSuite

#### BaseTest - 测试基类
```python
class BaseTest(unittest.TestCase, CaseRunLog):
    """所有测试用例的基类"""
```

**主要功能：**
- 发送 HTTP 请求
- 执行前置/后置脚本
- 环境变量管理
- 数据提取（JSONPath、正则）
- 断言验证
- 日志记录

#### CaseRunLog - 日志记录类
提供多级别日志：
- `debug_log()` - 调试日志
- `info_log()` - 信息日志
- `warning_log()` - 警告日志
- `error_log()` - 错误日志
- `exception_log()` - 异常日志
- `critical_log()` - 严重错误日志

### 2. runner.py - 测试运行器

#### TestResult - 自定义测试结果
```python
class TestResult(unittest.TestResult):
    """自定义测试结果记录"""
    
    result = {
        "all": 0,        # 总用例数
        "success": 0,    # 成功数
        "fail": 0,       # 失败数
        "error": 0,      # 错误数
        "cases": [],     # 用例详情列表
        "state": "",     # 状态（success/fail/error）
        "name": ""       # 测试类名
    }
```

#### TestRunner - 测试运行器
```python
class TestRunner:
    """支持多线程执行的测试运行器"""
    
    def run(self, thread_count=1):
        """执行测试套件"""
        pass
```

**特性：**
- 支持多线程并发执行
- 自动按测试类拆分测试套件
- 汇总测试结果

### 3. DBClient.py - 数据库客户端

```python
class DBClient:
    """数据库连接管理器"""
    
    def init_connect(self, DB):
        """初始化数据库连接"""
        pass
    
    def close_connect(self):
        """关闭所有数据库连接"""
        pass
```

**支持的数据库：**
- MySQL（通过 `pymysql`）

**使用方式：**
在测试脚本中通过 `db.数据库名` 访问数据库实例。

### 4. tools.py - 工具函数

提供常用的工具函数：
- **随机数据生成**：`random_mobile()`, `random_name()`, `random_email()` 等
- **加密工具**：`md5_encrypt()`, `base64_encode()`, `rsa_encrypt()`
- **时间工具**：`get_timestamp()`

## 📝 使用方法

### 基本使用

```python
from apitestengine.core.cases import run_test

# 测试数据
case_data = [
    {
        "name": "用户接口测试",  # 测试套件名称
        "Cases": [
            {
                "title": "用户登录",
                "interface": {
                    "url": "/api/login",
                    "method": "POST"
                },
                "headers": {
                    "Content-Type": "application/json"
                },
                "request": {
                    "json": {
                        "username": "testuser",
                        "password": "testpass"
                    }
                },
                "setup_script": "",      # 前置脚本（可选）
                "teardown_script": ""   # 后置脚本（可选）
            }
        ]
    }
]

# 环境配置
env_config = {
    "ENV": {
        "host": "http://api.example.com",
        "headers": {
            "Authorization": "Bearer token123"
        }
    },
    "DB": [
        {
            "name": "test_db",
            "type": "mysql",
            "config": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "password",
                "database": "testdb"
            }
        }
    ],
    "global_func": """
from apitestengine.core.tools import *
# 自定义函数
def custom_function():
    return "custom_value"
"""
}

# 执行测试
result, debug_env = run_test(
    case_data=case_data,
    env_config=env_config,
    thread_count=1,  # 线程数
    debug=True        # 调试模式
)
```

### 测试数据格式说明

#### 测试套件结构
```python
{
    "name": "测试套件名称",  # 可选，默认 "Demo"
    "Cases": [
        # 测试用例列表
    ]
}
```

#### 测试用例结构
```python
{
    "title": "用例标题",           # 用例描述
    "interface": {                 # 接口信息
        "url": "/api/endpoint",    # 接口路径（相对或绝对URL）
        "method": "GET"            # 请求方法：GET, POST, PUT, DELETE 等
    },
    "headers": {                   # 请求头（可选）
        "Content-Type": "application/json"
    },
    "request": {                   # 请求参数
        "json": {},                # JSON 请求体
        "data": {},                # Form 数据
        "params": {},               # URL 参数
        "files": {},                # 文件上传
        "timeout": 30               # 超时时间
    },
    "file": {                      # 文件上传（可选）
        "file_field": [
            "filename.txt",        # 文件名
            "/path/to/file.txt",   # 文件路径
            "text/plain"           # MIME 类型
        ]
    },
    "setup_script": "",            # 前置脚本（Python 代码字符串）
    "teardown_script": ""          # 后置脚本（Python 代码字符串）
}
```

### 环境变量使用

#### 变量引用语法
使用 `${{变量名}}` 引用环境变量：

```python
{
    "request": {
        "json": {
            "user_id": "${{user_id}}",      # 引用环境变量
            "token": "${{token}}"
        }
    }
}
```

#### 设置环境变量

**前置脚本中设置：**
```python
"setup_script": """
# 设置临时变量（仅当前测试类可用）
save_env_variable('user_id', 1001)

# 设置全局变量（所有测试用例可用）
save_global_variable('token', 'abc123')
"""
```

**后置脚本中设置：**
```python
"teardown_script": """
# 从响应中提取数据并保存
user_id = json_extract(response.json(), '$.data.user_id')
save_env_variable('user_id', user_id)
"""
```

### 数据提取

#### JSONPath 提取
```python
"teardown_script": """
# 从 JSON 响应中提取数据
user_id = json_extract(response.json(), '$.data.user_id')
token = json_extract(response.json(), '$.data.token')
"""
```

**JSONPath 示例：**
- `$.data.user_id` - 提取 user_id
- `$.data.users[0].name` - 提取第一个用户的名称
- `$.data.*.id` - 提取所有 id

#### 正则表达式提取
```python
"teardown_script": """
# 从响应文本中提取数据
token = re_extract(response.text, r'token=(\w+)')
"""
```

### 断言验证

```python
"teardown_script": """
# 断言状态码
assertion("相等", 200, status_cede)

# 断言响应内容
response_data = response.json()
assertion("相等", "success", response_data['code'])
assertion("包含", "登录成功", response_data['message'])
"""
```

**支持的断言方法：**
- `"相等"` - 使用 `assertEqual`
- `"包含"` - 使用 `assertIn`

### 数据库操作

```python
"setup_script": """
# 查询数据库
result = db.test_db.execute("SELECT * FROM users WHERE id = 1")
user_id = result['id']

# 执行更新
db.test_db.execute("UPDATE users SET status = 1 WHERE id = 1")

# 查询多条
users = db.test_db.execute_all("SELECT * FROM users")
"""
```

**注意事项：**
- 数据库连接在 `env_config` 中配置
- 通过 `db.数据库名` 访问数据库实例
- 数据库连接在执行完成后自动关闭

### 前置/后置脚本

#### 前置脚本（setup_script）
在发送请求前执行，通常用于：
- 准备测试数据
- 设置环境变量
- 数据库查询
- 调用工具函数生成数据

```python
"setup_script": """
# 生成随机数据
mobile = random_mobile()
email = random_email()

# 设置变量
save_env_variable('mobile', mobile)
save_env_variable('email', email)

# 查询数据库
user = db.test_db.execute("SELECT * FROM users WHERE id = 1")
save_env_variable('user_id', user['id'])
"""
```

#### 后置脚本（teardown_script）
在收到响应后执行，通常用于：
- 提取响应数据
- 设置环境变量供后续用例使用
- 断言验证
- 数据库验证

```python
"teardown_script": """
# 提取响应数据
response_data = response.json()
token = json_extract(response_data, '$.data.token')
user_id = json_extract(response_data, '$.data.user_id')

# 保存变量
save_env_variable('token', token)
save_global_variable('user_id', user_id)

# 断言
assertion("相等", 200, status_cede)
assertion("包含", "成功", response_data['message'])
"""
```

**可用对象：**
- `response` - requests.Response 对象
- `status_cede` - 响应状态码
- `response_header` - 响应头字典
- `response_body` - 响应体（JSON 字符串）
- `requests_header` - 请求头字典
- `requests_body` - 请求体（JSON 字符串）
- `url` - 请求 URL
- `method` - 请求方法

### 文件上传

```python
{
    "interface": {
        "url": "/api/upload",
        "method": "POST"
    },
    "file": {
        "file": [
            "test.txt",              # 字段名
            "/path/to/test.txt",     # 文件路径
            "text/plain"             # MIME 类型
        ],
        "avatar": [
            "avatar.jpg",
            "/path/to/avatar.jpg",
            "image/jpeg"
        ]
    }
}
```

## 🔄 执行流程

```
1. 调用 run_test() 函数
   ↓
2. 初始化环境配置（ENV、DB、global_func）
   ↓
3. GenerateCase.data_to_suite() 生成测试套件
   ├─ 为每个测试套件创建测试类
   └─ 为每个测试用例创建测试方法
   ↓
4. TestRunner.run() 执行测试
   ├─ 按测试类拆分套件（支持多线程）
   ├─ 执行测试用例
   │   ├─ setUpClass() 初始化测试类
   │   ├─ setUp() 初始化测试方法
   │   ├─ perform() 执行测试
   │   │   ├─ __run_log() 输出日志
   │   │   ├─ __run_setup_script() 执行前置脚本
   │   │   ├─ __send_request() 发送请求
   │   │   └─ __run_teardown_script() 执行后置脚本
   │   └─ tearDown() 清理
   └─ tearDownClass() 清理测试类
   ↓
5. 汇总测试结果
   ↓
6. 关闭数据库连接
   ↓
7. 返回结果
```

## 📊 返回结果格式

### Debug 模式返回
```python
result, debug_env = run_test(..., debug=True)

# result 结构
{
    "all": 10,           # 总用例数
    "success": 8,        # 成功数
    "fail": 1,           # 失败数
    "error": 1,          # 错误数
    "results": [
        {
            "name": "用户接口测试",  # 测试类名
            "all": 5,
            "success": 4,
            "fail": 1,
            "error": 0,
            "state": "fail",
            "cases": [
                {
                    "name": "用户登录",      # 用例标题
                    "state": "成功",         # 状态
                    "run_time": "0.123s",    # 执行时间
                    "log_data": [...]        # 日志数据
                },
                # ... 更多用例
            ]
        }
    ]
}

# debug_env 结构（全局环境变量）
{
    "host": "http://api.example.com",
    "headers": {...},
    "token": "abc123",
    "user_id": 1001,
    # ... 其他变量
}
```

### 非 Debug 模式返回
```python
result = run_test(..., debug=False)
# 只返回 result，不返回 debug_env
```

## 🎨 高级用法

### 1. 多线程执行

```python
result = run_test(
    case_data=case_data,
    env_config=env_config,
    thread_count=5,  # 5个线程并发执行
    debug=False
)
```

**注意：**
- 多线程时，每个测试类在独立线程中执行
- 如果多个测试类共享全局变量，可能出现资源竞争
- 建议每个测试类使用独立的数据

### 2. 自定义工具函数

```python
env_config = {
    "ENV": {...},
    "global_func": """
from apitestengine.core.tools import *

def generate_order_id():
    '''生成订单ID'''
    import uuid
    return str(uuid.uuid4())

def encrypt_password(password):
    '''加密密码'''
    return md5_encrypt(password)
"""
}
```

在前置/后置脚本中使用：
```python
"setup_script": """
order_id = generate_order_id()
password = encrypt_password("123456")
save_env_variable('order_id', order_id)
"""
```

### 3. 变量优先级

变量查找顺序：
1. 临时变量（`self.env`）- 当前测试类
2. 全局变量（`ENV`）- 所有测试用例共享

如果变量在临时变量和全局变量中都存在，优先使用临时变量。

### 4. URL 处理

- 如果 URL 以 `http://` 或 `https://` 开头，直接使用
- 否则，自动拼接 `ENV['host']` + URL

```python
# 绝对 URL
"url": "http://api.example.com/login"  # 直接使用

# 相对 URL
"url": "/api/login"  # 自动拼接为 http://api.example.com/api/login
```

## ⚠️ 注意事项

1. **变量引用语法**：必须使用 `${{变量名}}` 格式
2. **脚本执行**：前置/后置脚本中的代码会直接 `exec()` 执行，注意安全性
3. **数据库连接**：确保数据库配置正确，连接会在执行完成后自动关闭
4. **文件路径**：文件上传时，确保文件路径存在且可读
5. **调试模式**：Debug 模式下，临时变量会保存到全局变量，便于调试
6. **多线程**：多线程执行时，避免测试类之间的数据依赖

## 🔍 调试技巧

1. **开启 Debug 模式**：查看详细的日志输出
2. **使用 print()**：在脚本中使用 `print()` 输出调试信息（会被记录到日志）
3. **查看日志**：检查 `log_data` 字段中的详细日志
4. **检查环境变量**：使用 `debug_log()` 输出环境变量状态

## 📚 项目中的使用示例

在 `test_backend/apps/testplans/tasks.py` 中可以看到实际使用：

```python
from apitestengine.core.cases import run_test

def run_test_step(case, env_id):
    """执行单条测试步骤"""
    env = TestEnv.objects.get(id=env_id)
    config = __get_env_config(env)
    
    res, debug_var = run_test(
        case_data=[{"Cases": [case]}], 
        env_config=config, 
        debug=True
    )
    
    result = res['results'][0]['cases'][0]
    env.debug_global_variable = debug_var
    env.save()
    return result
```

## 🛠️ 扩展开发

### 添加新的断言方法

在 `BaseTest.assertion()` 方法中添加：

```python
methods_map = {
    "相等": self.assertEqual,
    "包含": self.assertIn,
    "大于": self.assertGreater,  # 新增
    "小于": self.assertLess,      # 新增
}
```

### 添加新的数据库类型

在 `DBClient.py` 中添加新的数据库类，类似 `DBMysql`。

## 📞 联系方式

- 作者：litao
- 邮箱：litao163email@163.com

---

**版本：** 1.0  
**最后更新：** 2025/4/26

