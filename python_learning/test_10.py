"""
test_10.py — pytest fixture：一处定义，处处使用
=================================================

对照 Postman 理解：
    Postman 环境变量 {{base_url}}        → fixture 的 return 值
    Postman Pre-request Script（自动执行）→ fixture 函数体
    Postman {{变量名}} 引用              → 测试函数参数里写 fixture 名

fixture 两个零件：
    零件1：@pytest.fixture + def xxx(): return 值      （定义）
    零件2：测试函数参数里写 xxx                          （使用）

==============================================================================
基础用法：共享 URL（== Postman 环境变量）
==============================================================================
"""

import pytest
import requests


# ============================================================
# 零件1：定义 fixture
# ============================================================
# @pytest.fixture 告诉 pytest："这是个 fixture，哪个用例要用就传给它"
# 函数名 base_url 就是 fixture 的名字
# return 后面的值就是 fixture 提供的东西
@pytest.fixture
def base_url():
    """提供统一的接口基础地址"""
    return "https://postman-echo.com"


# ============================================================
# 零件2：使用 fixture
# ============================================================
# 测试函数参数里写 base_url，pytest 自动把 fixture 的返回值传进来
# 不需要 import，不需要赋值，pytest 全自动
def test_用fixture发GET(base_url):
    """GET 请求 —— 使用 fixture 提供的 URL"""
    # f"{base_url}/get" → "https://postman-echo.com/get"
    # f-string = 把变量拼进字符串，{} 里的变量会被替换成实际值
    # 跟 Postman 里 {{base_url}}/get 完全一样
    r = requests.get(f"{base_url}/get?name=Qiucen_Lyu")
    assert r.status_code == 200


def test_用fixture发POST(base_url):
    """POST 请求 —— 使用同一个 fixture"""
    r = requests.post(
        f"{base_url}/post",
        json={"username": "Qiucen_Lyu"}
    )
    assert r.status_code == 200

# ============================================================
# 好处：
# ============================================================
#   改 URL 只改一处：base_url 里 return 的值改掉，所有用例自动生效
#   以前每个函数都要写一遍完整的 "https://postman-echo.com"
#   现在只在 fixture 里写一次
#
# ⚠️ 你电脑上必须用：python -m pytest python_learning/test_10.py -v
#    裸 pytest 是 Anaconda 旧版，不认 fixture
