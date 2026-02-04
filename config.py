import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN env o'zgaruvchisi topilmadi!")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY env o'zgaruvchisi topilmadi!")
