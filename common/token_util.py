# -*- coding: utf-8 -*-
"""
token_util.py — 统一管理 token 读写
"""

import os
import yaml

# 默认 token 文件路径
PROJECT_ROOT = os.getcwd()
TOKEN_FILE = os.path.join(PROJECT_ROOT, "token.yaml")

def save_token(token_value: str):
    """
    保存 token 到 token.yaml 文件
    """
    if not token_value:
        print("[WARN] save_token: token 为空，不写入")
        return
    data = {"token": token_value}
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)
    print(f"[INFO] 已写入 token.yaml -> token={token_value[:15]}...")

def read_token() -> str:
    """
    从 token.yaml 读取 token 值
    """
    if not os.path.exists(TOKEN_FILE):
        print(f"[WARN] token.yaml 不存在: {TOKEN_FILE}")
        return ""
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    token = data.get("token", "")
    if not token:
        print(f"[WARN] token.yaml 中未找到 token 字段")
    return token
