"""
conftest.py — pytest 自动发现，全文件夹共享
=============================================

这是什么？
    跟每个 test_*.py 放在同一个文件夹里的特殊文件
    pytest 启动时会自动读它，里面的 fixture 不需要 import 就能用

对照 Postman：
    Postman Collection 级别变量 —— 定义一次，集合里所有请求自动能引用
    conftest.py               —— 定义一次，文件夹里所有 test_ 文件自动能用

作用域：
    当前文件夹 + 所有子文件夹（除非子文件夹有自己的 conftest）

==============================================================================
这个文件里有什么：
==============================================================================
    token fixture（scope="session"）
        → 整个测试会话只登录一次
        → 任何 test_ 文件都能直接用，参数里写 token 就行
        → 省掉每个文件重复写"登录→提取token"的代码

    后续可以往这里加：
        @pytest.fixture(scope="session")
        def base_url():
            return "https://api.xxx.com"     ← 统一的基础 URL

        @pytest.fixture(scope="function")
        def db_connection():
            ...                               ← 数据库连接

==============================================================================
"""
import pytest
import requests


@pytest.fixture(scope="session")
def token():
    """全项目共享的登录 token —— 只登录一次"""
    r = requests.post(
        "https://postman-echo.com/post",
        json={"username": "admin", "password": "123456"}
    )
    return r.json()["json"]["username"]
