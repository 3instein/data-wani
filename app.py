from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('m7oF0Ii4/ufgqDT9V29TOBW1D5715GpgqEX8Ltia29qXY1OH5iLriTRo6IuNxG9q3zIqNjsofByRoWX2Sm9z7m6epPcanjbz4JJ+i75TCqEVff2jisPpnZllzRm6h9uuCY4q31ikDdjhnrtEVrZrSAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('cb15d13e97326a3349cb158e03846af1')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
