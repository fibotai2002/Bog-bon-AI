"""
Konfiguratsiya moduli
Muhit o'zgaruvchilarini yuklash va sozlamalarni boshqarish
"""

import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Telegram Bot sozlamalari
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN muhit o'zgaruvchisi topilmadi!")

# Gemini API sozlamalari
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY muhit o'zgaruvchisi topilmadi!")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Admin sozlamalari
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]

ADMIN_CHANNEL_ID_STR = os.getenv("ADMIN_CHANNEL_ID", "")
ADMIN_CHANNEL_ID = int(ADMIN_CHANNEL_ID_STR) if ADMIN_CHANNEL_ID_STR else None

# Rasm qayta ishlash sozlamalari
MAX_IMAGE_SIZE = 1280  # pikselda
JPEG_QUALITY = 85

# Gemini retry sozlamalari
GEMINI_TIMEOUT = 30  # soniya
GEMINI_MAX_RETRIES = 1

import json
from typing import Dict, Any

# ... (boshqa importlar o'z joyida qoladi)

# JSON fayl yo'li
DATA_FILE = "data/users.json"

def load_users() -> Dict[str, Any]:
    """Userlarni fayldan yuklash"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            # Fayl bo'sh bo'lsa
            content = f.read()
            if not content:
                return {}
            # Keys JSON da string bo'ladi, bizga int kerak
            data = json.loads(content)
            return {int(k): v for k, v in data.items()}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}

def save_users():
    """Userlarni faylga saqlash"""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(USER_DB, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving users: {e}")

# In-memory user database (fayldan yuklanadi)
USER_DB = load_users()

# Tarif turlari
PLAN_FREE = "FREE"
PLAN_PRO = "PRO"
PLAN_BUSINESS = "BUSINESS"

def get_user_plan(user_id: int) -> str:
    """Foydalanuvchi tarifini olish"""
    if user_id not in USER_DB:
        USER_DB[user_id] = {"plan": PLAN_FREE, "history": []}
        save_users()
    return USER_DB[user_id].get("plan", PLAN_FREE)

def set_user_plan(user_id: int, plan: str) -> None:
    """Foydalanuvchi tarifini o'rnatish"""
    if plan not in [PLAN_FREE, PLAN_PRO, PLAN_BUSINESS]:
        raise ValueError(f"Noto'g'ri tarif: {plan}")
    
    if user_id not in USER_DB:
        USER_DB[user_id] = {"plan": plan, "history": []}
    
    USER_DB[user_id]["plan"] = plan
    save_users()

def get_user_data(user_id: int) -> Dict[str, Any]:
    """Foydalanuvchi ma'lumotlarini olish"""
    return USER_DB.get(user_id, {})

def update_user_data(user_id: int, data: Dict[str, Any]) -> None:
    """Foydalanuvchi ma'lumotlarini yangilash"""
    if user_id not in USER_DB:
        USER_DB[user_id] = {"plan": PLAN_FREE, "history": []}
    
    USER_DB[user_id].update(data)
    save_users()

def is_user_registered(user_id: int) -> bool:
    """Foydalanuvchi registratsiyadan o'tganmi?"""
    user = USER_DB.get(user_id)
    return user is not None and user.get("is_registered", False)

def get_user_lang(user_id: int) -> str:
    """Foydalanuvchi tilini olish (default: uz)"""
    user = USER_DB.get(user_id)
    if not user:
        return "uz"
    return user.get("language", "uz")

def set_user_lang(user_id: int, lang: str) -> None:
    """Foydalanuvchi tilini o'rnatish"""
    update_user_data(user_id, {"language": lang})

def is_admin(user_id: int) -> bool:
    """
    Foydalanuvchi admin ekanligini tekshirish
    """
    return user_id in ADMIN_IDS
