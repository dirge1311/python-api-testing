import requests
import pytest

# ============================================================
# 测试数据
# ============================================================
new_post_data = [
    ("测试标题_Python", "内容_自动化测试", 1),
    ("测试标题_空内容", "", 2),
    ("英文标题_test", "english_body", 3),
]


# ============================================================
# 用例1：查所有文章
# ============================================================
def test_查看所有文章(base_url):
    r = requests.get(f"{base_url}/posts")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0


# ============================================================
# 用例2：新建文章（单组数据）
# ============================================================
def test_新建文章(base_url):
    new_post = {
        "title": "测试标题_learn_python",
        "body": "测试内容_hello_world",
        "userId": 1
    }
    r = requests.post(f"{base_url}/posts", json=new_post)
    assert r.status_code == 201              # POST 创建成功 = 201
    assert r.json()["title"] == new_post["title"]
    assert r.json()["body"] == new_post["body"]


# ============================================================
# 用例3：新建文章（parametrize，3组数据 → 3个独立用例）
# ============================================================
@pytest.mark.parametrize("title,body,user_id", new_post_data)
def test_新建文章_parametrize(base_url, title, body, user_id):
    new_post = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    r = requests.post(f"{base_url}/posts", json=new_post)
    assert r.status_code == 201
    assert r.json()["title"] == title
    assert r.json()["body"] == body
def test_修改文章(base_url):
    change_post = {
        "title": "修改后的标题",
        "body": "修改后的内容"
    }
    r = requests.put(f"{base_url}/posts/1", json=change_post)
    assert r.status_code == 200
    assert r.json()["title" ] == change_post["title"]
def test_删除文章(base_url):
    r = requests.delete(f"{base_url}/posts/1")
    assert r.status_code == 200