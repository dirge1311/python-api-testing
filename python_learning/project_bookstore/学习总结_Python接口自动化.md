# Python 接口自动化测试 — 学习总结

> 学习时间：2026年7月19日 - 7月23日  
> 学习方式：Postman 对照 Python，一步一步动手实操

---

## 一、学习路线回顾

| 阶段 | 文件 | 内容 | 对照 Postman |
|---|---|---|---|
| 基础 | test_01.py | GET 请求 | Select GET → 填 URL → Send |
| 基础 | test_02.py | POST 请求 | Body → raw → JSON → Send |
| 基础 | test_03.py | assert 断言 | Tests 标签页 pm.expect() |
| 进阶 | test_04.py | pytest 框架 | Collection Runner |
| 进阶 | test_05.py | CSV 数据驱动 | Runner + CSV 加载 |
| 进阶 | test_06.py | 独立练习 | 综合 |
| 进阶 | test_07.py | parametrize | Runner 进阶（行级定位） |
| 进阶 | test_08.py | 引导练习 | 综合 |
| 进阶 | test_09.py | 独立练习 | 脱离模板 |
| 高级 | test_10.py | fixture 基础 | 环境变量 {{base_url}} |
| 高级 | test_11.py | fixture 自动提取 token | Pre-request Script + 提取变量 |
| 高级 | test_12.py | scope="session" | 全局变量（一次登录） |
| 高级 | test_13.py | conftest.py | Collection 级别变量 |
| 项目 | project_bookstore/ | 完整项目实战 | Postman 全流程→Python 自动化 |

---

## 二、必须背下来的东西（面试 + 工作）

### 2.1 发请求（两条命令）

```python
# GET
r = requests.get("URL地址")

# POST
r = requests.post("URL地址", json={"key": "value"})

# PUT（跟 POST 一样）
r = requests.put("URL地址", json={"key": "value"})

# DELETE
r = requests.delete("URL地址")
```

### 2.2 看返回（两条命令）

```python
r.status_code    # 状态码：200=成功  201=创建成功  400=客户端错  500=服务器错
r.json()         # 返回的 JSON 数据（注意括号！）
```

### 2.3 四种断言

```python
assert r.status_code == 200                    # 1. 状态码
assert r.json()["字段名"] == 预期值             # 2. 字段值相等
assert "字段名" in r.json()                     # 3. 字段是否存在
assert 值 in [列表]                              # 4. 包含判断
```

> 口诀：**assert = "我断言"，后面跟判断题，对了没反应，错了红色 AssertionError**

### 2.4 pytest 两条规则

```python
# 规则1：函数名 test_ 开头
def test_用例名():
    ...

# 规则2：运行命令
python -m pytest 文件名 -v    # 你电脑必须加 python -m！
```

### 2.5 parametrize 模板

```python
import pytest

test_data = [
    ("参数1_值1", "参数1_值2", 预期值),    # 一行 = 一个用例
    ("参数2_值1", "参数2_值2", 预期值),
]

@pytest.mark.parametrize("参数名1,参数名2,期望结果", test_data)
def test_xxx(参数名1, 参数名2, 期望结果):
    r = requests.post(url, json={"key": 参数名1})
    assert r.status_code == 期望结果
```

### 2.6 fixture 模板

```python
# 定义（放在 conftest.py 里，全项目共享）
@pytest.fixture(scope="session")        # session = 整个测试只跑一次
def token():
    r = requests.post(登录URL, json={...})
    return r.json()["token"]

# 使用（测试函数参数名 = fixture 函数名）
def test_xxx(token):
    r = requests.get(URL, headers={"Authorization": f"Bearer {token}"})
```

### 2.7 生成测试报告

```bash
python -m pytest 文件夹/ -v --html=report.html --self-contained-html
```

---

## 三、踩过的坑（不用背，但别忘）

| 坑 | 症状 | 原因 | 解决 |
|---|---|---|---|
| r.json 漏括号 | TypeError: argument of type 'method' is not iterable | 写成 `r.json` 没加 `()` | `r.json()` |
| assert 用 = | 断言不生效但无报错 | `=` 是赋值，`==` 才是判断 | `==` |
| 列表漏逗号 | SyntaxError | 每个元素之间要逗号 | `[a, b, c]` |
| 字典漏逗号 | SyntaxError | 每个键值对之间要逗号 | `{"a": 1, "b": 2}` |
| parametrize 函数忘参数 | 数据传不进去 | def 没声明参数名 | `def test_xxx(a, b):` |
| pytest 裸命令不认 | collected 0 items | Anaconda 旧版 pytest | `python -m pytest` |
| URL 忘加引号 | SyntaxError | 浏览器写法 `https://...` | `"https://..."` |
| CSV 列名不对 | KeyError | 代码里的 key 跟 CSV 表头不一致 | 完全一致（含大小写） |

---

## 四、项目实战：图书管理系统 API 自动化

### 项目结构
```
project_bookstore/
├── conftest.py       # 公共 fixture：base_url
├── test_posts.py     # 7 个用例（增删改查 + parametrize）
├── test_auth.py      # 1 个用例（登录拿 token）
├── run_report.py     # 一键运行 + 生成报告
└── report.html       # 可视化测试报告（39KB）
```

### 技术栈
- **requests**：发 HTTP 请求（GET/POST/PUT/DELETE）
- **pytest**：用例管理 + fixture 前置处理
- **pytest.mark.parametrize**：数据驱动测试
- **pytest.fixture + scope="session"**：一次登录，全项目共享
- **conftest.py**：公共 fixture 集中管理
- **pytest-html**：自动生成可视化测试报告

### 简历描述
> 独立完成图书管理系统接口自动化测试，基于 requests + pytest，覆盖 CRUD 全链路 + 鉴权，8 条用例全部通过，使用 parametrize 实现数据驱动（3组数据自动生成3个独立用例），通过 fixture + conftest.py 管理测试前置（base_url、token），使用 pytest-html 产出可视化测试报告。

---

## 五、还没学但应该知道的（后续方向）

1. **Git**：把代码推到 GitHub，简历放链接
2. **Jenkins / GitHub Actions**：CI/CD 自动跑测试
3. **Allure**：比 pytest-html 更好看的测试报告
4. **Postman Newman**：Postman 导出的脚本用命令行跑
5. **Selenium**：Web UI 自动化（不是接口，是操作浏览器）

---

## 六、面试高频问题速答

**Q：你会用 Python 做接口自动化测试吗？**

会。用 requests 发请求，pytest 管理用例，fixture 做前置处理（如登录获取 token），parametrize 做数据驱动测试。一个命令跑完全部用例，通过 pytest-html 生成可视化报告。

**Q：fixture 是什么？跟 Postman 环境变量有什么区别？**

fixture 比环境变量更强——不仅能存值，还能执行代码。比如 token fixture 会自动登录、提取 token、传给后面的用例。scope="session" 保证只登录一次。conftest.py 让所有测试文件自动共享 fixture。

**Q：怎么处理接口关联（上一个接口的返回值作为下一个接口的入参）？**

用 fixture。比如登录返回 token，fixture 里 return token，后面所有用例参数里写 token 就能直接用。pytest 自动处理传递，不需要手动存变量。

**Q：数据驱动怎么做？**

两种方式：① parametrize 装饰器，数据写在 Python 列表里，每组数据自动生成独立用例（推荐）；② CSV 文件 + csv.DictReader + for 循环，适合数据量大的场景。
