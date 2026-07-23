"""
test_07.py — pytest parametrize：每行数据自动变成一个独立用例
===============================================================

对比 test_05 的 for 循环方式：
    test_05：3行数据 → 1个测试用例 → 哪行挂了不知道
    test_07：3行数据 → 3个测试用例 → 挂哪个一目了然

==============================================================================
核心语法拆解：
==============================================================================

① 数据列表（相当于 CSV 文件的内容）
    test_data = [
        ("用户名1", "密码1", 预期状态码1),    ← 一个元组 = 一组数据
        ("用户名2", "密码2", 预期状态码2),
    ]

② 装饰器（@ 开头的那行，放在 def 上一行）
    @pytest.mark.parametrize("参数名1,参数名2,参数名3", test_data)
                             └───────────────────┘  └───────┘
                             函数里要用的参数名        数据从哪来

③ 测试函数（参数名跟装饰器里声明的对上就行）
    def test_xxx(参数名1, 参数名2, 参数名3):
        # 直接用参数名，不用 row["列名"]，比 CSV 更简单

==============================================================================
parametrize vs CSV（test_05）对比：
==============================================================================

                    CSV + for 循环              parametrize
                    ─────────────               ────────────
    数据格式         CSV 文件                     Python 列表/元组
    用例数量         1 个（循环包在一起）          N 个（每组数据一个）
    挂了定位         看 print 日志               输出直接显示是哪组数据
    适用场景         数据量大的时候               数据量中等，要清晰报告
"""

import requests
import pytest

# ============================================================
# 准备数据：一个列表，每个元组就是一组测试数据
# ============================================================
# 元组格式：(用户名, 密码, 预期状态码)
# 3 个元组 = 生成 3 个测试用例
test_data = [
    ("Qiucen_Lyu", "123456", 200),     # 正常登录
    ("testuser",   "abcdef", 200),     # 正常登录
    ("",           "",       200),     # 空用户名密码（echo 接口不校验）
]

# ============================================================
# @pytest.mark.parametrize 装饰器
# ============================================================
# 第一个参数：字符串，"参数名1,参数名2,参数名3"（逗号分隔）
# 第二个参数：数据列表
#
# pytest 做的事：
#   取 test_data 第一行 → ("Qiucen_Lyu", "123456", 200)
#   拆开赋给函数参数 → username="Qiucen_Lyu", password="123456", expected_status=200
#   执行函数 → 生成用例 test_登录多组数据[Qiucen_Lyu-123456-200]
#   再取第二行... 循环直到数据用完
@pytest.mark.parametrize("username,password,expected_status", test_data)
def test_登录多组数据(username, password, expected_status):
    """
    这个函数会被 pytest 调用 3 次，每次传不同的参数
    第1次：username="Qiucen_Lyu", password="123456", expected_status=200
    第2次：username="testuser",    password="abcdef", expected_status=200
    第3次：username="",            password="",       expected_status=200
    """
    r = requests.post(
        "https://postman-echo.com/post",
        json={"username": username, "password": password}
    )
    assert r.status_code == expected_status

# ============================================================
# 注意：
# ============================================================
# 你电脑上必须用 python -m pytest，不能用裸 pytest
#   ✅ python -m pytest python_learning/test_07.py -v
#   ❌ pytest python_learning/test_07.py -v  （可能用错 Python 环境）
#
# 原因：电脑上有两个 Python（Anaconda + Microsoft Store），
#       裸 pytest 指向旧版本，不支持 parametrize
