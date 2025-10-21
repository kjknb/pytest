from common.yaml_util import write_yaml, read_yaml_file
import os
import yaml

# 统一文件路径
BASE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../extract.yaml"))

def save_user_id(user_id):
    """
    保存用户ID到 extract.yaml
    """
    write_yaml("user_id", user_id, BASE_FILE)
    print(f"[INFO] 已保存 user_id={user_id} 到 {BASE_FILE}")

def get_user_id():
    """
    从 extract.yaml 读取 user_id
    """
    if not os.path.exists(BASE_FILE):
        print(f"[WARN] 文件不存在: {BASE_FILE}")
        return None

    with open(BASE_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    user_id = data.get("user_id")
    print(f"[INFO] 从 extract.yaml 读取 user_id={user_id}")
    return user_id
