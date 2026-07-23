"""
test_13.py — conftest.py 实战：fixture 不在本文件，但自动能找到
================================================================

注意看这个文件：
    ❌ 没有 @pytest.fixture
    ❌ 没有 def token()
    ❌ 没有 import conftest.py 的任何东西

    但是 test_用conftest的token(token) 的 token 参数 —— 能用！

    因为 pytest 启动时自动读了同文件夹的 conftest.py，
    发现了里面的 token fixture，然后自动传进来了。

对照 Postman：
    你在 Postman 集合的"变量"里定义了 {{token}}
    集合里的每个请求都能直接用，不需要每个请求里重新定义
    conftest.py 就是这个意思 —— 放进去就不用管了

==============================================================================
你的 fixture 学习路线（完结）：
==============================================================================

    test_10.py → fixture 基础            （= Postman 环境变量）
    test_11.py → fixture 自动提取 token  （= Postman Pre-request Script）
    test_12.py → scope="session"        （= 全局只登录一次）
    test_13.py → conftest.py            （= Collection 级别变量，全文件夹共享）

    这四条 = fixture 的全部核心用法。
==============================================================================
"""
import requests


def test_用conftest的token(token):
    """fixture 来自 conftest.py，本文件看不到它的定义，但能用"""
    r = requests.get(
        "https://postman-echo.com/get",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
