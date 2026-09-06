import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"{name} не найден в .env")

    return value


BOT_TOKEN = get_required_env("BOT_TOKEN")
OPENROUTER_API_KEY = get_required_env("OPENROUTER_API_KEY")
MODEL_NAME = get_required_env("MODEL_NAME")
DATABASE_URL = get_required_env("DATABASE_URL")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_HISTORY = 20

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден в .env")

if not MODEL_NAME:
    raise ValueError("MODEL_NAME не найден в .env")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в .env")
