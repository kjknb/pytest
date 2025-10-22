import os
import yaml

# ============================================================
# 📂 全局路径配置
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT_PATH = os.path.join(BASE_DIR, "extract.yaml")


# ============================================================
# 🧩 读取 YAML 文件
# ============================================================
def read_yaml_file(file_path=EXTRACT_PATH):
    """读取 YAML 文件，返回字典"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f) or {}
            return data
        except yaml.YAMLError as e:
            print(f"[ERROR] YAML 读取失败: {e}")
            return {}


# ============================================================
# ✏️ 写入 YAML 指定 key
# ============================================================
def write_yaml(key, value, file_path=EXTRACT_PATH):
    """
    向 YAML 文件中写入指定 key（会保留其他内容）
    例: write_yaml("users", [{"id": 1, "name": "test"}])
    """
    data = read_yaml_file(file_path)
    data[key] = value
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"[INFO] 写入键 {key} 到 YAML 文件: {file_path}")


# ============================================================
# ➕ 追加写入 YAML（不会覆盖）
# ============================================================
def append_yaml(key, value, file_path=EXTRACT_PATH):
    """向 YAML 文件追加 key，不覆盖原内容"""
    data = read_yaml_file(file_path)
    if key not in data:
        data[key] = []
    if isinstance(data[key], list):
        data[key].append(value)
    else:
        data[key] = value
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"[INFO] 追加写入 {key} 到 YAML 文件: {file_path}")


# ============================================================
# 🧹 清空 YAML 文件
# ============================================================
def clear_yaml(file_path=EXTRACT_PATH):
    """清空 YAML 文件内容"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.truncate()
    print(f"[INIT] ✅ 已清空提取文件: {file_path}")


# ============================================================
# ✅ 兼容：直接写入整个 YAML 文件（新增）
# ============================================================
def write_yaml_file(file_path=EXTRACT_PATH, data=None):
    """
    覆盖写入整个 YAML 文件（完全替换）
    等价于 write_yaml_file("extract.yaml", {"users": [...]})
    """
    if data is None:
        data = {}
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"[INFO] ✅ 已更新 YAML 文件: {file_path}")


# ============================================================
# 🔧 提取方法（兼容旧版接口）
# ============================================================
def extract_get(key, file_path=EXTRACT_PATH):
    """根据 key 获取 YAML 中的值"""
    data = read_yaml_file(file_path)
    return data.get(key, None)


def extract_set(key, value, file_path=EXTRACT_PATH):
    """设置 key 对应的值"""
    write_yaml(key, value, file_path)


def extract_list_append(key, value, file_path=EXTRACT_PATH):
    """向列表类型 key 中追加一个元素"""
    append_yaml(key, value, file_path)


# ============================================================
# 🔐 Token 专用函数
# ============================================================
def save_token(token, file_path=EXTRACT_PATH):
    """单独保存 token 节点"""
    write_yaml("token", token, file_path)
