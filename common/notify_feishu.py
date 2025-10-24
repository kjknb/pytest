# -*- coding: utf-8 -*-
"""
飞书通知工具
==========================
用于在 Jenkins 或 CI/CD 流程中发送飞书通知。
支持文本内容、异常捕获、防止 Jenkins 误判失败退出。
"""

import requests
import json
import sys
import traceback

# ✅ 你的飞书 Webhook 地址（请替换成你自己的）
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/47e139e1-1a4f-49f1-b8f1-20e7f85af93d"  # ← 修改这里


def send_feishu_msg(message: str, at_all: bool = False):
    """
    发送飞书群通知消息
    :param message: 通知内容文本
    :param at_all: 是否 @所有人
    """
    try:
        headers = {"Content-Type": "application/json"}

        # 如果需要 @所有人
        mention = "<at user_id=\"all\">所有人</at>\n" if at_all else ""

        payload = {
            "msg_type": "text",
            "content": {
                "text": f"{mention}{message}"
            }
        }

        print(f"🚀 正在发送飞书消息: {message}")

        resp = requests.post(
            FEISHU_WEBHOOK_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )

        if resp.status_code == 200:
            print("✅ Feishu 通知已发送成功")
        else:
            print(f"⚠️ Feishu 通知发送失败: HTTP {resp.status_code}")
            print(f"响应内容: {resp.text}")

    except Exception as e:
        print("❌ 发送飞书通知时出现异常：", str(e))
        traceback.print_exc()

    finally:
        # ✅ 永远保证退出码为 0，避免 Jenkins 误判构建失败
        sys.exit(0)


if __name__ == "__main__":
    # 从命令行接收消息内容
    message = sys.argv[1] if len(sys.argv) > 1 else "🔔 自动化测试任务执行完毕"
    send_feishu_msg(message, at_all=True)
