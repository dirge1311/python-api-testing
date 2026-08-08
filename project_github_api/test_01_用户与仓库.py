"""
test_01 — 用户信息 & 仓库查询（基础 GET 请求）
================================================

【这是你第 N 次写 GET 了】
    test_01.py → postman-echo
    project_bookstore → jsonplaceholder
    project_ai_test → DeepSeek
    这里 → GitHub API

    每次都是同一件事：requests.get(url) → assert status_code → assert 返回不为空

【GitHub API 查用户信息的特点】
    /users/{用户名} 是公开接口，不带 Token 也能查（但速率限制低 60次/小时）
    带 Token 速率限制 5000次/小时 —— 所以加上 headers=auth_headers 是好习惯

【断言设计】
    查用户：assert r.json()["login"] == "dirge1311" → 精确，因为你的用户名是固定的
    查仓库：assert len(data) > 0 → 你仓库数量会变，不能精确断言数量，断言"有仓库"即可
"""
import requests


def test_查自己的用户信息(base_url, auth_headers):
    """GET /users/{username} — 查自己的 GitHub 用户信息"""
    r = requests.get(
        f"{base_url}/users/dirge1311",
        headers=auth_headers
    )

    # 断言1：状态码 200
    assert r.status_code == 200

    # 断言2：返回的 login 字段确实是你
    # GitHub API 返回结构：{"login": "dirge1311", "id": ..., "name": ..., ...}
    # 跟 echo 接口不同——echo 有 "args" 包一层，GitHub 直接就是字段
    assert r.json()["login"] == "dirge1311"


def test_查自己的仓库列表(base_url, auth_headers):
    """GET /users/{username}/repos — 查自己的仓库列表"""
    r = requests.get(
        f"{base_url}/users/dirge1311/repos",
        headers=auth_headers
    )

    assert r.status_code == 200

    data = r.json()
    # GitHub 返回的是一个数组：[{...repo1...}, {...repo2...}, ...]
    # 不能断言数量（以后仓库会变），断言列表不为空就行
    assert len(data) > 0
