# testcases/test_message_send.py
import pytest
import requests
from common.yaml_util import read_yaml_file


@pytest.mark.parametrize("data", [
    {"user_id": 1, "content": "hello world"}
])
def test_message_send(get_base_url, get_token, data):
    """
    发送消息接口测试
    """
    url = f"{get_base_url}/message/send"
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    resp = requests.post(url, headers=headers, data=data)
    print(resp.text)
    assert resp.status_code in (200, 404)
