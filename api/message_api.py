from common.request_util import RequestUtil
from common.yaml_util import read_yaml_file


class MessageApi:
    def __init__(self):
        self.req = RequestUtil()
        cfg = read_yaml_file("config/config.yaml")
        env = cfg["env"]
        self.base = cfg[env]["base_url"]
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def send(self, user_id: int, content: str, token_required=True):
        url = f"{self.base}/message/send"
        data = {"user_id": user_id, "content": content}
        return self.req.request("POST", url, headers=self.headers, data=data, token_required=token_required)
