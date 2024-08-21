import google.generativeai as genai
from config import GEMINI_API_KEY
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class GeminiAPI:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.text_model = genai.GenerativeModel('gemini-pro')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')

    def generate_text(self, prompt):
        try:
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error in generate_text: {str(e)}")
            return "عذرًا، حدث خطأ أثناء توليد النص. الرجاء المحاولة مرة أخرى."

    def describe_image(self, image_path, prompt):
        try:
            image = Image.open(image_path)
            response = self.vision_model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            logger.error(f"Error in describe_image: {str(e)}")
            return "عذرًا، حدث خطأ أثناء وصف الصورة. الرجاء المحاولة مرة أخرى."

    def analyze_text(self, text):
        prompt = f"قم بتحليل النص التالي بعمق: {text}"
        return self.generate_text(prompt)

    def extract_info(self, text):
        prompt = f"استخرج المعلومات الرئيسية من النص التالي: {text}"
        return self.generate_text(prompt)

    def process_code(self, code):
        prompt = f"قم بتحليل أو تحسين الكود التالي: {code}"
        return self.generate_text(prompt)

    def analyze_data(self, data):
        prompt = f"قم بتحليل البيانات التالية وتقديم رؤى: {data}"
        return self.generate_text(prompt)

    def process_text(self, text):
        try:
            if text.startswith("تحليل:"):
                return self.analyze_text(text[7:])
            elif text.startswith("استخراج:"):
                return self.extract_info(text[9:])
            elif text.startswith("كود:"):
                return self.process_code(text[5:])
            elif text.startswith("بيانات:"):
                return self.analyze_data(text[7:])
            else:
                return self.generate_text(text)
        except Exception as e:
            logger.error(f"Error in process_text: {str(e)}")
            return "عذرًا، حدث خطأ أثناء معالجة النص. الرجاء المحاولة مرة أخرى."
