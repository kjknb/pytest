import requests
import json
import sys
import time
import hmac
import hashlib
import base64
import urllib.parse

# ========== 配置区 ==========
WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/47e139e1-1a4f-49f1-b8f1-20e7f85af93d"
SECRET = ""  # 如果你在机器人设置中启用了“加签”，请填写对应的 Secret
# ============================

def sign():
    """生成 Feishu 加签（如果启用了安全设置）"""
    if not SECRET:
        return ""
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{SECRET}".encode('utf-8')
    hmac_code = hmac.new(SECRET.encode('utf-8'), string_to_sign, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return f"&timestamp={timestamp}&sign={urllib.parse.quote_plus(sign)}"

def send_feishu_msg(content: str, at_all=False):
    """发送 Feishu 机器人消息"""
    url = WEBHOOK + sign()
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {
        "msg_type": "text",
        "content": {"text": content},
        "at": {"is_at_all": at_all}
    }
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") == 0:
            print("✅ Feishu 通知已发送成功")
        else:
            print(f"⚠️ Feishu 通知发送失败: {result}")
    except Exception as e:
        print(f"❌ Feishu 通知异常: {e}")

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "🔔 自动化测试任务执行完毕"
    send_feishu_msg(message, at_all=True)
