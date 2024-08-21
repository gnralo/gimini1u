import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import os
from config import TELEGRAM_BOT_TOKEN
from gemini_api import GeminiAPI
import logging
import time

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
    *⚜️ مـرحـبًا بـك في بـوت الـذكـاء الاصـطـنـاعـي الـشـامـل! ⚜️*
    
    *✨ يـمـكـنـك اسـتـخـدام الـأزرار أدناه لـلـوصـول إلـى الـوظـائـف الـمـخـتـلـفـة ✨*
    
    *🖼 وصـف صـورة - لـوصـف الـصـور*
    *📝 تـولـيـد نـص - لـتـولـيـد نـصـوص*
    *🔍 تـحـلـيـل نـص - لـتـحـلـيـل الـنـصـوص*
    *📊 اسـتـخـراج مـعـلـومـات - لـاسـتـخـراج مـعـلـومـات مـن الـنـصـوص*
    *💻 مـعـالـجـة كـود - لـتـحـلـيـل أو تـحـسـيـن الـكـود بـرمـجـيـة*
    *📈 تـحـلـيـل بـيـانـات - لـتـحـلـيـل الـبـيـانـات*
    
    *✨ يـمـكـنـك أيـضًا إرسال صـورة مـبـاشـرة لـوصـفـهـا ✨*
    """
    bot.reply_to(message, welcome_text, reply_markup=create_main_keyboard(), parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_image(message: Message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, "⏳ جـاري تـحـمـيـل الـصـورة و وصـفـهـا،  يُـرجـى الانـتـظـار ⏳")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("temp_image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        response = gemini.describe_image("temp_image.jpg", "قم بوصف هذه الصورة بالتفصيل.")
        bot.reply_to(message, f"🖼 *وصـف الـصـورة:*\n{response}", parse_mode='Markdown')
        
        os.remove("temp_image.jpg")
    except Exception as e:
        logger.error(f"Error in handle_image: {str(e)}")
        bot.reply_to(message, "❌ عـذرًا،  حـدث خـطـأ أثـنـاء مـعـالـجـة الـصـورة.  الـرجـاء الـمـحـاولـة مـرة أخـرى. ❌")

@bot.message_handler(func=lambda message: True)
def handle_text(message: Message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, "⏳ جـاري مـعـالـجـة طـلـبـك،  يُـرجـى الانـتـظـار ⏳")
    try:
        text = message.text
        if text == "🖼 وصف صورة":
            bot.reply_to(message, "📷  الـرجـاء إرسال الـصـورة الـتـي تـريـد وصـفـهـا. 📷 ")
        elif text == "📝 توليد نص":
            bot.reply_to(message, "✏️  الـرجـاء إدراج مـوضـوع أو بـدايـة الـنـص الـذي تـريـد تـولـيـده. ✏️")
        elif text == "🔍 تحليل نص":
            bot.reply_to(message, "📝  الـرجـاء إدراج الـنـص الـذي تـريـد تـحـلـيـلـه. 📝")
        elif text == "📊 استخراج معلومات":
            bot.reply_to(message, "📝  الـرجـاء إدراج الـنـص الـذي تـريـد اسـتـخـراج الـمـعـلـومـات مـنـه. 📝")
        elif text == "💻 معالجة كود":
            bot.reply_to(message, "💻  الـرجـاء إدراج الـكـود الـبـرمـجـي الـذي تـريـد تـحـلـيـلـه أو تـحـسـيـنـه. 💻")
        elif text == "📈 تحليل بيانات":
            bot.reply_to(message, "📊  الـرجـاء إدراج الـبـيـانـات الـتـي تـريـد تـحـلـيـلـهـا. 📊")
        else:
            response = gemini.process_text(text)
            bot.reply_to(message, f"*✨  الـنـتـيـجـة ✨:*\n{response}", parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in handle_text: {str(e)}")
        bot.reply_to(message, "❌ عـذرًا،  حـدث خـطـأ أثـنـاء مـعـالـجـة طـلـبـك.  الـرجـاء الـمـحـاولـة مـرة أخـرى ❌")

if __name__ == '__main__':
    logger.info("🚀  تـم تـشـغـيـل الـبـوت بـنـجـاح 🚀 ")
    bot.polling(none_stop=True)
