import pytest
import requests
from common.yaml_util import read_yaml_file, write_yaml

@pytest.mark.dependency(name="login_users", depends=["create_users"], scope="session")
def test_login_all(get_base_url):
    """登录所有用户并保存 token"""
    data = read_yaml_file("extract.yaml") or {}
    users = data.get("users", [])
    assert users, "未找到用户数据，请先执行创建用户用例"

    for user in users:
        url = f"{get_base_url}/user/findUserByNameAndPwd"   # ✅ 修正路径
        params = {"name": user["name"], "password": user["password"]}
        resp = requests.post(url, data=params)              # ✅ 改为 POST
        print(resp.text)
        assert resp.status_code == 200

        j = resp.json()
        assert j["code"] == 0, f"登录失败: {j['message']}"
        user["token"] = j["data"]["token"]
        print(f"[INFO] 登录成功: {user['name']}")

    write_yaml("users", users, "extract.yaml")
    print("[INFO] 所有用户登录成功")
