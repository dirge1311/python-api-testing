# Python 接口自动化测试 — 图书管理系统

基于 **requests + pytest** 的接口自动化测试项目，覆盖 CRUD 全链路 + 鉴权 + 数据驱动 + HTML 测试报告。

## 项目结构

```
python_learning/
├── test_01.py ~ test_13.py    # 从零学习的 13 个练习文件
├── conftest.py                 # 公共 fixture（token 自动登录）
├── project_bookstore/          # 完整实战项目
│   ├── conftest.py             # base_url fixture
│   ├── test_posts.py           # 文章 CRUD 用例（7 条）
│   ├── test_auth.py            # 鉴权用例
│   ├── run_report.py           # 一键运行 + 生成报告
│   ├── report.html             # 可视化测试报告
│   └── 学习总结_Python接口自动化.md  # 完整学习笔记
└── 必背清单_Python接口自动化.py     # 面试速查卡片
```

## 技术栈

| 工具 | 用途 |
|---|---|
| **requests** | 发送 HTTP 请求（GET/POST/PUT/DELETE） |
| **pytest** | 测试用例管理 + 运行 |
| **pytest.fixture** | 前置处理（自动登录获取 token、base_url 管理） |
| **pytest.mark.parametrize** | 数据驱动测试（每组数据自动生成独立用例） |
| **conftest.py** | 公共 fixture 集中管理（= Postman Collection 变量） |
| **pytest-html** | 自动生成可视化测试报告 |

## 快速开始

```bash
# 1. 安装依赖
pip install requests pytest pytest-html

# 2. 运行全部用例 + 生成 HTML 报告
cd python_learning/project_bookstore
python run_report.py

# 3. 或者只用命令行
python -m pytest . -v --html=report.html --self-contained-html

# 4. 浏览器打开 report.html 查看报告
```

## 测试覆盖

| 模块 | 接口 | 用例数 | 覆盖方式 |
|---|---|---|---|
| 文章管理 | GET /posts | 1 | 查询所有 + 非空校验 |
| 文章管理 | POST /posts | 4 | 单组 + parametrize 3 组数据 |
| 文章管理 | PUT /posts/1 | 1 | 修改文章 + 字段校验 |
| 文章管理 | DELETE /posts/1 | 1 | 删除文章 |
| 鉴权 | POST /posts → GET /posts/1 | 1 | fixture 自动登录 + Bearer Token |

**总计：8 条用例，全部通过**

## 核心技能展示

- ✅ requests 发送 GET/POST/PUT/DELETE 请求
- ✅ assert 四种断言模式（状态码、字段值、字段存在、包含判断）
- ✅ pytest 用例组织 + fixture 前置处理
- ✅ parametrize 数据驱动（3 组数据 → 3 个独立用例）
- ✅ conftest.py 公共配置管理
- ✅ pytest-html 可视化测试报告

## 学习路径

| 文件 | 内容 | 对照 Postman |
|---|---|---|
| test_01.py | GET 请求 | Params + Send |
| test_02.py | POST 请求 | Body → raw → JSON |
| test_03.py | assert 断言 | Tests 标签页 |
| test_04.py | pytest 框架 | Collection Runner |
| test_05.py | CSV 数据驱动 | Runner + CSV |
| test_07.py | parametrize | 行级定位 |
| test_10~13 | fixture + conftest | 环境变量 + Pre-request Script |

> 北京邮电大学 电子信息工程 | 2027 届本科 | 软件测试方向
