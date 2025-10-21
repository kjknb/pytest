# -*- coding: utf-8 -*-
import pytest
import requests
from common.yaml_util import extract_get

@pytest.mark.dependency(depends=["login_users"], name="update_user")
def test_update_user(get_base_url, get_token):
    """
    更新 primary_user
    """
    user_id = extract_get("primary_user_id")
    print(f"[INFO] 从 extract.yaml 读取的 primary_user_id: {user_id}")
    assert user_id, "primary_user_id 为空，请先执行创建与登录用例"

    url = f"{get_base_url}/user/updateUser"
    # 根据你的后端字段改；示例：更新昵称
    data = {"id": user_id, "name": "test003_updated"}
    headers = {}
    if get_token and get_token.get("token"):
        headers["Authorization"] = f"Bearer {get_token['token']}"
    resp = requests.post(url, params=data, headers=headers or None)
    print(resp.text)
    assert resp.status_code == 200
    j = resp.json()
    assert j["code"] == 0, f"更新失败: {j['message']}"
