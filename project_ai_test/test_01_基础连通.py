"""
test_01 — 最基础的 AI 接口测试：能不能通
===========================================

跟 test_01.py 一模一样：发请求 → 看状态码 → 看返回
唯一区别：普通接口返回的是确定的 JSON，AI 接口返回的是智能回复
"""
import requests


def test_能连上DeepSeek(api_url, api_key):
    """确认 API 能正常工作"""
    # 构造请求 —— 跟 Postman 的 POST + Body + Headers 完全一样
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "你好，请用一句话介绍你自己"}
        ]
    }

    # 发请求 —— 跟 test_02.py 的 POST 一模一样
    r = requests.post(api_url, headers=headers, json=body)

    # 断言1：状态码 200（服务器正常响应了）
    assert r.status_code == 200

    # 断言2：返回里有 AI 的回复
    data = r.json()
    reply = data["choices"][0]["message"]["content"]
    assert len(reply) > 0   # 回复不为空

    print(f"\n>>> AI 回复: {reply}")
