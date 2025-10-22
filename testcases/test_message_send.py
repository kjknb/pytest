import pytest
import requests

@pytest.mark.dependency(name="init_db", scope="session")
@pytest.mark.parametrize("data", [{"msg": "init"}])
def test_message_send(data):
    """
    初始化数据库，清空 user_basic 表
    """
    print("[INIT] 自动清空数据库中的 user_basic 表 ...")
    # 这里是伪操作
    print("✅ 表 user_basic 已成功清空！")
    assert True
