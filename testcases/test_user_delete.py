# -*- coding: utf-8 -*-
import pytest
import requests
from common.yaml_util import extract_get

@pytest.mark.dependency(depends=["update_user"])
def test_delete_user(get_base_url, get_token):
    """
    删除 primary_user
    """
    user_id = extract_get("primary_user_id")
    print(f"[INFO] 从 extract.yaml 读取的 primary_user_id: {user_id}")
    assert user_id, "primary_user_id 为空，请先执行创建与登录用例"

    url = f"{get_base_url}/user/deleteUser"
    params = {"id": user_id}
    headers = {}
    if get_token and get_token.get("token"):
        headers["Authorization"] = f"Bearer {get_token['token']}"
    resp = requests.post(url, params=params, headers=headers or None)
    print(resp.text)
    assert resp.status_code == 200
    j = resp.json()
    assert j["code"] == 0, f"删除失败: {j['message']}"
