import os
import logging
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# إعداد السيرفر ليبقى نشطاً 24/7 على Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Naourisol Bot is running 24/7 successfully!"

# إعداد توكن البوت
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "ضع_توكن_البوت_هنا")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 تحليل السوق الشامل", callback_data='market_analysis')],
        [InlineKeyboardButton("🪙 Bitcoin (BTC)", callback_data='btc_analysis'),
         InlineKeyboardButton("💎 Ethereum (ETH)", callback_data='eth_analysis')],
        [InlineKeyboardButton("⚡ Solana (SOL)", callback_data='sol_analysis'),
         InlineKeyboardButton("📈 S&P 500 Index", callback_data='sp500')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🤖 مرحباً بك مجدداً في مركز القيادة والتحليل الذكي\n\n"
        "اختر من الأزرار بالأسفل لمتابعة السوق أو فحص العملات بدقة:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'btc_analysis':
        text = (
            "⚙️ تحليل العملة: (BTC-USDT)\n\n"
            "💵 السعر الحالي: 92400.0 USDT\n"
            "📊 التغير (24س): 0.5%+\n"
            "📉 مؤشر RSI: 50.0\n"
            "📌 الحالة الفنية: ⚖️ في منطقة استقرار\n\n"
            "👉 اختر الإجراء التنفيذي أو عد للقائمة:"
        )
        keyboard = [
            [InlineKeyboardButton("💰 بيع العملة", callback_data='sell'),
             InlineKeyboardButton("🚀 شراء فوري 5$", callback_data='buy')],
            [InlineKeyboardButton("🔄 تحديث التحليل", callback_data='btc_analysis'),
             InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='main_menu')]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data == 'main_menu':
        await start(update, context)

# تشغيل البوت والسيرفر معاً
def run_telegram_bot():
    if TOKEN != "ضع_توكن_البوت_هنا":
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.run_polling()

if __name__ == "__main__":
    import threading
    # تشغيل البوت في خلفية السيرفر
    t = threading.Thread(target=run_telegram_bot)
    t.start()
    
    # تشغيل سيرفر Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

