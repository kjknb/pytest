import requests
from common.yaml_util import read_yaml_file


def get_swagger_endpoints():
    config = read_yaml_file("config/config.yaml")
    env = config["env"]
    base_url = config[env]["base_url"]
    url = f"{base_url}/swagger/doc.json"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    endpoints = []
    for path, methods in data.get("paths", {}).items():
        for method, info in methods.items():
            endpoints.append({
                "method": method.upper(),
                "path": path,
                "summary": info.get("summary", ""),
            })
    return endpoints
