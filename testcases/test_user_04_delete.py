import pytest
import requests
from common.yaml_util import read_yaml_file

@pytest.mark.dependency( depends=["update_user"], scope="session")
def test_delete_user(get_base_url):
    """删除用户（依赖更新用例）"""
    users = read_yaml_file("extract.yaml").get("users", [])
    assert users, "❌ 未找到用户信息"

    for user in users:
        url = f"{get_base_url}/user/deleteUser"
        headers = {"token": user.get("token", "")}
        params = {"id": user["id"]}
        resp = requests.delete(url, params=params, headers=headers)
        print(resp.text)
        j = resp.json()

        # 验证接口返回
        assert resp.status_code == 200
        assert j["code"] == 0, f"删除失败: {j['message']}"
        print(f"✅ 用户 {user['name']} (id={user['id']}) 删除成功")
