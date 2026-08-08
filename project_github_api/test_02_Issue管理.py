"""
test_02 — Issue 增删改查（核心业务）
======================================

【这是你第一个"真的会产生副作用"的测试】
    之前 echo/jsonplaceholder → POST 返回 201 但没真的创建东西
    这里 POST /repos/.../issues → GitHub 真的生成了一个 Issue

    你打开 github.com/dirge1311/python-api-testing/issues 就能看到
    标题为 "测试Issue_Python自动化" 的 Issue —— 那是代码创建的。

【201 vs 200】
    GET 成功 → 200 OK
    POST 创建成功 → 201 Created
    两者不一样。你 test_02.py 里第一次学 POST 时就记过这个区别。

【关于跑完后 GitHub 上有残留 Issue】
    真实测试项目里，测完要清理——写 DELETE 用例把创建的 Issue 删掉。
    这就是"测试数据清理"。后续可以补上这个功能。
"""
import requests


def test_创建Issue(base_url, auth_headers):
    """POST /repos/{owner}/{repo}/issues — 创建一个真实的 Issue"""
    data = {
        "title": "测试Issue_Python自动化",
        "body": "这是一个由自动化测试创建的Issue"
    }

    r = requests.post(
        f"{base_url}/repos/dirge1311/python-api-testing/issues",
        json=data,
        headers=auth_headers   # 必须有 Token，否则 401
    )

    # 创建成功的状态码是 201，不是 200
    assert r.status_code == 201

    # 确认创建出来的 Issue 标题正确
    assert r.json()["title"] == "测试Issue_Python自动化"


def test_查Issue列表(base_url, auth_headers):
    """GET /repos/{owner}/{repo}/issues — 查所有 Issue（应该不为空）"""
    r = requests.get(
        f"{base_url}/repos/dirge1311/python-api-testing/issues",
        headers=auth_headers
    )

    assert r.status_code == 200

    data = r.json()
    assert len(data) > 0   # 刚才创建了一个，列表至少有一个
