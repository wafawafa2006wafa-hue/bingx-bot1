import os
from flask import Flask, request
import requests

app = Flask(__name__)

# استبدل هذا التوكن بتوكن بوتك الحقيقي أو اتركه هكذا مؤقتاً
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")

@app.route('/')
def home():
    return "BingX Bot is active and running 24/7!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        if text == '/start':
            send_welcome(chat_id)
            
    return 'ok', 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def send_welcome(chat_id):
    msg = (
        "🤖 *أهلاً بك يا سرار في نظام التداول والتحليل الشامل!*\n\n"
        "✅ السيرفر يعمل الآن بنجاح تام 24/7.\n"
        "📊 سيتم ربط الإشارات والأزرار فوراً."
    )
    send_message(chat_id, msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
