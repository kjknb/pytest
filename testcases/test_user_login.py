# -*- coding: utf-8 -*-
import os
import pytest
import requests
from common.yaml_util import extract_get
from common.token_util import save_token # 兼容你现有的工具，若函数名不同，替换为你的保存方法

@pytest.mark.dependency(depends=["create_users"], name="login_users")
def test_login_all(get_base_url):
    """
    使用创建的用户逐个登录；第一次成功后将 token 保存到 token.yaml
    """
    users = extract_get("users", [])
    assert users, "extract.yaml 中没有 users，请先运行创建用例"

    saved = False
    for u in users:
        url = f"{get_base_url}/user/findUserByNameAndPwd"
        resp = requests.post(url, params={"name": u["name"], "password": u["password"]})
        print(resp.text)
        assert resp.status_code == 200
        j = resp.json()
        assert j["code"] == 0, f"登录失败: {j['message']}"

        # 你的后端登录接口可能返回 token 的接口是另外一个（比如 /user/login 获取 token）
        # 如果本接口不返回 token，请在 conftest 或这里调用颁发 token 的接口。
        # 下面示例假装 token 在响应头/或次接口返回，这里演示保存一个占位符：
        token = j.get("data", {}).get("token", "")
        if not token:
            # 如果没有 token，可以不保存，后续用例依赖 get_token fixture 时会告警
            # 或者这里调用你的颁发 token 接口获取后再保存
            pass
        else:
            if not saved:
                try:
                    save_token(token)   # 写入 token.yaml
                except Exception as e:
                    print(f"[WARN] 保存 token 失败: {e}")
                saved = True
