import pytest
import requests

@pytest.mark.dependency(name="list_users", depends=["create_users"], scope="session")
def test_user_list(get_base_url):
    """获取用户列表"""
    url = f"{get_base_url}/user/list"
    resp = requests.get(url)
    print(resp.text)
    assert resp.status_code == 200
