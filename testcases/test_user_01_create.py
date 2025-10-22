import pytest
import requests
from common.yaml_util import read_yaml_file, write_yaml

def _load_create_data():
    return [
        {"name": "test001", "password": "123456"},
        {"name": "test002", "password": "123456"},
    ]

@pytest.mark.dependency(name="create_users", depends=["init_db"], scope="session")
@pytest.mark.parametrize("item", _load_create_data())
def test_create_user(get_base_url, item):
    """创建用户并保存至 extract.yaml"""
    url = f"{get_base_url}/user/createUser"
    resp = requests.post(url, params=item)
    print(resp.text)
    assert resp.status_code == 200

    j = resp.json()
    assert j["code"] == 0, f"创建失败: {j['message']}"

    u = {
        "id": j["data"]["id"],
        "identity": j["data"]["identity"],
        "name": j["data"]["name"],
        "password": item["password"],
    }

    data = read_yaml_file("extract.yaml") or {}
    users = data.get("users", [])
    users.append(u)
    write_yaml("users", users, "extract.yaml")
    print(f"[INFO] 已保存用户: {u}")
