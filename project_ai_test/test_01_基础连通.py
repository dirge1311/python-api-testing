"""
test_01 — 基础连通测试：AI API 能不能调通
=============================================

【这是你第几次写这种测试了】
    第一次：test_01.py → GET postman-echo，看状态码和返回
    第二次：project_bookstore/test_posts.py → GET jsonplaceholder，看文章列表
    第三次：这里 → POST DeepSeek API，看 AI 回复

    每次的区别只是 URL 和参数不同，核心动作一模一样：
        发请求 → 看状态码 → 看返回数据 → 断言

【AI 接口跟普通接口的核心区别】
    普通接口（图书管理）：POST /posts → 返回 {"id": 101, "title": "hello"}
        → 返回的是确定的、可预测的数据

    AI 接口（DeepSeek）：   POST /chat → 返回 {"choices": [{"message": {"content": "你好！..."}}]}
        → 返回的是不固定的、每次可能不一样的自然语言

    这意味着：
        普通接口的断言：assert r.json()["title"] == "hello"  ← 精确匹配
        AI 接口的断言：assert len(reply) > 0                 ← 只能保证"有回复"
        （后面 test_02 会教你怎么更精确地断言 AI 的回复质量）

【调用 AI API 的固定格式（跟 Postman 对照）】
    Postman:
        Headers → Authorization: Bearer sk-xxx...
               → Content-Type: application/json
        Body   → {"model": "...", "messages": [...]}

    Python（下面要写的代码）:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        body = {"model": "deepseek-chat", "messages": [{"role": "user", "content": "..."}]}
        requests.post(api_url, headers=headers, json=body)

    → 任何大模型的 API 都是这个套路，只是 model 名字不同
"""
import requests


def test_能连上DeepSeek(api_url, api_key):
    """
    验证能连上 DeepSeek API 并获得有效回复

    【这个测试做了什么】
        ① 构造请求头：Bearer Token 鉴权 + JSON 类型声明
        ② 构造请求体：指定模型 + 发送一条用户消息
        ③ 发 POST 请求
        ④ 断言：状态码 == 200（连通了）
        ⑤ 断言：回复不为空（真的回复了，不是空字符串）

    【你之前在哪学过这些】
        test_02.py  → requests.post(url, json={...})  发送 POST
        test_03.py  → assert r.status_code == 200      状态码断言
        test_10.py  → fixture base_url                  用 fixture 管理 URL
        test_11.py  → f"Bearer {token}"                 Bearer Token 拼接
    """
    # ---------------------------------------------------------------
    # 构造请求头
    # Authorization: Bearer xxx  =  你 Postman 里鉴权标签页选"Bearer Token"
    # Content-Type: application/json = Postman 自动帮你加的，Python 要手动写
    # ---------------------------------------------------------------
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # ---------------------------------------------------------------
    # 构造请求体
    # model: "deepseek-chat" → 用哪个模型（相当于你选工具版本）
    # messages: [{"role": "user", "content": "..."}]  → 对话内容
    #   role: "user" = 你发的消息（如果是 "assistant" 就是 AI 的回话）
    #   content = 你发的话
    # 如果你想让 AI 扮演某个角色，可以加一条 {"role": "system", "content": "你是一个测试专家"}
    # ---------------------------------------------------------------
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "你好，请用一句话介绍你自己"}
        ]
    }

    # 发请求 —— 跟 test_02.py 的 requests.post() 一模一样
    r = requests.post(api_url, headers=headers, json=body)

    # ---------------------------------------------------------------
    # 断言1：HTTP 状态码 200
    # 如果返回 401 → API Key 错了或过期了
    # 如果返回 429 → 调用太频繁，被限流了
    # 如果返回 500 → DeepSeek 服务器出了问题
    # ---------------------------------------------------------------
    assert r.status_code == 200

    # ---------------------------------------------------------------
    # 断言2：AI 真的回复了
    # 返回的 JSON 结构（打印出来看看就知道了）：
    # {
    #   "choices": [
    #     {
    #       "message": {
    #         "role": "assistant",
    #         "content": "你好！我是DeepSeek..."
    #       }
    #     }
    #   ]
    # }
    # choices[0] = 第一个回答（一般只有一个）
    # .message.content = AI 回复的文本内容
    # ---------------------------------------------------------------
    data = r.json()
    reply = data["choices"][0]["message"]["content"]
    assert len(reply) > 0   # 回复不能是空字符串

    # -s 参数让 pytest 不吞掉 print，这样你能看到 AI 说了什么
    print(f"\n>>> AI 回复: {reply}")
