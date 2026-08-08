"""
test_03 — 异常场景：401 未授权 + 404 不存在
=============================================

【这是测试工程师的"反向思维"】
    前面你测的是"正常情况"——正确输入返回正确结果。
    但真实 Bug 藏在"异常情况"——错误输入时接口有没有给出合理的错误提示。
    这是面试官最想听到的测试思维。

【两个异常场景】
    401 Unauthorized → 没权限。用了假 Token，GitHub 拒绝访问。
    404 Not Found    → 不存在。查一个不存在的仓库，GitHub 告诉你找不到。

【401 场景的坑（你已经踩过了）】
    最初你想"不带 Token 去请求，预期 401"。
    但 /users/{username} 是公开接口，不带 Token 返回 200。
    所以换了 /user（查当前登录用户），不带真 Token 必然 401。

    这叫"先探路再写断言"——不猜 API 会返回什么，先在 Postman 或 Python 里
    实际调一下看返回，再根据真实行为写断言。工作中这就是标准流程。

【404 场景的注意事项】
    用了 auth_headers —— 其实公开查询不需要，但带了也没坏处。
    如果不带 headers，速率限制是 60次/小时；带了是 5000次/小时。
"""
import requests


def test_用假Token返回401(base_url):
    """验证假 Token 无法访问需要鉴权的接口"""
    # 随便编的一个假 Token
    fake_headers = {"Authorization": "Bearer fake_token_12345"}

    # /user 接口需要鉴权（查当前登录用户）
    r = requests.get(f"{base_url}/user", headers=fake_headers)

    # GitHub 认不出这个 Token → 401 Unauthorized
    assert r.status_code == 401


def test_查不存在仓库返回404(base_url, auth_headers):
    """验证不存在的仓库返回 404"""
    r = requests.get(
        f"{base_url}/repos/dirge1311/no-exist-repo",
        headers=auth_headers
    )

    # 这个仓库名不存在 → 404
    assert r.status_code == 404
