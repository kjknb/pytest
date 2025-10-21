# -*- coding: utf-8 -*-
import pytest
from common.yaml_util import extract_get
from api.user_api import UserApi  # 你已有的封装，内部使用 RequestUtil

@pytest.mark.dependency(depends=["create_users"], name="list_users")
def test_user_list():
    api = UserApi()
    j = api.user_list()
    print(j)
    assert j["code"] == 0
    created = extract_get("users", [])
    assert isinstance(j["data"]["list"], list)
    # 至少包含我们创建的数量
    assert j["data"]["total"] >= len(created)
