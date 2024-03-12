from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# 用你的Channel access token和Channel secret替换下面的'YourChannelAccessToken'和'YourChannelSecret'
line_bot_api = LineBotApi('Bj65Ib1yiL/OVq9oLUaJFOoPEUet8E7RAeed9sFuUPPQ/pKw+7q8tNygqcW7OBnSEJ6zbse/UemryALoHaBJDPi8DvE7Jl7ZK7wHImFw92nYP8Uvqx8z1D4lVi76ZXzr/0gm32ZbQMAWEwnYVbt2HgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('895bc81a30d64c919c1c7c5244a71f1a')

@app.route("/callback", methods=['POST'])
def callback():
    # 获取请求头中的X-Line-Signature
    signature = request.headers['X-Line-Signature']

    # 获取请求体
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 处理Webhook
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 把用户发送的消息回发给他
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    app.run()
