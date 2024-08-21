import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import os
from config import TELEGRAM_BOT_TOKEN, KOYEB_APP_URL
from gemini_api import GeminiAPI
import logging
from flask import Flask, request
import time # تأكد من استيراد مكتبة time

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
gemini = GeminiAPI()

app = Flask(__name__)

def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(KeyboardButton("🖼 وصف صورة"), KeyboardButton("📝 توليد نص"))
    keyboard.add(KeyboardButton("🔍 تحليل نص"), KeyboardButton("📊 استخراج معلومات"))
    keyboard.add(KeyboardButton("💻 معالجة كود"), KeyboardButton("📈 تحليل بيانات"))
    return keyboard

# ... (باقي الكود كما هو) ...

if __name__ == '__main__':
    logger.info("Starting the bot...")
    # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))  # تم حذف هذا السطر
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(e)
            time.sleep(15)
