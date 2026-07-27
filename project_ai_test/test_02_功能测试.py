"""
test_02 — AI 功能测试：不同类型的问题能不能得到合理回复
===========================================================

跟普通接口的 parametrize 一模一样：准备多组数据 → 逐组发请求 → 断言
区别：断言逻辑不同——不是 assert 返回值 == 某个确切值
                         而是 assert 返回值满足质量标准
"""
import pytest
import requests

# 多种类型的提问 —— 跟 test_07 的 test_data 完全一样的格式
test_prompts = [
    # (提示词,              期望回复中至少包含的关键词)
    ("你好，请用一句话介绍你自己", ["AI", "助手"]),         # 自我介绍
    ("1+1等于几",              ["2"]),                     # 数学
    ("用中文翻译：hello world", ["世界"]),                  # 翻译
    ("请用 JSON 格式回复：姓名张三，年龄25", ["张三", "25"]),# 结构化输出
]


@pytest.mark.parametrize("prompt,expected_keywords", test_prompts)
def test_不同提问类型(api_url, api_key, prompt, expected_keywords):
    """验证不同类型的提问都能正常回复，且回复包含预期关键词"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post(api_url, headers=headers, json=body)

    # 断言1：HTTP 正常
    assert r.status_code == 200

    # 断言2：有回复内容
    reply = r.json()["choices"][0]["message"]["content"]
    assert len(reply) > 0

    # 断言3：AI 测试的核心 —— 回复里至少包含预期关键词
    # 不是 assert == 确切值，而是 assert "关键词" in 回复
    for keyword in expected_keywords:
        assert keyword in reply, f"期望回复包含'{keyword}'，实际回复：{reply}"

    print(f"\n>>> 提问: {prompt}")
    print(f">>> 回复: {reply[:80]}...")
