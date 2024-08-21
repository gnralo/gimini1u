import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import os
from config import TELEGRAM_BOT_TOKEN
from gemini_api import GeminiAPI
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
gemini = GeminiAPI()

def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(KeyboardButton("🖼 وصف صورة"), KeyboardButton("📝 توليد نص"))
    keyboard.add(KeyboardButton("🔍 تحليل نص"), KeyboardButton("📊 استخراج معلومات"))
    keyboard.add(KeyboardButton("💻 معالجة كود"), KeyboardButton("📈 تحليل بيانات"))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    welcome_text = """
    مرحبًا بك في بوت الذكاء الاصطناعي الشامل! 
    يمكنك استخدام الأزرار أدناه للوصول إلى الوظائف المختلفة.
    
    🖼 وصف صورة - لوصف الصور
    📝 توليد نص - لتوليد نصوص
    🔍 تحليل نص - لتحليل النصوص
    📊 استخراج معلومات - لاستخراج معلومات من النصوص
    💻 معالجة كود - لتحليل أو تحسين الأكواد البرمجية
    📈 تحليل بيانات - لتحليل البيانات
    
    يمكنك أيضًا إرسال صورة مباشرة لوصفها.
    """
    bot.reply_to(message, welcome_text, reply_markup=create_main_keyboard())

@bot.message_handler(content_types=['photo'])
def handle_image(message: Message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("temp_image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        response = gemini.describe_image("temp_image.jpg", "قم بوصف هذه الصورة بالتفصيل.")
        bot.reply_to(message, response)
        
        os.remove("temp_image.jpg")
    except Exception as e:
        logger.error(f"Error in handle_image: {str(e)}")
        bot.reply_to(message, "عذرًا، حدث خطأ أثناء معالجة الصورة. الرجاء المحاولة مرة أخرى.")

@bot.message_handler(func=lambda message: True)
def handle_text(message: Message):
    try:
        text = message.text
        if text == "🖼 وصف صورة":
            bot.reply_to(message, "الرجاء إرسال الصورة التي تريد وصفها.")
        elif text == "📝 توليد نص":
            bot.reply_to(message, "الرجاء إدخال موضوع أو بداية النص الذي تريد توليده.")
        elif text == "🔍 تحليل نص":
            bot.reply_to(message, "الرجاء إدخال النص الذي تريد تحليله.")
        elif text == "📊 استخراج معلومات":
            bot.reply_to(message, "الرجاء إدخال النص الذي تريد استخراج المعلومات منه.")
        elif text == "💻 معالجة كود":
            bot.reply_to(message, "الرجاء إدخال الكود البرمجي الذي تريد تحليله أو تحسينه.")
        elif text == "📈 تحليل بيانات":
            bot.reply_to(message, "الرجاء إدخال البيانات التي تريد تحليلها.")
        else:
            response = gemini.process_text(text)
            bot.reply_to(message, response)
    except Exception as e:
        logger.error(f"Error in handle_text: {str(e)}")
        bot.reply_to(message, "عذرًا، حدث خطأ أثناء معالجة طلبك. الرجاء المحاولة مرة أخرى.")

if __name__ == '__main__':
    logger.info("Starting the bot...")
    bot.polling(none_stop=True)
