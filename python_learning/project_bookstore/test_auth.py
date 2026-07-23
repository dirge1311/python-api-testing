import pytest
import requests

@pytest.fixture(scope="session")
def auth_token(base_url):
    r = requests.post(
        f"{base_url}/posts",
        json={"username": "test_user", "password": "123456"}
    )
    assert r.status_code == 201
    return f"fake_token_{r.json()['id']}"


def test_需要登陆的请求(base_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = requests.get(f"{base_url}/posts/1", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == 1
