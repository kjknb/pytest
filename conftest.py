import os
import pytest
import subprocess
import yaml

# ============================================================
# ✅ 自动清空数据库（在所有测试前执行）
# ============================================================

@pytest.fixture(scope="session", autouse=True)
def clear_db_before_tests():
    """
    在执行 pytest 前，自动运行 PowerShell 脚本 clear_db.ps1
    以清空 user_basic 表，确保测试数据环境干净。
    """
    print("\n[INIT] 自动清空数据库中的 user_basic 表 ...")

    script_path = os.path.join(os.getcwd(), "clear_db.ps1")
    if os.path.exists(script_path):
        try:
            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
                check=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"⚠️ 数据库清空脚本执行失败：{e}")
    else:
        print("⚠️ 未找到 clear_db.ps1，跳过清库操作。")


# ============================================================
# ✅ 加载配置文件 config/config.yaml
# ============================================================

@pytest.fixture(scope="session")
def get_base_url():
    """读取 config/config.yaml 中的 base_url"""
    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"[ERROR] 配置文件未找到: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        env = data.get("env", "test")
        base_url = data["env_config"].get(env, {}).get("base_url")
        print(f"[INIT] 当前环境: {env} -> {base_url}")
        return base_url


# ============================================================
# ✅ 加载 Token（从 extract.yaml）
# ============================================================

@pytest.fixture(scope="session")
def get_token():
    """从 extract.yaml 读取 token（兼容 list/dict 两种结构）"""
    extract_path = os.path.join(os.getcwd(), "extract.yaml")

    if not os.path.exists(extract_path):
        print("[WARN] extract.yaml 不存在，将返回空 token")
        return {"token": ""}

    with open(extract_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f) or {}

            # 🧩 如果是 dict 格式
            if isinstance(data, dict):
                token = data.get("token", "")

            # 🧩 如果是 list 格式（老版本）
            elif isinstance(data, list):
                token = ""
                for item in data:
                    if isinstance(item, dict) and "token" in item:
                        token = item["token"]
                        break
            else:
                token = ""

        except Exception as e:
            print(f"[ERROR] 读取 token 失败: {e}")
            token = ""

    return {"token": token}



# ============================================================
# ✅ 全局日志初始化
# ============================================================

@pytest.fixture(scope="session", autouse=True)
def init_env():
    """初始化日志目录"""
    log_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    print(f"[INIT] 日志目录已准备: {log_dir}")
