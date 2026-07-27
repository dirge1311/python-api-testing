"""
test_04 — AI 性能测试：响应时间 + Token 消耗
===============================================

【传统性能测试 vs AI 性能测试】
    传统接口：只测响应时间（多少毫秒返回）
    AI 接口：  响应时间 + Token 消耗 + 费用估算
            因为每次 API 调用都是要花钱的，Token 越多越贵

【什么是 Token】
    Token ≠ 字数。一个汉字 ≈ 1-2 个 Token，一个英文单词 ≈ 1-2 个 Token。
    比如 "你好世界" ≈ 4 个 Token，"Hello World" ≈ 2 个 Token。

    输入 Token（prompt_tokens）：你发给 AI 的话，也要算钱
    输出 Token（completion_tokens）：AI 回复你的话，也要算钱
    总 Token = 输入 + 输出

    DeepSeek 价格（写代码时）：
        输入：¥1 / 百万 Token
        输出：¥2 / 百万 Token
    所以这个测试里你花了 输入15 + 输出30 = 45 Token ≈ ¥0.000075

【为什么要用 time.time()】
    这是 Python 内置的时间函数，返回当前时间戳（秒）。
    start = time.time()  → 记录开始时间
    发请求...
    elapsed = time.time() - start  → 结束时间 - 开始时间 = 耗时

【max_tokens 参数的作用】
    限制 AI 最多输出多少 Token。
    不加这个参数的话，AI 可能滔滔不绝回复 500 Token，
    虽然也没多少钱，但量大了就是浪费。
    测试环境里加 max_tokens=100 是个好习惯。
"""
import pytest
import requests
import time    # Python 自带的计时模块


def test_响应时间和Token消耗(api_url, api_key):
    """
    验证 AI 接口的响应速度和 Token 使用都在合理范围内

    【这个测试的三层断言】
        ① 时间维度：响应 < 5 秒（用户等不了太久）
        ② 成本维度：Token 消耗不超过 max_tokens 的限制
        ③ 可用维度：总 Token > 0（确实消耗了，不是返回错误）
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "请用 50 字以内介绍北京邮电大学"}
        ],
        "max_tokens": 100  # 限制最大输出 Token，既省钱又控制测试范围
    }

    # ---------------------------------------------------------------
    # 计时开始
    # time.time() 返回从 1970-01-01 到现在经过的秒数（浮点数）
    # 两个时间戳相减 = 中间经过的秒数
    # ---------------------------------------------------------------
    start = time.time()
    r = requests.post(api_url, headers=headers, json=body)
    elapsed = time.time() - start

    data = r.json()

    # 断言1：连通性
    assert r.status_code == 200

    # ---------------------------------------------------------------
    # 断言2：响应时间
    # 为什么是 5 秒而不是更严格的值？
    #   AI 推理本身就要 1-3 秒，加上网络延迟，3-5 秒是正常的。
    #   超过 5 秒说明要么服务器负载高，要么网络有问题。
    #   在真实项目里，这个阈值要根据 SLA（服务等级协议）来定。
    # ---------------------------------------------------------------
    assert elapsed < 5.0, (
        f"响应时间 {elapsed:.2f} 秒，超过 5 秒阈值。"
        f"可能原因：网络波动 或 DeepSeek 服务器繁忙"
    )

    # ---------------------------------------------------------------
    # 断言3：Token 消耗
    #
    # data.get("usage", {}) 跟 data["usage"] 的区别：
    #   data["usage"] → 如果 usage 不存在，程序直接崩溃（KeyError）
    #   data.get("usage", {}) → 如果 usage 不存在，返回 {} （空字典），不崩
    #   测试代码里用 .get() 更安全，因为 API 返回格式可能会变
    #
    # usage.get("prompt_tokens", 0) 同理：
    #   如果字段不存在，返回 0 而不是崩溃
    # ---------------------------------------------------------------
    usage = data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    # 总 Token 必须 > 0（如果等于 0 说明 API 没正常处理请求）
    assert total_tokens > 0, "Token 消耗量为 0，API 可能没有正常处理请求"

    # 输出 Token 不能超过 max_tokens 限制
    assert completion_tokens <= 100, (
        f"输出 Token {completion_tokens} 超过了 max_tokens=100 的限制"
    )

    # ---------------------------------------------------------------
    # 打印性能报告
    # 这个报告就是"测试产出物"——跑完就能看到 API 的表现
    # ---------------------------------------------------------------
    print(f"\n>>> 性能报告 <<<")
    print(f"  响应时间:    {elapsed:.2f} 秒")
    print(f"  输入 Token:  {prompt_tokens}")
    print(f"  输出 Token:  {completion_tokens}")
    print(f"  总 Token:    {total_tokens}")

    # 费用估算公式
    # 输入 1 元/百万token + 输出 2 元/百万token
    # 除以 1,000,000 把"元/百万"换算成"元/Tok"
    cost = (prompt_tokens * 1 + completion_tokens * 2) / 1_000_000
    print(f"  估算费用:    ¥{cost:.6f}（不到 1 分钱）")

    # 思考题：如果要测 100 个不同的问题，Token 费用会是多少？
    #   答：100 × 45 Token ≈ 4500 Token ≈ ¥0.0075（不到 1 分钱）
    #   所以 AI 接口测试的成本极低，大规模测试完全可行。
