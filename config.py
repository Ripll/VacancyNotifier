from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot
from datetime import datetime
import os

load_dotenv()


API_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")
DB_URL = os.getenv("DB_URL")
CHAT_ID = os.getenv("CHAT_ID")

START_TIME = datetime.now()

DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT"))
bot = Bot(token=API_TOKEN)
