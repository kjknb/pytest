from common.request_util import RequestUtil
from common.yaml_util import read_yaml_file


class UserApi:
    def __init__(self):
        self.req = RequestUtil()
        cfg = read_yaml_file("config/config.yaml")
        env = cfg["env"]
        # ✅ 新结构读取方式
        self.base = cfg["env_config"][env]["base_url"]
        self.headers = cfg["env_config"][env]["headers"]

    def create_user(self, name: str, password: str, repassword: str):
        url = f"{self.base}/user/createUser"
        return self.req.request("POST", url, headers=self.headers, data={
            "name": name, "password": password, "repassword": repassword
        })

    def login(self, name: str, password: str):
        url = f"{self.base}/user/findUserByNameAndPwd"
        return self.req.request("POST", url, headers=self.headers, params={
            "name": name, "password": password
        })

    def list_users(self, token_required=True):
        url = f"{self.base}/user/list"
        return self.req.request("GET", url, token_required=token_required)

    def update_user(self, user_id: int, name=None, password=None, phone=None, email=None, token_required=True):
        url = f"{self.base}/user/updateUser"
        data = {"id": user_id}
        if name is not None: data["name"] = name
        if password is not None: data["password"] = password
        if phone is not None: data["phone"] = phone
        if email is not None: data["email"] = email
        return self.req.request("PUT", url, headers=self.headers, data=data, token_required=token_required)

    def delete_user(self, user_id: int, token_required=True):
        url = f"{self.base}/user/deleteUser"
        return self.req.request("DELETE", url, params={"id": user_id}, token_required=token_required)
