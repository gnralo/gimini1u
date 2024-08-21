from flask import Flask
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'هذا البوت تم إنشاؤه وهو مستضاف حاليًا ومتاح للجميع'

if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run()
