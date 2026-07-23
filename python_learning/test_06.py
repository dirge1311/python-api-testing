"""
test_06.py — 独立练习：不靠模板，自己写两个测试用例
=====================================================

这次是从零写的，只给了需求，没给模板：
    test_登录()   → POST 登录 + 断言
    test_查商品() → GET 查询 + 断言

踩过的坑（已修复）：
    坑：assert "args" in r.json   → 漏了括号 ()，报 TypeError
    改：assert "args" in r.json() → 正确

现在你已经能脱离模板独立写接口测试了。
"""

import requests


def test_登录():
    """POST 登录接口测试"""
    # 准备登录数据 —— 跟 Postman Body → raw → JSON 里写的一样
    data = {
        "username": "Qiucen_Lyu",
        "password": "123"
    }

    # 发 POST 请求
    r = requests.post("https://postman-echo.com/post", json=data)

    # 断言1：HTTP 状态码是 200（服务器正常响应了）
    assert r.status_code == 200

    # 断言2：返回的 JSON 里有 "data" 字段
    # "data" 字段存放的是服务器收到的原始请求体
    # 确认数据确实发出去了，并且服务器收到了
    assert "data" in r.json()


def test_查商品():
    """GET 商品查询接口测试"""
    # 发 GET 请求，URL 里带参数 type=phone
    # 这跟你 Postman 里 GET + Params 填 type: phone 是一样的
    r = requests.get("https://postman-echo.com/get?type=phone")

    # 断言1：状态码 200
    assert r.status_code == 200

    # 断言2：返回的 JSON 里有 "args" 字段
    # "args" 存放的是服务器收到的 URL 参数
    # 如果 args 存在，说明参数 type=phone 被服务器正确接收了
    assert "args" in r.json()

# ============================================================
# 小结：你现在能独立做什么
# ============================================================
#
#   给定一个接口（GET 或 POST），你能：
#   ① 用 requests 发请求
#   ② 用 assert 写断言校验结果
#   ③ 用 def test_xxx() 组织成 pytest 用例
#   ④ 跑 pytest 命令看结果汇总
#
#   这四条 = 接口自动化测试的最小完整闭环。
# ============================================================
