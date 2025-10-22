import pytest
import requests
from common.yaml_util import read_yaml_file, write_yaml
from common.yaml_util import EXTRACT_PATH  # 提供 extract.yaml 路径

@pytest.mark.dependency(name="update_user", depends=["login_users"], scope="session")
def test_update_user(get_base_url):
    """更新用户信息"""
    users = read_yaml_file(EXTRACT_PATH).get("users", [])
    assert users, "未找到用户信息"

    updated_users = []
    for user in users:
        url = f"{get_base_url}/user/updateUser"
        payload = {"id": user["id"], "name": user["name"] + "_new"}
        headers = {"token": user.get("token", "")}
        resp = requests.put(url, data=payload, headers=headers)
        print(resp.text)
        assert resp.status_code == 200

        j = resp.json()
        if j["code"] == 0:
            user["name"] = j["data"]["name"]
        updated_users.append(user)

    # ✅ 用现有的 write_yaml() 函数覆盖更新
    write_yaml("users", updated_users, EXTRACT_PATH)
