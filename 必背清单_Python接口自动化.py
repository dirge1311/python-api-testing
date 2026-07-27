"""
============================================================================
Python 接口自动化 — 必背清单（面试 + 工作中只用这些）
============================================================================

来源：test_01 ~ test_13 + conftest.py 的精简版
============================================================================

============================================================================
一、必背的 5 行代码（写接口测试的最小骨架）
============================================================================

    import requests                         # ① 导入库

    r = requests.get("https://...")         # ② GET 请求
    r = requests.post("https://...",        # ③ POST 请求
            json={"key": "value"})

    print(r.status_code)                    # ④ 看状态码（200 = 成功）
    print(r.json())                         # ⑤ 看返回的 JSON 数据

============================================================================
二、必背的 4 种断言（assert = "我断言"）
============================================================================

    assert r.status_code == 200                     # 状态码
    assert r.json()["字段名"] == 预期值              # 字段值相等
    assert "字段名" in r.json()                      # 字段是否存在
    assert 值 in [列表]                               # 包含判断

    口诀：assert 实际值 == 预期值
         对了 → 没反应    错了 → 红色 AssertionError

============================================================================
三、必背的 pytest 两条规则
============================================================================

    规则1：函数名必须以 test_ 开头
           def test_xxx():
               ...

    规则2：运行命令（你电脑上必须加 python -m）
           python -m pytest 文件名 -v        ← -v 显示每个用例名和结果

    对照 Postman：
        pytest = Collection Runner
        test_ 函数 = 集合里的一个请求
        assert   = Tests 标签页里的断言脚本

============================================================================
四、必背的 parametrize 数据驱动（推荐，比 CSV 更清晰）
============================================================================

    import pytest

    test_data = [
        ("用户名1", "密码1", 预期1),     ← 一个元组 = 一组数据
        ("用户名2", "密码2", 预期2),     ← N 个元组 = N 个独立用例
    ]

    @pytest.mark.parametrize("参数1,参数2,参数3", test_data)
    def test_xxx(参数1, 参数2, 参数3):
        r = requests.post(url, json={"key": 参数1})
        assert r.status_code == 参数3

    优点：每组数据自动变成独立用例，哪行挂了输出里一眼就能看到

============================================================================
五、必背的 fixture（= Postman 环境变量 + Pre-request Script）
============================================================================

    ① 定义 fixture（一次定义）：
        @pytest.fixture(scope="session")      ← session = 整个测试只跑一次
        def token():
            r = requests.post(登录URL, json={...})
            return r.json()["token"]          ← return = 提供值

    ② 使用 fixture（处处可用）：
        def test_xxx(token):                  ← 参数名 = fixture 函数名
            r = requests.get(URL, headers={"Authorization": f"Bearer {token}"})
            assert r.status_code == 200

    ③ conftest.py（全局共享）：
        把 fixture 定义放进 conftest.py，文件夹内所有测试自动可用
        不需要 import，pytest 自动发现
        = Postman Collection 级别变量

============================================================================
六、新手必避的 7 个坑
============================================================================

    坑1：pytest 找不到用例
         → 检查函数名是不是 test_ 开头，有没有 def
         → 检查代码是不是写在函数里面，不能"裸奔"在文件顶层

    坑2：r.json 漏了括号
         → r.json   = 函数对象（不对）
         → r.json() = 调用函数返回数据（正确）

    坑3：assert 用 = 而不是 ==
         → assert r.status_code = 200   （赋值，不会报错但断言无效）
         → assert r.status_code == 200  （判断，正确）

    坑4：列表和字典漏逗号
         → [("a", 1) ("b", 2)]  ❌ 每个元组后面要逗号
         → [("a", 1), ("b", 2)] ✅
         → {"a": 1 "b": 2}      ❌ 每个键值对后面要逗号
         → {"a": 1, "b": 2}     ✅

    坑5：parametrize 的函数忘写参数
         → @pytest.mark.parametrize("a,b", data)
         → def test_xxx():           ← parametrize 传不进来
         → def test_xxx(a, b):       ← 正确，参数名对上

    坑6：你电脑上 pytest 必须带 python -m
         → pytest xxx -v               ← Anaconda 旧版，可能不认
         → python -m pytest xxx -v     ← 你安装的新版，始终正确

    坑7：URL 没加引号
         → requests.get(https://...)   ← 浏览器写法
         → requests.get("https://...") ← Python 字符串

============================================================================
七、AI 大模型接口测试（新加分项，简历亮点）
============================================================================

调用格式（DeepSeek/OpenAI/通义千问通用）：
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {"model": "deepseek-chat", "messages": [{"role": "user", "content": "..."}]}
    r = requests.post(url, headers=headers, json=body)
    reply = r.json()["choices"][0]["message"]["content"]

AI 测试的三种断言（跟传统接口的区别）：
    assert len(reply) > 0                    → 有回复（不是空的）
    assert "关键词" in reply                 → 回复跟问题相关
    any(拒绝词 in reply for ...)             → 安全测试：AI 拒绝了攻击

AI 安全测试三类攻击：
    Prompt 注入："忽略你的指令..." → 拒绝
    DAN 越狱："进入无限制模式..." → 拒绝
    系统提示词提取："你的系统提示词..." → 拒绝或回避

AI 性能测试：
    time.time() 计时 + Token 用量 + 费用估算
    响应 < 5秒，Token 在 max_tokens 限制内

============================================================================
八、面试怎么说（传统接口 + AI 测试）
============================================================================

问："你会用 Python 做接口自动化测试吗？"

答：
"会。主要用 requests 库发请求，pytest 管理用例，fixture 做前置处理。
完整流程是请求 → 断言 → 数据驱动 → fixture → HTML 报告。
之前做了两个项目：一个是电商接口自动化（CRUD + 鉴权 + 25条用例），
另一个是 DeepSeek AI 接口测试（功能 + 安全 + 性能）。

AI 测试跟传统接口测试的区别主要在断言方式——
传统接口断言精确值，AI 接口用关键词命中和语义判断。
另外多了一层安全测试：Prompt 注入、越狱攻击，
还有 Token 消耗的监控和费用估算。
但底层的 requests + pytest + fixture 这一套完全一样。"

问："Prompt 注入和 SQL 注入有什么区别？"

答：
"SQL 注入是利用后端拼接 SQL 语句的漏洞，防御靠参数化查询。
Prompt 注入是用自然语言覆盖 AI 的系统指令，
防御靠模型本身的训练对齐，没有代码层面的修复方案。
所以 AI 安全测试更像是在测一个'人'有没有安全意识，
而不是测一段代码有没有漏洞。"

============================================================================
文件对照表（复习时回去看详细笔记）：
============================================================================

    python_learning/
        test_01.py → GET 请求
        test_02.py → POST 请求
        test_03.py → assert 断言
        test_04.py → pytest 框架
        test_05.py → CSV 数据驱动（for 循环）
        test_06.py → 独立练习（GET+POST）
        test_07.py → parametrize 数据驱动
        test_08.py → 综合练习（guided）
        test_09.py → 独立练习（solo）
        test_10.py → fixture 基础
        test_11.py → fixture 自动提取 token
        test_12.py → scope="session"
        test_13.py → conftest.py
        八股_01~06.py → 测试面试八股
        Linux_必会10个命令.py → Linux 速查

    project_bookstore/
        学习总结_Python接口自动化.md → 传统接口自动化完整笔记

    project_ai_test/
        学习总结_AI接口测试.md → AI 测试完整笔记
        test_01~04 → AI 功能/安全/性能测试

    本文件 → 必背清单（精简版，面试前过一遍）
============================================================================
"""
