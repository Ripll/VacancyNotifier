import json
from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot
from datetime import datetime
import os
import codecs

load_dotenv()


API_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")
DB_URL = os.getenv("DB_URL")

with codecs.open("./settings.json", "r", "utf_8_sig") as f:
    SETTINGS = json.loads(f.read())

START_TIME = datetime.now()

DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT"))
bot = Bot(token=API_TOKEN)
