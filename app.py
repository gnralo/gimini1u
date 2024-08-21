from flask import Flask
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '✅  هـذا الـبـوت تـم إنـشـائـه و هـو مـسـتـضـاف حـالـيـًا و مـتـاح لـلـجـمـيـع ✅ '

if __name__ == '__main__':
    logger.info("🚀  تـم تـشـغـيـل تـطـبـيـق Flask بـنـجـاح 🚀 ")
    app.run()
