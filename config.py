import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY_2 = os.getenv("GEMINI_API_KEY_2")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN env o'zgaruvchisi topilmadi!")

if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY env o'zgaruvchisi topilmadi!")
