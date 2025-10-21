# -*- coding: utf-8 -*-
import os
import pytest
import requests
import yaml

from common.yaml_util import extract_list_append, extract_get, extract_set

DATA_FILE = os.path.join(os.getcwd(), "create_user.yaml")  # 你已经放在根目录
# 如你把数据放在 data/ 目录：DATA_FILE = os.path.join(os.getcwd(), "data", "create_user.yaml")

def _load_create_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f) or {}
    return y if isinstance(y, list) else y.get("users", [])


@pytest.mark.dependency(name="create_users")
@pytest.mark.parametrize("item", _load_create_data())
def test_create_user(get_base_url, item):
    """
    创建用户，落盘到 extract.yaml
    """
    url = f"{get_base_url}/user/createUser"
    resp = requests.post(url, params={"name": item["name"], "password": item["password"]})
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
    # 1) 把该用户追加到 extract.yaml -> users 列表
    extract_list_append(u)

    # 2) 设定 primary_user_id（仅在第一次写入时设置）
    primary_id = extract_get("primary_user_id")
    if not primary_id:
        extract_set("primary_user_id", u["id"])

    print(f"[INFO] 已保存 user: {u}")
