import os
import pytest
import subprocess
import shutil
from datetime import datetime

# ANSI 颜色定义（Windows PowerShell / PyCharm 都支持）
GREEN = "\033[92m"    # ✅ 成功（绿色）
YELLOW = "\033[93m"   # ⚠️ 警告（黄色）
RED = "\033[91m"      # ❌ 错误（红色）
CYAN = "\033[96m"     # 🚀 提示（青色）
RESET = "\033[0m"     # 重置颜色

def color_log(msg, color=RESET):
    """带颜色输出"""
    print(f"{color}{msg}{RESET}")

# ================================
# 🧹 自动初始化逻辑
# ================================
def pytest_sessionstart(session):
    """测试会话开始时执行：清空 extract.yaml、数据库表、Allure 报告"""
    base_dir = os.path.dirname(__file__)
    extract_file = os.path.join(base_dir, "extract.yaml")

    # === 1️⃣ 清空 extract.yaml 文件 ===
    if os.path.exists(extract_file):
        open(extract_file, "w").close()
        color_log(f"[INIT] ✅ 已清空提取文件: {extract_file}", GREEN)
    else:
        color_log(f"[INIT] ⚠️ 未找到提取文件 extract.yaml，将在首次写入时自动创建", YELLOW)

    # === 2️⃣ 清空数据库 user_basic 表 ===
    try:
        color_log("[INIT] 🚀 正在清空数据库中的 user_basic 表 ...", CYAN)
        cmd = (
            'docker exec -i mysql-docker mysql -uroot -p123456 ginchat '
            '-e "TRUNCATE TABLE user_basic;"'
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            color_log("✅ 数据库表 user_basic 已成功清空并重置自增 ID！", GREEN)
        else:
            color_log(f"❌ 数据库清空失败：{result.stderr}", RED)
    except Exception as e:
        color_log(f"⚠️ 数据库清空操作异常: {e}", YELLOW)

    # === 3️⃣ 清理 Allure 报告目录 ===
    allure_dirs = ["reports/allure-results", "reports/allure-report"]
    for d in allure_dirs:
        full_path = os.path.join(base_dir, d)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
            color_log(f"[INIT] 🧹 已清空 Allure 报告目录: {full_path}", GREEN)
        else:
            color_log(f"[INIT] ⚠️ Allure 报告目录不存在: {full_path}", YELLOW)

        # ✅ 删除后立即重建目录
        os.makedirs(full_path, exist_ok=True)
        color_log(f"[INIT] 📁 已重新创建 Allure 报告目录: {full_path}", CYAN)

    # === 4️⃣ 初始化日志目录 ===
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    color_log(f"[INIT] 日志目录已准备: {log_dir}", GREEN)


# ================================
# 🌍 环境配置
# ================================
@pytest.fixture(scope="session")
def get_base_url():
    """获取当前测试环境的 base_url"""
    env = "test"
    base_url = "http://localhost:8080"
    color_log(f"[INIT] 当前环境: {env} -> {base_url}", CYAN)
    return base_url


# ================================
# 🧾 测试日志分隔
# ================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    color_log(f"\n{'='*80}\n[TEST START] {item.name} - {datetime.now()}\n{'='*80}", CYAN)
    yield


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_teardown(item):
    yield
    color_log(f"\n{'-'*80}\n[TEST END] {item.name} - {datetime.now()}\n{'-'*80}\n", CYAN)
