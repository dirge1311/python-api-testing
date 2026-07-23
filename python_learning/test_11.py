"""
test_11.py — fixture 进阶：自动登录 + 提取 token
===================================================

对照 Postman 你烂熟于心的流程：
    Postman                                pytest fixture
    ────────                               ──────────────
    ① POST 登录请求                         fixture 函数体里发 requests.post()
    ② Tests 标签页提取 token                函数体里 return 取出来的值
    ③ 存进环境变量 {{token}}                return 的值自动传给测试函数
    ④ 后续接口引用 {{token}}                测试函数参数里写 token，直接用

关键理解：
    测试函数参数名 = fixture 函数名  →  pytest 自动匹配，自动传值
    不需要 import，不需要赋值，不需要写任何胶水代码

=======================================================================
具体到这个文件：
=======================================================================

    token fixture 做的事：
        1. 发 POST 登录
        2. 从响应里取出 data["json"]["username"]
        3. return 给测试函数

    test_用token发请求 做的事：
        1. 参数里写 token → pytest 自动把 fixture 返回值传进来
        2. 拼到 Authorization header 里
        3. 发 GET 请求 + 断言

    这跟你电商项目里"登录 → 提取 Token → 后续接口携带 Token"
    是同一套流程，只是从手动变成了自动。
"""

import pytest
import requests


# ============================================================
# fixture：自动登录，返回 token
# ============================================================
# 每次有测试函数需要 token，pytest 就会执行这个函数
# return 的值就是测试函数收到的那个参数
@pytest.fixture
def token():
    """自动登录，提取并返回 token"""
    # ① 发登录请求（= Postman 里 POST + Body 填用户名密码 + 点 Send）
    r = requests.post(
        "https://postman-echo.com/post",
        json={"username": "admin", "password": "123456"}
    )

    # ② 拆开响应 JSON
    data = r.json()

    # ③ 提取"token"并返回
    #    真实项目里通常是 data["data"]["token"] 或 data["token"]
    #    这里用 echo 接口模拟，把 username 当场 token 用
    return data["json"]["username"]


# ============================================================
# 测试函数：直接用 token
# ============================================================
def test_用token发请求(token):
    """发 GET 请求，自动携带 token"""
    # 拼 Authorization header
    # f"Bearer {token}" = Postman 里的 "Bearer {{token}}"
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(
        "https://postman-echo.com/get",
        headers=headers
    )

    assert r.status_code == 200

    # 额外验证：确认服务器收到了 Authorization header
    assert "authorization" in r.json()["headers"]

# ============================================================
# 下一步会学的：
# ============================================================
#   如果多个测试函数都要用 token，每个函数跑一次 fixture 就太慢了
#   → fixture scope="session"：只登录一次，所有测试共享同一个 token
# ============================================================
