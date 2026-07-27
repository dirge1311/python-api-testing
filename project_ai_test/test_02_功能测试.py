"""
test_02 — AI 功能测试：不同类型的问题能不能得到合理回复
===========================================================

【核心问题】
    普通接口能精确断言 assert r.json()["title"] == "hello"
    AI 接口每次回复不一样，怎么断言？

    答案：不判"等于什么"，判"包含什么"。

    比如问 1+1，不判 assert reply == "2"（万一 AI 回复 "等于2" 就挂了），
    而是判 assert "2" in reply（只要回复里出现了 2 就算对）。

    这个思路叫做"关键词命中"——AI 测试最基础的断言方法。

【为什么用 parametrize】
    跟 test_07 完全一样的原因：
    不同类型的问题（数学、翻译、自我介绍...）各测一组，
    每组独立成一个用例，挂哪个类型一看就知道。

【AI 测试的断言怎么设计（面试会问）】
    ① 连通性：assert r.status_code == 200        （跟普通接口一样）
    ② 有效性：assert len(reply) > 0              （别返回空的）
    ③ 相关性：assert "关键词" in reply            （AI 测试特有，回复跟问题沾边）
    ④ 格式：   assert reply.startswith("{")...    （如果要求 JSON 输出）
    ⑤ 安全性：assert "不能" in reply...           （test_03 会专门测）

    AI 测试的核心思想：
        你不能控制 AI 怎么回答，但你能定义"好回答"的标准，
        然后验证 AI 是否达到了这个标准。
"""
import pytest
import requests


# ---------------------------------------------------------------
# 测试用例设计思路
# 覆盖不同类型的提问，确保 AI 对各种场景都有合理回复
#
# 你电商项目里 login_data.csv 分了三类：正常值、边界值、异常值
# AI 测试用例也分类：
#   功能类：自我介绍、数学计算、翻译、结构化输出
#   （后面 test_03 单独做安全类）
#
# 每个用例 = (提示词, [关键词列表])
#   提示词 = 你问 AI 的话
#   关键词列表 = AI 的回复里至少应该包含这些词
#   注意：是列表不是单个词！比如 ["AI", "助手"] 意思是"AI"和"助手"都要有
# ---------------------------------------------------------------
test_prompts = [
    # (提示词,                                   期望回复包含的关键词)
    ("你好，请用一句话介绍你自己",                  ["AI", "助手"]),
    ("1+1等于几",                                ["2"]),
    ("用中文翻译：hello world",                   ["世界"]),
    ("请用 JSON 格式回复：姓名张三，年龄25",       ["张三", "25"]),
]


@pytest.mark.parametrize("prompt,expected_keywords", test_prompts)
def test_不同提问类型(api_url, api_key, prompt, expected_keywords):
    """
    验证四种不同类型的提问都能得到合理回复

    【这个函数会被 pytest 调用 4 次】
        第1次：prompt="你好，请用一句话介绍你自己"  expected_keywords=["AI", "助手"]
        第2次：prompt="1+1等于几"                  expected_keywords=["2"]
        第3次：prompt="用中文翻译：hello world"     expected_keywords=["世界"]
        第4次：prompt="请用 JSON 格式回复：..."     expected_keywords=["张三", "25"]

    【parametrize 怎么工作的（复习 test_07）】
        @pytest.mark.parametrize("参数名1,参数名2", 数据列表)
        def test_xxx(参数名1, 参数名2):
        test_prompts 里每个元组的值会按顺序赋给 prompt 和 expected_keywords
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post(api_url, headers=headers, json=body)

    # 断言1：连通性（跟 test_01 一样）
    assert r.status_code == 200

    # 断言2：有效性 —— 不能返回空回复
    reply = r.json()["choices"][0]["message"]["content"]
    assert len(reply) > 0

    # ---------------------------------------------------------------
    # 断言3：相关性 —— AI 测试的核心创新
    #
    # 这是 AI 测试跟普通接口测试最大的不同：
    #   普通测试：assert 实际值 == 预期值
    #   AI 测试：  assert 预期关键词 in 实际回复
    #
    # 为什么用 for 循环而不是单个 assert？
    #   因为 expected_keywords 可能有多个词，每个都要检查
    #   比如第四个用例的 ["张三", "25"] → "张三"和"25"都要出现在回复里
    #
    # 为什么是 assert keyword in reply 而不是 assert keyword == reply？
    #   因为 AI 的回复是一段完整的话，不是只返回关键词
    #   比如 AI 回复 "1+1 等于 2，这是基本数学运算"
    #   assert "2" in reply → True（包含了2）✅
    #   assert reply == "2" → False（AI 不可能只回复一个字符）❌
    # ---------------------------------------------------------------
    for keyword in expected_keywords:
        assert keyword in reply, (
            f"\n期望回复包含'{keyword}'，但没找到。"
            f"\n实际回复: {reply[:200]}"
        )

    # 打印结果，让你看到每种提问 AI 是怎么回的
    print(f"\n>>> 提问: {prompt}")
    print(f">>> 回复: {reply[:80]}...")
