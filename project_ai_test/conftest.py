"""
project_ai_test/conftest.py — AI 测试项目公共配置

对照图书管理项目：
    project_bookstore/conftest.py → base_url = "https://jsonplaceholder..."
    project_ai_test/conftest.py   → 同样的模式，只是换成了 AI API 的地址和 key
"""
import pytest
import os


@pytest.fixture(scope="session")
def api_key():
    """从环境变量读取 API Key（不写死在代码里，安全）"""
    return os.environ["DEEPSEEK_KEY"]


@pytest.fixture(scope="session")
def api_url():
    """DeepSeek API 地址（跟 OpenAI 接口兼容）"""
    return "https://api.deepseek.com/v1/chat/completions"
