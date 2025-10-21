# -*- coding: utf-8 -*-
"""
yaml_util.py —— 统一封装 YAML 文件的 读 / 写 / 追加 / 清空 操作
兼容老版本 extract_get, extract_set, extract_list_append 函数
"""

import os
import yaml

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# ======================================================================
# 🟩 通用读写操作
# ======================================================================

def read_yaml_file(file_path):
    """读取 YAML 文件（返回 dict 或 list）"""
    if not os.path.exists(file_path):
        print(f"[WARN] 文件不存在: {file_path}")
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def write_yaml(key, value, file_path):
    """写入或更新 YAML 文件中的某个键"""
    data = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    if isinstance(data, list):
        data = {"users": data}  # 自动修正为标准结构
    data[key] = value

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)
    print(f"[INFO] 写入键 {key} 到 YAML 文件: {file_path}")

def append_yaml(new_data, file_path):
    """向 YAML 文件追加一条记录"""
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_data = yaml.safe_load(f) or []
    if not isinstance(existing_data, list):
        existing_data = [existing_data]
    existing_data.append(new_data)
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(existing_data, f, allow_unicode=True)
    print(f"[INFO] 成功追加 YAML 文件: {file_path}")

def clear_yaml(file_path):
    """清空 YAML 文件内容"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.truncate()
    print(f"[INFO] 已清空 YAML 文件: {file_path}")

# ======================================================================
# 🟨 兼容旧版接口（extract 系列函数）
# ======================================================================

EXTRACT_PATH = os.path.abspath(os.path.join(BASE_DIR, "extract.yaml"))

def extract_get(key, file_path=EXTRACT_PATH):
    """兼容新版 + 旧版 extract.yaml 结构"""
    data = read_yaml_file(file_path)

    if isinstance(data, dict):
        # 新写入的 key-value 结构
        return data.get(key)
    elif isinstance(data, list):
        # 如果是列表，看看是否有字典元素含 key
        for item in data:
            if isinstance(item, dict) and key in item:
                return item[key]
        # 没找到则返回 None
        return None
    else:
        return None


def extract_set(key, value, file_path=EXTRACT_PATH):
    """兼容旧版：写入 extract.yaml 指定 key"""
    write_yaml(key, value, file_path)

def extract_list_append(new_user, file_path=EXTRACT_PATH):
    """将新用户追加到 extract.yaml 的 users 列表中"""
    data = {}

    # 1️⃣ 读取原文件（如果存在）
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    # 2️⃣ 若文件是列表，转换为 dict
    if isinstance(data, list):
        data = {"users": data}

    # 3️⃣ 确保存在 users 键
    if "users" not in data or not isinstance(data["users"], list):
        data["users"] = []

    # 4️⃣ 追加用户
    data["users"].append(new_user)

    # 5️⃣ 写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

    print(f"[INFO] 成功追加用户信息到 users 节点: {file_path}")
