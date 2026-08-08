"""
project_github_api/conftest.py — GitHub API 测试公共配置
==========================================================

【你写 conftest 的标准模板 —— 以后所有项目就这样起手】
    ① import pytest + import os
    ② @pytest.fixture(scope="session") def base_url() → return 固定地址
    ③ @pytest.fixture(scope="session") def api_token() → return os.environ["KEY"]
    ④ @pytest.fixture(scope="session") def auth_headers(api_token) → return {"Authorization": ...}

【设计思路】
    三个 fixture 层层依赖：
        base_url → 独立的，不依赖别人
        api_token → 独立的，从环境变量读
        auth_headers → 依赖 api_token，用它拼 "Bearer xxx"

    为什么 auth_headers 不依赖 base_url？
    → 请求头跟 URL 没关系。每个 fixture 只做一件事，不乱耦合。

【跟前两个项目对比】
    project_bookstore/conftest.py → base_url（只有 URL，不需要 Token）
    project_ai_test/conftest.py   → api_url + api_key（Token 叫 key）
    project_github_api/conftest.py → base_url + api_token + auth_headers（Token 叫 token，且多了 headers 组装）

    三个项目都是同一套逻辑，只是参数名和 URL 不同。
"""
import pytest
import os


@pytest.fixture(scope="session")
def base_url():
    """GitHub API 根地址 —— 后面拼 /users /repos /issues"""
    return "https://api.github.com"


@pytest.fixture(scope="session")
def api_token():
    """
    从环境变量读 GitHub Personal Access Token

    设环境变量步骤（忘了回去翻 AI 测试项目的教程）：
        Win 键 → 搜"环境变量" → 用户变量 → 新建
        变量名：GITHUB_TOKEN
        变量值：ghp_你的Token
    """
    return os.environ["GITHUB_TOKEN"]


@pytest.fixture(scope="session")
def auth_headers(api_token):
    """
    组装请求头 —— Token 装进 Bearer

    后面的测试函数直接当参数用，不需要手动拼 Authorization 那一行。
    这就是 fixture 的价值：写一次，处处用。
    """
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
