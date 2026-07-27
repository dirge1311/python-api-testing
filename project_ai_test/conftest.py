"""
project_ai_test/conftest.py — AI 测试项目公共配置
===================================================

【为什么需要这个文件】
    跟 Postman 的环境变量一样 —— 你把 {{base_url}} 和 {{token}}
    定义一次，所有请求自动能用。conftest.py 就是 Python 里的环境变量。

【对照你之前写过的图书管理项目】
    project_bookstore/conftest.py → base_url = "https://jsonplaceholder..."
    project_ai_test/conftest.py   → api_url + api_key（多了一个 key，因为 AI API 要鉴权）

【设计思路】
    为什么 key 不写死在代码里？
    → API Key 等于你的银行卡密码。写死进代码里，推到 GitHub 上全世界都能看到。
      别人拿到你的 Key 就能用你的额度疯狂调 API，一晚刷掉几千块。
      所以用环境变量 os.environ["DEEPSEEK_KEY"] 读取，代码里不存。

    为什么 scope="session"？
    → 整个测试跑一次就够了，不需要每个用例都读一次环境变量。
      跟 test_12 里 token fixture 加 scope="session" 是同一个道理。

【怎么灵活变通】
    换成别的 AI API（OpenAI / 通义千问 / 文心一言），只改两样：
        ① api_url 换成对应的地址
        ② api_key 的环境变量名换一个

    加更多公共配置（比如请求超时时间）：
        再加一个 fixture：
        @pytest.fixture(scope="session")
        def timeout():
            return 30  # 30 秒超时
"""
import pytest
import os


@pytest.fixture(scope="session")
def api_key():
    """
    从 Windows 环境变量读取 DeepSeek API Key

    【你是怎么设的】
        Win 键 → 搜"环境变量" → 用户变量 → 新建：
        变量名：DEEPSEEK_KEY
        变量值：sk-a88d2c...（你在 DeepSeek 后台复制的）

    【代码里怎么读】
        os.environ["DEEPSEEK_KEY"] → Python 直接拿到那个值
        不需要 import 任何配置，操作系统替你存着

    【为什么不用 input() 让用户每次手输】
        ① 自动化测试不能有人工干预
        ② CI/CD 跑的时候没人给你输
        ③ 环境变量是业界标准做法
    """
    return os.environ["DEEPSEEK_KEY"]


@pytest.fixture(scope="session")
def api_url():
    """
    DeepSeek Chat API 地址

    【为什么是这个 URL】
        DeepSeek 的 API 兼容 OpenAI 的接口格式。
        大部分国产大模型（DeepSeek/通义千问/GLM）都兼容 OpenAI 格式，
        所以你学会这一个，80% 的 AI API 都会调。

    【换成别家的模板】
        OpenAI:      https://api.openai.com/v1/chat/completions
        DeepSeek:    https://api.deepseek.com/v1/chat/completions
        通义千问:    https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
        格式全都一样，换个 URL 就行。
    """
    return "https://api.deepseek.com/v1/chat/completions"
