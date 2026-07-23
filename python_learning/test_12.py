"""
test_12.py — fixture scope="session"：一次登录，全用例共享
=============================================================

问题：test_11 里，每个用到 token 的用例都会重新执行 fixture
      → 100 个用例 = 登录 100 次 → 太慢，浪费资源

解决：scope="session" → 整个测试跑完只登录一次

==============================================================================
scope 四种级别（像 Postman 变量作用域）：
==============================================================================

    scope="function"（默认）：每个测试函数跑一次 fixture
    scope="class"           ：每个测试类跑一次
    scope="module"          ：每个 .py 文件跑一次
    scope="session"         ：整个测试跑一次（最常用，= 全局只登录一次）

    对照 Postman：
        function → Local 变量（每个请求独立）
        session  → Global 变量（整个集合共享，跟你的 {{token}} 一样）

==============================================================================
"""
import pytest
import requests


# scope="session" = 整个测试会话只执行一次
# 第一个用到 token 的用例触发登录，后续用例直接复用结果
@pytest.fixture(scope="session")
def token():
    """登录只跑一次，所有用例共用同一个 token"""
    r = requests.post(
        "https://postman-echo.com/post",
        json={"username": "admin", "password": "123456"}
    )
    return r.json()["json"]["username"]


def test_用例1(token):
    """第1个用例 —— 用 token 发请求"""
    r = requests.get(
        "https://postman-echo.com/get",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200


def test_用例2(token):
    """第2个用例 —— 用同一个 token"""
    r = requests.get(
        "https://postman-echo.com/get",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200

# ============================================================
# fixture 速查：
# ============================================================
#   @pytest.fixture                    → 默认 function 级别，每个用例跑一次
#   @pytest.fixture(scope="session")   → 整个测试只跑一次（推荐用于登录）
#   @pytest.fixture(scope="module")    → 每个 .py 文件跑一次
# ============================================================
