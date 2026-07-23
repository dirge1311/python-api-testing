"""
test_08.py — 综合练习：parametrize + 普通函数混用
===================================================

本文件包含：
    test_注册用户() → parametrize 数据驱动，3组数据 → 3个用例
    test_查询用户() → 普通函数，1个用例

你已经掌握的能力：
    ✅ GET / POST 请求
    ✅ assert 断言（状态码、字段存在、字段值）
    ✅ pytest 组织用例
    ✅ parametrize 数据驱动（每组数据自动变独立用例）
"""

import requests
import pytest


# ============================================================
# 函数1：用户注册 — parametrize 数据驱动
# ============================================================
# 数据列表：每个元组 = (用户名, 邮箱, 年龄, 预期状态码)
test_data = [
    ("zhangsan", "zhangsan@test.com", 25, 200),
    ("lisi",     "lisa@test.com",     30, 200),
    ("wangwu",   "wangwu@test.com",   28, 200),
]

# @parametrize 会把 test_data 拆开，每组数据生成一个独立用例
# 输出会显示：test_注册用户[zhangsan-zhangsan@test.com-25-200]  ← 清晰的用例名
@pytest.mark.parametrize("username,email,age,expected_status", test_data)
def test_注册用户(username, email, age, expected_status):
    """测试用户注册接口 —— 3组数据，每组跑一次"""
    # POST 请求，把用户名、邮箱、年龄都发过去
    r = requests.post(
        "https://postman-echo.com/post",
        json={
            "username": username,
            "email": email,
            "age": age
        }
    )
    # 断言1：状态码正确
    assert r.status_code == expected_status

    # 断言2：服务器正确识别了 JSON 格式
    # "json" 字段存在 = 服务器成功解析了 JSON Body
    assert "json" in r.json()


# ============================================================
# 函数2：用户查询 — 普通测试函数
# ============================================================
def test_查询用户():
    """测试用户查询接口 —— 根据 user_id 查询"""
    # GET 请求，URL 参数 user_id=001
    r = requests.get("https://postman-echo.com/get?user_id=001")

    # 断言1：状态码 200
    assert r.status_code == 200

    # 断言2：返回的 args 里 user_id 等于 "001"
    # r.json()["args"]["user_id"] 就是服务器收到的那个参数值
    assert r.json()["args"]["user_id"] == "001"

# ============================================================
# 踩过的坑（已修复）：
# ============================================================
# 坑1：parametrize 的 def 要顶格写，不能套在外层函数里
# 坑2：URL 必须加引号，https://... 是浏览器写法，Python 要 "https://..."
# 坑3：没有定义过的变量不能拿来 assert（expected_status 只在 parametrize 函数里有）
