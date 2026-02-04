import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from bot.handlers import start, image_analysis

# Loglarni sozlash
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    """
    Botni ishga tushirish funksiyasi.
    """
    # Bot va Dispatcher obyektlarini yaratish
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(image_analysis.router)

    print("Bot ishga tushdi... 🚀")
    # Pollingni boshlash
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
