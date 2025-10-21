import requests
from common.logger import logger
from common.yaml_util import read_yaml_file


class RequestUtil:
    def __init__(self):
        self.session = requests.Session()

    def request(self, method: str, url: str, *, headers=None, params=None, data=None, json=None, token_required: bool=False, timeout: int=10):
        headers = dict(headers or {})
        if token_required:
            token = read_yaml_file("config/token.yaml").get("token", "")
            if token:
                headers["Authorization"] = f"Bearer {token}"

        logger.info(f"请求方法: {method.upper()}")
        logger.info(f"请求URL: {url}")
        logger.info(f"请求头: {headers}")
        logger.info(f"请求params: {params}")
        logger.info(f"请求data: {data}")
        logger.info(f"请求json: {json}")

        resp = self.session.request(method=method.upper(), url=url, headers=headers, params=params, data=data, json=json, timeout=timeout)

        logger.info(f"响应状态码: {resp.status_code}")
        logger.info(f"响应内容: {resp.text}")
        return resp
