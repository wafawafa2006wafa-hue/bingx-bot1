import os
from flask import Flask, request
import requests

app = Flask(__name__)

# قراءة التوكن بأمان من متغيرات البيئة في Render
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

@app.route('/')
def home():
    return "Bot is running successfully!"

@app.route('/', methods=['POST'])
def receive_update():
    data = request.json
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        if text == '/start':
            send_welcome(chat_id)
            
    return {"status": "ok"}, 200

def send_welcome(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 تحليل السوق الشامل", "callback_data": "market"}],
            [{"text": "🪙 Bitcoin (BTC)", "callback_data": "btc"}, {"text": "💎 Ethereum (ETH)", "callback_data": "eth"}],
            [{"text": "⚡ Solana (SOL)", "callback_data": "sol"}],
            [{"text": "📈 S&P 500 Index", "callback_data": "sp500"}]
        ]
    }
    
    payload = {
        "chat_id": chat_id,
        "text": "🤖 **أهلاً بك مجدداً في مركز القيادة والتحليل الذكي**\n\nاختر من الأزرار بالأسفل لمتابعة السوق أو فحص العملات بدقة:",
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
