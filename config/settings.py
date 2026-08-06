import os

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден в .env")

if not MODEL_NAME:
    raise ValueError("MODEL_NAME не найден в .env")