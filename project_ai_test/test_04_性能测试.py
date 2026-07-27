"""
test_04 — AI 性能测试：响应时间、Token 消耗
=============================================

传统接口性能：只测响应时间
AI 接口性能：响应时间 + Token 消耗（花了多少钱）
"""
import pytest
import requests
import time


def test_响应时间和Token消耗(api_url, api_key):
    """验证 AI 接口的响应速度和 Token 使用"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "请用 50 字以内介绍北京邮电大学"}
        ],
        "max_tokens": 100    # 限制最大 Token，控制成本
    }

    # 记录开始时间
    start = time.time()
    r = requests.post(api_url, headers=headers, json=body)
    elapsed = time.time() - start    # 实际响应耗时

    data = r.json()

    # 断言1：HTTP 正常
    assert r.status_code == 200

    # 断言2：响应时间在可接受范围（5 秒以内）
    # DeepSeek 通常 1-3 秒，超过 5 秒说明有问题
    assert elapsed < 5.0, f"响应太慢：{elapsed:.2f} 秒"

    # 断言3：Token 消耗合理（不超过限制）
    usage = data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)     # 输入花了多少 Token
    completion_tokens = usage.get("completion_tokens", 0)  # 输出花了多少 Token
    total_tokens = usage.get("total_tokens", 0)       # 总共

    assert total_tokens > 0, "Token 消耗量为 0，异常"
    assert completion_tokens <= 100, f"输出 Token 超过限制：{completion_tokens}"

    # 打印性能报告
    print(f"\n>>> 性能报告 <<<")
    print(f"  响应时间: {elapsed:.2f} 秒")
    print(f"  输入 Token: {prompt_tokens}")
    print(f"  输出 Token: {completion_tokens}")
    print(f"  总 Token:   {total_tokens}")
    # DeepSeek 当前价格约：输入 1 元/百万token，输出 2 元/百万token
    cost = (prompt_tokens * 1 + completion_tokens * 2) / 1_000_000
    print(f"  估算费用:   ¥{cost:.6f}（不到 1 分钱）")
